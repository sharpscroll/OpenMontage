import wave
import subprocess
import numpy as np
from pathlib import Path

# 1. Synthesize narration
narr_wav = Path("temp_narr.wav")
ps_code = """
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SelectVoice('Microsoft David Desktop')
$synth.Rate = 0
$synth.SetOutputToWaveFile('temp_narr.wav')
$synth.Speak('A single lightning bolt delivers 300 million volts. Without protection, it destroys structures. But a pointed copper lightning rod intercepts the strike, channeling the massive surge down the building exterior, safely dissipating it deep into the earth.')
$synth.Dispose()
"""
subprocess.run(["powershell", "-Command", ps_code], check=True)

# 2. Mix with sound design
sr = 44100
dur = 20.0
n = int(sr * dur)
t = np.linspace(0, dur, n, endpoint=False)
master = np.zeros(n, dtype=np.float32)

with wave.open("temp_narr.wav", "rb") as wf:
    n_frames = wf.getnframes()
    data = wf.readframes(n_frames)
    narr = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
    copy_len = min(len(narr), n)
    master[:copy_len] += narr[:copy_len] * 0.95

# Thunder crack at t=4.5s
strike_t = 4.5
idx = int(strike_t * sr)
strike_len = int(3.5 * sr)
t_strike = np.linspace(0, 3.5, strike_len, endpoint=False)
noise = np.random.normal(0, 1.0, strike_len).astype(np.float32) * np.exp(-12.0 * t_strike)
boom = np.sin(2 * np.pi * 55 * t_strike) * np.exp(-1.8 * t_strike)
master[idx : idx + strike_len] += (noise * 0.45 + boom * 0.4) * 0.75

# Surge hum (t=4.6s to 12.5s)
hum_mask = (t >= 4.6) & (t <= 12.5)
hum_env = np.sin(np.pi * (t[hum_mask] - 4.6) / 7.9)
master[hum_mask] += (np.sin(2 * np.pi * 120 * t[hum_mask]) + 0.4 * np.sin(2 * np.pi * 240 * t[hum_mask])) * hum_env * 0.12

# Subtle musical bed
master += 0.03 * (np.sin(2 * np.pi * 110 * t) + 0.5 * np.sin(2 * np.pi * 220 * t))

# Normalize
max_val = np.max(np.abs(master))
if max_val > 0:
    master = (master / max_val) * 0.88

pcm = (master * 32767).astype(np.int16)
out_wav = Path("remotion-composer/public/lightning-audio.wav")
with wave.open(str(out_wav), "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())

print("Successfully saved:", out_wav, "Size:", out_wav.stat().st_size)
if narr_wav.exists():
    narr_wav.unlink()
