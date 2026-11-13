#!/usr/bin/env python3
"""
Initialize the Mars Explorer SQLite database (database/mars_explorer.db)
and seed official NASA & USGS records across all 7 required tables:
  1. mars_locations
  2. dataset_sources
  3. scientific_layers
  4. mission_sites
  5. saved_routes
  6. route_waypoints
  7. user_preferences
Supports both SQLAlchemy ORM and native Python sqlite3.
"""
import json
import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
DB_PATH = PROJECT_ROOT / "database" / "mars_explorer.db"
DATA_DIR = PROJECT_ROOT / "data"
sys.path.insert(0, str(BACKEND_DIR))

from app.services.route_service import plan_marswalk_route

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS mars_locations (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    feature_type TEXT NOT NULL,
    category TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    diameter_km REAL,
    elevation_m REAL,
    zoom_tier TEXT NOT NULL,
    quadrangle TEXT,
    slope_deg REAL,
    roughness_index REAL,
    risk_level TEXT,
    description TEXT NOT NULL,
    source_name TEXT NOT NULL,
    source_url TEXT NOT NULL,
    is_sample INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS dataset_sources (
    id TEXT PRIMARY KEY,
    short_name TEXT NOT NULL,
    title TEXT NOT NULL,
    mission TEXT NOT NULL,
    agency TEXT NOT NULL,
    url TEXT NOT NULL,
    portal_url TEXT,
    data_type TEXT NOT NULL,
    resolution TEXT NOT NULL,
    coverage TEXT NOT NULL,
    status TEXT NOT NULL,
    citation TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS scientific_layers (
    id TEXT PRIMARY KEY,
    layer_number INTEGER NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    data_source TEXT NOT NULL,
    instrument_mission TEXT NOT NULL,
    observation_date TEXT,
    units TEXT NOT NULL,
    resolution TEXT,
    availability_status TEXT NOT NULL,
    is_derived INTEGER NOT NULL DEFAULT 0,
    calculation_method TEXT NOT NULL,
    scientific_disclaimer TEXT NOT NULL,
    wmts_layer TEXT,
    source_url TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS mission_sites (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    mission_name TEXT NOT NULL,
    agency TEXT NOT NULL,
    site_type TEXT NOT NULL,
    status TEXT NOT NULL,
    landing_date TEXT NOT NULL,
    sols_operated INTEGER,
    mass_kg REAL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    elevation_m REAL,
    region TEXT NOT NULL,
    zoom_tier TEXT NOT NULL,
    instruments TEXT NOT NULL,
    scientific_summary TEXT NOT NULL,
    source_url TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS saved_routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    profile TEXT NOT NULL,
    start_name TEXT NOT NULL,
    start_lat REAL NOT NULL,
    start_lon REAL NOT NULL,
    end_name TEXT NOT NULL,
    end_lat REAL NOT NULL,
    end_lon REAL NOT NULL,
    total_distance_km REAL NOT NULL,
    estimated_difficulty TEXT NOT NULL,
    mean_risk_score REAL NOT NULL,
    max_slope_deg REAL NOT NULL,
    elevation_gain_m REAL NOT NULL,
    is_provisional INTEGER NOT NULL DEFAULT 1,
    is_sample INTEGER NOT NULL DEFAULT 0,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS route_waypoints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    route_id INTEGER NOT NULL,
    sequence_index INTEGER NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    elevation_m REAL NOT NULL,
    slope_deg REAL NOT NULL,
    risk_score REAL NOT NULL,
    risk_class TEXT NOT NULL,
    cumulative_km REAL NOT NULL,
    FOREIGN KEY(route_id) REFERENCES saved_routes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_key TEXT UNIQUE NOT NULL,
    default_view TEXT NOT NULL DEFAULT 'solar-system',
    active_layer_id TEXT NOT NULL DEFAULT 'base_map',
    scale_mode TEXT NOT NULL DEFAULT 'visual',
    show_labels INTEGER NOT NULL DEFAULT 1,
    show_mission_sites INTEGER NOT NULL DEFAULT 1,
    preferred_route_profile TEXT NOT NULL DEFAULT 'balanced'
);
"""

def init_and_seed_sqlite():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.executescript(SCHEMA_SQL)

    locs_data = json.loads((DATA_DIR / "processed" / "usgs_mars_nomenclature.json").read_text(encoding="utf-8"))
    ds_data = json.loads((DATA_DIR / "metadata" / "dataset_sources.json").read_text(encoding="utf-8"))
    layers_data = json.loads((DATA_DIR / "metadata" / "scientific_layers.json").read_text(encoding="utf-8"))
    missions_data = json.loads((DATA_DIR / "processed" / "nasa_missions.json").read_text(encoding="utf-8"))

    for item in locs_data:
        cur.execute("""
            INSERT OR REPLACE INTO mars_locations (
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

    for item in ds_data:
        cur.execute("""
            INSERT OR REPLACE INTO dataset_sources (
                id, short_name, title, mission, agency, url, portal_url,
                data_type, resolution, coverage, status, citation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item["id"], item["short_name"], item["title"], item["mission"],
            item["agency"], item["url"], item.get("portal_url"),
            item["data_type"], item["resolution"], item["coverage"],
            item["status"], item["citation"]
        ))

    for item in layers_data:
        cur.execute("""
            INSERT OR REPLACE INTO scientific_layers (
                id, layer_number, name, category, description, data_source,
                instrument_mission, observation_date, units, resolution,
                availability_status, is_derived, calculation_method,
                scientific_disclaimer, wmts_layer, source_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item["id"], item["layer_number"], item["name"], item["category"],
            item["description"], item["data_source"], item["instrument_mission"],
            item["observation_date"], item["units"], item["resolution"],
            item["availability_status"], 1 if item["is_derived"] else 0,
            item["calculation_method"], item["scientific_disclaimer"],
            item["wmts_layer"], item["source_url"]
        ))

    for item in missions_data:
        cur.execute("""
            INSERT OR REPLACE INTO mission_sites (
                id, name, mission_name, agency, site_type, status, landing_date,
                sols_operated, mass_kg, latitude, longitude, elevation_m,
                region, zoom_tier, instruments, scientific_summary, source_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item["id"], item["name"], item["mission_name"], item["agency"],
            item["site_type"], item["status"], item["landing_date"],
            item["sols_operated"], item["mass_kg"], item["latitude"],
            item["longitude"], item["elevation_m"], item["region"],
            item["zoom_tier"], item["instruments"], item["scientific_summary"],
            item["source_url"]
        ))

    cur.execute("SELECT COUNT(*) FROM saved_routes")
    if cur.fetchone()[0] == 0:
        sample_routes_spec = [
            (
                "Jezero Crater to Syrtis Major Planum Traverse (Reference Sample)",
                "balanced",
                "Jezero Crater", 18.38, 77.58,
                "Syrtis Major Planum", 10.00, 69.00,
                "Sample reference traverse across the western Isidis rim."
            ),
            (
                "Gale Crater (Bradbury Landing) to Elysium Planitia (InSight) Low-Risk Corridor",
                "lowest_risk",
                "Gale Crater", -5.40, 137.80,
                "Elysium Planitia", 3.00, 155.00,
                "Sample reference dichotomy-boundary crossing minimizing slope exposure."
            ),
        ]
        for r_name, prof, s_name, s_lat, s_lon, e_name, e_lat, e_lon, notes in sample_routes_spec:
            plan = plan_marswalk_route(s_lat, s_lon, s_name, e_lat, e_lon, e_name, prof, locs_data)
            cur.execute("""
                INSERT INTO saved_routes (
                    name, profile, start_name, start_lat, start_lon,
                    end_name, end_lat, end_lon, total_distance_km,
                    estimated_difficulty, mean_risk_score, max_slope_deg,
                    elevation_gain_m, is_provisional, is_sample, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 1, ?)
            """, (
                r_name, prof, s_name, s_lat, s_lon, e_name, e_lat, e_lon,
                plan["total_distance_km"], plan["estimated_difficulty"],
                plan["mean_risk_score"], plan["max_slope_deg"],
                plan["elevation_gain_m"], notes
            ))
            route_id = cur.lastrowid
            for wp in plan["waypoints"]:
                cur.execute("""
                    INSERT INTO route_waypoints (
                        route_id, sequence_index, latitude, longitude,
                        elevation_m, slope_deg, risk_score, risk_class, cumulative_km
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    route_id, wp["sequence_index"], wp["latitude"], wp["longitude"],
                    wp["elevation_m"], wp["slope_deg"], wp["risk_score"],
                    wp["risk_class"], wp["cumulative_km"]
                ))

    cur.execute("""
        INSERT OR IGNORE INTO user_preferences (
            profile_key, default_view, active_layer_id, scale_mode,
            show_labels, show_mission_sites, preferred_route_profile
        ) VALUES ('default_commander', 'solar-system', 'base_map', 'visual', 1, 1, 'balanced')
    """)

    conn.commit()
    tables = [
        "mars_locations", "dataset_sources", "scientific_layers",
        "mission_sites", "saved_routes", "route_waypoints", "user_preferences"
    ]
    print(f"[Mars Explorer] Initialized SQLite database at {DB_PATH}")
    for t in tables:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        print(f"  - {t}: {cur.fetchone()[0]} records")
    conn.close()

if __name__ == "__main__":
    init_and_seed_sqlite()
