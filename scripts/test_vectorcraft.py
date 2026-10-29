import subprocess
from pathlib import Path

svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
  <rect width="1080" height="1920" fill="#faf9f4"/>
  <rect x="100" y="100" width="880" height="400" rx="40" fill="#1b2e38"/>
  <circle cx="540" cy="960" r="150" fill="#ffe35a" stroke="#1b2e38" stroke-width="12"/>
</svg>'''

Path("test.svg").write_text(svg_content, encoding="utf-8")
cli = r"E:\Data\Craft\apps\vectorcraft\vectorcraft-0.13.1-windows-x64-portable\vectorcraft-cli.exe"
res = subprocess.run([cli, "convert", "test.svg", "test.png"], capture_output=True, text=True)
print("Return code:", res.returncode)
print("Stdout:", res.stdout)
print("Stderr:", res.stderr)
print("Output file exists:", Path("test.png").exists())
