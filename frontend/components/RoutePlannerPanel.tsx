"use client";
import React, { useState } from "react";
import { MarsLocation, RouteProfileResult } from "../types/mars";

export default function RoutePlannerPanel({
  locations,
  routes,
  onGenerateRoutes,
}: {
  locations: MarsLocation[];
  routes: RouteProfileResult[];
  onGenerateRoutes: (start: MarsLocation, end: MarsLocation) => void;
}) {
  const [startId, setStartId] = useState<string>("jezero-crater");
  const [endId, setEndId] = useState<string>("syrtis-major-planum");

  const handlePlan = () => {
    const s = locations.find((l) => l.id === startId) || locations[0];
    const e = locations.find((l) => l.id === endId) || locations[1];
    if (s && e) onGenerateRoutes(s, e);
  };

  return (
    <div className="glass-panel rounded-xl p-5 space-y-4">
      <h3 className="text-lg font-bold text-white">Marswalk A* Surface Route Planner</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 items-end">
        <div>
          <label className="block text-xs text-slate-400 mb-1">Starting Location</label>
          <select
            value={startId}
            onChange={(e) => setStartId(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white"
          >
            {locations.map((l) => (
              <option key={l.id} value={l.id}>
                {l.name} ({l.latitude.toFixed(1)}°, {l.longitude.toFixed(1)}°E)
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-xs text-slate-400 mb-1">Destination Location</label>
          <select
            value={endId}
            onChange={(e) => setEndId(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white"
          >
            {locations.map((l) => (
              <option key={l.id} value={l.id}>
                {l.name} ({l.latitude.toFixed(1)}°, {l.longitude.toFixed(1)}°E)
              </option>
            ))}
          </select>
        </div>
        <button
          onClick={handlePlan}
          className="bg-mars-500 hover:bg-mars-600 text-white font-semibold py-2 px-4 rounded-lg text-xs transition"
        >
          Compute 3 A* Route Profiles
        </button>
      </div>

      {routes.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-2">
          {routes.map((r) => (
            <div key={r.profile} className="p-3.5 rounded-lg bg-slate-900/90 border border-slate-800 space-y-1.5 text-xs">
              <div className="font-bold text-mars-400">{r.profile_label}</div>
              <div>Total Distance: <strong>{r.total_distance_km.toLocaleString()} km</strong></div>
              <div>Mean Risk Score: <strong>{r.mean_risk_score}/100</strong></div>
              <div>Max Slope: <strong>{r.max_slope_deg}°</strong></div>
              <div>Elevation Gain: <strong>+{r.elevation_gain_m.toLocaleString()} m</strong></div>
              <div className="text-[11px] text-slate-400">{r.estimated_difficulty}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
