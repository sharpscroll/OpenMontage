import re

with open("capabilities_dump.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find occurrences of 'sand'
sand_matches = [m.start() for m in re.finditer(r"sand", html, re.I)]
print("Matches for 'sand':", len(sand_matches))
for idx in sand_matches:
    print("--- SAND CONTEXT ---")
    print(html[max(0, idx - 150):min(len(html), idx + 250)])

# Find video tags and src
video_tags = re.findall(r"<video[^>]*>.*?</video>", html, re.DOTALL | re.I)
print(f"\nFound {len(video_tags)} video tags.")
for i, v in enumerate(video_tags[:15]):
    srcs = re.findall(r'src=["\']([^"\']+)["\']', v)
    print(f"Video {i}: {srcs}")

# Find section or element with id="motion" or similar
sections = re.findall(r'<[^>]+id=["\'][^"\']*motion[^"\']*["\'][^>]*>', html, re.I)
print("\nSections with motion in ID:", sections)

# Find all headings
headings = re.findall(r'<h[1-4][^>]*>(.*?)</h[1-4]>', html, re.DOTALL | re.I)
print(f"\nHeadings ({len(headings)}):")
for h in headings[:30]:
    clean_h = re.sub(r'<[^>]+>', '', h).strip()
    if clean_h:
        print(f"  - {clean_h}")
