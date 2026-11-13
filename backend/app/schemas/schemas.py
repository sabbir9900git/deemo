from typing import List, Optional
from pydantic import BaseModel, Field

class MarsLocationSchema(BaseModel):
    id: str
    name: str
    feature_type: str
    category: str
    latitude: float
    longitude: float
    diameter_km: Optional[float] = None
    elevation_m: Optional[float] = None
    zoom_tier: str
    quadrangle: Optional[str] = None
    slope_deg: Optional[float] = None
    roughness_index: Optional[float] = None
    risk_level: Optional[str] = None
    description: str
    source_name: str
    source_url: str
    is_sample: bool = False

    class Config:
        from_attributes = True

class TerrainRiskResponse(BaseModel):
    latitude: float
    longitude: float
    nearest_feature_name: str
    nearest_feature_distance_km: float
    elevation_m: float
    slope_deg: float
    roughness_index: float
    thermal_inertia_tiu: float
    radiation_msv_day: float
    atmospheric_pressure_mbar: float
    risk_score: float
    risk_classification: str  # Low Risk | Moderate Risk | High Risk | Very High Risk
    steep_terrain_flag: bool
    traversal_assessment: str
    calculation_method: str
    data_status: str
    scientific_disclaimer: str

class RouteRequest(BaseModel):
    start_lat: float = Field(..., ge=-90.0, le=90.0)
    start_lon: float = Field(..., ge=0.0, le=360.0)
    start_name: str = "Origin Site"
    end_lat: float = Field(..., ge=-90.0, le=90.0)
    end_lon: float = Field(..., ge=0.0, le=360.0)
    end_name: str = "Destination Site"
    profile: str = "balanced"  # shortest | lowest_risk | balanced

class WaypointSchema(BaseModel):
    sequence_index: int
    latitude: float
    longitude: float
    elevation_m: float
    slope_deg: float
    risk_score: float
    risk_class: str
    cumulative_km: float

class RouteProfileResult(BaseModel):
    profile: str
    profile_label: str
    start_name: str
    end_name: str
    total_distance_km: float
    direct_great_circle_km: float
    detour_factor: float
    estimated_difficulty: str
    mean_risk_score: float
    max_slope_deg: float
    mean_slope_deg: float
    elevation_gain_m: float
    elevation_loss_m: float
    estimated_radiation_msv: float
    is_provisional: bool
    algorithm: str
    scientific_disclaimer: str
    waypoints: List[WaypointSchema]

class RouteComparisonResponse(BaseModel):
    start_name: str
    end_name: str
    recommended_profile: str
    profiles: List[RouteProfileResult]

class AssistantQueryRequest(BaseModel):
    question: str
    context_location_id: Optional[str] = None
    active_layer_id: Optional[str] = None

class AssistantQueryResponse(BaseModel):
    answer: str
    referenced_locations: List[str]
    referenced_datasets: List[str]
    confidence_note: str
    mode: str
