"""Generate a 20-second technical explainer sample on Lightning Conductors.

Modeled on the Zenthral / Technical Explainer visual grammar:
- 1920x1080 16:9 Full HD, 30 FPS, exactly 20.0 seconds (600 frames)
- Deep technical navy blueprint canvas with architectural grid
- 2D/3D cutaway of modern building, roof-mounted copper Franklin rod,
  exterior copper down-conductor, and underground earthing pit
- 4 Timed Physical Phases:
  1. (0.0s - 4.3s): Thundercloud charge accumulation & 300MV threat
  2. (4.3s - 6.5s): Lightning strike intercepted by pointed air terminal
  3. (6.5s - 13.5s): High-speed electrical surge channeled down the copper cable
  4. (13.5s - 20.0s): Radial earth dissipation into grounding electrodes
- Synchronized voiceover narration, thunder crack, electric hum, and sound design
- Engineering HUD callouts and highlighted technical subtitles
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
USER_REF_DIR = Path(r"E:\Data\YT\Video Data\00_Channel_Assets\Reference Images")

WIDTH = 1920
HEIGHT = 1080
FPS = 30
DURATION_SEC = 20.0
TOTAL_FRAMES = int(FPS * DURATION_SEC)  # 600 frames

# Palette
BG_NAVY = (11, 18, 28)
GRID_LINE = (22, 38, 58)
BUILDING_WALL = (24, 38, 56)
BUILDING_ROOF = (32, 50, 72)
WINDOW_COLOR = (18, 30, 46)
WINDOW_LIT = (40, 70, 100)
EARTH_SOIL = (38, 26, 20)
EARTH_BED = (52, 38, 30)

COPPER_COLOR = (230, 126, 34)
COPPER_HIGHLIGHT = (255, 178, 90)
SURGE_YELLOW = (255, 235, 70)
SURGE_GLOW = (255, 200, 30, 180)
ELECTRIC_CYAN = (100, 220, 255)
LIGHTNING_WHITE = (255, 255, 255)
SAFE_GREEN = (46, 204, 113)

TEXT_WHITE = (245, 248, 252)
TEXT_MUTED = (140, 160, 185)
BADGE_BG = (15, 24, 38, 230)
BADGE_BORDER = (40, 65, 95, 220)


def generate_soundtrack(output_wav: Path, narration_wav: Path):
    """Mix voiceover narration with synthesized thunder, electric hum, and background bed."""
    sr = 44100
    n_samples = int(sr * DURATION_SEC)
    t = np.linspace(0, DURATION_SEC, n_samples, endpoint=False)

    master = np.zeros(n_samples, dtype=np.float32)

    # 1. Load narration
    if narration_wav.exists():
        with wave.open(str(narration_wav), "rb") as wf:
            n_narr = wf.getnframes()
            narr_data = wf.readframes(n_narr)
            narr_audio = np.frombuffer(narr_data, dtype=np.int16).astype(np.float32) / 32768.0
            # If narration sample rate differs, resample or copy
            narr_sr = wf.getframerate()
            if narr_sr == sr:
                copy_len = min(len(narr_audio), n_samples)
                master[:copy_len] += narr_audio[:copy_len] * 0.95
            else:
                # Basic linear interpolation
                t_narr = np.linspace(0, n_narr / narr_sr, n_narr)
                narr_interp = np.interp(t, t_narr, narr_audio, left=0, right=0)
                master += narr_interp * 0.95

    # 2. Thunder Rumble & Strike Crack at t=4.4s
    strike_t = 4.4
    strike_idx = int(strike_t * sr)
    strike_dur = int(3.5 * sr)
    if strike_idx + strike_dur <= n_samples:
        t_crack = np.linspace(0, 3.5, strike_dur, endpoint=False)
        # Sharp explosive crack + low boom
        noise = np.random.normal(0, 1.0, strike_dur).astype(np.float32)
        crack_env = np.exp(-12.0 * t_crack)
        boom_env = np.exp(-1.5 * t_crack)
        low_boom = np.sin(2 * np.pi * 55 * t_crack) * boom_env
        strike_audio = (noise * crack_env * 0.5 + low_boom * 0.45)
        master[strike_idx : strike_idx + strike_dur] += strike_audio * 0.7

    # 3. Electric Surge Hum (t=4.5s to 12.0s)
    hum_mask = (t >= 4.5) & (t <= 12.5)
    hum_env = np.zeros(n_samples, dtype=np.float32)
    hum_env[hum_mask] = np.sin(np.pi * (t[hum_mask] - 4.5) / 8.0)
    hum = (np.sin(2 * np.pi * 120 * t) + 0.4 * np.sin(2 * np.pi * 240 * t)) * hum_env * 0.12
    master += hum

    # 4. Tech Documentary Music Bed
    # Ambient pulsating pads (D minor / G minor)
    chord_bed = (
        0.04 * np.sin(2 * np.pi * 73.42 * t) +   # D2
        0.03 * np.sin(2 * np.pi * 146.83 * t) +  # D3
        0.02 * np.sin(2 * np.pi * 220.00 * t)    # A3
    )
    master += chord_bed

    # Master normalization
    max_amp = np.max(np.abs(master))
    if max_amp > 0:
        master = (master / max_amp) * 0.90

    pcm = (master * 32767).astype(np.int16)
    with wave.open(str(output_wav), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())


def draw_lightning_bolt(draw: ImageDraw.ImageDraw, start_pt: tuple[float, float], end_pt: tuple[float, float], branches: int = 3, seed: int = 0):
    """Draw procedural branching electric lightning discharge."""
    np.random.seed(seed)
    x1, y1 = start_pt
    x2, y2 = end_pt

    num_segs = 8
    pts = [(x1, y1)]
    for i in range(1, num_segs):
        f = i / float(num_segs)
        bx = (1 - f) * x1 + f * x2 + np.random.uniform(-40, 40)
        by = (1 - f) * y1 + f * y2 + np.random.uniform(-15, 15)
        pts.append((bx, by))
    pts.append((x2, y2))

    # Outer cyan bloom
    draw.line(pts, fill=(100, 220, 255, 180), width=16)
    # Mid glow
    draw.line(pts, fill=(180, 240, 255, 230), width=8)
    # Core bright white
    draw.line(pts, fill=(255, 255, 255, 255), width=4)

    # Branch arcs
    for b in range(branches):
        b_idx = np.random.randint(2, num_segs - 1)
        sx, sy = pts[b_idx]
        b_pts = [(sx, sy)]
        for j in range(3):
            sx += np.random.uniform(-60, 60)
            sy += np.random.uniform(30, 80)
            b_pts.append((sx, sy))
        draw.line(b_pts, fill=(100, 200, 255, 140), width=5)
        draw.line(b_pts, fill=(255, 255, 255, 200), width=2)


def render_lightning_video():
    PROJECT_DIR.mkdir(parents=True, exist_ok=True)
    RENDERS_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    output_mp4 = RENDERS_DIR / "lightning_conductor_sample_20s.mp4"
    audio_wav = ASSETS_DIR / "lightning_final_audio.wav"
    narr_wav = ASSETS_DIR / "lightning_narration.wav"

    print("[1/4] Preparing soundtrack & narration...", flush=True)
    generate_soundtrack(audio_wav, narr_wav)

    print("[2/4] Rendering technical blueprint vector scenes...", flush=True)

    # Fonts
    font_bold = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 28)
    font_sub = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 19)
    font_head = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 36)
    font_label = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 16)
    font_cap = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 30)

    # Static blueprint canvas
    canvas_bg = Image.new("RGB", (WIDTH, HEIGHT), BG_NAVY)
    draw_bg = ImageDraw.Draw(canvas_bg, "RGBA")

    # Grid lines
    for x in range(0, WIDTH, 60):
        draw_bg.line([(x, 0), (x, HEIGHT)], fill=GRID_LINE, width=1)
    for y in range(0, HEIGHT, 60):
        draw_bg.line([(0, y), (WIDTH, y)], fill=GRID_LINE, width=1)

    # Soil Section (Ground)
    ground_y = 820
    draw_bg.rectangle([0, ground_y, WIDTH, HEIGHT], fill=EARTH_SOIL)
    draw_bg.line([(0, ground_y), (WIDTH, ground_y)], fill=(80, 60, 45), width=4)
    # Earth depth strata lines
    for gy in [890, 970, 1040]:
        draw_bg.line([(0, gy), (WIDTH, gy)], fill=(48, 34, 26), width=2)

    # Building Structure
    bx1, bx2 = 560, 1420
    by_roof = 380
    by_peak = 270
    peak_x = 880

    # Main building wall
    draw_bg.rectangle([bx1, by_roof, bx2, ground_y], fill=BUILDING_WALL, outline=(45, 68, 96), width=4)

    # Pitched roof
    roof_poly = [(bx1 - 20, by_roof), (peak_x, by_peak), (bx2 + 20, by_roof)]
    draw_bg.polygon(roof_poly, fill=BUILDING_ROOF, outline=(60, 90, 125), width=4)

    # Windows matrix
    for wx in range(bx1 + 60, bx2 - 60, 120):
        for wy in range(by_roof + 60, ground_y - 60, 90):
            draw_bg.rectangle([wx, wy, wx + 65, wy + 55], fill=WINDOW_COLOR, outline=(38, 56, 80), width=2)
            # Window mullions
            draw_bg.line([(wx + 32, wy), (wx + 32, wy + 55)], fill=(30, 45, 65), width=1)

    # Franklin Rod base structure (mount)
    rod_tip = (peak_x, by_peak - 120)
    rod_base = (peak_x, by_peak)
    draw_bg.rectangle([peak_x - 12, by_peak - 10, peak_x + 12, by_peak + 10], fill=(70, 80, 95))

    # Underground Earthing Pit
    pit_x = bx1 - 30
    pit_y1 = ground_y
    pit_y2 = 1000
    # Bentonite conductive backfill bed
    draw_bg.rectangle([pit_x - 45, pit_y1 + 40, pit_x + 45, pit_y2 + 20], fill=(65, 45, 35), outline=(90, 65, 50), width=2)
    draw_bg.text((pit_x - 85, pit_y2 + 30), "EARTH PIT (BENTONITE)", font=font_label, fill=(160, 140, 120))

    # Pre-render array
    bg_array = np.array(canvas_bg, dtype=np.uint8)

    # Conductor Path coordinates
    conductor_path = [
        rod_tip,                                  # (880, 150)
        rod_base,                                 # (880, 270)
        (bx1 - 30, by_roof + 10),                 # Roof eaves corner (530, 390)
        (pit_x, ground_y),                        # Ground entry (530, 820)
        (pit_x, pit_y2),                          # Deep electrode (530, 1000)
    ]

    print("[3/4] Launching FFmpeg encoder pipeline (rawvideo -> libx264)...", flush=True)
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-i", str(audio_wav),
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
    frame_buf = bg_array.copy()
    start_time = time.time()

    # Particle pulse streams for down-conductor
    N_PULSE = 120
    pulse_offsets = np.linspace(0, 1, N_PULSE)

    for f in range(TOTAL_FRAMES):
        np.copyto(frame_buf, bg_array)
        pil_frame = Image.fromarray(frame_buf)
        draw = ImageDraw.Draw(pil_frame, "RGBA")

        # Top Header Banner
        draw.rectangle([0, 0, WIDTH, 85], fill=(15, 24, 38, 240))
        draw.line([(0, 85), (WIDTH, 85)], fill=(45, 75, 110), width=2)
        draw.text((60, 22), "HOW A LIGHTNING CONDUCTOR WORKS", font=font_head, fill=TEXT_WHITE)
        draw.rectangle([560, 35, 620, 50], fill=SURGE_YELLOW)
        draw.text((635, 28), "TECHNICAL EXPLAINER SAMPLE", font=font_label, fill=SURGE_YELLOW)

        # Draw Copper Conductor Lines (Always visible)
        # 1. Pointed Franklin Rod
        draw.line([rod_tip, rod_base], fill=COPPER_COLOR, width=10)
        draw.line([(rod_tip[0] - 2, rod_tip[1]), (rod_base[0] - 2, rod_base[1])], fill=COPPER_HIGHLIGHT, width=3)
        # Pointed sharp tip
        draw.polygon([(rod_tip[0], rod_tip[1] - 15), (rod_tip[0] - 8, rod_tip[1]), (rod_tip[0] + 8, rod_tip[1])], fill=COPPER_COLOR)

        # 2. Down-conductor along roof & wall to ground pit
        draw.line([rod_base, conductor_path[2]], fill=COPPER_COLOR, width=8)
        draw.line([conductor_path[2], conductor_path[3]], fill=COPPER_COLOR, width=8)
        draw.line([conductor_path[3], conductor_path[4]], fill=COPPER_COLOR, width=10)

        # 3. Grounding plate / radial spikes
        draw.rectangle([pit_x - 30, pit_y2 - 6, pit_x + 30, pit_y2 + 6], fill=COPPER_COLOR)
        draw.line([(pit_x - 35, pit_y2), (pit_x - 60, pit_y2 + 20)], fill=COPPER_COLOR, width=5)
        draw.line([(pit_x + 35, pit_y2), (pit_x + 60, pit_y2 + 20)], fill=COPPER_COLOR, width=5)

        # ==============================================================
        # PHASE 1 (0s - 4.3s / Frames 0 - 130): The Threat & Charge
        # ==============================================================
        if f < 130:
            badge_title = "POTENTIAL DIFFERENCE: 300,000,000 VOLTS"
            badge_sub = "Negative stepped leader forms in charged thundercloud"
            badge_color = (235, 87, 87)

            # Storm cloud at top
            cloud_cx, cloud_cy = 850, 40
            for off_x, off_y, rad in [(-120, 10, 80), (0, 0, 95), (140, 15, 85), (-60, -20, 75), (80, -15, 75)]:
                draw.ellipse([cloud_cx + off_x - rad, cloud_cy + off_y - rad, cloud_cx + off_x + rad, cloud_cy + off_y + rad], fill=(28, 42, 60, 220))

            # Charge symbols in cloud (-)
            for cx_pos in [760, 820, 880, 940]:
                draw.text((cx_pos, 50), "−", font=font_head, fill=(120, 180, 255))

            # Positive charges on building tip (+)
            if (f // 8) % 2 == 0:
                draw.text((rod_tip[0] + 15, rod_tip[1] - 30), "+", font=font_head, fill=SURGE_YELLOW)

            # Upward corona streamer hint
            streamer_h = min(40.0, f * 0.35)
            draw.line([rod_tip, (rod_tip[0], rod_tip[1] - streamer_h)], fill=ELECTRIC_CYAN, width=3)

        # ==============================================================
        # PHASE 2 (4.3s - 6.5s / Frames 130 - 195): The Strike
        # ==============================================================
        elif f < 195:
            badge_title = "DIRECT STRIKE INTERCEPTED AT AIR TERMINAL"
            badge_sub = "Pointed copper rod provides preferential attachment point"
            badge_color = SURGE_YELLOW

            # Lightning bolt striking rod tip
            seed = (f // 2) * 17
            draw_lightning_bolt(draw, (850, 40), rod_tip, branches=4, seed=seed)

            # Impact flash bloom at tip
            flash_r = 35 + ((f - 130) % 5) * 6
            draw.ellipse([rod_tip[0] - flash_r, rod_tip[1] - flash_r, rod_tip[0] + flash_r, rod_tip[1] + flash_r], fill=(255, 255, 255, 180))
            draw.ellipse([rod_tip[0] - flash_r * 1.6, rod_tip[1] - flash_r * 1.6, rod_tip[0] + flash_r * 1.6, rod_tip[1] + flash_r * 1.6], fill=(100, 220, 255, 90))

        # ==============================================================
        # PHASE 3 (6.5s - 13.5s / Frames 195 - 405): The Down-Conductor Surge
        # ==============================================================
        elif f < 405:
            badge_title = "COPPER DOWN-CONDUCTOR // LOW IMPEDANCE PATH"
            badge_sub = "30,000 Amperes routed along exterior, completely bypassing structure"
            badge_color = COPPER_HIGHLIGHT

            # Glow on conductor lines
            draw.line([rod_base, conductor_path[2]], fill=SURGE_GLOW, width=16)
            draw.line([conductor_path[2], conductor_path[3]], fill=SURGE_GLOW, width=16)
            draw.line([conductor_path[3], conductor_path[4]], fill=SURGE_GLOW, width=16)

            # Moving surge particle packets
            surge_speed = 0.05
            for i in range(N_PULSE):
                p_progress = (pulse_offsets[i] + (f - 195) * surge_speed) % 1.0

                # Map progress to 3 segments:
                # Seg 1: rod_base -> corner (35%)
                # Seg 2: corner -> ground (45%)
                # Seg 3: ground -> pit (20%)
                if p_progress < 0.35:
                    u = p_progress / 0.35
                    px = (1 - u) * rod_base[0] + u * conductor_path[2][0]
                    py = (1 - u) * rod_base[1] + u * conductor_path[2][1]
                elif p_progress < 0.80:
                    u = (p_progress - 0.35) / 0.45
                    px = (1 - u) * conductor_path[2][0] + u * conductor_path[3][0]
                    py = (1 - u) * conductor_path[2][1] + u * conductor_path[3][1]
                else:
                    u = (p_progress - 0.80) / 0.20
                    px = (1 - u) * conductor_path[3][0] + u * conductor_path[4][0]
                    py = (1 - u) * conductor_path[3][1] + u * conductor_path[4][1]

                draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=SURGE_YELLOW)

            # Green safe shield glow on protected building interior
            draw.rectangle([bx1 + 10, by_roof + 10, bx2 - 10, ground_y - 10], outline=(46, 204, 113, 80), width=4)
            draw.text((bx1 + 240, by_roof + 180), "PROTECTED INTERIOR // 0V SURGE", font=font_head, fill=(46, 204, 113, 140))

        # ==============================================================
        # PHASE 4 (13.5s - 20.0s / Frames 405 - 600): Ground Dissipation
        # ==============================================================
        else:
            badge_title = "EQUIPOTENTIAL GROUND DISSIPATION // ZERO DAMAGE"
            badge_sub = "Massive charge safely dispersed into earth grid reference"
            badge_color = SAFE_GREEN

            # Concentric expanding ground dissipation waves
            wave_f = f - 405
            for w_idx in range(4):
                w_rad = ((wave_f * 4.5 + w_idx * 55) % 220) + 15
                w_alpha = int(220 * max(0.0, 1.0 - w_rad / 235.0))
                draw.ellipse([pit_x - w_rad, pit_y2 - w_rad * 0.6, pit_x + w_rad, pit_y2 + w_rad * 0.6], outline=(100, 240, 160, w_alpha), width=4)

            # Building checkmark indicator
            draw.rectangle([bx1 + 220, by_roof + 160, bx2 - 220, by_roof + 260], fill=(15, 35, 25, 230), outline=SAFE_GREEN, width=3)
            draw.text((bx1 + 260, by_roof + 185), "BUILDING & RESIDENTS PROTECTED", font=font_bold, fill=SAFE_GREEN)

        # -------------------------------------------------------------
        # Draw Technical HUD Callout Badge
        # -------------------------------------------------------------
        badge_x, badge_y = 60, 120
        draw.rectangle([badge_x, badge_y, badge_x + 720, badge_y + 85], fill=BADGE_BG, outline=BADGE_BORDER, width=2)
        draw.rectangle([badge_x, badge_y, badge_x + 8, badge_y + 85], fill=badge_color)
        draw.text((badge_x + 25, badge_y + 14), badge_title, font=font_bold, fill=badge_color)
        draw.text((badge_x + 25, badge_y + 48), badge_sub, font=font_sub, fill=TEXT_MUTED)

        # -------------------------------------------------------------
        # Synchronized Voiceover Captions (Zenthral Style)
        # -------------------------------------------------------------
        # 0s - 4.5s: "A single lightning bolt delivers 300 million volts..."
        # 4.5s - 9.0s: "Without protection, it shatters structures and starts fires."
        # 9.0s - 14.5s: "But a pointed copper rod intercepts the strike, channeling it down..."
        # 14.5s - 20.0s: "and safely dissipating it deep into the earth."
        if f < 135:
            caption_text = "A SINGLE LIGHTNING BOLT DELIVERS 300 MILLION VOLTS"
        elif f < 270:
            caption_text = "WITHOUT PROTECTION, IT SHATTERS STRUCTURES AND STARTS FIRES"
        elif f < 435:
            caption_text = "A COPPER ROD INTERCEPTS AND CHANNELS THE SURGE DOWN"
        else:
            caption_text = "SAFELY DISSIPATING THE ENORMOUS CHARGE DEEP INTO THE EARTH"

        # Caption box at bottom
        cap_y = HEIGHT - 85
        bbox = draw.textbbox((0, 0), caption_text, font=font_cap)
        cap_w = bbox[2] - bbox[0]
        cap_x = (WIDTH - cap_w) // 2

        draw.rectangle([cap_x - 20, cap_y - 10, cap_x + cap_w + 20, cap_y + 42], fill=(8, 14, 22, 230), outline=(35, 55, 80), width=2)
        draw.text((cap_x, cap_y), caption_text, font=font_cap, fill=SURGE_YELLOW)

        # Write frame to FFmpeg pipe
        proc.stdin.write(pil_frame.tobytes())

        if (f + 1) % 100 == 0 or f == TOTAL_FRAMES - 1:
            fps_proc = (f + 1) / (time.time() - start_time)
            print(f"  -> Rendered frame {f + 1}/{TOTAL_FRAMES} ({fps_proc:.1f} fps)", flush=True)

    proc.stdin.close()
    proc.wait()
    total_time = time.time() - start_time
    print(f"[4/4] 20s Lightning Conductor Explainer finished in {total_time:.2f} seconds!", flush=True)
    print(f"Primary Output: {output_mp4} ({output_mp4.stat().st_size / (1024 * 1024):.2f} MB)", flush=True)

    # Copy directly into user's requested Reference Images folder
    if USER_REF_DIR.exists():
        dest_user = USER_REF_DIR / "lightning_conductor_sample_20s.mp4"
        shutil.copy2(output_mp4, dest_user)
        print(f"Copied to requested channel location: {dest_user}", flush=True)


if __name__ == "__main__":
    render_lightning_video()
