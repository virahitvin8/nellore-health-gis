<div align="center">

# 🛰️ Nellore City & Kovur Mandal: 3D Digital Twin & Water Sentinel
### **Dual-Engine WebGIS (Leaflet 2D + Mapbox GL 3D Terrain DEM) • Copernicus Sentinel-2 Studio • SCADA Hydraulic Simulator**
#### **Nellore Municipal Corporation (NMC) & Kovur Mandal • SPSR Nellore District, Andhra Pradesh, India**

<br/>

[![Live WebGIS Demo](https://img.shields.io/badge/🌐_Explore_Live_WebGIS-3D_Digital_Twin-0ea5e9?style=for-the-badge&logo=google-chrome&logoColor=white)](https://virahitvin8.github.io/nellore-health-gis/)
[![Download Shapefiles](https://img.shields.io/badge/📦_Download-ESRI_Shapefiles_(.ZIP)-f59e0b?style=for-the-badge&logo=esotericsoftware&logoColor=white)](https://virahitvin8.github.io/nellore-health-gis/data/shapefiles/nellore_kovur_gis_shapefiles.zip)
[![Starred Repos](https://img.shields.io/badge/⭐_227_Starred_Repos-Startup_Launchpad-ffd700?style=for-the-badge&logo=github&logoColor=black)](STARRED_REPOSITORIES.md)
[![GitHub Stars](https://img.shields.io/github/stars/virahitvin8/nellore-health-gis?style=for-the-badge&color=ffd700)](https://github.com/virahitvin8/nellore-health-gis/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald?style=for-the-badge)](LICENSE)

<p align="center">
  <img src="https://img.shields.io/badge/Dual_Engine-Leaflet_2D_+_Mapbox_GL_3D-0284c7?style=flat-square&logo=mapbox&logoColor=white" alt="Dual Engine"/>
  <img src="https://img.shields.io/badge/3D_Elevation-1.5x_DEM_Terrain_Mesh-38bdf8?style=flat-square" alt="3D DEM"/>
  <img src="https://img.shields.io/badge/Copernicus_CDSE-Sentinel--2_MSI_Tile_44NNC-0ea5e9?style=flat-square&logo=european-space-agency&logoColor=white" alt="Sentinel-2"/>
  <img src="https://img.shields.io/badge/SCADA_Sandbox-Hydraulic_Plume_Simulator-10b981?style=flat-square" alt="SCADA"/>
  <img src="https://img.shields.io/badge/ESRI_Shapefiles-.SHP_.DBF_.PRJ-005E95?style=flat-square&logo=esri&logoColor=white" alt="Shapefiles"/>
  <img src="https://img.shields.io/badge/Starred_Ecosystem-227_Repos_Embedded-ffd700?style=flat-square" alt="227 Starred Repos"/>
  <img src="https://img.shields.io/badge/Strict_AOI-Nellore_NMC_&_Kovur_Only-orange?style=flat-square" alt="Strict AOI"/>
</p>

**A next-generation Geospatial AI & Smart Water Infrastructure Digital Twin. Featuring a Dual-Engine architecture (Leaflet 2D Tactical GIS + Mapbox GL JS 3D WebGL Digital Twin with actual 3D DEM elevation relief), live Copernicus Sentinel-2 Remote Sensing Studio, SCADA Hydraulic sandbox with cross-contamination breach plume modeling, downloadable ESRI Shapefiles, and an embedded 227-repo Open Source Startup Launchpad.**

[Explore Live Map 🗺️](https://virahitvin8.github.io/nellore-health-gis/) • [227 Starred Repos ⭐](STARRED_REPOSITORIES.md) • [Download Shapefiles (.ZIP) 📦](https://virahitvin8.github.io/nellore-health-gis/data/shapefiles/nellore_kovur_gis_shapefiles.zip) • [API Credentials Guide 🔑](API_KEYS_GUIDE.md) • [QGIS Loader 🐍](qgis/load_nellore_health_gis.py)

</div>

---

## 📑 Table of Contents

- [🌟 Breakthrough Innovations](#-breakthrough-innovations)
- [🌐 Dual-Engine 3D Digital Twin Architecture](#-dual-engine-3d-digital-twin-architecture)
- [🛰️ Copernicus Sentinel-2 Remote Sensing Studio](#-copernicus-sentinel-2-remote-sensing-studio)
- [⚡ SCADA Hydraulic Sandbox & Contamination Crisis Simulator](#-scada-hydraulic-sandbox--contamination-crisis-simulator)
- [🎯 Strict Area of Interest (AOI) Focus](#-strict-area-of-interest-aoi-focus)
- [💧 Water Supply Distribution Flow Network](#-water-supply-distribution-flow-network)
- [🏰 Overhead Storage Tanks (ELSR / OHT) Network](#-overhead-storage-tanks-elsr--oht-network)
- [📦 ESRI Shapefiles Package Included](#-esri-shapefiles-package-included)
- [👤 Author & Institutional Affiliation](#-author--institutional-affiliation)

---

## 🌟 Breakthrough Innovations

1. **Dual-Engine Seamless Switcher**: Toggle with 1-click between high-speed **2D Tactical GIS (Leaflet)** and photorealistic **3D Digital Twin (Mapbox GL JS WebGL)**.
2. **True 3D Terrain Elevation Mesh**: Powered by `mapbox-terrain-dem-v1` with 1.5x vertical exaggeration, rendering the real 3D topography of the Pennar River valley and delta.
3. **Copernicus Sentinel-2 Remote Sensing Studio**: Authenticated via ESA Copernicus Data Space Ecosystem (CDSE) OAuth with Client ID `sh-3320f912...` and SHIATS Lab account `25msrsgis001@shiats.edu.in`.
4. **12-Band Spectral Reflectance Signature Curves**: Interactive Chart.js graph plotting bottom-of-atmosphere (BOA) surface reflectance across 12 Sentinel-2 spectral channels for water, crops, urban concrete, and river alluvium.
5. **SCADA Hydraulic Flow Sandbox**: Simulate Peak Morning Demand (72.0 MLD) vs Night Refill (35.0 MLD) with Hazen-Williams head loss and live line pressures.
6. **Contamination Crisis Simulator (What-If Analysis)**: Trigger a simulated sullage sewer infiltration plume, watch downstream uPVC pipes flash into emergency lockdown, and generate automated boil-water advisories with alternative safe RO water plants.
7. **Live Municipal IoT Telemetry Stream**: Glassmorphism live ticker streaming turbidity, residual chlorine, trunk pipeline pressure, and drainage outfall depths.
8. **Official GADM 4.1 Administrative Boundary Extraction & 3D Clip Curtain**: Picked and clipped exact official GADM Level 3 boundaries for Nellore (`IND.2.7.14_1`) and Kovur (`IND.2.7.4_1`), extruded as a 75-meter 3D holographic boundary curtain enclosing the 3D terrain!

---

## 🌐 Dual-Engine 3D Digital Twin Architecture

```
                                  ┌────────────────────────────────────────┐
                                  │   Nellore & Kovur WebGIS Platform     │
                                  └──────────────────┬─────────────────────┘
                                                     │
                         ┌───────────────────────────┴───────────────────────────┐
                         ▼                                                       ▼
        ┌──────────────────────────────────┐                    ┌──────────────────────────────────┐
        │     2D Tactical GIS Engine       │                    │    3D Digital Twin WebGL Engine  │
        │           (Leaflet)              │                    │          (Mapbox GL JS)          │
        ├──────────────────────────────────┤                    ├──────────────────────────────────┤
        │ • Mapbox Retina Satellite Tiles  │                    │ • Real 3D Terrain DEM (1.5x)     │
        │ • Animated Flow Pulses on Pipes  │                    │ • 3D Building Extrusions (City)  │
        │ • Strict Inverted AOI Mask       │                    │ • Dynamic Sky Atmosphere & Fog   │
        │ • 3D Perspective Isometric Pitch │                    │ • 360° Cinematic Orbital Tour    │
        │ • Drone Flyover with HUD         │                    │ • 3D Glowing Neon Pipe Conduits  │
        └──────────────────────────────────┘                    └──────────────────────────────────┘
```

---

## 🛰️ Copernicus Sentinel-2 Remote Sensing Studio

Directly connected to the **European Space Agency (ESA) Copernicus Data Space Ecosystem**:
* **Granule Tile**: `T44NNC` (EPSG:32644 - SPSR Nellore District, AP)
* **Constellation**: Sentinel-2A & Sentinel-2B Multi-Spectral Instrument (MSI)
* **Revisit Frequency**: 5 Days (10m Spatial Resolution)

### False-Color Band Composites Available
* **Natural True Color (B04 - B03 - B02)**: Real natural surface inspection.
* **Color Infrared (CIR: B08 - B04 - B03)**: Highlights chlorophyll crop vigor in Kovur paddy fields in vivid red/magenta.
* **Normalized Difference Water Index (NDWI: $(B03 - B08)/(B03 + B08)$)**: Zero-haze delineation of Pennar River and irrigation canals.
* **Short-Wave Infrared (SWIR: B12 - B8A - B04)**: Measures soil moisture and discriminates riverbed alluvium.

---

## ⚡ SCADA Hydraulic Sandbox & Contamination Crisis Simulator

### Flow Network Hierarchy & Discharge
```
┌─────────────┬────────────────────────────────────────────────────────┬───────────┬─────────┬──────────┐
│ Conduit ID  │ Pipeline Description                                   │ Diameter  │ Material│ Discharge│
├─────────────┼────────────────────────────────────────────────────────┼───────────┼─────────┼──────────┤
│ PL-RAW-01   │ Pennar River Infiltration Wells ➔ NMC Central Headworks│ 600 mm    │ DI K9   │ 18.0 MLD │
│ PL-FEED-01  │ NMC Central Headworks ➔ Stonehousepet ELSR Tank        │ 450 mm    │ DI      │ 6.5 MLD  │
│ PL-FEED-02  │ NMC Central Headworks ➔ Santhapet Central ELSR Tank    │ 500 mm    │ MS      │ 8.0 MLD  │
│ PL-FEED-03  │ NMC Central Headworks ➔ Ranganayakulapet ELSR Branch   │ 350 mm    │ DI      │ 3.5 MLD  │
│ PL-RAW-02   │ Somasila Canal Gravity Intake ➔ Vedayapalem Booster    │ 700 mm    │ PSC     │ 15.0 MLD │
│ PL-FEED-04  │ Vedayapalem Booster ➔ Vedayapalem High-Level ELSR Tank │ 450 mm    │ HDPE    │ 7.0 MLD  │
│ PL-FEED-05  │ Vedayapalem Booster ➔ Dargamitta Water Tower           │ 400 mm    │ DI      │ 5.0 MLD  │
│ PL-DIST-01  │ Stonehousepet ELSR ➔ Ward Distribution & RO ATMs       │ 300 mm    │ HDPE    │ 1.8 MLD  │
│ PL-KVR-01   │ Kovur North Infiltration Wells ➔ Kovur Treatment Plant │ 350 mm    │ DI      │ 5.5 MLD  │
│ PL-KVR-02   │ Kovur Treatment Headworks ➔ Kovur Main Bazaar ELSR Tank│ 300 mm    │ DI      │ 3.0 MLD  │
│ PL-KVR-03   │ Kovur Treatment Headworks ➔ Padugupadu Railway OHT     │ 200 mm    │ HDPE    │ 1.8 MLD  │
│ PL-KVR-04   │ Kovur Treatment Headworks ➔ Inamadugu Rural OHT Feeder │ 160 mm    │ HDPE    │ 0.9 MLD  │
└─────────────┴────────────────────────────────────────────────────────┴───────────┴─────────┴──────────┘
```

---

## 🏰 Overhead Storage Tanks (ELSR / OHT) Network

Total Municipal Storage: **12.1 Million Liters per Day (MLD)** across 8 strategic elevated service reservoirs:

```
┌──────────────┬──────────────────────────────────────────┬──────────┬───────────┬────────────┐
│ Tank ID      │ Overhead Reservoir Name                  │ Capacity │ Height    │ Population │
├──────────────┼──────────────────────────────────────────┼──────────┼───────────┼────────────┤
│ ELSR-NMC-01  │ Stonehousepet Elevated Reservoir (ELSR)  │ 1.8 MLD  │ 18 meters │ 42,000     │
│ ELSR-NMC-02  │ Santhapet Central Municipal Water Tower  │ 2.2 MLD  │ 20 meters │ 55,000     │
│ ELSR-NMC-03  │ Ranganayakulapet Riverside Reservoir     │ 1.2 MLD  │ 16 meters │ 28,000     │
│ ELSR-NMC-04  │ Vedayapalem - Ramalingapuram High Tank   │ 2.5 MLD  │ 22 meters │ 62,000     │
│ ELSR-NMC-05  │ Dargamitta Municipal Water Tower         │ 1.5 MLD  │ 18 meters │ 36,000     │
│ ELSR-KVR-01  │ Kovur Main Bazaar Gram Panchayat Tank    │ 1.4 MLD  │ 18 meters │ 32,000     │
│ ELSR-KVR-02  │ Padugupadu Railway Colony Overhead Tank  │ 0.9 MLD  │ 16 meters │ 19,000     │
│ ELSR-KVR-03  │ Inamadugu Rural Gram Panchayat Reservoir │ 0.6 MLD  │ 15 meters │ 14,000     │
└──────────────┴──────────────────────────────────────────┴──────────┴───────────┴────────────┘
```

---

## 🌾 AP Rythu Bharosa & Satellite Crop Health Studio (Farmer Perspective)

Engineered specifically from a **farmer's point of view** in the Nellore & Kovur agricultural delta (*Rice Bowl of Andhra Pradesh*):

```
┌─────────────────────────┬──────────────┬───────────────┬────────────────────────────────────────────────────────┐
│ Agro-Zonal Sector       │ Mean NDVI    │ NDRE Red-Edge │ Phenology & Crop Advisory                              │
├─────────────────────────┼──────────────┼───────────────┼────────────────────────────────────────────────────────┤
│ Kovur North Paddy Delta │ +0.74 (High) │ +0.52 (SPAD44)│ Nellore Masuri (BPT 5204) • Panicle Initiation stage.   │
│                         │              │               │ Apply MOP @ 25 kg/acre. Maintain 3-5cm standing water. │
│ Kovur Sugarcane Belt    │ +0.66 (Mod)  │ +0.46 (Good)  │ Sugarcane (Co 86032) & Robusta Banana. Earthing up.    │
│ Pottepalem Delta Clay   │ +0.68 (High) │ +0.48 (SPAD42)│ Wetland Paddy. Zinc Sulphate 0.2% foliar spray alert.  │
│ Vedayapalem Peri-Urban  │ +0.38 (Mod)  │ +0.28 (Urban) │ Hybrid Napier Fodder & Greens. NSKE 5% organic spray.  │
└─────────────────────────┴──────────────┴───────────────┴────────────────────────────────────────────────────────┘
```

- **Multi-Spectral Early Nitrogen Stress Detection**: Utilizes Sentinel-2 MSI **Red-Edge Band 5 (705nm)** to calculate **NDRE** $(B08 - B05)/(B08 + B05)$, detecting nitrogen deficiency and chlorophyll decline up to **10 days before visible leaf yellowing**.
- **Pest Early Warning (Rice Blast & BPH)**: Sensor & microclimate fusion tracks Kovur night humidity (>85%) and temperature (~24°C) to alert farmers of *Magnaporthe oryzae* (Rice Blast) spore windows with proactive spray advisories (*Tricyclazole 75% WP @ 0.6g/L*).
- **Rythu Bharosa Kendram (RBK) Directory**: Direct telephone dialer and spatial pins for all village-level RBKs (*Kovur Gram, Padugupadu, Inamadugu, Pottepalem*) with Village Agriculture Assistant (VAA) details.
- **Live Mandi Minimum Support Price (MSP) Ticker**: Verified procurement rates for Nellore Masuri Paddy (Grade A: ₹2,320/quintal) and Sugarcane (₹3,150/ton).

---

## 🆘 Citizen Services, Need Seekers & 24/7 Public Health Helpdesk

Built for immediate, frictionless access by citizens and emergency seekers:

- **1-Click Emergency Dialers**: Instant direct calls to **108 (Free Emergency Ambulance)**, **104 (Health Info & Doctor on Call)**, and **1916 (NMC Water Supply Grievance)**.
- **Certified RO Mineral Water Finder**: Real-time potability ratings, TDS ppm levels (165 - 190 ppm), and locations for all municipal NTR Sujala RO Mineral Water ATMs.
- **Emergency Healthcare Directory**: ACSR Govt General Hospital (750 Beds, 40 ICU, free Aarogyasri care) and Kovur Community Health Center (50 Beds).
- **Online Water & Drain Grievance Redressal**: Interactive citizen complaint form that dispatches authentic tracking tickets (`NMC-GRV-2026-XXXX`) with 4-hour SLA directly to NMC Ward Sanitary Inspectors.

---

## 💬 Andhra GIS Sahayak — ChatGPT-Style Conversational AI Copilot

Integrated directly into the WebGIS interface with a floating, ChatGPT-style glassmorphism window:

- **Multi-Domain Intelligence**: Understands questions in plain English and Telugu transliteration regarding crop vigor, blast pest spray schedules, safe drinking water TDS, hospital beds, and market sanitation.
- **Automated Spatial Actions**: The AI copilot does not just answer with text — it **actively drives the map**, auto-zooming to requested farms or tanks, toggling layers, highlighting high-risk drain buffers, and opening detail cards!
- **Quick-Prompt Suggestion Pills**: 1-click prompts for *"Kovur Crop Vigor"*, *"Clean RO Water"*, *"Emergency 108"*, *"Market Drain Hazard"*, *"Rice Blast Advisory"*, and *"Mandi MSP Rates"*.

---

## 🏛️ Designed for Government of Andhra Pradesh & Govt of India Showcasing

- **Nellore Municipal Corporation (NMC)**: Real-time municipal water grid telemetry, trunk line pressure balancing, and citizen grievance redressal.
- **AP Department of Agriculture & Cooperation**: District-wide crop health monitoring, E-Crop verification, and RBK service delivery.
- **AP Disaster Management Authority (APDMA)**: Hydraulic crisis simulations, open sullage sewage flood breach modeling, and emergency healthcare capacity tracking.

---

## 📦 ESRI Shapefiles Package Included

Pre-packaged genuine ESRI Shapefiles (`.shp`, `.shx`, `.dbf`, `.prj` in WGS84 EPSG:4326):

Download: **[nellore_kovur_gis_shapefiles.zip](https://virahitvin8.github.io/nellore-health-gis/data/shapefiles/nellore_kovur_gis_shapefiles.zip)**

1. `nellore_city_boundary` — Exact Nellore Municipal Corporation boundary polygon
2. `kovur_mandal_boundary` — Exact Kovur Mandal boundary polygon
3. `water_distribution_pipelines` — Conduits with diameter, material, and discharge
4. `overhead_storage_tanks` — ELSR/OHT tanks with staging heights & capacity
5. `underground_wells_sources` — Infiltration galleries & borewells with yields
6. `rythu_bharosa_kendrams` — RBK agricultural service centers & farmer kiosks

---

## ⭐ 227 Starred Repositories & Startup Launchpad

This platform directly integrates all **227 curated GitHub starred repositories** of `@virahitvin8`, categorized and ranked by star count with startup applications:

- 🤖 **AI Agents, Autonomous Swarms & Skills (84 Repos)**: `AutoGPT` (187k★), `superpowers` (289k★), `agency-agents` (153k★), `anthropics/skills` (177k★), `mcp-flow`.
- ⚡ **Vibe Coding, Rapid App Builders & Prototyping (47 Repos)**: `Dokploy` (37k★), `Dyad` (21k★), `Spec-Kit` (138k★), `bolt.diy`.
- 🛰️ **Geospatial Intelligence, Remote Sensing & Agriculture GIS (29 Repos)**: `RuView` (94k★), `WorldMonitor` (87k★), `Gods-Eye-View` (39k★), `opengeos/GeoLibre` (7.5k★), `@virahitvin8`'s own `crafty-gis`, `farmhealth`, `Krishi-Drishti`, `khetmap`.
- 💰 **Startup From Scratch, Monetization & Automated Trading (18 Repos)**: `MoneyPrinterTurbo` (124k★), `Vibe-Trading` (33k★), `FinceptTerminal` (31k★), `AutoHedge` (6.1k★).
- 🔍 **Data Intelligence, OSINT, Curated APIs & Infrastructure (49 Repos)**: `public-apis` (481k★), `the-book-of-secret-knowledge` (244k★).

👉 **Browse the full interactive launcher in the WebGIS top navigation bar (`Starred (227)`) or read the complete ranked breakdown in [STARRED_REPOSITORIES.md](STARRED_REPOSITORIES.md).**

---

## 👤 Author & Institutional Affiliation

<div align="center">

### **Neelam.Akshit VinaY (@virahitvin8)**
*Remote Sensing & GIS Scholar • Agriculture X Technology Enthusiast*  
**Sam Higginbottom University of Agriculture, Technology and Sciences (SHIATS)**  
*Department of Remote Sensing & GIS*

[![GitHub](https://img.shields.io/badge/GitHub-virahitvin8-181717?style=for-the-badge&logo=github)](https://github.com/virahitvin8)
[![Portfolio](https://img.shields.io/badge/Portfolio-virahitvin8.github.io-0284c7?style=for-the-badge&logo=google-chrome&logoColor=white)](https://virahitvin8.github.io/)
[![Email](https://img.shields.io/badge/Email-akshitvinay4636@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:akshitvinay4636@gmail.com)
[![Academic](https://img.shields.io/badge/SHIATS_GIS_Lab-25msrsgis001@shiats.edu.in-7c3aed?style=for-the-badge&logo=google-scholar&logoColor=white)](mailto:25msrsgis001@shiats.edu.in)

</div>

---

<div align="center">
  <sub>Built with ❤️ for Public Health, Smart City Governance, and Sustainable Urban Planning.</sub>
</div>
