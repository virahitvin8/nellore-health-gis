<div align="center">

# 🛰️ GeoHealth Sentinel: AI-Enabled Health GIS & Urban Infrastructure Platform
### Wet Market Zoonotic Vulnerability, Drinking Water Contamination & Urban Healthcare Access
#### **Nellore Municipal Corporation (NMC) & Kovur Mandal • SPSR Nellore District, Andhra Pradesh, India**

<br/>

[![Live WebGIS Demo](https://img.shields.io/badge/🌐_Explore_Live_WebGIS-Demo_Platform-0ea5e9?style=for-the-badge&logo=google-chrome&logoColor=white)](https://virahitvin8.github.io/nellore-health-gis/)
[![GitHub Stars](https://img.shields.io/github/stars/virahitvin8/nellore-health-gis?style=for-the-badge&color=ffd700)](https://github.com/virahitvin8/nellore-health-gis/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/virahitvin8/nellore-health-gis?style=for-the-badge&color=60a5fa)](https://github.com/virahitvin8/nellore-health-gis/network/members)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald?style=for-the-badge)](LICENSE)

<p align="center">
  <img src="https://img.shields.io/badge/Leaflet-1.9.4-199900?style=flat-square&logo=leaflet&logoColor=white" alt="Leaflet"/>
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Scikit--Learn-Random_Forest_76.2%25-F7931E?style=flat-square&logo=scikit-learn&logoColor=white" alt="Scikit-Learn"/>
  <img src="https://img.shields.io/badge/QGIS-3.16_to_3.34+-589632?style=flat-square&logo=qgis&logoColor=white" alt="QGIS"/>
  <img src="https://img.shields.io/badge/Chart.js-4.4+-FF6384?style=flat-square&logo=chartdotjs&logoColor=white" alt="Chart.js"/>
  <img src="https://img.shields.io/badge/GeoJSON-WGS84_EPSG:4326-blueviolet?style=flat-square" alt="GeoJSON"/>
  <img src="https://img.shields.io/badge/Govt_of_Andhra_Pradesh-Nellore_NMC-orange?style=flat-square" alt="AP Govt"/>
</p>

**A full-stack, end-to-end Geospatial AI & Epidemiological Platform integrating Multi-Criteria Spatial Decision Analysis (MCSDA), Machine Learning predictive modeling, 3D Drone & Bike Commute simulations, and automated two-way desktop QGIS synchronization.**

[Explore Live Map 🗺️](https://virahitvin8.github.io/nellore-health-gis/) • [QGIS Python Script 🐍](qgis/load_nellore_health_gis.py) • [Report Bug 🐛](https://github.com/virahitvin8/nellore-health-gis/issues) • [Request Feature 💡](https://github.com/virahitvin8/nellore-health-gis/issues)

</div>

---

## 📑 Table of Contents

- [Executive Summary & Background](#-executive-summary--background)
- [Study Area Overview](#-study-area-overview)
- [System Architecture](#-system-architecture)
- [Spatial Infrastructure Mapped](#-spatial-infrastructure-mapped)
- [Multi-Criteria Geo-Risk Index (GRI) Formulation](#-multi-criteria-geo-risk-index-gri-formulation)
- [AI & Machine Learning Predictive Modeling](#-ai--machine-learning-predictive-modeling)
- [Interactive WebGIS Dashboard Features](#-interactive-webgis-dashboard-features)
  - [🦅 3D Drone Flyover Mode](#-3d-drone-flyover-mode)
  - [🚴 Motorcycle / Bicycle Supply Route Commute Mode](#-motorcycle--bicycle-supply-route-commute-mode)
  - [🚶 Ground Perspective & Google Maps 3D Integration](#-ground-perspective--google-maps-3d-integration)
  - [🧪 Simulated Allotment Assessment Tool](#-simulated-allotment-assessment-tool)
- [Two-Way QGIS Desktop Synchronization](#-two-way-qgis-desktop-synchronization)
- [Municipal Policy Directives (NMC & Kovur)](#-municipal-policy-directives-nmc--kovur)
- [Project Directory Structure](#-project-directory-structure)
- [Quick Start Guide](#-quick-start-guide)
- [Author & Acknowledgments](#-author--acknowledgments)

---

## 🔬 Executive Summary & Background

Following global epidemiological lessons from the 2019–2021 zoonotic transmission events in Wuhan and urban municipal challenges in developing countries, this project develops an **AI-Enabled Health GIS and Spatial Risk Assessment Platform** for **Nellore City (Nellore Municipal Corporation - NMC)** and **Kovur Mandal** (SPSR Nellore District, Andhra Pradesh, India).

In rapidly expanding urban settlements, meat and seafood wet markets operate as vital cultural and nutritional food supply hubs. However, when high-throughput live animal slaughter occurs in dense street bazaars directly adjacent to **open municipal sullage drains**, unlined wastewater channels, and shallow underground **drinking water pipelines**, critical disease transmission pathways emerge:

1. **Zoonotic Aerosolization**: Pathogen dispersion during uncontained on-site slaughter in crowded pedestrian bazaars.
2. **Drinking Water Cross-Contamination**: Subsurface sewage ingress into aging water supply pipes and public hand pumps during low water pressure hours.
3. **Food Supply Chain Cross-Contamination**: Mechanical transmission (flies, rodents, surface runoff) carrying fecal and biological pathogens from butcher stalls into neighboring fresh vegetable stalls and Rythu Bazaars.

This platform bridges remote sensing, spatial multi-criteria analytics, and machine learning to deliver actionable decision support for public health epidemiologists and municipal administrators.

---

## 📍 Study Area Overview

<div align="center">

| Metric | Nellore Municipal Corporation (NMC) | Kovur Mandal (Panchayati Raj) |
| :--- | :--- | :--- |
| **Administrative Class** | Tier-2 Urban Local Body (ULB) | Peri-Urban / Rural Mandal |
| **Geographic Location** | South of Pennar River (~14.4426°N, 79.9865°E) | North of Pennar River (~14.4950°N, 79.9780°E) |
| **Area & Population** | 150.4 sq km • ~600,000 residents | 112.8 sq km • ~125,000 residents |
| **Key Commercial Hubs** | Stonehousepet, Santhapet, Vedayapalem, Trunk Road | Kovur Main Bazaar, Padugupadu Junction, Inamadugu |
| **Major Water Sinks** | Pennar River, Buckingham Canal, Sarvepalli Canal | Pennar River North Bank, Irrigation Outfalls |

</div>

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   GeoHealth Sentinel Platform                                    │
└────────────────────────────────────────────────┬─────────────────────────────────────────────────┘
                                                 │
    ┌───────────────────────────┬────────────────┴────────────────┬───────────────────────────┐
    ▼                           ▼                                 ▼                           ▼
[Spatial Data Engine]    [MCSDA Geo-Risk]                  [Machine Learning]          [Interactive WebGIS]
• 81 Wet Markets         • Multi-Criteria Formula          • Random Forest (100)       • Leaflet 1.9 + Chart.js
• 8 Veg Rythu Bazaars    • 7 Weighted Indicators           • 76.19% Test Accuracy      • 🦅 3D Drone Flyover
• Tagged Water Pipes     • 250m Bio-Aerosol Buffers        • Drain distance #1         • 🚴 Bike Supply Commute
• 18 RO / Well Points    • 500m Secondary Exposure           factor (33.4%)            • 🚶 Street Walk & 3D Earth
• 15 Hospitals           • Municipal Directives            • Confidence scoring        • 🧪 Permit Simulator
```

---

## 🗺️ Spatial Infrastructure Mapped

```
┌──────────────────────────────────────┬─────────┬────────────────────────────────────────────────────────┐
│ Spatial Infrastructure Layer         │ Features│ Key Attributes & Real-World Context                    │
├──────────────────────────────────────┼─────────┼────────────────────────────────────────────────────────┤
│ 🥩 Wet Market Inventory (Meat/Fish)  │ 81      │ Poultry, Mutton, Fish, Mixed stalls with supply routes │
│ 🥦 Vegetable Markets & Rythu Bazaars │ 8       │ AP Govt Agricultural Marketing hubs, footfall & stalls │
│ 💧 Tagged Drinking Water Pipelines   │ 9 lines │ NMC-WTR-PL-01 to 05 (DI/HDPE), Kovur GP Water Mains    │
│ 🚰 Water Points (RO Plants & Pumps)  │ 18      │ NTR Sujala RO ATMs, Borewells, Public Hand Pumps       │
│ 🚨 Open Sewage & Sullage Drains      │ 7 lines │ Stonehousepet Outfall, Central Drain, Kovur Sludge     │
│ 🌊 Pennar River Basin & Canals       │ 3       │ Pennar River, Sarvepalli Canal, Buckingham Feeder      │
│ 🏥 Healthcare Network (Govt + Pvt)   │ 15      │ GGH Nellore, ACSR Medical College, Narayana, Apollo    │
│ ⭕ Bio-Hazard Exposure Buffers       │ 40      │ 250m Bio-Aerosol & 500m Secondary Transmission Rings   │
│ 🏛️ Administrative Boundaries        │ 2       │ Nellore Municipal Corporation (NMC) & Kovur Mandal     │
└──────────────────────────────────────┴─────────┴────────────────────────────────────────────────────────┘
```

---

## ⚖️ Multi-Criteria Geo-Risk Index (GRI) Formulation

Each market $j$ is evaluated using a scientifically grounded **Multi-Criteria Spatial Decision Analysis (MCSDA)** composite risk function:

$$\text{Geo-Risk Score}_j = \left( \sum_{i=1}^{n} W_i \times X_{i,j}^{\text{norm}} \right) \times 100$$

Where $W_i$ represents the indicator weight ($\sum W_i = 1.00$), and $X_{i,j}^{\text{norm}} \in [0, 1]$ represents the normalized factor value:

```
┌──────────────────────────────────────┬────────┬───────────────────────────────────────────┐
│ Risk Factor Indicator (Xi)           │ Weight │ Scientific & Epidemiological Rationale    │
├──────────────────────────────────────┼────────┼───────────────────────────────────────────┤
│ Proximity to Open Drainage / Sewer   │ 0.25   │ Inversely scaled (0 to 300m setback)      │
│ Waste Disposal Practice              │ 0.20   │ Direct drain discharge (1.0) vs Bins (0.1)│
│ On-Site Live Animal Slaughter        │ 0.15   │ Pathogen bio-aerosolization hazard (Y/N)  │
│ Market Crowd & Pedestrian Footfall   │ 0.15   │ Human-animal contact intensity (1 to 10)  │
│ Absence of Cold-Chain Refrigeration  │ 0.10   │ Microbial growth in ambient tropical temp │
│ Daily Animal Throughput Volume       │ 0.10   │ 0 to 450 units/day volume scale           │
│ Distance to Pennar River Basin       │ 0.05   │ Surface water infiltration vulnerability  │
└──────────────────────────────────────┴────────┴───────────────────────────────────────────┘
```

### Risk Stratification & Distribution
```
🚨 Very High Risk (Score ≥ 72) : [████████░░░░░░░░░░░░░░░░░░░░░░] 11 markets (13.6%)
⚠️ High Risk      (Score 56-71): [████████████████████░░░░░░░░░░] 29 markets (35.8%)
⚡ Moderate Risk  (Score 40-55): [██████████████░░░░░░░░░░░░░░░░] 20 markets (24.7%)
✅ Low Risk       (Score < 40) : [███████████████░░░░░░░░░░░░░░░] 21 markets (25.9%)
```

---

## 🤖 AI & Machine Learning Predictive Modeling

A supervised **Random Forest Classifier (100 Decision Trees)** was trained to predict Geo-Risk categories based on spatial and operational indicators:

- **Model Accuracy**: **76.19%** test accuracy (with **69.19%** 5-fold cross-validation across spatial coordinates).
- **Driving Feature Importance Ranking**:
  ```
  distance_to_drain_m     [███████████████████████████████████] 33.41%
  distance_to_waterbody_m [████████████]                        11.81%
  daily_animals_handled   [███████████]                         10.97%
  waste_severity_score    [██████████]                           9.75%
  distance_to_hospital_m  [██████████]                           9.71%
  market_crowd_index      [████████]                             8.46%
  slaughter_flag          [██████]                               6.51%
  refrig_flag             [█████]                                5.38%
  category_code           [████]                                 4.00%
  ```

---

## 🎮 Interactive WebGIS Dashboard Features

### 🦅 3D Drone Flyover Mode
Automated aerial inspection flight across 7 critical checkpoints: *Vedayapalem South $\rightarrow$ Santhapet Commercial Hub $\rightarrow$ Stonehousepet Wholesale Hub $\rightarrow$ Pennar River Basin $\rightarrow$ Padugupadu Rail Junction $\rightarrow$ Kovur Main Bazaar $\rightarrow$ Inamadugu Shandy*.
- Live **Heads-Up Display (HUD)** tracks altitude (70m–210m AGL), speed (30–65 km/h), and real-time bio-hazard alerts.

### 🚴 Motorcycle / Bicycle Supply Route Commute Mode
Simulates a live livestock courier transporting poultry/meat from rural breeding units across the historic Pennar Bridge into urban markets.
- Real-time speedometer (32 km/h), odometer, and an active **bio-exposure alarm** that turns flashing RED when passing within 30 meters of open sullage lines.

### 🚶 Ground Perspective & Google Maps 3D Integration
Click any wet market, vegetable market, pipeline, or hospital on the map and click **"Street Walk View"** or **"Google Maps 3D"** to instantly launch the exact coordinates in Google Maps Street View / 3D Earth view!

### 🧪 Simulated Allotment Assessment Tool
Click anywhere on the map to evaluate a new prospective wet market location—the engine dynamically calculates distance to the nearest drain and waterbody, runs the MCSDA formula, and outputs an instant municipal permit recommendation (*Approved / Conditional / Rejected*).

---

## 🔄 Two-Way QGIS Desktop Synchronization

Edits made in desktop QGIS automatically synchronize with the WebGIS dashboard:
1. Open QGIS and run `qgis/load_nellore_health_gis.py` in the Python Console (`Ctrl + Alt + P`).
2. Digitize new pipelines, hand pumps, or market stalls using the pencil tool (✏️).
3. Save edits in QGIS (edits save directly to `data/*.geojson`).
4. Run `python3 src/compile_bundle.py` in your terminal.
5. Refresh your browser — your newly drawn features appear instantly in the live WebGIS dashboard!

---

## 🏛️ Municipal Policy Directives (NMC & Kovur)

Based on spatial analytics and AI feature importances, the following municipal interventions are prioritized:

1. **Stonehousepet Sullage Outfall**: Prioritize immediate construction of a reinforced concrete masonry cover over the 450m open sullage drain directly abutting wholesale fish stalls.
2. **Drinking Water Pipeline Replacement**: Replace aging uPVC pipeline joints along Ranganayakulapet and Kovur Main Bazaar where pipes run directly submerged under open sullage gutters.
3. **Hand Pump Bio-Remediation**: Decommission or install deep chlorination filters on 4 public hand pumps identified within 12 meters of open sewers in Stonehousepet and Santhapet slum clusters.
4. **Rythu Bazaar Buffer Separation**: Maintain physical 50m separation between open poultry stalls and fresh vegetable vendors at Stonehousepet and Kovur markets to prevent cross-contamination.

---

## 📁 Project Directory Structure

```
.
├── index.html                           # Full WebGIS Application Dashboard
├── css/
│   └── style.css                        # Modern dark-themed GIS UI & HUD telemetry styles
├── js/
│   ├── app.js                           # WebGIS controller, Drone, Bike & Street view modes
│   └── charts.js                        # Chart.js analytics engine
├── data/
│   ├── embedded_data.js                 # Self-contained spatial data bundle (CORS-safe)
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
├── push_to_github.sh                    # Automated deployment script
├── LINKEDIN_POST_GUIDE.md               # GitHub upload guide & viral LinkedIn post copy
└── README.md
```

---

## 🚀 Quick Start Guide

### Option 1: Live Interactive Demo
Visit the live platform hosted on GitHub Pages:
👉 **[https://virahitvin8.github.io/nellore-health-gis/](https://virahitvin8.github.io/nellore-health-gis/)**

### Option 2: Run Locally
```bash
# Clone the repository
git clone https://github.com/virahitvin8/nellore-health-gis.git
cd nellore-health-gis

# Launch a local HTTP server
python3 -m http.server 8000
```
Open `http://localhost:8000` in your web browser.

---

## 👤 Author & Acknowledgments

<div align="center">

### **Neelam.Akshit VinaY (@virahitvin8)**
*Remote Sensing & GIS Scholar • Agriculture X Technology Enthusiast*

[![GitHub](https://img.shields.io/badge/GitHub-virahitvin8-181717?style=for-the-badge&logo=github)](https://github.com/virahitvin8)
[![Portfolio](https://img.shields.io/badge/Portfolio-virahitvin8.github.io-0284c7?style=for-the-badge&logo=google-chrome&logoColor=white)](https://virahitvin8.github.io/)
[![Email](https://img.shields.io/badge/Email-akshitvinay4636@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:akshitvinay4636@gmail.com)

</div>

---

<div align="center">
  <sub>Built with ❤️ for Public Health, Smart City Governance, and Sustainable Urban Planning.</sub>
</div>
