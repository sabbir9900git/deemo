import {
  MarsLocation,
  MissionSite,
  RouteProfileResult,
  ScientificLayer,
  SolarPlanet,
  TerrainRiskResult,
} from "../types/mars";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000/api";

export async function fetchSolarSystem(): Promise<{ scale_note: string; planets: SolarPlanet[] }> {
  const res = await fetch(`${API_BASE}/solar-system`);
  if (!res.ok) throw new Error("Failed to fetch Solar System telemetry");
  return res.json();
}

export async function fetchMarsLocations(zoomLevel?: string, category?: string, search?: string): Promise<MarsLocation[]> {
  const params = new URLSearchParams();
  if (zoomLevel) params.set("zoom_level", zoomLevel);
  if (category) params.set("category", category);
  if (search) params.set("search", search);
  const res = await fetch(`${API_BASE}/locations?${params.toString()}`);
  if (!res.ok) throw new Error("Failed to fetch USGS Mars locations");
  return res.json();
}

export async function fetchScientificLayers(): Promise<ScientificLayer[]> {
  const res = await fetch(`${API_BASE}/layers`);
  if (!res.ok) throw new Error("Failed to fetch scientific layers");
  return res.json();
}

export async function fetchMissionSites(): Promise<MissionSite[]> {
  const res = await fetch(`${API_BASE}/missions`);
  if (!res.ok) throw new Error("Failed to fetch NASA mission sites");
  return res.json();
}

export async function fetchTerrainRisk(lat: number, lon: number): Promise<TerrainRiskResult> {
  const res = await fetch(`${API_BASE}/terrain-risk?lat=${lat}&lon=${lon}`);
  if (!res.ok) throw new Error("Failed to evaluate MOLA terrain risk");
  return res.json();
}

export async function planMarswalkRoutes(payload: {
  start_lat: number;
  start_lon: number;
  start_name: string;
  end_lat: number;
  end_lon: number;
  end_name: string;
}): Promise<{ start_name: string; end_name: string; recommended_profile: string; profiles: RouteProfileResult[] }> {
  const res = await fetch(`${API_BASE}/routes/plan`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to generate Marswalk routes");
  return res.json();
}

export async function askMissionAssistant(payload: {
  question: string;
  context_location_id?: string;
  active_layer_id?: string;
}): Promise<{
  answer: string;
  referenced_locations: string[];
  referenced_datasets: string[];
  confidence_note: string;
  mode: string;
}> {
  const res = await fetch(`${API_BASE}/assistant/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to query Mission Assistant");
  return res.json();
}
