export type ZoomTier = "zoom_out" | "medium_zoom" | "zoom_in";

export interface SolarPlanet {
  id: string;
  name: string;
  type: string;
  distance_au: number;
  distance_mkm: number;
  diameter_km: number;
  mass_10_24_kg: number;
  gravity_m_s2: number;
  escape_velocity_km_s: number;
  rotation_period_hr: number;
  length_of_day_hr: number;
  orbital_period_days: number;
  orbital_velocity_km_s: number;
  mean_temp_c: number;
  surface_pressure_bar: number | null;
  moons: number;
  has_rings: boolean;
  global_magnetic_field: boolean;
  visual_radius: number;
  visual_orbit_radius: number;
  color: string;
  description: string;
  source_url: string;
}

export interface MarsLocation {
  id: string;
  name: string;
  feature_type: string;
  category: string;
  latitude: number;
  longitude: number;
  diameter_km: number | null;
  elevation_m: number | null;
  zoom_tier: ZoomTier;
  quadrangle: string | null;
  slope_deg: number | null;
  roughness_index: number | null;
  risk_level: string | null;
  description: string;
  source_name: string;
  source_url: string;
  is_sample: boolean;
}

export interface ScientificLayer {
  id: string;
  layer_number: number;
  name: string;
  category: string;
  description: string;
  data_source: string;
  instrument_mission: string;
  observation_date: string;
  units: string;
  resolution: string;
  availability_status: string;
  is_derived: boolean;
  calculation_method: string;
  scientific_disclaimer: string;
  wmts_layer: string | null;
  source_url: string;
}

export interface MissionSite {
  id: string;
  name: string;
  mission_name: string;
  agency: string;
  site_type: string;
  status: string;
  landing_date: string;
  sols_operated: number;
  mass_kg: number;
  latitude: number;
  longitude: number;
  elevation_m: number;
  region: string;
  zoom_tier: ZoomTier;
  instruments: string;
  scientific_summary: string;
  source_url: string;
}

export interface TerrainRiskResult {
  latitude: number;
  longitude: number;
  nearest_feature_name: string;
  nearest_feature_distance_km: number;
  elevation_m: number;
  slope_deg: number;
  roughness_index: number;
  thermal_inertia_tiu: number;
  radiation_msv_day: number;
  atmospheric_pressure_mbar: number;
  risk_score: number;
  risk_classification: "Low Risk" | "Moderate Risk" | "High Risk" | "Very High Risk";
  steep_terrain_flag: boolean;
  traversal_assessment: string;
  calculation_method: string;
  data_status: string;
  scientific_disclaimer: string;
}

export interface RouteWaypoint {
  sequence_index: number;
  latitude: number;
  longitude: number;
  elevation_m: number;
  slope_deg: number;
  risk_score: number;
  risk_class: string;
  cumulative_km: number;
}

export interface RouteProfileResult {
  profile: "shortest" | "lowest_risk" | "balanced";
  profile_label: string;
  start_name: string;
  end_name: string;
  total_distance_km: number;
  direct_great_circle_km: number;
  detour_factor: number;
  estimated_difficulty: string;
  mean_risk_score: number;
  max_slope_deg: number;
  mean_slope_deg: number;
  elevation_gain_m: number;
  elevation_loss_m: number;
  estimated_radiation_msv: number;
  is_provisional: boolean;
  algorithm: string;
  scientific_disclaimer: string;
  waypoints: RouteWaypoint[];
}
