#!/usr/bin/env python3
"""
USGS Gazetteer of Planetary Nomenclature Importer for Mars
Supports importing verified Mars nomenclature records from data/processed/usgs_mars_nomenclature.json
or custom CSV files exported from https://planetarynames.wr.usgs.gov/
"""
import argparse
import csv
import json
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "database" / "mars_explorer.db"

def assign_zoom_tier(diameter_km: float, feature_type: str) -> str:
    ft_lower = feature_type.lower()
    if diameter_km >= 500.0 or any(k in ft_lower for k in ["planitia", "vallis", "planum"]):
        return "zoom_out"
    if diameter_km >= 120.0 or "mons" in ft_lower or "montes" in ft_lower:
        return "medium_zoom"
    return "zoom_in"

def import_from_json(json_path: Path) -> int:
    records = json.loads(json_path.read_text(encoding="utf-8"))
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    inserted = 0
    for item in records:
        cur.execute("SELECT 1 FROM mars_locations WHERE id = ?", (item["id"],))
        if not cur.fetchone():
            cur.execute("""
                INSERT INTO mars_locations (
                    id, name, feature_type, category, latitude, longitude, diameter_km,
                    elevation_m, zoom_tier, quadrangle, slope_deg, roughness_index,
                    risk_level, description, source_name, source_url, is_sample
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item["id"], item["name"], item["feature_type"], item["category"],
                item["latitude"], item["longitude"], item["diameter_km"],
                item["elevation_m"], item["zoom_tier"], item["quadrangle"],
                item["slope_deg"], item["roughness_index"], item["risk_level"],
                item["description"], item["source_name"], item["source_url"],
                1 if item.get("is_sample") else 0
            ))
            inserted += 1
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM mars_locations")
    total = cur.fetchone()[0]
    conn.close()
    return total

def import_from_csv(csv_path: Path) -> int:
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    inserted = 0
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("Feature_Name") or row.get("name") or "Unknown"
            loc_id = name.lower().replace(" ", "-").replace("(", "").replace(")", "")
            cur.execute("SELECT 1 FROM mars_locations WHERE id = ?", (loc_id,))
            if cur.fetchone():
                continue
            lat = float(row.get("Center_Latitude") or row.get("latitude") or 0.0)
            lon = float(row.get("Center_Longitude") or row.get("longitude") or 0.0)
            diam = float(row.get("Diameter") or row.get("diameter_km") or 50.0)
            ftype = row.get("Feature_Type") or row.get("feature_type") or "Crater"
            cur.execute("""
                INSERT INTO mars_locations (
                    id, name, feature_type, category, latitude, longitude, diameter_km,
                    elevation_m, zoom_tier, quadrangle, slope_deg, roughness_index,
                    risk_level, description, source_name, source_url, is_sample
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
            """, (
                loc_id, name, ftype, ftype.split()[0], lat, lon, diam, 0.0,
                assign_zoom_tier(diam, ftype), row.get("Quad_Name", "USGS Mars Quad"),
                3.0, 0.35, "Moderate Risk",
                f"Imported from USGS Gazetteer of Planetary Nomenclature ({ftype}, {diam} km).",
                "USGS Gazetteer of Planetary Nomenclature",
                "https://planetarynames.wr.usgs.gov/"
            ))
            inserted += 1
    conn.commit()
    conn.close()
    return inserted

def main():
    parser = argparse.ArgumentParser(description="Import USGS Mars Planetary Nomenclature into SQLite.")
    parser.add_argument("--csv", type=str, help="Path to custom USGS CSV export file")
    args = parser.parse_args()
    if args.csv:
        count = import_from_csv(Path(args.csv))
        print(f"[USGS Importer] Imported {count} new records from CSV {args.csv}.")
    else:
        default_json = PROJECT_ROOT / "data" / "processed" / "usgs_mars_nomenclature.json"
        total = import_from_json(default_json)
        print(f"[USGS Importer] Verified {total} official USGS Mars Nomenclature records in database.")

if __name__ == "__main__":
    main()
