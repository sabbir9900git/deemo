"""
Marswalk A* Surface Route Planner Service
Implements A* pathfinding over a dynamic spherical waypoint lattice between start and destination
coordinates on Mars, generating three scientifically distinct traversal profiles:
  1. shortest     (Minimal great-circle distance cost)
  2. lowest_risk  (Heavily penalizes steep slopes, rough terrain, and extreme altitudes)
  3. balanced     (Optimal trade-off between distance and terrain risk)
"""
import heapq
import math
from typing import Dict, List, Tuple
from app.services.terrain_service import (
    MARS_MEAN_RADIUS_KM,
    evaluate_terrain_risk,
    great_circle_distance_km,
    normalize_lon,
)

PROFILE_CONFIGS = {
    "shortest": {
        "label": "Shortest Route",
        "dist_weight": 1.0,
        "risk_weight": 0.04,
        "slope_weight": 0.05,
        "elev_weight": 0.02,
    },
    "lowest_risk": {
        "label": "Lowest Terrain Risk",
        "dist_weight": 1.0,
        "risk_weight": 1.65,
        "slope_weight": 2.40,
        "elev_weight": 0.85,
    },
    "balanced": {
        "label": "Balanced Route",
        "dist_weight": 1.0,
        "risk_weight": 0.65,
        "slope_weight": 0.90,
        "elev_weight": 0.35,
    },
}

def _interpolate_great_circle(
    lat1: float, lon1: float, lat2: float, lon2: float, f: float
) -> Tuple[float, float]:
    """Spherical linear interpolation (SLERP) along great circle."""
    phi1, lam1 = math.radians(lat1), math.radians(lon1)
    phi2, lam2 = math.radians(lat2), math.radians(lon2)

    x1 = math.cos(phi1) * math.cos(lam1)
    y1 = math.cos(phi1) * math.sin(lam1)
    z1 = math.sin(phi1)

    x2 = math.cos(phi2) * math.cos(lam2)
    y2 = math.cos(phi2) * math.sin(lam2)
    z2 = math.sin(phi2)

    dot = max(-1.0, min(1.0, x1 * x2 + y1 * y2 + z1 * z2))
    omega = math.acos(dot)
    if omega < 1e-6:
        return lat1, normalize_lon(lon1)

    sin_omega = math.sin(omega)
    a = math.sin((1.0 - f) * omega) / sin_omega
    b = math.sin(f * omega) / sin_omega
    x = a * x1 + b * x2
    y = a * y1 + b * y2
    z = a * z1 + b * z2

    lat = math.degrees(math.atan2(z, math.sqrt(x * x + y * y)))
    lon = normalize_lon(math.degrees(math.atan2(y, x)))
    return lat, lon

def plan_marswalk_route(
    start_lat: float,
    start_lon: float,
    start_name: str,
    end_lat: float,
    end_lon: float,
    end_name: str,
    profile_key: str,
    locations: List[Dict],
) -> Dict:
    """
    Run A* pathfinding on an oriented spherical corridor grid (N_steps x M_offsets)
    connecting (start_lat, start_lon) to (end_lat, end_lon).
    """
    if profile_key not in PROFILE_CONFIGS:
        profile_key = "balanced"
    cfg = PROFILE_CONFIGS[profile_key]

    s_lon = normalize_lon(start_lon)
    e_lon = normalize_lon(end_lon)
    direct_km = max(1.0, great_circle_distance_km(start_lat, s_lon, end_lat, e_lon))

    # Build oriented corridor lattice: 16 longitudinal steps x 7 lateral offsets
    n_steps = 16
    lateral_offsets = [-3, -2, -1, 0, 1, 2, 3]
    # Lateral spread scales with route length (up to +/- 14 degrees for trans-regional routes)
    max_lat_spread_deg = min(14.0, max(1.2, (direct_km / MARS_MEAN_RADIUS_KM) * 18.0))

    # Compute tangent unit normal in (lat, lon) space
    dlat = end_lat - start_lat
    dlon = ((e_lon - s_lon + 180.0) % 360.0) - 180.0
    norm_len = math.hypot(dlat, dlon) or 1.0
    perp_lat = -dlon / norm_len
    perp_lon = dlat / norm_len

    # Precompute node coordinates & terrain telemetry
    nodes: Dict[Tuple[int, int], Dict] = {}
    for i in range(n_steps + 1):
        f = i / n_steps
        base_lat, base_lon = _interpolate_great_circle(start_lat, s_lon, end_lat, e_lon, f)
        # Taper lateral spread at endpoints (sin(pi * f))
        envelope = math.sin(math.pi * f)
        offsets_for_step = [0] if (i == 0 or i == n_steps) else lateral_offsets
        for j in offsets_for_step:
            shift = (j / 3.0) * max_lat_spread_deg * envelope
            n_lat = max(-88.5, min(88.5, base_lat + perp_lat * shift))
            n_lon = normalize_lon(base_lon + perp_lon * shift)
            terrain = evaluate_terrain_risk(n_lat, n_lon, locations)
            nodes[(i, j)] = terrain

    start_node = (0, 0)
    goal_node = (n_steps, 0)

    # A* Search
    open_heap = [(0.0, start_node)]
    g_score = {start_node: 0.0}
    came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}

    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current == goal_node:
            break
        ci, cj = current
        if ci >= n_steps:
            continue
        next_i = ci + 1
        next_js = [0] if next_i == n_steps else [k for k in lateral_offsets if abs(k - cj) <= 2]
        for nj in next_js:
            neighbor = (next_i, nj)
            cur_t = nodes[current]
            nxt_t = nodes[neighbor]
            seg_km = great_circle_distance_km(
                cur_t["latitude"], cur_t["longitude"],
                nxt_t["latitude"], nxt_t["longitude"]
            )
            elev_diff_km = abs(nxt_t["elevation_m"] - cur_t["elevation_m"]) / 1000.0
            mean_risk = 0.5 * (cur_t["risk_score"] + nxt_t["risk_score"]) / 100.0
            mean_slope = 0.5 * (cur_t["slope_deg"] + nxt_t["slope_deg"]) / 15.0

            edge_cost = seg_km * (
                cfg["dist_weight"]
                + cfg["risk_weight"] * (mean_risk ** 1.4)
                + cfg["slope_weight"] * (mean_slope ** 1.6)
                + cfg["elev_weight"] * elev_diff_km
            )
            tentative_g = g_score[current] + edge_cost
            if tentative_g < g_score.get(neighbor, 1e18):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                h_km = great_circle_distance_km(
                    nxt_t["latitude"], nxt_t["longitude"],
                    end_lat, e_lon
                )
                f_score = tentative_g + h_km * cfg["dist_weight"]
                heapq.heappush(open_heap, (f_score, neighbor))

    # Reconstruct path
    path_keys = [goal_node]
    cur = goal_node
    while cur in came_from:
        cur = came_from[cur]
        path_keys.append(cur)
    path_keys.reverse()

    waypoints = []
    cum_km = 0.0
    elev_gain = 0.0
    elev_loss = 0.0
    for idx, key in enumerate(path_keys):
        t = nodes[key]
        if idx > 0:
            prev_t = nodes[path_keys[idx - 1]]
            d_km = great_circle_distance_km(
                prev_t["latitude"], prev_t["longitude"],
                t["latitude"], t["longitude"]
            )
            cum_km += d_km
            dz = t["elevation_m"] - prev_t["elevation_m"]
            if dz > 0:
                elev_gain += dz
            else:
                elev_loss += abs(dz)
        waypoints.append({
            "sequence_index": idx,
            "latitude": t["latitude"],
            "longitude": t["longitude"],
            "elevation_m": t["elevation_m"],
            "slope_deg": t["slope_deg"],
            "risk_score": t["risk_score"],
            "risk_class": t["risk_classification"],
            "cumulative_km": round(cum_km, 2),
        })

    mean_risk = sum(w["risk_score"] for w in waypoints) / len(waypoints)
    max_slope = max(w["slope_deg"] for w in waypoints)
    mean_slope = sum(w["slope_deg"] for w in waypoints) / len(waypoints)

    # Estimate rover/crew traverse sols at 15 km/sol nominal pressurized rover speed & radiation dose
    est_sols = max(1.0, cum_km / 15.0)
    est_radiation_msv = round(est_sols * 0.64, 2)

    if mean_risk < 28 and max_slope < 5.0:
        difficulty = "Low (Nominal Rover / Pressurized Traverse)"
    elif mean_risk < 50 and max_slope < 10.0:
        difficulty = "Moderate (Standard Hazard Avoidance Required)"
    elif mean_risk < 70:
        difficulty = "High (Steep Grades & Rough Regolith)"
    else:
        difficulty = "Extreme (Severe Topographic Escarpments)"

    return {
        "profile": profile_key,
        "profile_label": cfg["label"],
        "start_name": start_name,
        "end_name": end_name,
        "total_distance_km": round(cum_km, 2),
        "direct_great_circle_km": round(direct_km, 2),
        "detour_factor": round(cum_km / max(1.0, direct_km), 3),
        "estimated_difficulty": difficulty,
        "mean_risk_score": round(mean_risk, 1),
        "max_slope_deg": round(max_slope, 2),
        "mean_slope_deg": round(mean_slope, 2),
        "elevation_gain_m": round(elev_gain, 1),
        "elevation_loss_m": round(elev_loss, 1),
        "estimated_radiation_msv": est_radiation_msv,
        "is_provisional": True,
        "algorithm": "Spherical Corridor A* Pathfinding (MOLA 463-m Topographic Cost Grid)",
        "scientific_disclaimer": (
            "PROVISIONAL PLANNING ROUTE: Computed using regional MOLA topography (~463 m grid). "
            "Meter-scale boulders, unconsolidated drift sand, and local scarps require HiRISE stereo DTM "
            "validation. Never treat as certified real-astronaut navigation."
        ),
        "waypoints": waypoints,
    }

def compare_all_route_profiles(
    start_lat: float,
    start_lon: float,
    start_name: str,
    end_lat: float,
    end_lon: float,
    end_name: str,
    locations: List[Dict],
) -> Dict:
    """Generate and compare all 3 required Marswalk route profiles."""
    results = []
    for prof in ["shortest", "lowest_risk", "balanced"]:
        res = plan_marswalk_route(
            start_lat, start_lon, start_name,
            end_lat, end_lon, end_name,
            prof, locations
        )
        results.append(res)

    # Recommend lowest_risk if max_slope of balanced > 9 deg, else balanced
    balanced_res = next(r for r in results if r["profile"] == "balanced")
    recommended = "lowest_risk" if balanced_res["max_slope_deg"] > 9.0 else "balanced"

    return {
        "start_name": start_name,
        "end_name": end_name,
        "recommended_profile": recommended,
        "profiles": results,
    }
