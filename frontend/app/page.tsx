"use client";
import React, { useState } from "react";
import { useMarsExplorer } from "../hooks/useMarsExplorer";
import SolarSystem3D from "../features/SolarSystem3D";
import MarsGlobe3D from "../features/MarsGlobe3D";
import LayerControlPanel from "../components/LayerControlPanel";
import TerrainRiskDashboard from "../components/TerrainRiskDashboard";
import RoutePlannerPanel from "../components/RoutePlannerPanel";
import MissionAssistantPanel from "../components/MissionAssistantPanel";
import { SolarPlanet } from "../types/mars";

export default function MarsExplorerPage() {
  const {
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
  } = useMarsExplorer();

  const [selectedPlanet, setSelectedPlanet] = useState<SolarPlanet | null>(null);
  const [activeRouteProfile, setActiveRouteProfile] = useState<string>("balanced");

  return (
    <main className="min-h-screen flex flex-col bg-space-950 text-slate-100">
      <header className="glass-panel border-b border-slate-800 px-6 py-3 flex flex-wrap items-center justify-between gap-4">
        <div>
          <span className="text-[11px] font-bold tracking-widest uppercase text-mars-400">
            NASA Space Apps Challenge • Planetary Exploration Platform
          </span>
          <h1 className="text-xl font-extrabold tracking-tight text-white">
            MARS EXPLORER{" "}
            <span className="text-xs font-normal text-slate-400">
              AI-Powered Interplanetary Survival & Mission Planning System
            </span>
          </h1>
        </div>
        <nav className="flex flex-wrap gap-2 text-xs">
          {[
            { id: "solar-system", label: "1. 3D Solar System" },
            { id: "mars-globe", label: "2. 3D Mars Explorer" },
            { id: "layers", label: "3. 13 Scientific Layers" },
            { id: "terrain-risk", label: "4. Terrain Risk & Route Planner" },
            { id: "assistant", label: "5. AI Mission Assistant" },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveView(tab.id)}
              className={`px-3 py-1.5 rounded-lg font-semibold transition ${
                activeView === tab.id
                  ? "bg-mars-500 text-white"
                  : "bg-slate-900 text-slate-300 hover:bg-slate-800"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </header>

      <div className="flex-1 p-6 space-y-6">
        {activeView === "solar-system" && (
          <SolarSystem3D
            planets={planets}
            selectedPlanet={selectedPlanet}
            onSelectPlanet={setSelectedPlanet}
            onEnterMarsExplorer={() => setActiveView("mars-globe")}
          />
        )}

        {activeView === "mars-globe" && (
          <MarsGlobe3D
            locations={locations}
            missions={missions}
            activeLayerId={activeLayerId}
            selectedLocation={selectedLocation}
            onSelectLocation={(loc) => {
              setSelectedLocation(loc);
              inspectCoordinates(loc.latitude, loc.longitude);
            }}
            routes={routes}
            activeRouteProfile={activeRouteProfile}
          />
        )}

        {activeView === "layers" && (
          <LayerControlPanel
            layers={layers}
            activeLayerId={activeLayerId}
            onSelectLayer={setActiveLayerId}
          />
        )}

        {activeView === "terrain-risk" && (
          <div className="space-y-6">
            <TerrainRiskDashboard risk={terrainRisk} onInspectCoords={inspectCoordinates} />
            <RoutePlannerPanel
              locations={locations}
              routes={routes}
              onGenerateRoutes={computeRoutes}
            />
          </div>
        )}

        {activeView === "assistant" && <MissionAssistantPanel />}
      </div>
    </main>
  );
}
