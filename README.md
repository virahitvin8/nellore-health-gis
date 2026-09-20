# GeoHealth Sentinel: AI-Enabled Health GIS & Urban Infrastructure Sentinel
### Wet Markets, Drinking Water Pipelines, RO Plants & Hospitals • Nellore City (NMC) & Kovur Mandal, Andhra Pradesh

[![WebGIS](https://img.shields.io/badge/WebGIS-Leaflet%201.9-blue?style=for-the-badge&logo=leaflet)](https://leafletjs.com/)
[![GeoAI](https://img.shields.io/badge/GeoAI-Random%20Forest%2076.2%25-brightgreen?style=for-the-badge&logo=scikit-learn)](https://scikit-learn.org/)
[![QGIS](https://img.shields.io/badge/Desktop%20GIS-QGIS%20%2F%20ArcMap-success?style=for-the-badge&logo=qgis)](https://qgis.org/)
[![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)](LICENSE)

---

## Executive Summary & Background

Following epidemiological insights from the 2019–2021 zoonotic transmission events in Wuhan and global wet-market pathogen dynamics, this project develops an **AI-Enabled Health GIS and Urban Infrastructure Multi-Criteria Decision Framework** for **Nellore City (Nellore Municipal Corporation - NMC)** and **Kovur Mandal** (SPSR Nellore District, Andhra Pradesh, India).

In fast-growing urban Indian centers, wet markets handling live poultry, mutton, and fresh/marine fish operate in close proximity to **open municipal sullage drains**, unlined sewage channels, and underground **drinking water pipelines**. This creates critical public health hazard vectors:
1. **Zoonotic Bio-Aerosolization**: Airborne transmission during uncontained on-site live slaughter in crowded bazaars.
2. **Drinking Water Cross-Contamination**: Subsurface sewage ingress into aging water supply pipes and shallow public hand pumps during low-pressure hours.
3. **Food Supply Chain Contamination**: Flies and surface runoff transmitting pathogens from meat/fish butcher stalls into adjacent fresh vegetable stalls and Rythu Bazaars.

This project delivers a complete **end-to-end Health GIS platform**: from spatial synthesis and Multi-Criteria Decision Analysis (MCSDA) to Machine Learning risk prediction, 3D Drone & Bike commute simulations, and an interactive **WebGIS Leaflet Dashboard** with two-way QGIS synchronization.

---

## Spatial Infrastructure Mapped (Nellore NMC & Kovur GP)

```
┌──────────────────────────────────────┬─────────┬────────────────────────────────────────────────────────┐
│ Infrastructure Category              │ Count   │ Description & Key Examples                             │
├──────────────────────────────────────┼─────────┼────────────────────────────────────────────────────────┤
│ Wet Markets (Poultry, Mutton, Fish)  │ 81      │ Stonehousepet, Santhapet, Kovur Bazaar, Inamadugu      │
│ Vegetable Markets & Rythu Bazaars    │ 8       │ Stonehousepet Rythu Bazaar, Santhapet Produce Market   │
│ Tagged Drinking Water Pipelines      │ 9 lines │ NMC-WTR-PL-01 to 05 (DI/HDPE), Kovur GP Water Mains    │
│ Drinking Water Points                │ 18      │ Community Mineral Water RO Plants, Borewells, Pumps    │
│ Open Sullage Drains & Outfalls       │ 7 lines │ Stonehousepet Outfall, Central Drain, Kovur Gutter     │
│ Surface Water Bodies & River         │ 3       │ Pennar River Basin, Sarvepalli & Buckingham Canals     │
│ Healthcare Facilities (Govt + Pvt)   │ 15      │ GGH Nellore, ACSR Medical College, Narayana, Apollo    │
│ Hazard Exposure Buffers              │ 40      │ 250m Bio-Aerosol Buffers & 500m Secondary Zones        │
└──────────────────────────────────────┴─────────┴────────────────────────────────────────────────────────┘
```

---

## Multi-Criteria Geo-Risk Index (GRI) Formulation

Each market $j$ is evaluated using a **Multi-Criteria Spatial Decision Analysis (MCSDA)** composite risk function:

$$\text{Geo-Risk Score}_j = \left( \sum_{i=1}^{n} W_i \times X_{i,j}^{\text{norm}} \right) \times 100$$

- **Open Drain Proximity ($W = 0.25$)**: Inversely scaled (0–300m buffer).
- **Waste Disposal Practice ($W = 0.20$)**: Direct open drain discharge (1.0) vs. closed bins (0.1).
- **On-Site Live Slaughter ($W = 0.15$)**: Biological effluent and aerosol hazard.
- **Market Crowd & Density ($W = 0.15$)**: Human-animal contact intensity in central bazaars.
- **Absence of Cold-Chain ($W = 0.10$)**: Bacterial multiplication in tropical ambient temperatures.
- **Daily Animal Volume ($W = 0.10$)**: 0 to 450 units/day throughput scale.
- **Pennar River Proximity ($W = 0.05$)**: Riverbed infiltration and water resource contamination.

### Risk Classification Distribution
- **🚨 Very High Risk ($\ge 72$)**: 11 markets (13.6%) — Immediate bio-sanitation audit; mandatory effluent traps.
- **⚠️ High Risk ($56 - 71$)**: 29 markets (35.8%) — Bi-weekly disinfection; covered bins; cold storage subsidy.
- **⚡ Moderate Risk ($40 - 55$)**: 20 markets (24.7%) — Routine monthly surveillance.
- **✅ Low Risk ($< 40$)**: 21 markets (25.9%) — Standard food safety audit.

---

## AI & Machine Learning Predictive Modeling

A supervised **Random Forest Classifier (100 Decision Trees)** was trained to predict risk categories based on spatial and operational indicators:
- **Test Accuracy**: **76.19%** (Cross-validation mean: 69.19%).
- **Primary Driving Factors (Feature Importance)**:
  1. `distance_to_drain_m`: **33.41%** (The single strongest determinant of bio-risk).
  2. `distance_to_waterbody_m`: **11.81%**
  3. `daily_animals_handled`: **10.97%**
  4. `waste_severity_score`: **9.75%**
  5. `distance_to_hospital_m`: **9.71%**
  6. `market_crowd_index`: **8.46%**

---

## Interactive WebGIS Platform Features

The web application is built with **Leaflet 1.9**, **Chart.js**, and modern CSS:

1. **Multi-Basemap Switching**: CartoDB Dark Theme, Esri World Satellite Imagery, CartoDB Light, and OpenStreetMap.
2. **🦅 3D Drone Flyover Mode**:
   - Automated aerial inspection flight across 7 critical checkpoints from Vedayapalem South to Kovur and Inamadugu.
   - Live Heads-Up Display (HUD) displaying altitude (AGL), flight speed, and bio-hazard alerts.
3. **🚴 Motorcycle / Bicycle Commute Simulation**:
   - Simulates a livestock courier moving from rural breeding hatcheries across the historic Pennar Bridge into Stonehousepet Market.
   - Real-time speedometer, odometer, and hazard alert system (triggers RED when within 30m of open drainage lines).
4. **🚶 Street Walk View with Google Maps 3D Integration**:
   - Click any market, pipeline, or hospital to inspect street-level ground perspectives and launch Google Maps Street View directly.
5. **Interactive Permit Simulator**:
   - Click anywhere in Nellore or Kovur to evaluate a new prospective market location—calculates distance to open drains and waterbodies, runs the formula, and outputs an instant permit decision (*Approved / Conditional / Rejected*).
6. **Live Analytics Drawer (Chart.js)**:
   - Interactive charts of risk distribution, commodity breakdown, cluster rankings, and AI feature importance.

---

## Two-Way QGIS Desktop Synchronization

Edits made in desktop QGIS automatically synchronize with the WebGIS dashboard:
1. Open QGIS and run `qgis/load_nellore_health_gis.py` in the Python Console (`Ctrl + Alt + P`).
2. Digitize new pipelines, hand pumps, or market stalls using the pencil tool.
3. Save edits in QGIS (saves directly to `data/*.geojson`).
4. Run `python3 src/compile_bundle.py` in the terminal.
5. Refresh your browser — your new drawn features appear instantly in the live WebGIS dashboard!

---

## Repository Structure

```
.
├── index.html                           # Full WebGIS Application Dashboard
├── css/
│   └── style.css                        # Modern dark-themed GIS UI & HUD telemetry styles
├── js/
│   ├── app.js                           # WebGIS controller, Drone, Bike & Street view modes
│   └── charts.js                        # Chart.js analytics engine
├── data/
│   ├── embedded_data.js                 # Self-contained spatial data bundle
│   ├── boundaries/                      # Nellore NMC & Kovur Mandal boundary GeoJSONs
│   ├── markets/                         # Wet markets & Vegetable Rythu Bazaars GeoJSONs
│   ├── infrastructure/                  # Water pipelines, RO plants, drains, river, hospitals
│   └── risk_analysis/                   # Classified Geo-Risk dataset and 250m/500m buffers
├── models/
│   ├── risk_predictor_random_forest.pkl # Trained Random Forest ML model
│   ├── model_evaluation_metrics.json    # Accuracy, confusion matrix & metrics
│   └── feature_importance.json          # Driving risk factors ranking
├── qgis/
│   ├── load_nellore_health_gis.py       # One-click QGIS automation script
│   └── README.md                        # Desktop GIS digitizing & sync guide
├── src/
│   ├── generate_spatial_data.py         # Spatial synthesis pipeline
│   ├── geo_risk_engine.py               # MCSDA Geo-Risk Index calculator
│   ├── train_ai_model.py                # Machine learning training & evaluation
│   └── compile_bundle.py                # Client data bundler
├── LINKEDIN_POST_GUIDE.md               # GitHub upload guide & viral LinkedIn post copy
└── README.md
```

---

## Authors & Acknowledgments
- **Project Lead**: AI & Health GIS Researcher
- **Institutions**: Nellore Municipal Corporation (NMC), Kovur Gram Panchayat, Department of Health & Family Welfare, Government of Andhra Pradesh.
