# QGIS & ArcMap Desktop Integration & Two-Way Editing Guide
## Health GIS: Nellore City (NMC) & Kovur Mandal

This guide explains how to:
1. **Load and visualize** all Health GIS datasets in desktop QGIS and ArcMap.
2. **Draw and digitize** new water pipelines, hand pumps, or wet markets directly in QGIS.
3. **Interlink and sync** your QGIS edits seamlessly with the live WebGIS dashboard!

---

## Part 1: Instant One-Click Load in QGIS

1. Open **QGIS** (versions 3.16 LTR through 3.34+).
2. Open the Python Console:
   - Go to `Plugins` ➔ `Python Console` (or press `Ctrl + Alt + P`).
3. Click the **Show Editor** icon (the small notepad icon in the Python Console).
4. Click **Open Script** and select `qgis/load_nellore_health_gis.py`.
5. Click the green **Run Script** button (or press `F5`).
6. **Result**: QGIS automatically loads all 9 vector layers:
   - Administrative Boundaries (Nellore NMC & Kovur GP)
   - Pennar River Basin & Irrigation Canals
   - Open Drainage & Sullage Lines (Red dashed)
   - Drinking Water Pipelines (Cyan lines)
   - RO Mineral Water Plants & Public Hand Pumps
   - Vegetable Markets & Rythu Bazaars (Green markers)
   - Hospitals (Govt & Private)
   - 250m Bio-Aerosol Hazard Buffers
   - Wet Markets (Risk-Categorized in Red, Orange, Yellow, Green)

---

## Part 2: How to Draw / Digitize in QGIS & Interlink with WebGIS

### What Can You Draw?
- **New Drinking Water Pipelines**: e.g., drawing a new branch line in Kovur Ward 4 or Vedayapalem.
- **New RO Water Plants or Hand Pumps**: marking drinking water points in slum clusters or villages.
- **New Open Drains or Wet Markets**: adding new butcher stalls or unlined drainage ditches.

---

### Step-by-Step Two-Way Sync Workflow:

```
[1. Draw in QGIS] ──> [2. Save Edits] ──> [3. Run 1-sec Compiler] ──> [4. Live WebGIS Updates!]
```

#### Step 1: Select the Layer in QGIS to Edit
- In QGIS **Layers Panel**, click on the layer you want to add to (for example: `Drinking Water Pipelines` or `RO Water Plants & Public Hand Pumps`).

#### Step 2: Enable Toggle Editing
- Click the yellow **Pencil Icon** (✏️) on the top toolbar (or press `Ctrl + E`).
- You will see red cross marks on the existing features, indicating the layer is now editable.

#### Step 3: Draw the Feature
- **If drawing a Pipeline or Open Drain (Line)**:
  - Click **Add Line Feature** icon (or press `Ctrl + .`).
  - Click points along the street where the pipe or drain runs.
  - Right-click when finished.
  - A form will pop up asking for attributes:
    - `pipe_id`: e.g. `NMC-WTR-PL-09` or `KVR-PNC-WTR-07`
    - `name`: e.g. `Kovur Ward 4 Extension Main`
    - `diameter_mm`: e.g. `160`
    - `material`: e.g. `HDPE`
    - `cross_contamination_risk`: e.g. `Moderate`
  - Click **OK**.
- **If drawing a Water Point, Hand Pump, or Shop (Point)**:
  - Click **Add Point Feature** icon.
  - Click on the map where the borewell/shop is located.
  - Fill in the popup attributes (e.g. `name: Stonehousepet RO Unit 2`, `type: Mineral Water RO Plant`, `tds_ppm: 90`, `drain_dist_m: 20`).
  - Click **OK**.

#### Step 4: Save Layer Edits in QGIS
- Click the **Save Layer Edits** icon (💾 floppy disk next to the pencil).
- Click the **Toggle Editing** pencil icon again to turn off edit mode.
- Because QGIS edits the underlying GeoJSON file directly in `data/`, your data is already saved!

#### Step 5: Sync with the WebGIS Dashboard (1 Second)
Open your terminal in this project folder and run:
```bash
python3 src/compile_bundle.py
```
*(Or if you modified wet markets, run `python3 src/geo_risk_engine.py` to re-score risk!)*

#### Step 6: Refresh your Browser!
- Open or refresh `index.html` in your web browser.
- **Your newly drawn lines and points from QGIS will instantly appear on the interactive WebGIS map with popups, filters, and analytics intact!**

#### Step 7: Push Updates to Live GitHub Pages
```bash
git add .
git commit -m "feat: added new digitized water pipeline from QGIS"
git push
```
Within 60 seconds, your live GitHub Pages website updates for the whole world!
