"""Generate fresh, high-resolution Cause & Motion engineering illustrations for Q61
and convert them using VectorCraft CLI.
"""

import subprocess
from pathlib import Path

# Paths
BASE_DIR = Path(r"E:\Data\Youtube\OpenMontage-main\OpenMontage-main")
PROJECT_ASSETS = BASE_DIR / "projects" / "q61-earth-wire" / "assets" / "images" / "new"
REMOTION_ASSETS = BASE_DIR / "remotion-composer" / "public" / "q61_new"
PROJECT_ASSETS.mkdir(parents=True, exist_ok=True)
REMOTION_ASSETS.mkdir(parents=True, exist_ok=True)

VECTORCRAFT_CLI = r"E:\Data\Craft\apps\vectorcraft\vectorcraft-0.13.1-windows-x64-portable\vectorcraft-cli.exe"

# Brand Palette
INK = "#1b2e38"
PAPER = "#faf9f4"
GOLD = "#ffe35a"
GREEN = "#176e4e"
LIVE = "#c86b43"
NEUTRAL = "#5a82a6"
FAULT = "#d7584d"
STEEL = "#e2e8f0"
DARK_STEEL = "#475569"

SVGS = {}

# 1. NEW WASHER CUTAWAY
SVGS["scene1_washer_cutaway.svg"] = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
  <rect width="1080" height="1920" fill="{PAPER}"/>
  
  <!-- Outer Cabinet Outline -->
  <rect x="120" y="320" width="840" height="1140" rx="48" fill="#f1f5f7" stroke="{INK}" stroke-width="12"/>
  
  <!-- Back panel service access cutaway -->
  <rect x="180" y="440" width="720" height="960" rx="36" fill="#ffffff" stroke="{INK}" stroke-width="8" stroke-dasharray="16 12"/>
  
  <!-- Inner drum pulley and bearing housing -->
  <circle cx="540" cy="800" r="280" fill="#f8fafc" stroke="{INK}" stroke-width="10"/>
  <circle cx="540" cy="800" r="190" fill="#e2e8f0" stroke="{INK}" stroke-width="8"/>
  <circle cx="540" cy="800" r="60" fill="{INK}"/>
  
  <!-- Drive Belt down to motor -->
  <path d="M480 800 L440 1230 M600 800 L640 1230" stroke="{INK}" stroke-width="14" stroke-linecap="round"/>
  
  <!-- Motor at base -->
  <rect x="410" y="1220" width="260" height="160" rx="24" fill="#cbd5e1" stroke="{INK}" stroke-width="10"/>
  <rect x="460" y="1250" width="160" height="100" rx="14" fill="{INK}"/>
  <text x="540" y="1312" fill="#ffffff" font-family="Arial, sans-serif" font-weight="900" font-size="34" text-anchor="middle">MOTOR</text>
  
  <!-- 3-Core Supply Cable entering bottom right -->
  <path d="M960 1340 Q840 1340 760 1290" fill="none" stroke="{INK}" stroke-width="28" stroke-linecap="round"/>
  
  <!-- Live and Neutral going to motor -->
  <path d="M760 1290 Q720 1270 670 1270" fill="none" stroke="{LIVE}" stroke-width="12" stroke-linecap="round"/>
  <path d="M760 1290 Q720 1310 670 1310" fill="none" stroke="{NEUTRAL}" stroke-width="12" stroke-linecap="round"/>
  
  <!-- Earth Conductor splitting off and bolting directly to chassis metal -->
  <path d="M760 1290 Q820 1220 830 1100 Q840 980 840 880" fill="none" stroke="{GREEN}" stroke-width="18" stroke-linecap="round"/>
  <path d="M760 1290 Q820 1220 830 1100 Q840 980 840 880" fill="none" stroke="{GOLD}" stroke-width="6" stroke-linecap="round" stroke-dasharray="24 24"/>
  
  <!-- Earth Chassis Bolt Stud -->
  <circle cx="840" cy="880" r="38" fill="{GOLD}" stroke="{INK}" stroke-width="8"/>
  <circle cx="840" cy="880" r="16" fill="{INK}"/>
  
  <!-- High visibility callout badge -->
  <g transform="translate(490, 480)">
    <rect x="0" y="0" width="370" height="90" rx="18" fill="#ffffff" stroke="{GREEN}" stroke-width="6"/>
    <text x="185" y="58" fill="{GREEN}" font-family="Arial, sans-serif" font-weight="900" font-size="36" text-anchor="middle">EARTH / GROUND</text>
  </g>
  <path d="M675 570 Q750 680 820 840" fill="none" stroke="{GREEN}" stroke-width="7" stroke-linecap="round"/>
  <circle cx="820" cy="840" r="12" fill="{GOLD}" stroke="{GREEN}" stroke-width="4"/>
</svg>'''

# 2. NEW CIRCUIT SCHEMATIC (NORMAL LOOP)
SVGS["scene2_circuit_normal.svg"] = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
  <rect width="1080" height="1920" fill="{PAPER}"/>
  
  <!-- Appliance Metal Enclosure boundary -->
  <rect x="480" y="420" width="500" height="980" rx="36" fill="#f8fafc" stroke="{INK}" stroke-width="8" stroke-dasharray="16 12"/>
  <text x="730" y="480" fill="{INK}" font-family="Arial, sans-serif" font-weight="900" font-size="32" text-anchor="middle">WASHER METAL CHASSIS</text>
  
  <!-- AC Supply Source -->
  <circle cx="180" cy="780" r="80" fill="#ffffff" stroke="{INK}" stroke-width="10"/>
  <text x="180" y="792" fill="{INK}" font-family="Arial, sans-serif" font-weight="900" font-size="44" text-anchor="middle">230V AC</text>
  
  <!-- Motor Load Inside Washer -->
  <rect x="620" y="760" width="220" height="220" rx="36" fill="#ffffff" stroke="{INK}" stroke-width="10"/>
  <circle cx="730" cy="870" r="70" fill="#e2e8f0" stroke="{INK}" stroke-width="6"/>
  <text x="730" y="882" fill="{INK}" font-family="Arial, sans-serif" font-weight="900" font-size="34" text-anchor="middle">MOTOR</text>
  
  <!-- Live Conductor Loop (Brown) -->
  <path d="M180 700 V560 H620 V760" fill="none" stroke="{LIVE}" stroke-width="22" stroke-linecap="round"/>
  
  <!-- Neutral Return Loop (Blue) -->
  <path d="M840 870 H920 V1120 H180 V860" fill="none" stroke="{NEUTRAL}" stroke-width="22" stroke-linecap="round"/>
  
  <!-- Current Flow Animated Indicator Dots -->
  <path d="M180 700 V560 H620 V760" fill="none" stroke="{GOLD}" stroke-width="8" stroke-dasharray="28 20" stroke-linecap="round"/>
  <path d="M840 870 H920 V1120 H180 V860" fill="none" stroke="#93c5fd" stroke-width="8" stroke-dasharray="28 20" stroke-linecap="round"/>
  
  <!-- Earth Conductor connected only to Chassis boundary -->
  <path d="M480 920 H340 V1340 H180" fill="none" stroke="{GREEN}" stroke-width="20" stroke-linecap="round"/>
  <path d="M480 920 H340 V1340 H180" fill="none" stroke="{GOLD}" stroke-width="6" stroke-dasharray="18 18"/>
  <circle cx="480" cy="920" r="18" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>
  
  <!-- Earth Status Badge -->
  <g transform="translate(140, 1420)">
    <rect x="0" y="0" width="800" height="110" rx="22" fill="#ffffff" stroke="{GREEN}" stroke-width="6"/>
    <text x="400" y="70" fill="{GREEN}" font-family="Arial, sans-serif" font-weight="900" font-size="40" text-anchor="middle">CURRENT IN EARTH = 0.00 AMPS</text>
  </g>
</svg>'''

# 3. NEW CHASSIS STUD MACRO DETAIL
SVGS["scene3_chassis_stud.svg"] = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
  <rect width="1080" height="1920" fill="{PAPER}"/>
  
  <!-- Large Metal Chassis Sheet in Background -->
  <rect x="100" y="380" width="880" height="1100" rx="40" fill="#e2e8f0" stroke="{INK}" stroke-width="12"/>
  <line x1="160" y1="460" x2="920" y2="460" stroke="#cbd5e1" stroke-width="6"/>
  <line x1="160" y1="520" x2="920" y2="520" stroke="#cbd5e1" stroke-width="6"/>
  <text x="540" y="580" fill="{DARK_STEEL}" font-family="Arial, sans-serif" font-weight="900" font-size="44" text-anchor="middle">UNPAINTED CHASSIS STEEL</text>
  
  <!-- Ground Stud Assembly -->
  <!-- Radiating target circles -->
  <circle cx="540" cy="960" r="260" fill="none" stroke="{GOLD}" stroke-width="12" opacity="0.6"/>
  <circle cx="540" cy="960" r="190" fill="none" stroke="{GOLD}" stroke-width="8" stroke-dasharray="24 16"/>
  
  <!-- Star Washer (toothed) -->
  <circle cx="540" cy="960" r="140" fill="#94a3b8" stroke="{INK}" stroke-width="8"/>
  
  <!-- Brass Crimp Ring Lug -->
  <circle cx="540" cy="960" r="100" fill="#f59e0b" stroke="{INK}" stroke-width="10"/>
  <rect x="500" y="960" width="80" height="380" fill="#f59e0b" stroke="{INK}" stroke-width="8"/>
  
  <!-- Thick Earth Conductor running downwards -->
  <rect x="480" y="1300" width="120" height="340" rx="30" fill="{GREEN}" stroke="{INK}" stroke-width="10"/>
  <path d="M540 1300 V1640" stroke="{GOLD}" stroke-width="32" stroke-dasharray="50 50"/>
  
  <!-- Center Hex Bolt Head -->
  <polygon points="540,890 600,925 600,995 540,1030 480,995 480,925" fill="#334155" stroke="{INK}" stroke-width="8"/>
  <circle cx="540" cy="960" r="24" fill="{GOLD}"/>
  
  <!-- Callout Label -->
  <g transform="translate(180, 1680)">
    <rect x="0" y="0" width="720" height="100" rx="20" fill="#ffffff" stroke="{INK}" stroke-width="6"/>
    <text x="360" y="64" fill="{INK}" font-family="Arial, sans-serif" font-weight="900" font-size="42" text-anchor="middle">METALLIC BOND TO CHASSIS</text>
  </g>
</svg>'''

# 4. NEW INSULATION BARRIER CROSS-SECTION
SVGS["scene4_insulation_barrier.svg"] = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
  <rect width="1080" height="1920" fill="{PAPER}"/>
  
  <!-- Metal Case Wall at Right -->
  <rect x="760" y="380" width="180" height="1100" rx="24" fill="#94a3b8" stroke="{INK}" stroke-width="10"/>
  <text x="850" y="960" fill="#ffffff" font-family="Arial, sans-serif" font-weight="900" font-size="44" text-anchor="middle" transform="rotate(-90 850 960)">METAL CASE</text>
  
  <!-- Generous Air Clearance Gap -->
  <rect x="520" y="380" width="220" height="1100" fill="#f8fafc" stroke="#cbd5e1" stroke-width="4" stroke-dasharray="16 12"/>
  <text x="630" y="960" fill="{DARK_STEEL}" font-family="Arial, sans-serif" font-weight="800" font-size="34" text-anchor="middle" transform="rotate(-90 630 960)">AIR GAP</text>
  
  <!-- Insulated Cable Structure -->
  <!-- Outer Sheath (Grey) -->
  <rect x="140" y="440" width="360" height="980" rx="60" fill="#cbd5e1" stroke="{INK}" stroke-width="10"/>
  <text x="320" y="520" fill="{INK}" font-family="Arial, sans-serif" font-weight="900" font-size="32" text-anchor="middle">OUTER SHEATH</text>
  
  <!-- Primary Insulation Layer (Brown PVC) -->
  <rect x="200" y="580" width="240" height="740" rx="40" fill="{LIVE}" stroke="{INK}" stroke-width="8"/>
  <text x="320" y="660" fill="#ffffff" font-family="Arial, sans-serif" font-weight="900" font-size="30" text-anchor="middle">INSULATION</text>
  
  <!-- Bare Copper Core Carrying 230V -->
  <rect x="260" y="730" width="120" height="500" rx="20" fill="#f59e0b" stroke="{INK}" stroke-width="8"/>
  <text x="320" y="980" fill="{INK}" font-family="Arial, sans-serif" font-weight="900" font-size="32" text-anchor="middle" transform="rotate(-90 320 980)">LIVE (230V)</text>
  
  <!-- Bottom Safety Card -->
  <g transform="translate(100, 1560)">
    <rect x="0" y="0" width="880" height="110" rx="22" fill="#ffffff" stroke="{GREEN}" stroke-width="6"/>
    <text x="440" y="68" fill="{GREEN}" font-family="Arial, sans-serif" font-weight="900" font-size="38" text-anchor="middle">INSULATION KEEPS VOLTAGE CONTAINED</text>
  </g>
</svg>'''

# 5. NEW FAULT SURGE SCENARIO
SVGS["scene5_fault_surge.svg"] = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
  <rect width="1080" height="1920" fill="#fff5f5"/>
  
  <!-- Electrified Metal Chassis (Alert Red Glow) -->
  <rect x="520" y="420" width="460" height="980" rx="36" fill="#fee2e2" stroke="{FAULT}" stroke-width="14"/>
  <text x="750" y="490" fill="{FAULT}" font-family="Arial, sans-serif" font-weight="900" font-size="38" text-anchor="middle">⚡ LIVE VOLTAGE ON CASE ⚡</text>
  
  <!-- Source -->
  <circle cx="180" cy="780" r="80" fill="#ffffff" stroke="{INK}" stroke-width="10"/>
  <text x="180" y="792" fill="{INK}" font-family="Arial, sans-serif" font-weight="900" font-size="44" text-anchor="middle">230V AC</text>
  
  <!-- Loose Live Wire touching Case -->
  <path d="M180 700 V560 H600 L720 720" fill="none" stroke="{LIVE}" stroke-width="26" stroke-linecap="round"/>
  
  <!-- Contact Spark Point -->
  <circle cx="720" cy="720" r="50" fill="{GOLD}" stroke="{FAULT}" stroke-width="10"/>
  <circle cx="720" cy="720" r="24" fill="#ffffff"/>
  
  <!-- Earth Return Loop Carrying Massive Current -->
  <path d="M750 1400 V1500 H180 V860" fill="none" stroke="{GREEN}" stroke-width="26" stroke-linecap="round"/>
  <path d="M750 1400 V1500 H180 V860" fill="none" stroke="{GOLD}" stroke-width="12" stroke-dasharray="32 18" stroke-linecap="round"/>
  
  <!-- Massive Fault Alert Badge -->
  <g transform="translate(100, 1600)">
    <rect x="0" y="0" width="880" height="140" rx="26" fill="{FAULT}"/>
    <text x="440" y="60" fill="#ffffff" font-family="Arial, sans-serif" font-weight="900" font-size="42" text-anchor="middle">HIGH FAULT CURRENT FLOWS</text>
    <text x="440" y="110" fill="{GOLD}" font-family="Arial, sans-serif" font-weight="800" font-size="32" text-anchor="middle">SAFELY DIVERTED BACK THROUGH EARTH</text>
  </g>
</svg>'''

# 6. NEW BREAKER TRIP ACTION
SVGS["scene6_breaker_trip.svg"] = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
  <rect width="1080" height="1920" fill="{PAPER}"/>
  
  <!-- Breaker Enclosure -->
  <rect x="180" y="440" width="720" height="980" rx="40" fill="#ffffff" stroke="{INK}" stroke-width="12"/>
  <text x="540" y="530" fill="{INK}" font-family="Arial, sans-serif" font-weight="900" font-size="48" text-anchor="middle">CIRCUIT BREAKER</text>
  
  <!-- Magnetic Solenoid Coil -->
  <rect x="420" y="620" width="240" height="200" rx="20" fill="#e2e8f0" stroke="{INK}" stroke-width="8"/>
  <path d="M440 660 H640 M440 700 H640 M440 740 H640 M440 780 H640" stroke="{LIVE}" stroke-width="14" stroke-linecap="round"/>
  <text x="540" y="855" fill="{INK}" font-family="Arial, sans-serif" font-weight="900" font-size="32" text-anchor="middle">MAGNETIC COIL</text>
  
  <!-- Breaker Contacts in OPEN position -->
  <!-- Fixed Terminal Left -->
  <circle cx="340" cy="1040" r="24" fill="{INK}"/>
  <line x1="220" y1="1040" x2="340" y2="1040" stroke="{LIVE}" stroke-width="22" stroke-linecap="round"/>
  
  <!-- Fixed Terminal Right -->
  <circle cx="740" cy="1040" r="24" fill="{INK}"/>
  <line x1="740" y1="1040" x2="860" y2="1040" stroke="{LIVE}" stroke-width="22" stroke-linecap="round"/>
  
  <!-- Moving Contact Arm (Snapped Upward) -->
  <g transform="rotate(-45 340 1040)">
    <line x1="340" y1="1040" x2="620" y2="1040" stroke="{FAULT}" stroke-width="20" stroke-linecap="round"/>
    <circle cx="620" cy="1040" r="26" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>
  </g>
  
  <!-- Large CLEAR AIR GAP callout -->
  <path d="M490 920 Q560 980 620 1040" fill="none" stroke="{GOLD}" stroke-width="8" stroke-dasharray="16 12"/>
  <rect x="440" y="890" width="240" height="70" rx="14" fill="{INK}"/>
  <text x="560" y="938" fill="#ffffff" font-family="Arial, sans-serif" font-weight="900" font-size="32" text-anchor="middle">OPEN GAP</text>
  
  <!-- Success Safe Status -->
  <g transform="translate(100, 1500)">
    <rect x="0" y="0" width="880" height="130" rx="26" fill="{GREEN}"/>
    <text x="440" y="58" fill="#ffffff" font-family="Arial, sans-serif" font-weight="900" font-size="42" text-anchor="middle">POWER INTERRUPTED INSTANTLY</text>
    <text x="440" y="104" fill="{GOLD}" font-family="Arial, sans-serif" font-weight="800" font-size="32" text-anchor="middle">ZERO SHOCK HAZARD REMAINS</text>
  </g>
</svg>'''

# 7. NEW PAYOFF SUMMARY
SVGS["scene7_payoff_summary.svg"] = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
  <rect width="1080" height="1920" fill="{PAPER}"/>
  
  <!-- Card 1: Normal Power Duty -->
  <g transform="translate(80, 360)">
    <rect x="0" y="0" width="920" height="260" rx="30" fill="#ffffff" stroke="{LIVE}" stroke-width="8"/>
    <rect x="40" y="40" width="380" height="70" rx="14" fill="{LIVE}"/>
    <text x="230" y="88" fill="#ffffff" font-family="Arial, sans-serif" font-weight="900" font-size="36" text-anchor="middle">LIVE + NEUTRAL</text>
    <text x="40" y="170" fill="{INK}" font-family="Arial, sans-serif" font-weight="900" font-size="46">Runs the Machine</text>
    <text x="40" y="220" fill="{DARK_STEEL}" font-family="Arial, sans-serif" font-weight="700" font-size="32">Closed loop carrying 100% of motor current.</text>
  </g>
  
  <!-- Card 2: Protection Duty -->
  <g transform="translate(80, 680)">
    <rect x="0" y="0" width="920" height="260" rx="30" fill="#ffffff" stroke="{GREEN}" stroke-width="8"/>
    <rect x="40" y="40" width="380" height="70" rx="14" fill="{GREEN}"/>
    <text x="230" y="88" fill="#ffffff" font-family="Arial, sans-serif" font-weight="900" font-size="36" text-anchor="middle">EARTH / GROUND</text>
    <text x="40" y="170" fill="{INK}" font-family="Arial, sans-serif" font-weight="900" font-size="46">Protects the Person</text>
    <text x="40" y="220" fill="{DARK_STEEL}" font-family="Arial, sans-serif" font-weight="700" font-size="32">Safe bypass path ensuring the breaker trips.</text>
  </g>
  
  <!-- Channel Signature Branding Box -->
  <g transform="translate(80, 1060)">
    <rect x="0" y="0" width="920" height="420" rx="36" fill="#ffffff" stroke="{INK}" stroke-width="8"/>
    <text x="460" y="110" fill="{INK}" font-family="Arial, sans-serif" font-weight="900" font-size="58" text-anchor="middle">CAUSE &amp; MOTION</text>
    <text x="460" y="180" fill="{DARK_STEEL}" font-family="Arial, sans-serif" font-weight="800" font-size="38" text-anchor="middle">Engineering Explained Visually</text>
    
    <!-- YouTube CTA Button -->
    <rect x="220" y="240" width="480" height="110" rx="24" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>
    <text x="460" y="310" fill="{INK}" font-family="Arial, sans-serif" font-weight="900" font-size="42" text-anchor="middle">SUBSCRIBE</text>
  </g>
</svg>'''

def main():
    print("Generating fresh SVGs and converting with VectorCraft CLI...")
    temp_dir = BASE_DIR / "temp_svgs"
    temp_dir.mkdir(parents=True, exist_ok=True)

    for filename, svg in SVGS.items():
        svg_path = temp_dir / filename
        svg_path.write_text(svg, encoding="utf-8")
        
        png_name = filename.replace(".svg", ".png")
        proj_png = PROJECT_ASSETS / png_name
        remotion_png = REMOTION_ASSETS / png_name
        
        # Convert using VectorCraft CLI
        print(f"-> VectorCraft converting {filename} to {png_name}...")
        cmd = [VECTORCRAFT_CLI, "convert", str(svg_path), str(proj_png)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Error converting {filename}:", res.stderr)
        else:
            # Copy to remotion public dir
            import shutil
            shutil.copy2(proj_png, remotion_png)
            print(f"   [OK] Generated {proj_png.name} ({proj_png.stat().st_size} bytes)")

    print("\nAll brand-new images generated successfully via VectorCraft!")

if __name__ == "__main__":
    main()
