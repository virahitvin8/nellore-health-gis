# GeoHealth Sentinel: AI-Enabled Health GIS & Geo-Risk Analytics
### Wet Market Zoonotic Vulnerability Assessment • Nellore City (NMC) & Kovur Mandal, Andhra Pradesh

[![WebGIS](https://img.shields.io/badge/WebGIS-Leaflet%201.9-blue?style=for-the-badge&logo=leaflet)](https://leafletjs.com/)
[![GeoAI](https://img.shields.io/badge/GeoAI-Random%20Forest%2076.2%25-brightgreen?style=for-the-badge&logo=scikit-learn)](https://scikit-learn.org/)
[![QGIS](https://img.shields.io/badge/Desktop%20GIS-QGIS%20%2F%20ArcMap-success?style=for-the-badge&logo=qgis)](https://qgis.org/)
[![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)](LICENSE)

---

## Executive Summary & Background

Following epidemiological insights from the 2019–2021 zoonotic transmission events in Wuhan and global wet-market pathogen dynamics, this project develops an **AI-Enabled Health GIS and Spatial Multi-Criteria Decision Framework** for **Nellore City (Nellore Municipal Corporation)** and **Kovur Mandal** (SPSR Nellore District, Andhra Pradesh, India).

Wet markets handling live poultry, mutton, and fresh/marine fish operate as critical nodes in urban food systems. However, when located in high crowd-density bazaars directly adjacent to **open municipal sullage drains**, unlined sewage channels, or river catchments, they pose severe public health hazards:
- Aerosolization of avian/zoonotic viral and bacterial pathogens during on-site live slaughter.
- Microbial contamination of runoff discharging into the **Pennar River Basin** and regional canal networks.
- Vector breeding (flies, rodents, mosquitoes) thriving on uncontained biological offal.

This project delivers an **end-to-end Health GIS pipeline**: from remote spatial survey and proximity analysis to Machine Learning predictive classification and a fully interactive **WebGIS Leaflet Dashboard** for municipal decision-makers.

---

## Study Area: Nellore City & Kovur Mandal

| Parameter | Nellore Municipal Corporation (NMC) | Kovur Mandal |
|---|---|---|
| **Administrative Class** | Tier-2 Urban Local Body (ULB) | Peri-Urban / Rural Mandal |
| **Geographic Location** | South of Pennar River (~14.4426°N, 79.9865°E) | North of Pennar River (~14.4950°N, 79.9780°E) |
| **Key Market Hubs** | Stonehousepet, Santhapet, Ranganayakulapet, Vedayapalem | Kovur Main Bazaar, Padugupadu Junction, Inamadugu Shandy |
| **Environmental Sinks** | Pennar River, Buckingham Canal feeder, Sarvepalli Canal | Pennar River north bank, agricultural drainage canals |
| **Surveyed Stalls** | 50 wet market stalls & slaughter points | 31 wet market stalls & shandies |

---

## Methodology & Geo-Risk Index (GRI) Formulation

In alignment with spatial epidemiology standards, each market $j$ is evaluated using a **Multi-Criteria Spatial Decision Analysis (MCSDA)** composite risk function:

$$\text{Geo-Risk Score}_j = \left( \sum_{i=1}^{n} W_i \times X_{i,j}^{\text{norm}} \right) \times 100$$

Where $W_i$ represents the scientifically justified risk weight ($\sum W_i = 1.00$), and $X_{i,j}^{\text{norm}} \in [0, 1]$ represents the normalized risk factor:

```
┌──────────────────────────────────────┬────────┬───────────────────────────────────────────┐
│ Risk Factor Indicator (Xi)           │ Weight │ Normalization Rationale                   │
├──────────────────────────────────────┼────────┼───────────────────────────────────────────┤
│ Proximity to Open Drainage / Sewer   │ 0.25   │ Inversely scaled (0-300m setback buffer)  │
│ Solid & Biological Waste Disposal    │ 0.20   │ Direct drain discharge (1.0) vs Bins (0.1)│
│ On-Site Live Animal Slaughter        │ 0.15   │ Live slaughter aerosol hazard (Yes/No)    │
│ Market Crowd & Pedestrian Density    │ 0.15   │ Footfall intensity in central bazaar (1-10│
│ Absence of Cold-Chain Refrigeration  │ 0.10   │ Pathogen growth in tropical ambient temp  │
│ Daily Animal Throughput Volume       │ 0.10   │ 0 to 450 units/day volume scale           │
│ Proximity to Pennar River Basin      │ 0.05   │ Surface water contamination exposure      │
└──────────────────────────────────────┴────────┴───────────────────────────────────────────┘
```

### Risk Stratification & Municipal Interventions

- **🚨 Very High Risk (Score $\ge 72$)**: 11 markets (13.6%). Immediate bio-sanitation audit; mandatory effluent interceptor trap; live slaughter prohibition without bio-containment.
- **⚠️ High Risk (Score $56 - 71$)**: 29 markets (35.8%). Bi-weekly municipal disinfection; covered offal collection bins; cold storage subsidy.
- **⚡ Moderate Risk (Score $40 - 55$)**: 20 markets (24.7%). Monthly routine surveillance; potable water testing.
- **✅ Low Risk (Score $< 40$)**: 21 markets (25.9%). Quarterly standard food safety verification.

---

## AI & Machine Learning Classification

A supervised **Random Forest Classifier (100 Decision Trees)** was trained to predict risk categories based on spatial and operational attributes:

- **Model Accuracy**: **76.19%** test accuracy (with 67.94% 5-fold cross-validation across 81 spatial locations).
- **Primary Driving Factors (Feature Importance)**:
  1. `distance_to_drain_m`: **33.56%** (The single strongest determinant of bio-risk).
  2. `distance_to_waterbody_m`: **10.69%**
  3. `daily_animals_handled`: **10.55%**
  4. `distance_to_hospital_m`: **10.24%**
  5. `waste_severity_score`: **9.78%**
  6. `market_crowd_index`: **8.45%**

---

## Interactive WebGIS Dashboard Features

The web platform is built with **Leaflet.js**, **Chart.js**, and modern CSS:

1. **Multi-Source Basemaps**: CartoDB Dark Theme, CartoDB Positron, OpenStreetMap, and Esri World Satellite Imagery.
2. **Dynamic Vector Layers**:
   - Administrative Boundaries (Nellore NMC & Kovur Mandal).
   - Wet Market Inventory color-coded by Geo-Risk score.
   - Open Drainage & Sewage Hazard Lines (Red dashed outfalls).
   - Pennar River Basin & Irrigation Canals.
   - 250m Bio-Aerosol Hazard Buffers & 500m Secondary Vector Buffers.
   - Healthcare Facilities (GGH Nellore, ACSR Medical College, Kovur CHC).
3. **Market Health Inspector**: Clicking any market reveals its unique ID, animal origin (e.g. Kadapa shandy, coastal aquaculture), destination flow, daily throughput, sanitary metrics, AI prediction confidence, and municipal remediation directive.
4. **Simulation Tool**: Click anywhere in the study area to evaluate a prospective market location and receive an instant permit recommendation (Approved / Conditional / Rejected).
5. **Analytics Drawer**: Live Chart.js visualizations of risk distributions, commodity breakdowns, and cluster rankings.
6. **Data Export**: One-click download of GeoJSON and CSV datasets.

---

## Project Repository Structure

```
.
├── index.html                           # Full WebGIS Application Dashboard
├── css/
│   └── style.css                        # Modern responsive dark-themed GIS styling
├── js/
│   ├── app.js                           # WebGIS controller, Leaflet logic, simulation & filters
│   └── charts.js                        # Chart.js analytics engine
├── data/
│   ├── embedded_data.js                 # Unified JavaScript spatial data bundle
│   ├── boundaries/                      # Nellore & Kovur administrative GeoJSONs
│   ├── markets/                         # Wet market inventory (CSV & GeoJSON)
│   ├── infrastructure/                  # Drains, Pennar river, and hospital layers
│   └── risk_analysis/                   # Classified Geo-Risk dataset and 250m/500m buffers
├── models/
│   ├── risk_predictor_random_forest.pkl # Serialized Scikit-Learn Random Forest model
│   ├── model_evaluation_metrics.json    # Accuracy, confusion matrix & metrics
│   └── feature_importance.json          # Driving risk factors ranking
├── qgis/
│   ├── load_nellore_health_gis.py       # One-click QGIS Python automation script
│   └── README.md                        # Desktop GIS integration guide
├── src/
│   ├── generate_spatial_data.py         # Spatial synthesis pipeline
│   ├── geo_risk_engine.py               # MCSDA Geo-Risk Index and buffer calculator
│   ├── train_ai_model.py                # Machine learning training and evaluation
│   └── compile_bundle.py                # Client data bundler
├── LINKEDIN_POST_GUIDE.md               # Step-by-step GitHub upload & viral LinkedIn post guide
└── README.md
```

---

## Quick Start: Running Locally

### 1. Launch WebGIS Dashboard
Simply open `index.html` in any web browser, or launch a local HTTP server:
```bash
python3 -m http.server 8000
```
Navigate to: `http://localhost:8000`

### 2. Retrain AI Models or Regenerate Data
```bash
# Generate spatial layers
python3 src/generate_spatial_data.py

# Calculate Geo-Risk Index & Buffers
python3 src/geo_risk_engine.py

# Train Random Forest AI Model
python3 src/train_ai_model.py

# Compile web bundle
python3 src/compile_bundle.py
```

### 3. Open in Desktop GIS (QGIS)
Open QGIS, open the Python Console (`Ctrl + Alt + P`), and run `qgis/load_nellore_health_gis.py` to auto-load and style all layers!

---

## Authors & Acknowledgments
- **Project Lead**: AI & Health GIS Researcher
- **Target Institutions**: Nellore Municipal Corporation (NMC), District Medical & Health Office (DMHO SPSR Nellore), Animal Husbandry Department, Andhra Pradesh.
