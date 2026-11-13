"use client";
import React, { useMemo, useRef, useState } from "react";
import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { OrbitControls, Stars, Html, Line } from "@react-three/drei";
import * as THREE from "three";
import { MarsLocation, MissionSite, RouteProfileResult } from "../types/mars";
import { getZoomTierFromCameraDistance, latLonToVector3 } from "../lib/marsScience";

interface MarsGlobeProps {
  locations: MarsLocation[];
  missions: MissionSite[];
  activeLayerId: string;
  selectedLocation: MarsLocation | null;
  onSelectLocation: (loc: MarsLocation) => void;
  routes: RouteProfileResult[];
  activeRouteProfile: string;
}

function GlobeScene({
  locations,
  missions,
  selectedLocation,
  onSelectLocation,
  routes,
  activeRouteProfile,
}: MarsGlobeProps) {
  const { camera } = useThree();
  const [zoomTier, setZoomTier] = useState<"zoom_out" | "medium_zoom" | "zoom_in">("zoom_out");

  useFrame(() => {
    const dist = camera.position.length();
    const tier = getZoomTierFromCameraDistance(dist);
    if (tier !== zoomTier) setZoomTier(tier);
  });

  const visibleLocations = useMemo(() => {
    if (zoomTier === "zoom_out") {
      return locations.filter((l) => l.zoom_tier === "zoom_out");
    }
    if (zoomTier === "medium_zoom") {
      return locations.filter((l) => l.zoom_tier === "zoom_out" || l.zoom_tier === "medium_zoom");
    }
    return locations;
  }, [locations, zoomTier]);

  const activeRoute = useMemo(
    () => routes.find((r) => r.profile === activeRouteProfile),
    [routes, activeRouteProfile]
  );

  const routePoints = useMemo(() => {
    if (!activeRoute) return [];
    return activeRoute.waypoints.map((wp) =>
      new THREE.Vector3(...latLonToVector3(wp.latitude, wp.longitude, 2.025))
    );
  }, [activeRoute]);

  return (
    <group>
      <mesh>
        <sphereGeometry args={[2.0, 64, 64]} />
        <meshStandardMaterial color="#c8532c" roughness={0.82} metalness={0.08} />
      </mesh>

      {visibleLocations.map((loc) => {
        const pos = latLonToVector3(loc.latitude, loc.longitude, 2.02);
        const isSelected = selectedLocation?.id === loc.id;
        return (
          <group key={loc.id} position={pos}>
            <mesh onClick={() => onSelectLocation(loc)}>
              <sphereGeometry args={[isSelected ? 0.045 : 0.028, 16, 16]} />
              <meshBasicMaterial color={isSelected ? "#fbbf24" : "#f97316"} />
            </mesh>
            <Html distanceFactor={8}>
              <button
                onClick={() => onSelectLocation(loc)}
                className={`px-1.5 py-0.5 rounded text-[11px] font-medium whitespace-nowrap border ${
                  isSelected
                    ? "bg-amber-500 text-slate-950 border-amber-300 font-bold"
                    : "bg-slate-950/85 text-orange-200 border-orange-500/40"
                }`}
              >
                {loc.name}
              </button>
            </Html>
          </group>
        );
      })}

      {zoomTier !== "zoom_out" &&
        missions.map((m) => {
          const pos = latLonToVector3(m.latitude, m.longitude, 2.03);
          return (
            <group key={m.id} position={pos}>
              <mesh>
                <boxGeometry args={[0.035, 0.035, 0.035]} />
                <meshBasicMaterial color="#38bdf8" />
              </mesh>
            </group>
          );
        })}

      {routePoints.length > 1 && (
        <Line points={routePoints} color="#22c55e" lineWidth={3} />
      )}
    </group>
  );
}

export default function MarsGlobe3D(props: MarsGlobeProps) {
  return (
    <div className="relative w-full h-full min-h-[560px] bg-space-950 rounded-xl overflow-hidden border border-slate-800">
      <Canvas camera={{ position: [0, 1.2, 4.2], fov: 45 }}>
        <ambientLight intensity={0.45} />
        <directionalLight position={[6, 4, 6]} intensity={1.6} color="#fff3e6" />
        <Stars radius={90} depth={40} count={3500} factor={3} fade />
        <GlobeScene {...props} />
        <OrbitControls enablePan={false} minDistance={2.35} maxDistance={6.0} />
      </Canvas>
    </div>
  );
}
