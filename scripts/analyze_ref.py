from pathlib import Path
import subprocess

ref = Path(r"E:\Data\YT\Video Data\00_Channel_Assets\Reference Images\vidssave.com You'll Finally Understand What Happens When a Neutral Wire Fails 720P.mp4")
print("Reference exists:", ref.exists())

# Extract 4 frames across first 60 seconds
for sec in [5, 15, 30, 50]:
    out_png = Path(f"ref_frame_{sec}s.png")
    subprocess.run(["ffmpeg", "-ss", str(sec), "-i", str(ref), "-vframes", "1", "-q:v", "2", str(out_png), "-y"], capture_output=True)
    if out_png.exists():
        print(f"Extracted frame at {sec}s ({out_png.stat().st_size} bytes)")
