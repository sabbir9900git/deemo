/**
 * Client-side Spherical Coordinate & MOLA Scientific Utilities
 * Converts aerographic (latitude, East longitude) to 3D Cartesian vectors on the Mars globe.
 */
export const MARS_MEAN_RADIUS_KM = 3389.5;

export function latLonToVector3(latDeg: number, lonEastDeg: number, radius: number): [number, number, number] {
  const phi = ((90 - latDeg) * Math.PI) / 180;
  const theta = ((lonEastDeg + 180) * Math.PI) / 180;
  const x = -(radius * Math.sin(phi) * Math.cos(theta));
  const z = radius * Math.sin(phi) * Math.sin(theta);
  const y = radius * Math.cos(phi);
  return [x, y, z];
}

export function getZoomTierFromCameraDistance(distance: number): "zoom_out" | "medium_zoom" | "zoom_in" {
  if (distance > 3.1) return "zoom_out";
  if (distance > 2.15) return "medium_zoom";
  return "zoom_in";
}
