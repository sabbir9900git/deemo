"use client";
import React from "react";
import { TerrainRiskResult } from "../types/mars";

export default function TerrainRiskDashboard({
  risk,
  onInspectCoords,
}: {
  risk: TerrainRiskResult | null;
  onInspectCoords: (lat: number, lon: number) => void;
}) {
  if (!risk) return null;

  return (
    <div className="glass-panel rounded-xl p-5 space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-3">
        <div>
          <h3 className="text-lg font-bold text-white">
            MOLA Terrain Risk Analysis — {risk.nearest_feature_name}
          </h3>
          <p className="text-xs text-slate-400">
            Coordinates: {risk.latitude.toFixed(2)}°N, {risk.longitude.toFixed(2)}°E
          </p>
        </div>
        <span className="px-3 py-1 rounded-full text-xs font-bold bg-mars-600/30 border border-mars-500 text-mars-400">
          {risk.risk_classification} (Score: {risk.risk_score}/100)
        </span>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
        <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
          <div className="text-slate-400">MOLA Elevation</div>
          <div className="text-base font-bold text-white mt-0.5">{risk.elevation_m.toLocaleString()} m</div>
        </div>
        <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
          <div className="text-slate-400">Regional Slope</div>
          <div className="text-base font-bold text-white mt-0.5">{risk.slope_deg}°</div>
        </div>
        <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
          <div className="text-slate-400">Surface Radiation (RAD)</div>
          <div className="text-base font-bold text-white mt-0.5">{risk.radiation_msv_day} mSv/day</div>
        </div>
        <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
          <div className="text-slate-400">Surface Pressure</div>
          <div className="text-base font-bold text-white mt-0.5">{risk.atmospheric_pressure_mbar} mbar</div>
        </div>
      </div>

      <p className="text-xs text-slate-300 leading-relaxed">{risk.traversal_assessment}</p>
      <div className="p-3 rounded-lg bg-amber-950/40 border border-amber-500/40 text-xs text-amber-200">
        {risk.scientific_disclaimer}
      </div>
    </div>
  );
}
