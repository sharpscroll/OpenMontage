"""Generate a 10-second cinematic Sand Simulation video on Electricity.

Adheres strictly to the OpenMontage 'time, told in sand' visual identity:
- Antique cream parchment canvas with soft radial vignette and paper texture
- Charcoal umber sand granules converging into line-drawn motifs of electrical history
- 3 Epochs:
  1. The Spark (c. 600 BCE): Lightning bolt & static friction
  2. The Illumination (1879): Edison incandescent bulb & filament current
  3. The Grid / Circuit (Modern): Microchip & electronic traces
- Organic windblown dispersal transitions between epochs
- Delicate classical serif typography (Georgia) in small-caps
- Warm acoustic chime chords & granular sand wind audio
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

REPO_ROOT = Path(__file__).resolve().parent.parent
PROJECT_DIR = REPO_ROOT / "projects" / "sand-simulation-motion"
RENDERS_DIR = PROJECT_DIR / "renders"
ASSETS_DIR = PROJECT_DIR / "assets"

WIDTH = 1920
HEIGHT = 1080
FPS = 30
DURATION_SEC = 10.0
TOTAL_FRAMES = int(FPS * DURATION_SEC)  # 300 frames

# OpenMontage Palette
PARCHMENT_LIGHT = (239, 232, 216)   # #EFE8D8
PARCHMENT_DARK = (218, 207, 184)    # #DACFB8
SAND_COLORS = np.array([
    [38, 33, 28],    # Charcoal umber
    [48, 41, 34],    # Medium umber
    [26, 22, 18],    # Deep charcoal black
    [58, 49, 41],    # Soft warm sepia
    [34, 29, 24],    # Raw umber
], dtype=np.uint8)

TEXT_COLOR = (42, 36, 31)
SUBTEXT_COLOR = (112, 100, 88)
RULE_COLOR = (180, 168, 150)


def create_parchment_background() -> np.ndarray:
    """Generate high-resolution antique paper canvas with radial vignette."""
    bg = Image.new("RGB", (WIDTH, HEIGHT), PARCHMENT_LIGHT)
    draw = ImageDraw.Draw(bg, "RGBA")

    # Radial vignette gradient
    cx, cy = WIDTH // 2, HEIGHT // 2
    max_dist = math.hypot(cx, cy)
    y_coords, x_coords = np.ogrid[:HEIGHT, :WIDTH]
    dist_map = np.hypot(x_coords - cx, y_coords - cy) / max_dist

    # Blend between light center and darker antique edges
    factor = np.clip((dist_map - 0.3) / 0.7, 0.0, 1.0)
    factor = factor[:, :, np.newaxis]

    bg_arr = np.array(bg, dtype=np.float32)
    dark_arr = np.array(PARCHMENT_DARK, dtype=np.float32)
    blended = bg_arr * (1.0 - factor * 0.45) + dark_arr * (factor * 0.45)

    # Add faint tactile paper grain noise
    np.random.seed(42)
    noise = np.random.normal(0, 1.8, (HEIGHT, WIDTH, 3))
    blended = np.clip(blended + noise, 0, 255).astype(np.uint8)

    return blended


def generate_target_masks(n_particles: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate target coordinate clouds for: Lightning, Edison Bulb, Circuit."""
    # -------------------------------------------------------------
    # 1. Lightning Bolt (The Spark)
    # -------------------------------------------------------------
    m1 = Image.new("L", (WIDTH, HEIGHT), 0)
    d1 = ImageDraw.Draw(m1)

    cx, cy = 960, 430
    # Outer jagged bolt
    bolt_pts = [
        (cx + 10, cy - 250),
        (cx - 75, cy - 10),
        (cx + 25, cy - 10),
        (cx - 50, cy + 250),
        (cx + 110, cy - 30),
        (cx + 20, cy - 30),
        (cx + 90, cy - 250),
    ]
    d1.polygon(bolt_pts, fill=255)
    # Electric aura sparks and branch discharges
    d1.line([(cx - 75, cy - 10), (cx - 150, cy + 40), (cx - 130, cy + 90)], fill=255, width=12)
    d1.line([(cx + 110, cy - 30), (cx + 180, cy - 80), (cx + 220, cy - 60)], fill=255, width=10)
    for x, y, r in [(cx - 180, cy - 80, 14), (cx + 190, cy + 80, 16), (cx - 100, cy + 180, 14), (cx + 120, cy + 200, 12)]:
        d1.ellipse([x - r, y - r, x + r, y + r], fill=255)

    pts1 = np.argwhere(np.array(m1) > 100)
    idx1 = np.random.choice(len(pts1), n_particles, replace=True)
    coords1 = pts1[idx1][:, [1, 0]].astype(np.float32)  # [x, y]

    # -------------------------------------------------------------
    # 2. Edison Lightbulb (The Illumination)
    # -------------------------------------------------------------
    m2 = Image.new("L", (WIDTH, HEIGHT), 0)
    d2 = ImageDraw.Draw(m2)

    cx, cy = 960, 420
    # Bulb glass envelope (pear shape)
    d2.ellipse([cx - 160, cy - 220, cx + 160, cy + 100], outline=255, width=16)
    d2.line([(cx - 120, cy + 20), (cx - 70, cy + 150)], fill=255, width=16)
    d2.line([(cx + 120, cy + 20), (cx + 70, cy + 150)], fill=255, width=16)

    # Screw base threads
    for y_off in [155, 175, 195, 215]:
        d2.line([(cx - 68, cy + y_off), (cx + 68, cy + y_off)], fill=255, width=14)
    # Bottom contact tip
    d2.ellipse([cx - 35, cy + 220, cx + 35, cy + 250], fill=255)

    # Internal dual lead wires
    d2.line([(cx - 35, cy + 150), (cx - 35, cy - 20)], fill=255, width=8)
    d2.line([(cx + 35, cy + 150), (cx + 35, cy - 20)], fill=255, width=8)

    # Looped incandescent filament
    filament_pts = [
        (cx - 35, cy - 20),
        (cx - 20, cy - 80),
        (cx, cy - 50),
        (cx + 20, cy - 80),
        (cx + 35, cy - 20),
    ]
    d2.line(filament_pts, fill=255, width=12)

    # Radiating warm light rays
    ray_angles = np.linspace(-150, -30, 7)
    for ang in ray_angles:
        rad = math.radians(ang)
        r1, r2 = 200, 260
        x1 = cx + r1 * math.cos(rad)
        y1 = (cy - 60) + r1 * math.sin(rad)
        x2 = cx + r2 * math.cos(rad)
        y2 = (cy - 60) + r2 * math.sin(rad)
        d2.line([(x1, y1), (x2, y2)], fill=255, width=8)

    pts2 = np.argwhere(np.array(m2) > 100)
    idx2 = np.random.choice(len(pts2), n_particles, replace=True)
    coords2 = pts2[idx2][:, [1, 0]].astype(np.float32)

    # -------------------------------------------------------------
    # 3. Microchip & Circuit Grid (The Modern Power)
    # -------------------------------------------------------------
    m3 = Image.new("L", (WIDTH, HEIGHT), 0)
    d3 = ImageDraw.Draw(m3)

    cx, cy = 960, 420
    # Outer IC silicon package
    d3.rectangle([cx - 130, cy - 130, cx + 130, cy + 130], outline=255, width=14)
    # Central die
    d3.rectangle([cx - 65, cy - 65, cx + 65, cy + 65], fill=255)

    # Little lightning motif inside die
    die_bolt = [(cx, cy - 40), (cx - 20, cy), (cx + 10, cy), (cx - 5, cy + 40), (cx + 25, cy - 5), (cx - 5, cy - 5)]
    d3.polygon(die_bolt, fill=0)

    # Circuit traces radiating in 4 directions
    trace_offsets = [-90, -45, 0, 45, 90]
    # Left / Right traces
    for off in trace_offsets:
        # Left
        d3.line([(cx - 130, cy + off), (cx - 280, cy + off)], fill=255, width=8)
        d3.ellipse([cx - 295, cy + off - 10, cx - 275, cy + off + 10], fill=255)
        # Right
        d3.line([(cx + 130, cy + off), (cx + 280, cy + off)], fill=255, width=8)
        d3.ellipse([cx + 275, cy + off - 10, cx + 295, cy + off + 10], fill=255)

    # Top / Bottom traces
    for off in [-80, 0, 80]:
        # Top
        d3.line([(cx + off, cy - 130), (cx + off, cy - 250)], fill=255, width=8)
        d3.ellipse([cx + off - 10, cy - 265, cx + off + 10, cy - 245], fill=255)
        # Bottom
        d3.line([(cx + off, cy + 130), (cx + off, cy + 250)], fill=255, width=8)
        d3.ellipse([cx + off - 10, cy + 245, cx + off + 10, cy + 265], fill=255)

    pts3 = np.argwhere(np.array(m3) > 100)
    idx3 = np.random.choice(len(pts3), n_particles, replace=True)
    coords3 = pts3[idx3][:, [1, 0]].astype(np.float32)

    return coords1, coords2, coords3


def generate_soundtrack(output_wav: Path, duration_sec: float = 10.0):
    """Synthesize warm acoustic guitar / piano chords & sand wind dispersal sound."""
    sr = 44100
    n_samples = int(sr * duration_sec)
    t = np.linspace(0, duration_sec, n_samples, endpoint=False)

    master = np.zeros(n_samples, dtype=np.float32)

    # 1. Warm harmonic acoustic chimes (E minor -> A major -> D major)
    chords = [
        # (start_time, frequencies in Hz)
        (0.2, [164.81, 196.00, 246.94, 329.63, 392.00]),  # E minor 9
        (3.6, [220.00, 277.18, 329.63, 440.00, 554.37]),  # A major
        (7.2, [146.83, 220.00, 293.66, 369.99, 440.00]),  # D major 9
    ]

    for (start_t, freqs) in chords:
        start_idx = int(start_t * sr)
        chord_len = int(3.2 * sr)
        if start_idx + chord_len > n_samples:
            chord_len = n_samples - start_idx
        t_chord = np.linspace(0, 3.2, chord_len, endpoint=False)

        for freq in freqs:
            # Pluck envelope: sharp attack, exponential ring
            env = np.exp(-1.4 * t_chord)
            # Harmonic richness
            tone = (
                0.60 * np.sin(2 * np.pi * freq * t_chord) +
                0.25 * np.sin(2 * np.pi * 2 * freq * t_chord) +
                0.15 * np.sin(2 * np.pi * 3 * freq * t_chord)
            ) * env
            master[start_idx : start_idx + chord_len] += tone * 0.12

    # 2. Granular sand wind whooshes during transitions (t=2.8-3.6 and t=6.4-7.2)
    noise = np.random.normal(0, 0.2, n_samples).astype(np.float32)
    # Bandpass filter for sand texture
    k = np.ones(20) / 20.0
    smooth_noise = np.convolve(noise, k, mode="same")
    grit = noise - smooth_noise

    wind_env = np.zeros(n_samples, dtype=np.float32)
    for gust_center in [3.1, 6.7]:
        dist = np.abs(t - gust_center)
        wind_env += np.exp(-0.5 * (dist / 0.35) ** 2)

    master += grit * wind_env * 0.22

    # Soft ambient room bed
    master += 0.02 * np.sin(2 * np.pi * 110 * t)

    # Master limiter & 16-bit PCM write
    max_amp = np.max(np.abs(master))
    if max_amp > 0:
        master = (master / max_amp) * 0.88

    pcm = (master * 32767).astype(np.int16)
    with wave.open(str(output_wav), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())


def render_electricity_sand_video():
    PROJECT_DIR.mkdir(parents=True, exist_ok=True)
    RENDERS_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    output_mp4 = RENDERS_DIR / "sand_electricity_10s.mp4"
    audio_wav = ASSETS_DIR / "sand_electricity_audio.wav"

    print("[1/4] Synthesizing acoustic chimes & wind audio...", flush=True)
    generate_soundtrack(audio_wav, duration_sec=DURATION_SEC)

    print("[2/4] Generating OpenMontage parchment canvas and sand particle target clouds...", flush=True)
    bg_canvas = create_parchment_background()

    N_PARTICLES = 26000
    c1, c2, c3 = generate_target_masks(N_PARTICLES)

    # Particle properties
    np.random.seed(1337)
    color_indices = np.random.randint(0, len(SAND_COLORS), N_PARTICLES)
    drag_factors = np.random.uniform(0.75, 1.35, N_PARTICLES)
    jitter_seeds = np.random.uniform(0, 2 * math.pi, N_PARTICLES)

    # Initial start positions (sweeping in from left/bottom wind cloud)
    pos_start = np.zeros((N_PARTICLES, 2), dtype=np.float32)
    pos_start[:, 0] = np.random.uniform(-400, 300, N_PARTICLES)
    pos_start[:, 1] = np.random.uniform(200, HEIGHT + 300, N_PARTICLES)

    # Font setup (Georgia / Times New Roman)
    font_path = "C:/Windows/Fonts/georgia.ttf" if os.path.exists("C:/Windows/Fonts/georgia.ttf") else "C:/Windows/Fonts/times.ttf"
    font_title = ImageFont.truetype(font_path, 34)
    font_sub = ImageFont.truetype(font_path, 21)

    print("[3/4] Launching FFmpeg encoder pipeline (rawvideo -> libx264)...", flush=True)
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

    frame_buf = bg_canvas.copy()
    start_time = time.time()

    # Timeline layout (300 frames total):
    # Scene 1: 0 - 100   (0.0s - 3.33s)
    # Scene 2: 100 - 210 (3.33s - 7.00s)
    # Scene 3: 210 - 300 (7.00s - 10.0s)

    current_pos = np.zeros((N_PARTICLES, 2), dtype=np.float32)

    for f in range(TOTAL_FRAMES):
        np.copyto(frame_buf, bg_canvas)

        # -------------------------------------------------------------
        # Scene 1: The Spark (Lightning Bolt)
        # -------------------------------------------------------------
        if f < 100:
            scene_title = "T H E   S P A R K"
            scene_sub = "c. 600 BCE · Static Friction & Amber"

            if f < 35:
                # Formation: sweep in from cloud
                u = f / 35.0
                p = u * u * (3.0 - 2.0 * u)
                turb_x = np.sin(0.015 * c1[:, 1] + 4.0 * u) * (1.0 - p) * 140.0
                turb_y = np.cos(0.012 * c1[:, 0] + 3.0 * u) * (1.0 - p) * 90.0
                current_pos[:, 0] = (1.0 - p) * pos_start[:, 0] + p * c1[:, 0] + turb_x
                current_pos[:, 1] = (1.0 - p) * pos_start[:, 1] + p * c1[:, 1] + turb_y
                text_alpha = p
            elif f < 80:
                # Hold & Electric Vibrate
                jit_x = np.sin(jitter_seeds + f * 0.4) * 1.5
                jit_y = np.cos(jitter_seeds + f * 0.4) * 1.5
                current_pos[:, 0] = c1[:, 0] + jit_x
                current_pos[:, 1] = c1[:, 1] + jit_y
                text_alpha = 1.0
            else:
                # Dispersal: wind sweeps to the right
                w = (f - 80) / 20.0
                wind_x = (w ** 2) * 1800.0 * drag_factors
                wind_y = w * 140.0 * np.sin(jitter_seeds)
                current_pos[:, 0] = c1[:, 0] + wind_x
                current_pos[:, 1] = c1[:, 1] + wind_y
                text_alpha = max(0.0, 1.0 - w * 1.5)

        # -------------------------------------------------------------
        # Scene 2: The Illumination (Edison Lightbulb)
        # -------------------------------------------------------------
        elif f < 210:
            sf = f - 100
            scene_title = "T H E   I L L U M I N A T I O N"
            scene_sub = "1879 · Incandescent Current & The Grid"

            if sf < 35:
                u = sf / 35.0
                p = u * u * (3.0 - 2.0 * u)
                turb_x = np.sin(0.014 * c2[:, 1] + 3.5 * u) * (1.0 - p) * 160.0
                turb_y = np.cos(0.012 * c2[:, 0] + 2.5 * u) * (1.0 - p) * 100.0
                current_pos[:, 0] = (1.0 - p) * (c1[:, 0] + 600.0) + p * c2[:, 0] + turb_x
                current_pos[:, 1] = (1.0 - p) * (c1[:, 1] + 100.0) + p * c2[:, 1] + turb_y
                text_alpha = p
            elif sf < 85:
                # Hold & Filament current circulation
                jit_x = np.sin(jitter_seeds + f * 0.35) * 1.4
                jit_y = np.cos(jitter_seeds + f * 0.35) * 1.4
                current_pos[:, 0] = c2[:, 0] + jit_x
                current_pos[:, 1] = c2[:, 1] + jit_y
                text_alpha = 1.0
            else:
                # Dispersal
                w = (sf - 85) / 25.0
                wind_x = (w ** 2) * 1900.0 * drag_factors
                wind_y = w * 160.0 * np.sin(jitter_seeds)
                current_pos[:, 0] = c2[:, 0] + wind_x
                current_pos[:, 1] = c2[:, 1] + wind_y
                text_alpha = max(0.0, 1.0 - w * 1.5)

        # -------------------------------------------------------------
        # Scene 3: The Modern Grid & Circuit (Conclusion)
        # -------------------------------------------------------------
        else:
            sf = f - 210
            scene_title = "P O W E R ,   T O L D   I N   S A N D"
            scene_sub = "From ancient friction to the planetary grid"

            if sf < 35:
                u = sf / 35.0
                p = u * u * (3.0 - 2.0 * u)
                turb_x = np.sin(0.015 * c3[:, 1] + 3.0 * u) * (1.0 - p) * 150.0
                turb_y = np.cos(0.012 * c3[:, 0] + 2.0 * u) * (1.0 - p) * 90.0
                current_pos[:, 0] = (1.0 - p) * (c2[:, 0] + 700.0) + p * c3[:, 0] + turb_x
                current_pos[:, 1] = (1.0 - p) * (c2[:, 1] + 120.0) + p * c3[:, 1] + turb_y
                text_alpha = p
            else:
                jit_x = np.sin(jitter_seeds + f * 0.3) * 1.2
                jit_y = np.cos(jitter_seeds + f * 0.3) * 1.2
                current_pos[:, 0] = c3[:, 0] + jit_x
                current_pos[:, 1] = c3[:, 1] + jit_y
                text_alpha = 1.0 if f < 285 else max(0.0, (300 - f) / 15.0)

        # Draw sand particles (organic stippling)
        valid = (current_pos[:, 0] >= 0) & (current_pos[:, 0] < WIDTH - 2) & (current_pos[:, 1] >= 0) & (current_pos[:, 1] < HEIGHT - 2)
        px = current_pos[valid, 0].astype(int)
        py = current_pos[valid, 1].astype(int)
        cols = SAND_COLORS[color_indices[valid]]

        # 2x2 grain stamp
        frame_buf[py, px] = cols
        frame_buf[py + 1, px] = cols
        frame_buf[py, px + 1] = cols
        frame_buf[py + 1, px + 1] = cols

        # Overlay Classical Typography
        pil_frame = Image.fromarray(frame_buf)
        draw = ImageDraw.Draw(pil_frame)

        if text_alpha > 0.05:
            # Interpolate text color toward parchment background for smooth alpha fade
            alpha = min(1.0, text_alpha)
            t_col = tuple(int(TEXT_COLOR[i] * alpha + PARCHMENT_LIGHT[i] * (1.0 - alpha)) for i in range(3))
            s_col = tuple(int(SUBTEXT_COLOR[i] * alpha + PARCHMENT_LIGHT[i] * (1.0 - alpha)) for i in range(3))
            r_col = tuple(int(RULE_COLOR[i] * alpha + PARCHMENT_LIGHT[i] * (1.0 - alpha)) for i in range(3))

            # Center Title
            bbox_title = draw.textbbox((0, 0), scene_title, font=font_title)
            title_w = bbox_title[2] - bbox_title[0]
            tx = (WIDTH - title_w) // 2
            ty = 820
            draw.text((tx, ty), scene_title, font=font_title, fill=t_col)

            # Delicate underline rule
            rule_w = min(title_w + 60, 420)
            rx1 = (WIDTH - rule_w) // 2
            rx2 = rx1 + rule_w
            draw.line([(rx1, ty + 50), (rx2, ty + 50)], fill=r_col, width=1)

            # Subtitle
            bbox_sub = draw.textbbox((0, 0), scene_sub, font=font_sub)
            sub_w = bbox_sub[2] - bbox_sub[0]
            sx = (WIDTH - sub_w) // 2
            draw.text((sx, ty + 62), scene_sub, font=font_sub, fill=s_col)

        # Write frame to FFmpeg pipe
        proc.stdin.write(pil_frame.tobytes())

        if (f + 1) % 60 == 0 or f == TOTAL_FRAMES - 1:
            fps_proc = (f + 1) / (time.time() - start_time)
            print(f"  -> Rendered frame {f + 1}/{TOTAL_FRAMES} ({fps_proc:.1f} fps)", flush=True)

    proc.stdin.close()
    proc.wait()
    total_time = time.time() - start_time
    print(f"[4/4] 10s Sand Simulation completed in {total_time:.2f} seconds!", flush=True)
    print(f"Output: {output_mp4} ({output_mp4.stat().st_size / (1024 * 1024):.2f} MB)", flush=True)


if __name__ == "__main__":
    render_electricity_sand_video()
