"""
Database Seeding Service for Mars Explorer
Loads verified USGS Planetary Nomenclature locations, NASA datasets, 13 scientific layers,
NASA mission landing sites, and sample Marswalk routes into SQLite.
"""
import json
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.models import (
    DatasetSource,
    MarsLocation,
    MissionSite,
    RouteWaypoint,
    SavedRoute,
    ScientificLayer,
    UserPreference,
)
from app.services.route_service import plan_marswalk_route

def seed_database(db: Session) -> dict:
    counts = {}

    # 1. MarsLocations
    loc_file = settings.DATA_DIR / "processed" / "usgs_mars_nomenclature.json"
    locs_data = json.loads(loc_file.read_text(encoding="utf-8"))
    if db.query(MarsLocation).count() == 0:
        for item in locs_data:
            db.add(MarsLocation(**item))
        db.commit()
    counts["mars_locations"] = db.query(MarsLocation).count()

    # 2. DatasetSources
    ds_file = settings.DATA_DIR / "metadata" / "dataset_sources.json"
    ds_data = json.loads(ds_file.read_text(encoding="utf-8"))
    if db.query(DatasetSource).count() == 0:
        for item in ds_data:
            db.add(DatasetSource(**item))
        db.commit()
    counts["dataset_sources"] = db.query(DatasetSource).count()

    # 3. ScientificLayers
    layers_file = settings.DATA_DIR / "metadata" / "scientific_layers.json"
    layers_data = json.loads(layers_file.read_text(encoding="utf-8"))
    if db.query(ScientificLayer).count() == 0:
        for item in layers_data:
            db.add(ScientificLayer(**item))
        db.commit()
    counts["scientific_layers"] = db.query(ScientificLayer).count()

    # 4. MissionSites
    missions_file = settings.DATA_DIR / "processed" / "nasa_missions.json"
    missions_data = json.loads(missions_file.read_text(encoding="utf-8"))
    if db.query(MissionSite).count() == 0:
        for item in missions_data:
            db.add(MissionSite(**item))
        db.commit()
    counts["mission_sites"] = db.query(MissionSite).count()

    # 5. SavedRoutes & RouteWaypoints (Clearly identified reference routes)
    if db.query(SavedRoute).count() == 0:
        sample_routes_spec = [
            (
                "Jezero Crater to Syrtis Major Planum Traverse (Reference)",
                "balanced",
                "Jezero Crater", 18.38, 77.58,
                "Syrtis Major Planum", 10.00, 69.00,
                "Reference astrobiology & volcanic stratigraphy traverse across the western Isidis rim."
            ),
            (
                "Gale Crater (Bradbury Landing) to Elysium Planitia (InSight) Low-Risk Corridor",
                "lowest_risk",
                "Gale Crater", -5.40, 137.80,
                "Elysium Planitia", 3.00, 155.00,
                "Reference dichotomy-boundary crossing minimizing slope exposure."
            ),
        ]
        for r_name, prof, s_name, s_lat, s_lon, e_name, e_lat, e_lon, notes in sample_routes_spec:
            plan = plan_marswalk_route(s_lat, s_lon, s_name, e_lat, e_lon, e_name, prof, locs_data)
            route_obj = SavedRoute(
                name=r_name,
                profile=prof,
                start_name=s_name,
                start_lat=s_lat,
                start_lon=s_lon,
                end_name=e_name,
                end_lat=e_lat,
                end_lon=e_lon,
                total_distance_km=plan["total_distance_km"],
                estimated_difficulty=plan["estimated_difficulty"],
                mean_risk_score=plan["mean_risk_score"],
                max_slope_deg=plan["max_slope_deg"],
                elevation_gain_m=plan["elevation_gain_m"],
                is_provisional=True,
                is_sample=True,
                notes=notes,
            )
            db.add(route_obj)
            db.flush()
            for wp in plan["waypoints"]:
                db.add(RouteWaypoint(route_id=route_obj.id, **wp))
        db.commit()
    counts["saved_routes"] = db.query(SavedRoute).count()
    counts["route_waypoints"] = db.query(RouteWaypoint).count()

    # 6. UserPreferences
    if db.query(UserPreference).count() == 0:
        db.add(UserPreference(
            profile_key="default_commander",
            default_view="solar-system",
            active_layer_id="base_map",
            scale_mode="visual",
            show_labels=True,
            show_mission_sites=True,
            preferred_route_profile="balanced",
        ))
        db.commit()
    counts["user_preferences"] = db.query(UserPreference).count()

    return counts
