# QGIS & ArcMap Desktop Integration Guide
## Health GIS: Nellore City (NMC) & Kovur Mandal Wet Market Geo-Risk Analytics

This directory contains automation scripts and instructions to load, symbolize, and analyze all Health GIS spatial datasets directly within desktop GIS software (**QGIS**, **ArcMap**, and **ArcGIS Pro**).

---

### Method 1: Instant One-Click Load in QGIS (Recommended)

1. Open **QGIS** (works on QGIS 3.16 LTR through 3.34+).
2. Open the Python Console by navigating to:
   - `Plugins` menu ➔ `Python Console` (or press `Ctrl + Alt + P` on Windows / `Cmd + Option + P` on Mac).
3. Click the **Show Editor** icon (the small notepad icon in the Python Console toolbar).
4. Click **Open Script** and select `qgis/load_nellore_health_gis.py` (or copy-paste its entire contents into the editor window).
5. If running on a different computer, update the `PROJECT_DIR` variable on line 22 to your local path.
6. Click the green **Run Script** button (or press `F5`).
7. **Result:** QGIS will instantly load all 6 spatial layers, automatically apply custom symbology (Red for Very High Risk, Orange for High Risk, Yellow for Moderate, Green for Low, Red dashed lines for open drains, Blue for Pennar river), and zoom directly into the Nellore & Kovur study area!

---

### Method 2: Manual Drag-and-Drop in QGIS

If you prefer not to use Python:
1. Open QGIS and create a new project.
2. In the Browser Panel on the left, navigate to this project's `data/` directory.
3. Drag and drop the following GeoJSON files into your QGIS Layers panel:
   - `data/boundaries/nellore_kovur_aoi.geojson`
   - `data/infrastructure/pennar_river_waterbodies.geojson`
   - `data/infrastructure/open_drainage_sewage_network.geojson`
   - `data/infrastructure/healthcare_facilities.geojson`
   - `data/risk_analysis/market_risk_buffers_250m.geojson`
   - `data/risk_analysis/market_geo_risk_classified.geojson`
4. **Style the Wet Markets layer**:
   - Right-click `market_geo_risk_classified` ➔ select `Properties...`
   - Go to `Symbology`. Change top dropdown from `Single Symbol` to `Categorized`.
   - Set **Value** to `risk_level`.
   - Click `Classify` at the bottom.
   - Set colors:
     - `Very High Risk`: Red (`#d90429`), Size 4.0
     - `High Risk`: Orange (`#f77f00`), Size 3.5
     - `Moderate Risk`: Yellow (`#ffd166`), Size 3.0
     - `Low Risk`: Green (`#06d6a0`), Size 2.5
   - Click `OK`.

---

### Method 3: Opening in ArcMap / ArcGIS Pro

1. Launch **ArcMap** or **ArcGIS Pro**.
2. To import GeoJSON into ESRI:
   - In the Search panel, search for the **JSON To Features** Geoprocessing tool.
   - **Input JSON or GeoJSON File**: Browse to `data/risk_analysis/market_geo_risk_classified.geojson`.
   - **Output Feature Class**: Choose your local File Geodatabase or Shapefile output path.
   - Click **Run**.
   - Repeat for `open_drainage_sewage_network.geojson` and `nellore_kovur_aoi.geojson`.
3. In ArcGIS Pro / ArcMap:
   - Right-click the imported market layer ➔ select `Symbology`.
   - Select **Unique Values** and set the Field to `risk_level`.
   - Match the color scheme (Red, Orange, Yellow, Green).
   - Right-click ➔ `Labeling` ➔ Label with `shop_name`.
