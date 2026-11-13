# MARS EXPLORER — REST API Documentation

Base URL: `http://127.0.0.1:8000/api`  
Interactive Swagger UI: `http://127.0.0.1:8000/docs`

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Returns operational status and row counts across all SQLite tables. |
| `GET` | `/api/solar-system` | Returns Sun + 8 planets with NASA NSSDCA Planetary Fact Sheet parameters and visual vs. astronomical scale metadata. |
| `GET` | `/api/locations` | Lists official USGS Mars locations. Supports `?zoom_level=zoom_out\|medium_zoom\|zoom_in`, `?category=Volcano`, and `?search=Olympus`. |
| `GET` | `/api/locations/{id}` | Returns full USGS & MOLA dossier for a specific Mars location (e.g., `/api/locations/olympus-mons`). |
| `GET` | `/api/layers` | Returns all 13 Mars scientific layers with data source, instrument, units, resolution, availability status, and derived calculation methods. |
| `GET` | `/api/missions` | Lists all 12 verified Mars surface landers, rovers, helicopter airfields, and sample return depots. |
| `GET` | `/api/datasets` | Lists all 10 official NASA & USGS dataset sources with PDS/Mars Trek URLs and scientific citations. |
| `GET` | `/api/terrain-risk?lat=18.38&lon=77.58` | Evaluates MOLA elevation, regional slope (deg), roughness index, RAD radiation dose (mSv/day), pressure (mbar), and 4-tier Terrain Risk at `(lat, lon)`. |
| `POST` | `/api/routes/plan` | Runs Spherical Corridor A* pathfinding between start and destination coordinates across all 3 profiles (`shortest`, `lowest_risk`, `balanced`). |
| `GET` | `/api/routes/saved` | Returns saved Marswalk routes and waypoint counts from SQLite. |
| `POST` | `/api/assistant/ask` | Queries the Grounded AI Mission Assistant using verified local NASA/USGS data. |
