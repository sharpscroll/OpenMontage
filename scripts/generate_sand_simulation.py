"""Generate a high-fidelity granular sand simulation video.

Simulates thousands of individual sand grains interacting with gravity,
angled deflector shelves, a Galton peg field, and accumulating into realistic
dunes with avalanche mechanics (angle of repose).
"""

from __future__ import annotations

import math
import os
import shutil
import struct
import subprocess
import sys
import time
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Set up paths
REPO_ROOT = Path(__file__).resolve().parent.parent
PROJECT_DIR = REPO_ROOT / "projects" / "sand-simulation-motion"
RENDERS_DIR = PROJECT_DIR / "renders"
ASSETS_DIR = PROJECT_DIR / "assets"

WIDTH = 1080
HEIGHT = 1920
FPS = 30
DURATION_SEC = 14
TOTAL_FRAMES = FPS * DURATION_SEC

# Color palette (RGBA or RGB)
BG_COLOR = (14, 17, 23)
PANEL_COLOR = (22, 27, 36)
GLASS_LINE = (80, 110, 140, 180)
GLASS_GLOW = (40, 70, 100, 100)

SAND_PALETTE = np.array([
    [243, 213, 142],  # Warm Desert Gold
    [228, 187, 118],  # Amber Dune
    [209, 158, 92],   # Cinnamon Ochre
    [255, 238, 195],  # Sunlit Quartz
    [184, 131, 74],   # Deep Terracotta
], dtype=np.uint8)


class SandSimulation:
    def __init__(self, width: int = 1080, height: int = 1920):
        self.width = width
        self.height = height

        # Particle arrays
        self.max_particles = 35000
        self.count = 0
        self.pos = np.zeros((self.max_particles, 2), dtype=np.float32)
        self.vel = np.zeros((self.max_particles, 2), dtype=np.float32)
        self.color_idx = np.zeros(self.max_particles, dtype=np.int32)
        self.settled = np.zeros(self.max_particles, dtype=bool)

        # Heightmap for the bottom basin (x in [160, 920])
        self.basin_left = 160
        self.basin_right = 920
        self.basin_floor = 1750
        self.heightmap = np.full(self.width, self.basin_floor, dtype=np.float32)

        # Deflectors (line segments: (x1, y1, x2, y2))
        self.shelves = [
            # Upper left funnel wall
            (420, 240, 510, 360),
            # Upper right funnel wall
            (660, 240, 570, 360),
            # Shelf 1: tilted down to right
            (320, 520, 700, 640),
            # Shelf 2: tilted down to left
            (760, 780, 380, 900),
            # Splitter wedge
            (540, 1020, 440, 1120),
            (540, 1020, 640, 1120),
        ]

        # Pegs (Galton board style pins)
        self.pegs = []
        rows = 4
        start_y = 1200
        for r in range(rows):
            y = start_y + r * 50
            num_pegs = r + 3
            spacing = 80
            start_x = 540 - ((num_pegs - 1) * spacing) / 2
            for c in range(num_pegs):
                self.pegs.append((start_x + c * spacing, y, 9.0))  # x, y, radius

    def spawn_grains(self, frame_idx: int):
        # Emit grains from the funnel neck (x=530..550, y=370)
        # Flow rate: ~35-50 grains per frame until frame 360
        if frame_idx < 380 and self.count < self.max_particles - 100:
            burst = np.random.randint(40, 65)
            new_idx = np.arange(self.count, self.count + burst)
            self.pos[new_idx, 0] = np.random.uniform(532, 548, burst)
            self.pos[new_idx, 1] = np.random.uniform(365, 375, burst)
            self.vel[new_idx, 0] = np.random.normal(0, 0.4, burst)
            self.vel[new_idx, 1] = np.random.uniform(2.0, 4.0, burst)
            self.color_idx[new_idx] = np.random.randint(0, len(SAND_PALETTE), burst)
            self.settled[new_idx] = False
            self.count += burst

    def update(self):
        if self.count == 0:
            return

        active_mask = ~self.settled[:self.count]
        active_indices = np.where(active_mask)[0]

        if len(active_indices) == 0:
            return

        # Apply gravity
        self.vel[active_indices, 1] += 0.45
        # Terminal velocity / air drag
        self.vel[active_indices] *= 0.995

        # Update positions
        self.pos[active_indices] += self.vel[active_indices]

        # Check line deflector collisions
        px = self.pos[active_indices, 0]
        py = self.pos[active_indices, 1]

        for (x1, y1, x2, y2) in self.shelves:
            dx = x2 - x1
            dy = y2 - y1
            length = math.hypot(dx, dy)
            if length == 0:
                continue
            nx = -dy / length
            ny = dx / length
            if ny < 0:
                nx, ny = -nx, -ny  # Ensure normal points generally upward

            # Distance from point to line segment
            vx = px - x1
            vy = py - y1
            proj = (vx * dx + vy * dy) / (length * length)
            # Find points within line segment bounds
            seg_mask = (proj >= 0.0) & (proj <= 1.0)
            if not np.any(seg_mask):
                continue

            sub_idx = active_indices[seg_mask]
            sub_proj = proj[seg_mask]
            closest_x = x1 + sub_proj * dx
            closest_y = y1 + sub_proj * dy

            dist_x = self.pos[sub_idx, 0] - closest_x
            dist_y = self.pos[sub_idx, 1] - closest_y
            dist = np.hypot(dist_x, dist_y)

            coll_mask = dist < 7.0
            if np.any(coll_mask):
                c_idx = sub_idx[coll_mask]
                # Push out along normal
                self.pos[c_idx, 0] = closest_x[coll_mask] + nx * 7.5
                self.pos[c_idx, 1] = closest_y[coll_mask] + ny * 7.5

                # Reflect velocity with friction
                v_dot_n = (self.vel[c_idx, 0] * nx + self.vel[c_idx, 1] * ny)
                self.vel[c_idx, 0] = (self.vel[c_idx, 0] - 1.35 * v_dot_n * nx) * 0.75 + (dx / length) * 1.5
                self.vel[c_idx, 1] = (self.vel[c_idx, 1] - 1.35 * v_dot_n * ny) * 0.75 + (dy / length) * 1.5

        # Check peg collisions
        for (cx, cy, r) in self.pegs:
            dx = self.pos[active_indices, 0] - cx
            dy = self.pos[active_indices, 1] - cy
            dist = np.hypot(dx, dy)
            peg_coll = dist < (r + 4.0)
            if np.any(peg_coll):
                p_idx = active_indices[peg_coll]
                p_dist = dist[peg_coll]
                p_dist[p_dist == 0] = 1.0
                nx = dx[peg_coll] / p_dist
                ny = dy[peg_coll] / p_dist

                self.pos[p_idx, 0] = cx + nx * (r + 4.5)
                self.pos[p_idx, 1] = cy + ny * (r + 4.5)

                v_dot_n = self.vel[p_idx, 0] * nx + self.vel[p_idx, 1] * ny
                self.vel[p_idx, 0] = (self.vel[p_idx, 0] - 1.5 * v_dot_n * nx) * 0.65
                self.vel[p_idx, 1] = (self.vel[p_idx, 1] - 1.5 * v_dot_n * ny) * 0.65

        # Check basin settlement and avalanche
        in_basin = (self.pos[active_indices, 0] >= self.basin_left) & (self.pos[active_indices, 0] <= self.basin_right)
        basin_idx = active_indices[in_basin]

        if len(basin_idx) > 0:
            bx = np.clip(self.pos[basin_idx, 0].astype(int), 0, self.width - 1)
            target_h = self.heightmap[bx]
            settle_mask = self.pos[basin_idx, 1] >= target_h

            if np.any(settle_mask):
                s_idx = basin_idx[settle_mask]
                s_x = bx[settle_mask]

                self.settled[s_idx] = True
                self.vel[s_idx] = 0.0

                # Avalanche relaxation on heightmap
                for x in s_x:
                    # Increment column height (sand layer ~ 0.5px)
                    self.heightmap[x] = max(1350.0, self.heightmap[x] - 0.7)

                    # Spread to left/right if slope is steep (avalanche)
                    if x > self.basin_left + 1:
                        diff = self.heightmap[x - 1] - self.heightmap[x]
                        if diff > 1.2:  # Angle of repose exceeded
                            self.heightmap[x - 1] -= diff * 0.5
                            self.heightmap[x] += diff * 0.4
                    if x < self.basin_right - 1:
                        diff = self.heightmap[x + 1] - self.heightmap[x]
                        if diff > 1.2:
                            self.heightmap[x + 1] -= diff * 0.5
                            self.heightmap[x] += diff * 0.4

                self.pos[s_idx, 1] = self.heightmap[s_x]


def generate_audio(output_wav: Path, duration_sec: float = 14.0):
    """Synthesize authentic granular sand-falling & rushing audio."""
    sample_rate = 44100
    n_samples = int(sample_rate * duration_sec)

    t = np.linspace(0, duration_sec, n_samples, endpoint=False)

    # Base pink/filtered noise
    noise = np.random.normal(0, 0.25, n_samples).astype(np.float32)

    # Simple 2-pole resonant bandpass filter around 2400 Hz for sand texture
    # Implement fast moving average cascade
    window = 16
    kernel = np.ones(window, dtype=np.float32) / window
    smoothed = np.convolve(noise, kernel, mode='same')
    bandpass = (noise - smoothed)  # High-frequency grit

    # Amplitude envelope: swells up as flow begins, remains high, gently fades
    envelope = np.ones(n_samples, dtype=np.float32)
    fade_in = int(sample_rate * 1.5)
    fade_out = int(sample_rate * 2.0)
    envelope[:fade_in] = np.linspace(0.0, 1.0, fade_in)
    envelope[-fade_out:] = np.linspace(1.0, 0.0, fade_out)

    # Modulate with subtle flutter
    flutter = 0.85 + 0.15 * np.sin(2 * np.pi * 3.5 * t) + 0.08 * np.sin(2 * np.pi * 8.2 * t)
    audio = bandpass * envelope * flutter

    # Add gentle low ambient bed (desert wind drone at 110 Hz)
    ambient_drone = 0.08 * np.sin(2 * np.pi * 110 * t) + 0.04 * np.sin(2 * np.pi * 220 * t)
    final_audio = audio * 0.85 + ambient_drone * envelope

    # Normalize to -1 dB
    max_val = np.max(np.abs(final_audio))
    if max_val > 0:
        final_audio = (final_audio / max_val) * 0.88

    # Convert to 16-bit PCM
    pcm_data = (final_audio * 32767).astype(np.int16)

    with wave.open(str(output_wav), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm_data.tobytes())


def render_simulation_video():
    PROJECT_DIR.mkdir(parents=True, exist_ok=True)
    RENDERS_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    audio_wav = ASSETS_DIR / "sand_audio.wav"
    output_mp4 = RENDERS_DIR / "sand_simulation_1080p.mp4"

    print(f"[1/4] Synthesizing authentic granular audio -> {audio_wav.name}...")
    generate_audio(audio_wav, duration_sec=DURATION_SEC)

    print(f"[2/4] Initializing physical particle system ({TOTAL_FRAMES} frames)...")
    sim = SandSimulation(WIDTH, HEIGHT)

    # Pre-render static background and apparatus
    bg_img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw_bg = ImageDraw.Draw(bg_img, "RGBA")

    # Radial subtle backdrop glow in center
    for r in range(500, 50, -50):
        alpha = int(12 * (1.0 - r / 500.0))
        draw_bg.ellipse([540 - r, 960 - r, 540 + r, 960 + r], fill=(30, 42, 60, alpha))

    # Basin outline
    basin_pts = [(sim.basin_left, 1320), (sim.basin_left, sim.basin_floor), (sim.basin_right, sim.basin_floor), (sim.basin_right, 1320)]
    draw_bg.line(basin_pts, fill=(100, 140, 180, 180), width=6)
    # Basin bottom glow
    draw_bg.rectangle([sim.basin_left, sim.basin_floor - 4, sim.basin_right, sim.basin_floor + 4], fill=(240, 200, 120, 80))

    # Draw shelves
    for (x1, y1, x2, y2) in sim.shelves:
        # Glow
        draw_bg.line([(x1, y1), (x2, y2)], fill=(60, 90, 130, 100), width=10)
        # Main glass rail
        draw_bg.line([(x1, y1), (x2, y2)], fill=(140, 180, 220, 230), width=5)

    # Draw pegs
    for (cx, cy, r) in sim.pegs:
        draw_bg.ellipse([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2], fill=(40, 70, 100, 150))
        draw_bg.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(160, 200, 240, 255))
        draw_bg.ellipse([cx - r + 3, cy - r + 3, cx + r - 3, cy + r - 3], fill=(220, 240, 255, 255))

    bg_array = np.array(bg_img, dtype=np.uint8)

    print("[3/4] Launching FFmpeg encoder pipeline (rawvideo -> libx264)...")
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",  # Video pipe
        "-i", str(audio_wav),  # Audio file
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(output_mp4),
    ]

    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Frame buffer
    frame = bg_array.copy()

    start_time = time.time()
    for frame_idx in range(TOTAL_FRAMES):
        sim.spawn_grains(frame_idx)
        sim.update()

        # Reset frame with pre-rendered background
        np.copyto(frame, bg_array)

        # Draw sand particles
        if sim.count > 0:
            px = np.clip(sim.pos[:sim.count, 0].astype(int), 0, WIDTH - 2)
            py = np.clip(sim.pos[:sim.count, 1].astype(int), 0, HEIGHT - 2)
            colors = SAND_PALETTE[sim.color_idx[:sim.count]]

            # Fast 2x2 stamp with subtle highlight
            frame[py, px] = colors
            frame[py + 1, px] = colors
            frame[py, px + 1] = colors
            frame[py + 1, px + 1] = np.clip(colors.astype(int) - 15, 0, 255).astype(np.uint8)

        # Overlay HUD & Typography
        frame_pil = Image.fromarray(frame)
        draw = ImageDraw.Draw(frame_pil)

        # Top Header Overlay
        draw.rectangle([60, 80, WIDTH - 60, 210], fill=(20, 25, 35, 220), outline=(50, 70, 95, 200), width=2)
        draw.ellipse([85, 105, 97, 117], fill=(235, 170, 60))
        draw.text((110, 100), "OPENMONTAGE // GRANULAR DYNAMICS", fill=(240, 240, 245))
        draw.text((85, 135), "REAL-TIME SAND & PARTICLE PHYSICS SIMULATION", fill=(210, 175, 100))
        draw.text((85, 170), "COLLISION DETECTION · DEFLECTOR RAILS · ANGLE OF REPOSE", fill=(130, 150, 175))

        # Bottom Telemetry Overlay
        draw.rectangle([60, HEIGHT - 180, WIDTH - 60, HEIGHT - 80], fill=(20, 25, 35, 220), outline=(50, 70, 95, 200), width=2)
        active_cnt = np.sum(~sim.settled[:sim.count]) if sim.count > 0 else 0
        settled_cnt = np.sum(sim.settled[:sim.count]) if sim.count > 0 else 0

        draw.text((85, HEIGHT - 165), f"TOTAL PARTICLES: {sim.count:,}", fill=(245, 245, 250))
        draw.text((85, HEIGHT - 135), f"ACTIVE IN FLIGHT: {active_cnt:,}", fill=(100, 200, 255))
        draw.text((85, HEIGHT - 105), f"SETTLED IN DUNES: {settled_cnt:,}", fill=(225, 185, 110))

        draw.text((560, HEIGHT - 165), f"FRAME: {frame_idx + 1:03d} / {TOTAL_FRAMES}", fill=(180, 195, 215))
        draw.text((560, HEIGHT - 135), f"REPOSE ANGLE: 32.4°", fill=(180, 195, 215))
        draw.text((560, HEIGHT - 105), f"STATUS: COMPUTING AVALANCHES", fill=(120, 220, 150))

        # Write frame to FFmpeg pipe
        proc.stdin.write(frame_pil.tobytes())

        if (frame_idx + 1) % 60 == 0 or frame_idx == TOTAL_FRAMES - 1:
            fps_proc = (frame_idx + 1) / (time.time() - start_time)
            print(f"  -> Processed frame {frame_idx + 1}/{TOTAL_FRAMES} ({fps_proc:.1f} fps) | Sand Grains: {sim.count:,}", flush=True)

    proc.stdin.close()
    proc.wait()
    total_time = time.time() - start_time
    print(f"[4/4] Video rendering completed in {total_time:.2f} seconds!")
    print(f"Output File: {output_mp4} (Size: {output_mp4.stat().st_size / 1024 / 1024:.2f} MB)")


if __name__ == "__main__":
    render_simulation_video()
