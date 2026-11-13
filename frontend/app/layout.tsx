import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "MARS EXPLORER — AI-Powered Interplanetary Survival & Mission Planning System",
  description:
    "NASA Space Apps Challenge Full-Stack Application integrating 3D Solar System, Interactive 3D Mars Globe, USGS Planetary Nomenclature, MOLA Terrain Risk, and A* Marswalk Route Planner.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
