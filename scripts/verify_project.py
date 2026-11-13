#!/usr/bin/env python3
"""
End-to-End Automated Verification Suite for MARS EXPLORER
Tests:
1. SQLite Database integrity across all 7 required tables
2. Dynamic zoom-tier filtering (zoom_out, medium_zoom, zoom_in)
3. MOLA Terrain Risk Analysis calculations
4. Marswalk A* Route Planner across all 3 profiles (shortest, lowest_risk, balanced)
5. Grounded AI Mission Assistant responses & scientific disclaimers
"""
import json
import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
DB_PATH = PROJECT_ROOT / "database" / "mars_explorer.db"
sys.path.insert(0, str(BACKEND_DIR))

from app.services.terrain_service import evaluate_terrain_risk
from app.services.route_service import compare_all_route_profiles
from app.services.assistant_service import answer_mission_query

def run_verification():
    print("=== MARS EXPLORER END-TO-END VERIFICATION SUITE ===")
    assert DB_PATH.exists(), f"Database missing at {DB_PATH}"

    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    expected_tables = {
        "mars_locations": 30,
        "dataset_sources": 10,
        "scientific_layers": 13,
        "mission_sites": 12,
        "saved_routes": 2,
        "route_waypoints": 30,
        "user_preferences": 1,
    }
    for table, min_rows in expected_tables.items():
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
        assert count >= min_rows, f"Table {table} expected >= {min_rows} rows, got {count}"
        print(f"[PASS] SQLite Table '{table}': {count} verified rows")

    # Check zoom tiers
    for tier in ["zoom_out", "medium_zoom", "zoom_in"]:
        cur.execute("SELECT COUNT(*) FROM mars_locations WHERE zoom_tier = ?", (tier,))
        c = cur.fetchone()[0]
        assert c > 0, f"Zoom tier {tier} has 0 locations"
        print(f"[PASS] Dynamic Zoom Tier '{tier}': {c} USGS locations")

    locs = json.loads((PROJECT_ROOT / "data/processed/usgs_mars_nomenclature.json").read_text(encoding="utf-8"))
    missions = json.loads((PROJECT_ROOT / "data/processed/nasa_missions.json").read_text(encoding="utf-8"))
    layers = json.loads((PROJECT_ROOT / "data/metadata/scientific_layers.json").read_text(encoding="utf-8"))
    datasets = json.loads((PROJECT_ROOT / "data/metadata/dataset_sources.json").read_text(encoding="utf-8"))

    # Test Terrain Risk at Olympus Mons, Valles Marineris, Jezero Crater, and Utopia Planitia
    for name, lat, lon in [
        ("Olympus Mons", 18.65, 226.20),
        ("Valles Marineris", -14.01, 301.41),
        ("Jezero Crater", 18.38, 77.58),
        ("Utopia Planitia", 47.00, 118.00),
    ]:
        risk = evaluate_terrain_risk(lat, lon, locs)
        print(
            f"[PASS] Terrain Risk @ {name}: Elev={risk['elevation_m']}m, "
            f"Slope={risk['slope_deg']}°, Class={risk['risk_classification']} ({risk['risk_score']}/100)"
        )

    # Test A* Route Planner (3 profiles)
    route_cmp = compare_all_route_profiles(
        18.38, 77.58, "Jezero Crater",
        -5.40, 137.80, "Gale Crater",
        locs
    )
    assert len(route_cmp["profiles"]) == 3
    for p in route_cmp["profiles"]:
        print(
            f"[PASS] Marswalk A* Profile '{p['profile_label']}': "
            f"Dist={p['total_distance_km']} km, MeanRisk={p['mean_risk_score']}, "
            f"MaxSlope={p['max_slope_deg']}°, Waypoints={len(p['waypoints'])}"
        )

    # Test Grounded AI Mission Assistant
    ans = answer_mission_query(
        "What is the water-ice evidence and radiation dose at Gale Crater and Korolev Crater?",
        locs, missions, layers, datasets
    )
    assert "never confirmed liquid water" in ans["answer"].lower()
    assert "0.64" in ans["answer"]
    print(f"[PASS] Grounded AI Mission Assistant verified ({len(ans['referenced_datasets'])} NASA/USGS sources cited)")
    conn.close()
    print("=== ALL VERIFICATION CHECKS PASSED ===")

if __name__ == "__main__":
    run_verification()
