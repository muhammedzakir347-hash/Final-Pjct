import os
import requests
import subprocess

INKSCAPE = r"C:\Program Files\Inkscape\bin\inkscape.exe"

BASE_URL = "https://surahquran.com/img/surat/"
SVG_DIR = "svg_files"
PNG_DIR = "png_surahs"

os.makedirs(SVG_DIR, exist_ok=True)
os.makedirs(PNG_DIR, exist_ok=True)

for i in range(1, 115):
    svg_url = f"{BASE_URL}{i}.svg"
    svg_path = os.path.join(SVG_DIR, f"{i}.svg")
    png_path = os.path.join(PNG_DIR, f"{i}.png")

    print(f"Processing Surah {i}...")

    r = requests.get(svg_url)
    r.raise_for_status()
    with open(svg_path, "wb") as f:
        f.write(r.content)

    subprocess.run([
        INKSCAPE,
        svg_path,
        "--export-type=png",
        "--export-filename", png_path,
        "--export-width=2000"
    ], check=True)

print("✅ All SVGs converted to PNG")
