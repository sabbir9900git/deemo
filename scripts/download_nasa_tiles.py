#!/usr/bin/env python3
"""
NASA Mars Trek WMTS Tile Fetcher & Local Cache Utility
Downloads official WMTS map tiles from https://trek.nasa.gov/tiles/Mars/EQ/
for offline caching when an internet connection is available.
"""
import argparse
from pathlib import Path
import urllib.request

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = PROJECT_ROOT / "data" / "raw" / "tiles_cache"

OFFICIAL_LAYERS = {
    "viking_color": "Mars_Viking_MDIM21_ClrMosaic_global_232m",
    "mola_hillshade": "Mars_MGS_MOLA_Colorhillshade_merge_global_463m",
    "themis_day_ir": "Mars_MO_THEMIS-IR-Day_mosaic_global_100m",
}

def build_wmts_url(layer_name: str, z: int, y: int, x: int) -> str:
    return (
        f"https://trek.nasa.gov/tiles/Mars/EQ/{layer_name}/1.0.0/"
        f"default/default028mm/{z}/{y}/{x}.jpg"
    )

def main():
    parser = argparse.ArgumentParser(description="Download NASA Mars Trek WMTS tiles.")
    parser.add_argument("--layer", default="viking_color", choices=list(OFFICIAL_LAYERS.keys()))
    parser.add_argument("--max-zoom", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true", help="Print official WMTS URLs without downloading")
    args = parser.parse_args()

    layer_id = OFFICIAL_LAYERS[args.layer]
    print(f"[NASA Mars Trek] Layer: {layer_id}")
    for z in range(args.max_zoom + 1):
        rows = 2 ** z
        cols = 2 ** (z + 1)
        for y in range(rows):
            for x in range(cols):
                url = build_wmts_url(layer_id, z, y, x)
                if args.dry_run:
                    print(f"  WMTS Tile ({z}/{y}/{x}): {url}")
                else:
                    dest = CACHE_DIR / layer_id / str(z) / str(y) / f"{x}.jpg"
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    try:
                        urllib.request.urlretrieve(url, dest)
                        print(f"  Downloaded {dest}")
                    except Exception as exc:
                        print(f"  [Offline/Skipped] Could not reach {url}: {exc}")
                        return

if __name__ == "__main__":
    main()
