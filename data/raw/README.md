# Raw NASA & USGS Datasets (`data/raw/`)

To keep this GitHub repository lightweight and fast to clone, multi-gigabyte raw NASA PDS IMG/GeoTIFF rasters (such as the 2 GB MOLA 128-pixel/degree global DEM `megt90n000eb.img`) are not committed directly to Git.

## How to Download Optional Raw Datasets Locally
1. **USGS Mars Nomenclature Shapefile / CSV**:
   Run `python scripts/import_usgs_nomenclature.py --fetch-live` to download the latest Mars nomenclature feed from `https://planetarynames.wr.usgs.gov/`, or run without flags to seed from the bundled verified dataset in `data/processed/usgs_mars_nomenclature.json`.
2. **NASA Mars Trek WMTS Map Tiles (MOLA / Viking MDIM 2.1 / THEMIS / CTX)**:
   Run `python scripts/download_nasa_tiles.py --layer Mars_MGS_MOLA_Colorhillshade_merge_global_463m --zoom 0 1 2` to cache official NASA Mars Trek WMTS tiles locally for offline use.
3. **NASA PDS Archives**:
   - MOLA MEGDR: https://pds-geosciences.wustl.edu/missions/mgs/megdr.html
   - Mars 2020 MEDA Bundle (`urn:nasa:pds:mars2020_meda::6.0`): https://pds-atmospheres.nmsu.edu/data_and_services/atmospheres_data/PERSEVERANCE/meda.html
   - HiRISE DTMs: https://www.uahirise.org/hiwish/maps/dtms.jsp
