"use client";
import React from "react";
import { ScientificLayer } from "../types/mars";

export default function LayerControlPanel({
  layers,
  activeLayerId,
  onSelectLayer,
}: {
  layers: ScientificLayer[];
  activeLayerId: string;
  onSelectLayer: (id: string) => void;
}) {
  const activeLayer = layers.find((l) => l.id === activeLayerId) || layers[0];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <div className="lg:col-span-1 glass-panel rounded-xl p-4 space-y-2 max-h-[600px] overflow-y-auto">
        <h3 className="text-sm font-bold uppercase tracking-wider text-mars-400">
          13 Mars Scientific Layers
        </h3>
        {layers.map((layer) => (
          <button
            key={layer.id}
            onClick={() => onSelectLayer(layer.id)}
            className={`w-full text-left p-2.5 rounded-lg border transition ${
              layer.id === activeLayerId
                ? "bg-mars-600/25 border-mars-500 text-white"
                : "bg-slate-900/60 border-slate-800 text-slate-300 hover:border-slate-700"
            }`}
          >
            <div className="flex items-center justify-between text-xs font-semibold">
              <span>
                {layer.layer_number}. {layer.name}
              </span>
              <span
                className={`px-1.5 py-0.5 rounded text-[10px] ${
                  layer.is_derived
                    ? "bg-amber-500/20 text-amber-300"
                    : "bg-emerald-500/20 text-emerald-300"
                }`}
              >
                {layer.is_derived ? "Derived" : "Raw / Calibrated"}
              </span>
            </div>
            <p className="text-[11px] text-slate-400 mt-1 truncate">{layer.instrument_mission}</p>
          </button>
        ))}
      </div>

      {activeLayer && (
        <div className="lg:col-span-2 glass-panel rounded-xl p-5 space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-3">
            <div>
              <span className="text-xs uppercase text-mars-400 font-semibold">
                {activeLayer.category}
              </span>
              <h2 className="text-xl font-bold text-white">{activeLayer.name}</h2>
            </div>
            <span className="px-3 py-1 rounded-full text-xs font-semibold bg-slate-800 text-slate-200">
              {activeLayer.availability_status}
            </span>
          </div>

          <p className="text-sm text-slate-300 leading-relaxed">{activeLayer.description}</p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
              <div className="text-slate-400">Official Data Source</div>
              <div className="font-semibold text-white mt-0.5">{activeLayer.data_source}</div>
            </div>
            <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
              <div className="text-slate-400">Instrument / Mission</div>
              <div className="font-semibold text-white mt-0.5">{activeLayer.instrument_mission}</div>
            </div>
            <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
              <div className="text-slate-400">Units & Resolution</div>
              <div className="font-semibold text-white mt-0.5">
                {activeLayer.units} ({activeLayer.resolution})
              </div>
            </div>
            <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
              <div className="text-slate-400">Observation Date</div>
              <div className="font-semibold text-white mt-0.5">{activeLayer.observation_date}</div>
            </div>
          </div>

          <div className="p-3.5 rounded-lg bg-slate-900/90 border border-slate-800 text-xs space-y-1.5">
            <div className="font-semibold text-mars-400">
              {activeLayer.is_derived ? "Derived Calculation Methodology:" : "Observation Methodology:"}
            </div>
            <p className="text-slate-300">{activeLayer.calculation_method}</p>
          </div>

          <div className="p-3.5 rounded-lg bg-amber-950/40 border border-amber-500/40 text-xs text-amber-200">
            <strong>Scientific Responsibility Note:</strong> {activeLayer.scientific_disclaimer}
          </div>
        </div>
      )}
    </div>
  );
}
