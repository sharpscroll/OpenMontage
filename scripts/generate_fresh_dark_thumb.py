import subprocess
from pathlib import Path

BASE_DIR = Path(r"E:\Data\Youtube\OpenMontage-main\OpenMontage-main")
PROJECT_ASSETS = BASE_DIR / "projects" / "q61-earth-wire" / "assets" / "images" / "new"
VECTORCRAFT_CLI = r"E:\Data\Craft\apps\vectorcraft\vectorcraft-0.13.1-windows-x64-portable\vectorcraft-cli.exe"

svg_thumb = '''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
  <!-- Deep Dark Slate Background with subtle radial glow -->
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="55%" r="65%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="60%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#020617"/>
    </radialGradient>
    <radialGradient id="sparkGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.9"/>
      <stop offset="40%" stop-color="#ffe35a" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="1080" height="1920" fill="url(#bgGlow)"/>

  <!-- Top Margin Display Badge -->
  <g transform="translate(140, 200)">
    <rect x="0" y="0" width="800" height="180" rx="36" fill="#0b1320" stroke="#ffe35a" stroke-width="8"/>
    <text x="400" y="118" fill="#ffffff" font-family="Arial, sans-serif" font-weight="900" font-size="82" text-anchor="middle" letter-spacing="1">
      WHY THIS <tspan fill="#ffe35a">WIRE?</tspan>
    </text>
  </g>

  <!-- Washing machine dark mechanical chassis silhouette -->
  <rect x="140" y="460" width="800" height="1060" rx="50" fill="#131c2e" stroke="#334155" stroke-width="12"/>
  <rect x="200" y="540" width="680" height="900" rx="36" fill="#090d16" stroke="#1e293b" stroke-width="8"/>

  <!-- Dark steel drum rim -->
  <circle cx="540" cy="880" r="280" fill="#0f172a" stroke="#334155" stroke-width="10"/>
  <circle cx="540" cy="880" r="200" fill="#090d16" stroke="#1e293b" stroke-width="6"/>

  <!-- Glowing Ground Lug & Bolt Stud -->
  <!-- Energy Spark Aura -->
  <circle cx="760" cy="1160" r="260" fill="url(#sparkGlow)"/>

  <!-- Heavy Green-Yellow Conductor -->
  <path d="M480 1680 Q640 1600 720 1400 Q750 1280 760 1160" fill="none" stroke="#15803d" stroke-width="38" stroke-linecap="round"/>
  <path d="M480 1680 Q640 1600 720 1400 Q750 1280 760 1160" fill="none" stroke="#ffe35a" stroke-width="14" stroke-linecap="round" stroke-dasharray="40 40"/>

  <!-- Brass ring lug on bolt -->
  <circle cx="760" cy="1160" r="60" fill="#f59e0b" stroke="#ffffff" stroke-width="8"/>
  <circle cx="760" cy="1160" r="28" fill="#38bdf8"/>

  <!-- Electric Cyan Arcs -->
  <path d="M720 1120 L760 1160 L800 1100 M700 1180 L760 1160 L820 1220" stroke="#38bdf8" stroke-width="8" stroke-linecap="round"/>

  <!-- Bottom Callout Badge -->
  <g transform="translate(140, 1600)">
    <rect x="0" y="0" width="800" height="120" rx="28" fill="#0f172a" stroke="#38bdf8" stroke-width="6"/>
    <text x="400" y="76" fill="#38bdf8" font-family="Arial, sans-serif" font-weight="900" font-size="44" text-anchor="middle" letter-spacing="2">
      ⚡ CARRIES 0 AMPS NORMALLY ⚡
    </text>
  </g>
</svg>'''

svg_path = BASE_DIR / "temp_thumb.svg"
svg_path.write_text(svg_thumb, encoding="utf-8")
out_png = PROJECT_ASSETS / "thumbnail_q61_vector_dark.png"

cmd = [VECTORCRAFT_CLI, "convert", str(svg_path), str(out_png)]
subprocess.run(cmd, check=True)
svg_path.unlink()
print("VectorCraft generated dark thumbnail:", out_png)
