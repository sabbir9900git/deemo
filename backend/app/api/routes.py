"""
FastAPI REST API Router for MARS EXPLORER
Exposes endpoints for Solar System planets, USGS Mars locations (with dynamic zoom filtering),
13 scientific layers, NASA missions, MOLA terrain risk analysis, A* Marswalk route planning,
saved routes, and the Grounded AI Mission Assistant.
"""
import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.models import (
    DatasetSource,
    MarsLocation,
    MissionSite,
    RouteWaypoint,
    SavedRoute,
    ScientificLayer,
    UserPreference,
)
from app.schemas.schemas import (
    AssistantQueryRequest,
    AssistantQueryResponse,
    MarsLocationSchema,
    RouteComparisonResponse,
    RouteRequest,
    TerrainRiskResponse,
)
from app.services.assistant_service import answer_mission_query
from app.services.route_service import compare_all_route_profiles, plan_marswalk_route
from app.services.terrain_service import evaluate_terrain_risk

router = APIRouter()

def _locs_as_dicts(db: Session) -> List[dict]:
    rows = db.query(MarsLocation).all()
    return [
        {
            "id": r.id,
            "name": r.name,
            "feature_type": r.feature_type,
            "category": r.category,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "diameter_km": r.diameter_km,
            "elevation_m": r.elevation_m,
            "zoom_tier": r.zoom_tier,
            "quadrangle": r.quadrangle,
            "slope_deg": r.slope_deg,
            "roughness_index": r.roughness_index,
            "risk_level": r.risk_level,
            "description": r.description,
            "source_name": r.source_name,
            "source_url": r.source_url,
            "is_sample": r.is_sample,
        }
        for r in rows
    ]

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    return {
        "status": "operational",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database_records": {
            "mars_locations": db.query(MarsLocation).count(),
            "scientific_layers": db.query(ScientificLayer).count(),
            "mission_sites": db.query(MissionSite).count(),
            "dataset_sources": db.query(DatasetSource).count(),
            "saved_routes": db.query(SavedRoute).count(),
        },
    }

@router.get("/solar-system")
def get_solar_system():
    planets_file = settings.DATA_DIR / "processed" / "solar_system_planets.json"
    return {
        "scale_note": (
            "Visual 3D mode uses logarithmic orbital radii and compressed planet radii so all 8 planets "
            "and the Sun remain interactive simultaneously. True astronomical scale metrics from the "
            "NASA NSSDCA Planetary Fact Sheet are displayed in each planet's telemetry dossier."
        ),
        "planets": json.loads(planets_file.read_text(encoding="utf-8")),
    }

@router.get("/locations", response_model=List[MarsLocationSchema])
def list_mars_locations(
    zoom_level: Optional[str] = Query(
        None,
        description="Dynamic zoom filter: zoom_out | medium_zoom | zoom_in | all",
    ),
    category: Optional[str] = Query(None, description="Filter by category (Volcano, Crater, Basin / Plain, etc.)"),
    search: Optional[str] = Query(None, description="Search by official USGS feature name"),
    db: Session = Depends(get_db),
):
    q = db.query(MarsLocation)
    if zoom_level == "zoom_out":
        q = q.filter(MarsLocation.zoom_tier == "zoom_out")
    elif zoom_level == "medium_zoom":
        q = q.filter(MarsLocation.zoom_tier.in_(["zoom_out", "medium_zoom"]))
    # zoom_in or all returns all 3 tiers
    if category and category.lower() != "all":
        q = q.filter(MarsLocation.category == category)
    if search:
        q = q.filter(MarsLocation.name.ilike(f"%{search}%"))
    return q.order_by(MarsLocation.diameter_km.desc()).all()

@router.get("/locations/{location_id}", response_model=MarsLocationSchema)
def get_mars_location(location_id: str, db: Session = Depends(get_db)):
    loc = db.query(MarsLocation).filter(MarsLocation.id == location_id).first()
    if not loc:
        raise HTTPException(status_code=404, detail=f"Mars location '{location_id}' not found")
    return loc

@router.get("/layers")
def list_scientific_layers(db: Session = Depends(get_db)):
    rows = db.query(ScientificLayer).order_by(ScientificLayer.layer_number.asc()).all()
    return [
        {
            "id": r.id,
            "layer_number": r.layer_number,
            "name": r.name,
            "category": r.category,
            "description": r.description,
            "data_source": r.data_source,
            "instrument_mission": r.instrument_mission,
            "observation_date": r.observation_date,
            "units": r.units,
            "resolution": r.resolution,
            "availability_status": r.availability_status,
            "is_derived": r.is_derived,
            "calculation_method": r.calculation_method,
            "scientific_disclaimer": r.scientific_disclaimer,
            "wmts_layer": r.wmts_layer,
            "source_url": r.source_url,
        }
        for r in rows
    ]

@router.get("/missions")
def list_mission_sites(
    site_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(MissionSite)
    if site_type:
        q = q.filter(MissionSite.site_type == site_type)
    return q.all()

@router.get("/datasets")
def list_dataset_sources(db: Session = Depends(get_db)):
    return db.query(DatasetSource).all()

@router.get("/terrain-risk", response_model=TerrainRiskResponse)
def analyze_terrain_risk(
    lat: float = Query(..., ge=-90.0, le=90.0),
    lon: float = Query(..., ge=-180.0, le=360.0),
    db: Session = Depends(get_db),
):
    locs = _locs_as_dicts(db)
    return evaluate_terrain_risk(lat, lon, locs)

@router.post("/routes/plan", response_model=RouteComparisonResponse)
def generate_marswalk_routes(req: RouteRequest, db: Session = Depends(get_db)):
    locs = _locs_as_dicts(db)
    return compare_all_route_profiles(
        req.start_lat, req.start_lon, req.start_name,
        req.end_lat, req.end_lon, req.end_name,
        locs,
    )

@router.get("/routes/saved")
def get_saved_routes(db: Session = Depends(get_db)):
    routes = db.query(SavedRoute).all()
    out = []
    for r in routes:
        out.append({
            "id": r.id,
            "name": r.name,
            "profile": r.profile,
            "start_name": r.start_name,
            "start_lat": r.start_lat,
            "start_lon": r.start_lon,
            "end_name": r.end_name,
            "end_lat": r.end_lat,
            "end_lon": r.end_lon,
            "total_distance_km": r.total_distance_km,
            "estimated_difficulty": r.estimated_difficulty,
            "mean_risk_score": r.mean_risk_score,
            "max_slope_deg": r.max_slope_deg,
            "elevation_gain_m": r.elevation_gain_m,
            "is_provisional": r.is_provisional,
            "is_sample": r.is_sample,
            "notes": r.notes,
            "waypoints_count": len(r.waypoints),
        })
    return out

@router.post("/assistant/ask", response_model=AssistantQueryResponse)
def ask_mission_assistant(req: AssistantQueryRequest, db: Session = Depends(get_db)):
    locs = _locs_as_dicts(db)
    missions = [
        {
            "id": m.id, "name": m.name, "mission_name": m.mission_name,
            "agency": m.agency, "status": m.status, "landing_date": m.landing_date,
            "latitude": m.latitude, "longitude": m.longitude, "elevation_m": m.elevation_m,
            "region": m.region, "instruments": m.instruments, "scientific_summary": m.scientific_summary,
        }
        for m in db.query(MissionSite).all()
    ]
    layers = [{"id": l.id, "name": l.name} for l in db.query(ScientificLayer).all()]
    datasets = [{"id": d.id, "short_name": d.short_name} for d in db.query(DatasetSource).all()]
    return answer_mission_query(
        req.question,
        locs,
        missions,
        layers,
        datasets,
        req.context_location_id,
        req.active_layer_id,
    )
