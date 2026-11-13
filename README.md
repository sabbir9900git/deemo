# MARS EXPLORER — AI-Powered Interplanetary Survival & Mission Planning System

**NASA Space Apps Challenge Project**  
A complete, locally runnable, scientifically grounded full-stack planetary exploration and mission planning platform built with **Next.js 14 (TypeScript + Tailwind CSS + Three.js / React Three Fiber + Recharts)** on the frontend and **Python FastAPI + SQLAlchemy / SQLite + NumPy** on the backend.

---

## 1. Key Capabilities & Scientific Responsibility

1. **Interactive 3D Solar System (`SolarSystem3D`)**
   - Displays the Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, and a 3D starfield background.
   - Supports orbit rotation, zoom, planet selection, and smooth camera transitions into **Mars Explorer**.
   - Explicitly distinguishes **Visual Scale Mode** (logarithmic orbital spacing for interactive 3D navigation) from **True Astronomical Scale** metrics sourced from the [NASA NSSDCA Planetary Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/).

2. **Interactive 3D Mars Globe (`MarsGlobe3D`) & Dynamic Zoom-Based USGS Labels**
   - 360-degree rotation, smooth zoom, mouse drag & touch controls, real-time aerographic latitude/longitude & MOLA elevation readout, and camera fly-to animations.
   - Integrates **32+ verified Martian geological features** from the [USGS Gazetteer of Planetary Nomenclature](https://planetarynames.wr.usgs.gov/) and **12 surface mission landing & research sites** ([NASA Science](https://science.nasa.gov/planetary-science/programs/mars-exploration/mission-timeline/how-we-land-on-mars/)).
   - **Dynamic Zoom-Dependent Label System** prevents label overlap:
     - **Zoom Out (Global View):** Major Regions, Major Volcanoes, Major Valleys, Large Basins (*Olympus Mons, Valles Marineris, Hellas Planitia, Utopia Planitia, Elysium Planitia, Syrtis Major Planum, Chryse Planitia, Isidis Planitia, Argyre Planitia, Acidalia Planitia, Amazonis Planitia, Arcadia Planitia, Alba Mons, Planum Boreum, Planum Australe*).
     - **Medium Zoom (Regional View):** Major Craters, Shield Volcanoes, Mountain Ranges, and Landing Sites (*Gale Crater, Jezero Crater, Ascraeus Mons, Pavonis Mons, Arsia Mons, Elysium Mons, Korolev Crater, Eridania Planitia, Charitum Montes, Libya Montes, Phlegra Montes, Apollinaris Mons*, plus NASA/CNSA landing sites).
     - **Zoom In (Local View):** Smaller Craters, Tholi, Dune Fields, and Local Research Locations (*Aeolis Mons / Mount Sharp, Hecates Tholus, Albor Tholus, Tharsis Tholus, Ceraunius Tholus, Ogygis Undae, Zunil Crater, Milankovič Crater, Wright Brothers Field, Three Forks Sample Depot*).

3. **13 Mars Scientific Data Layers (`LayerControlPanel`)**
   - Switchable scientific layers with full provenance metadata (Name, Description, Data Source, Instrument/Mission, Observation Date, Units, Resolution, Availability Status, Raw vs. Derived badge, Calculation Method, and Scientific Disclaimers):
     1. Mars Surface / Base Map (Viking MDIM 2.1 / MGS MOC, 232 m/pixel)
     2. Elevation Map (MGS MOLA DEM, 463 m/pixel, `-8,200 m` to `+21,229 m`)
     3. Terrain Slope (Derived from MOLA central finite differences, degrees)
     4. Terrain Risk (Derived 4-tier traversal hazard model: Low, Moderate, High, Very High Risk)
     5. Temperature / Thermal Data (Mars Odyssey THEMIS Day/Night IR & Thermal Inertia, 100 m/pixel)
     6. Water-Ice Evidence (Mars Odyssey GRS Water-Equivalent Hydrogen wt% & MRO SHARAD subsurface radar — *explicitly states that hydrogen evidence indicates subsurface water ice or bound hydrated minerals, never confirmed liquid water*)
     7. Mineral Distribution (MRO CRISM hydrous clays, sulfates, carbonates, and mafic silicates, 18–200 m/pixel)
     8. Geological Features (USGS SIM 3292 Global Geologic Map: Noachian, Hesperian, Amazonian units)
     9. Dust and Atmospheric Observations (Mars 2020 Perseverance MEDA archival PDS Bundle `urn:nasa:pds:mars2020_meda::6.0`, Sols 1–1859 — *explicitly marked as archival observations, never real-time weather*)
     10. Radiation Observations (MSL Curiosity RAD surface dosimetry `0.64 ± 0.12 mSv/day` / `0.205 ± 0.04 mGy/day` at Gale Crater + altitude column attenuation)
     11. Rover Landing Sites (Sojourner, Spirit, Opportunity, Curiosity, Perseverance, Zhurong)
     12. Mission Locations (All stationary landers, rovers, and helicopter sites)
     13. Scientific Research Locations (HiRISE stereo DTM sites & Mars Sample Return depots)

4. **MOLA Terrain Risk Analysis & Marswalk A* Surface Route Planner**
   - Computes regional slope, roughness index, barometric pressure, RAD surface radiation dose, and 4-tier Terrain Risk (`Low Risk`, `Moderate Risk`, `High Risk`, `Very High Risk`).
   - Runs **Spherical Corridor A* Pathfinding** over the MOLA topographic & slope cost surface to generate and compare three route profiles on the 3D Mars globe:
     1. **Shortest Route**
     2. **Lowest Terrain Risk**
     3. **Balanced Route**
   - Clearly marks routes as provisional planning estimates and never claims certified astronaut safety.

5. **Grounded AI Mission Assistant**
   - Answers questions about Mars terrain, USGS locations, scientific observations, route options, hazards, and NASA datasets using verified project records.
   - Runs 100% locally out-of-the-box with zero external API keys required.

---

## 2. Project Folder Structure

```text
mars-explorer/
├── frontend/                  # Next.js 14 + TypeScript + Tailwind + Three.js + Recharts
│   ├── app/                   # Next.js App Router (layout.tsx, page.tsx, globals.css)
│   ├── components/            # LayerControlPanel, TerrainRiskDashboard, RoutePlannerPanel, MissionAssistantPanel
│   ├── features/              # SolarSystem3D.tsx, MarsGlobe3D.tsx
│   ├── hooks/                 # useMarsExplorer.ts state & API hook
│   ├── lib/                   # marsScience.ts spherical coordinate & zoom-tier utilities
│   ├── services/              # api.ts REST client
│   ├── public/                # Static assets
│   ├── types/                 # mars.ts TypeScript interfaces
│   └── package.json
├── backend/                   # Python FastAPI + SQLAlchemy / SQLite + NumPy
│   ├── app/
│   │   ├── api/routes.py      # REST API endpoints (/api/solar-system, /api/locations, /api/layers, /api/terrain-risk, /api/routes/plan, /api/assistant/ask)
│   │   ├── core/              # config.py, database.py
│   │   ├── models/models.py   # 7 SQLite tables (MarsLocation, DatasetSource, ScientificLayer, MissionSite, SavedRoute, RouteWaypoint, UserPreference)
│   │   ├── schemas/schemas.py # Pydantic request/response schemas
│   │   ├── services/          # terrain_service.py, route_service.py, assistant_service.py, seed_data.py
│   │   └── main.py            # FastAPI application entrypoint
│   └── requirements.txt
├── database/
│   └── mars_explorer.db       # Pre-seeded SQLite database (all 7 tables populated)
├── data/
│   ├── raw/                   # Instructions & local cache directory for raw NASA WMTS tiles
│   ├── processed/             # usgs_mars_nomenclature.json, nasa_missions.json, solar_system_planets.json
│   └── metadata/              # scientific_layers.json, dataset_sources.json
├── scripts/
│   ├── init_db.py             # Creates & seeds SQLite database tables
│   ├── import_usgs_nomenclature.py # Imports official USGS Mars nomenclature JSON/CSV
│   ├── download_nasa_tiles.py # Downloads & caches NASA Mars Trek WMTS tiles
│   └── verify_project.py      # End-to-end verification test script
├── docs/
│   ├── API.md                 # Complete REST API documentation
│   ├── SETUP_WINDOWS.md       # Step-by-step Windows PowerShell / CMD setup guide
│   └── NASA_DATA_ATTRIBUTION.md # Official NASA & USGS dataset citations
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

---

## 3. Quick Start & Local Execution Instructions (Linux / macOS / Windows)

### Prerequisites
- **Python 3.10+**
- **Node.js 18+ & npm**
- No cloud server, external database, or paid API key is required.

### Step 1 — Configure Environment Variables
```bash
cp .env.example .env
# On Windows Command Prompt: copy .env.example .env
```

### Step 2 — Install Backend Dependencies & Initialize Database
```bash
# 1. Create and activate a Python virtual environment
python -m venv .venv
source .venv/bin/activate        # On Windows PowerShell: .\.venv\Scripts\Activate.ps1

# 2. Install backend dependencies
pip install -r backend/requirements.txt

# 3. Initialize the SQLite database & seed NASA/USGS datasets
python scripts/init_db.py

# 4. Import / verify official USGS Planetary Nomenclature place names
python scripts/import_usgs_nomenclature.py
```

### Step 3 — Start the FastAPI Backend Server
```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- Backend REST API: `http://127.0.0.1:8000/api/health`
- Interactive Swagger OpenAPI Docs: `http://127.0.0.1:8000/docs`

### Step 4 — Install & Start the Next.js Frontend
Open a second terminal at the repository root:
```bash
cd frontend
npm install
npm run dev
```
- Open `http://localhost:3000` in your browser.

---

## 4. Official NASA & USGS Data Attribution
- **NASA Mars Trek**: https://trek.nasa.gov/mars/
- **NASA Planetary Data System (PDS)**: https://pds.nasa.gov/
- **PDS Geosciences Node Orbital Data Explorer (ODE)**: https://ode.rsl.wustl.edu/
- **MRO HiRISE (University of Arizona LPL)**: https://hirise.lpl.arizona.edu/
- **USGS Gazetteer of Planetary Nomenclature**: https://planetarynames.wr.usgs.gov/
- **NASA NSSDCA Planetary Fact Sheet**: https://nssdc.gsfc.nasa.gov/planetary/factsheet/
- **Mars 2020 Perseverance MEDA PDS Archive**: https://pds-atmospheres.nmsu.edu/data_and_services/atmospheres_data/PERSEVERANCE/meda.html
- **MSL Curiosity RAD Dosimetry**: https://elib.dlr.de/106090/1/ME-SBA-2016-Reitz_MSL-RAD_ICES_2016.pdf

## 5. License
Released under the **MIT License** (see [`LICENSE`](./LICENSE)). NASA and USGS planetary datasets are in the public domain.
