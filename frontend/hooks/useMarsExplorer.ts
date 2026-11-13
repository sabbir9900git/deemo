import { useState, useEffect, useCallback } from "react";
import {
  MarsLocation,
  MissionSite,
  RouteProfileResult,
  ScientificLayer,
  SolarPlanet,
  TerrainRiskResult,
} from "../types/mars";
import {
  fetchMarsLocations,
  fetchMissionSites,
  fetchScientificLayers,
  fetchSolarSystem,
  fetchTerrainRisk,
  planMarswalkRoutes,
} from "../services/api";

export function useMarsExplorer() {
  const [activeView, setActiveView] = useState<string>("solar-system");
  const [planets, setPlanets] = useState<SolarPlanet[]>([]);
  const [locations, setLocations] = useState<MarsLocation[]>([]);
  const [layers, setLayers] = useState<ScientificLayer[]>([]);
  const [missions, setMissions] = useState<MissionSite[]>([]);
  const [activeLayerId, setActiveLayerId] = useState<string>("base_map");
  const [selectedLocation, setSelectedLocation] = useState<MarsLocation | null>(null);
  const [terrainRisk, setTerrainRisk] = useState<TerrainRiskResult | null>(null);
  const [routes, setRoutes] = useState<RouteProfileResult[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadInitialData() {
      try {
        setLoading(true);
        const [solarData, locs, scLayers, missionList] = await Promise.all([
          fetchSolarSystem(),
          fetchMarsLocations("all"),
          fetchScientificLayers(),
          fetchMissionSites(),
        ]);
        setPlanets(solarData.planets);
        setLocations(locs);
        setLayers(scLayers);
        setMissions(missionList);
        if (locs.length > 0) {
          setSelectedLocation(locs[0]);
          const risk = await fetchTerrainRisk(locs[0].latitude, locs[0].longitude);
          setTerrainRisk(risk);
        }
      } catch (err: any) {
        setError(err?.message || "Failed to load Mars Explorer telemetry");
      } finally {
        setLoading(false);
      }
    }
    loadInitialData();
  }, []);

  const inspectCoordinates = useCallback(async (lat: number, lon: number) => {
    const risk = await fetchTerrainRisk(lat, lon);
    setTerrainRisk(risk);
  }, []);

  const computeRoutes = useCallback(
    async (start: MarsLocation, end: MarsLocation) => {
      const resp = await planMarswalkRoutes({
        start_lat: start.latitude,
        start_lon: start.longitude,
        start_name: start.name,
        end_lat: end.latitude,
        end_lon: end.longitude,
        end_name: end.name,
      });
      setRoutes(resp.profiles);
      return resp;
    },
    []
  );

  return {
    activeView,
    setActiveView,
    planets,
    locations,
    layers,
    missions,
    activeLayerId,
    setActiveLayerId,
    selectedLocation,
    setSelectedLocation,
    terrainRisk,
    inspectCoordinates,
    routes,
    computeRoutes,
    loading,
    error,
  };
}
