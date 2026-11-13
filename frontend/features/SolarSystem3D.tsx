"use client";
import React, { useRef, useState } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { OrbitControls, Stars, Html } from "@react-three/drei";
import * as THREE from "three";
import { SolarPlanet } from "../types/mars";

interface SolarSystemProps {
  planets: SolarPlanet[];
  selectedPlanet: SolarPlanet | null;
  onSelectPlanet: (planet: SolarPlanet) => void;
  onEnterMarsExplorer: () => void;
}

function PlanetMesh({
  planet,
  isSelected,
  onSelect,
}: {
  planet: SolarPlanet;
  isSelected: boolean;
  onSelect: () => void;
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  const angleRef = useRef<number>(Math.random() * Math.PI * 2);

  useFrame((_, delta) => {
    if (!meshRef.current) return;
    meshRef.current.rotation.y += delta * 0.6;
    if (planet.visual_orbit_radius > 0 && planet.orbital_period_days > 0) {
      const angularSpeed = (2 * Math.PI) / (planet.orbital_period_days * 0.25);
      angleRef.current += delta * angularSpeed;
      meshRef.current.position.x = Math.cos(angleRef.current) * planet.visual_orbit_radius;
      meshRef.current.position.z = Math.sin(angleRef.current) * planet.visual_orbit_radius;
    }
  });

  return (
    <group>
      {planet.visual_orbit_radius > 0 && (
        <mesh rotation={[-Math.PI / 2, 0, 0]}>
          <ringGeometry args={[planet.visual_orbit_radius - 0.04, planet.visual_orbit_radius + 0.04, 128]} />
          <meshBasicMaterial
            color={planet.id === "mars" ? "#e05a33" : "#334155"}
            side={THREE.DoubleSide}
            transparent
            opacity={planet.id === "mars" ? 0.65 : 0.3}
          />
        </mesh>
      )}
      <mesh ref={meshRef} onClick={onSelect}>
        <sphereGeometry args={[planet.visual_radius, 32, 32]} />
        {planet.id === "sun" ? (
          <meshBasicMaterial color={planet.color} />
        ) : (
          <meshStandardMaterial
            color={planet.color}
            roughness={0.7}
            metalness={0.1}
            emissive={isSelected || planet.id === "mars" ? planet.color : "#000000"}
            emissiveIntensity={isSelected ? 0.35 : planet.id === "mars" ? 0.18 : 0}
          />
        )}
        <Html distanceFactor={18}>
          <button
            onClick={onSelect}
            className={`px-2 py-0.5 rounded text-xs font-semibold whitespace-nowrap border ${
              planet.id === "mars"
                ? "bg-mars-600/90 text-white border-mars-400 shadow-lg"
                : "bg-slate-900/80 text-slate-200 border-slate-700"
            }`}
          >
            {planet.name}
          </button>
        </Html>
      </mesh>
    </group>
  );
}

export default function SolarSystem3D({
  planets,
  selectedPlanet,
  onSelectPlanet,
  onEnterMarsExplorer,
}: SolarSystemProps) {
  return (
    <div className="relative w-full h-full min-h-[560px] bg-space-950 rounded-xl overflow-hidden border border-slate-800">
      <Canvas camera={{ position: [0, 18, 28], fov: 48 }}>
        <ambientLight intensity={0.35} />
        <pointLight position={[0, 0, 0]} intensity={2.6} color="#ffddaa" />
        <Stars radius={120} depth={60} count={4500} factor={4} fade />
        {planets.map((p) => (
          <PlanetMesh
            key={p.id}
            planet={p}
            isSelected={selectedPlanet?.id === p.id}
            onSelect={() => {
              onSelectPlanet(p);
              if (p.id === "mars") onEnterMarsExplorer();
            }}
          />
        ))}
        <OrbitControls enablePan enableZoom enableRotate minDistance={5} maxDistance={65} />
      </Canvas>
    </div>
  );
}
