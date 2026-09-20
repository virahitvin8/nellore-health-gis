<div align="center">

# 🛰️ Nellore City & Kovur Mandal: Urban Infrastructure & Water Flow Sentinel
### 3D Water Supply Flow Network, Overhead Storage Tanks (ELSR), Riverbed Wells & Strict AOI
#### **Nellore Municipal Corporation (NMC) & Kovur Mandal • SPSR Nellore District, Andhra Pradesh, India**

<br/>

[![Live WebGIS Demo](https://img.shields.io/badge/🌐_Explore_Live_WebGIS-Demo_Platform-0ea5e9?style=for-the-badge&logo=google-chrome&logoColor=white)](https://virahitvin8.github.io/nellore-health-gis/)
[![Download Shapefiles](https://img.shields.io/badge/📦_Download-ESRI_Shapefiles_(.ZIP)-f59e0b?style=for-the-badge&logo=esotericsoftware&logoColor=white)](https://virahitvin8.github.io/nellore-health-gis/data/shapefiles/nellore_kovur_gis_shapefiles.zip)
[![GitHub Stars](https://img.shields.io/github/stars/virahitvin8/nellore-health-gis?style=for-the-badge&color=ffd700)](https://github.com/virahitvin8/nellore-health-gis/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald?style=for-the-badge)](LICENSE)

<p align="center">
  <img src="https://img.shields.io/badge/Leaflet-1.9.4-199900?style=flat-square&logo=leaflet&logoColor=white" alt="Leaflet"/>
  <img src="https://img.shields.io/badge/ESRI_Shapefiles-.SHP_.DBF_.PRJ-005E95?style=flat-square&logo=esri&logoColor=white" alt="ESRI Shapefile"/>
  <img src="https://img.shields.io/badge/3D_Perspective-Isometric_Tilt_View-38bdf8?style=flat-square" alt="3D View"/>
  <img src="https://img.shields.io/badge/Water_Grid-Animated_Flow_Network-0284c7?style=flat-square" alt="Water Grid"/>
  <img src="https://img.shields.io/badge/Area_of_Interest-Nellore_NMC_&_Kovur_Only-orange?style=flat-square" alt="Strict AOI"/>
</p>

**A full-stack, 3D Geospatial Urban Water Supply & Infrastructure Platform. Strictly focused on Nellore City (NMC) and Kovur Mandal with an inverted boundary mask, animated water flow connectivity (Raw Source ➔ Treatment ➔ Overhead Tanks ➔ Consumer Wards), and downloadable ESRI Shapefiles.**

[Explore Live Map 🗺️](https://virahitvin8.github.io/nellore-health-gis/) • [Download Shapefiles (.ZIP) 📦](https://virahitvin8.github.io/nellore-health-gis/data/shapefiles/nellore_kovur_gis_shapefiles.zip) • [API Keys Guide 🔑](API_KEYS_GUIDE.md) • [QGIS Loader 🐍](qgis/load_nellore_health_gis.py)

</div>

---

## 📑 Table of Contents

- [Strict Area of Interest (AOI) Focus](#-strict-area-of-interest-aoi-focus)
- [3D Water Supply Distribution & Connectivity Flow](#-3d-water-supply-distribution--connectivity-flow)
- [Overhead Storage Tanks (ELSR / OHT) Network](#-overhead-storage-tanks-elsr--oht-network)
- [Raw Water Sources & Underground Riverbed Wells](#-raw-water-sources--underground-riverbed-wells)
- [ESRI Shapefiles Package Included](#-esri-shapefiles-package-included)
- [API Keys & Satellite Imagery Guide (Google & Sentinel)](#-api-keys--satellite-imagery-guide-google--sentinel)
- [Interactive Features & 3D Tilt Experience](#-interactive-features--3d-tilt-experience)
- [Two-Way QGIS Desktop Synchronization](#-two-way-qgis-desktop-synchronization)
- [Quick Start Guide](#-quick-start-guide)
- [Author Profile](#-author-profile)

---

## 🎯 Strict Area of Interest (AOI) Focus

The platform incorporates an **Inverted Boundary Polygon Mask** that veils the external surrounding areas in a darkened cinematic vignette (`fillOpacity: 0.72`) and locks map panning to `maxBounds`. 

The map display is **exclusively restricted to**:
1. **Nellore City (Nellore Municipal Corporation - NMC)**: South of the Pennar River (~150.4 sq km, 54 wards).
2. **Kovur Mandal (Gram Panchayat)**: North of the Pennar River (~112.8 sq km, 18 Gram Panchayats).

---

## 💧 3D Water Supply Distribution & Connectivity Flow

The municipal water grid is modeled with **explicit directional connectivity**:

```
[Raw River Infiltration / Canal] ──> [Central Treatment Plant] ──> [Elevated Storage Tanks (ELSR)] ──> [Ward Consumers & RO ATMs]
```

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

## 🌊 Raw Water Sources & Underground Riverbed Wells

- **Pennar South Riverbed Infiltration Wellfield (`SRC-PEN-S01`)**: Array of radial collector wells drawing from the 32m deep riverbed sand alluvial aquifer (Yield: 18,000 LPH).
- **Somasila Drinking Water Scheme West Canal Intake (`SRC-SOM-01`)**: Surface reservoir gravity intake delivering 35,000 LPH to southern booster stations.
- **Kovur North Bank Infiltration Wells (`SRC-PEN-N01`)**: Infiltration gallery yielding 12,000 LPH from 28m depth on the north bank.

---

## 📦 ESRI Shapefiles Package Included

All datasets are pre-packaged as genuine ESRI Shapefiles (`.shp`, `.shx`, `.dbf`, `.prj` in WGS84 EPSG:4326):

Download the complete package: **[data/shapefiles/nellore_kovur_gis_shapefiles.zip](https://virahitvin8.github.io/nellore-health-gis/data/shapefiles/nellore_kovur_gis_shapefiles.zip)**

Contains:
1. `nellore_city_boundary.shp` — Exact Nellore Municipal Corporation boundary
2. `kovur_mandal_boundary.shp` — Exact Kovur Mandal boundary
3. `water_distribution_pipelines.shp` — Flow pipelines with diameter, material, and discharge
4. `overhead_storage_tanks.shp` — ELSR/OHT tanks with staging heights & capacity
5. `underground_wells_sources.shp` — Infiltration galleries & borewells with yields

---

## 🔑 API Keys & Satellite Imagery Guide (Google & Sentinel)

To configure your own personal API keys for high-resolution satellite imagery or Google 3D Earth:
1. Open the in-app **"🔑 API Keys"** modal in the top header.
2. Enter your credentials (keys are stored securely in your browser's `localStorage`).
3. For step-by-step instructions on getting free keys from Google Cloud Console, Copernicus CDSE, and Mapbox, read:
   👉 **[API_KEYS_GUIDE.md](API_KEYS_GUIDE.md)**

---

## 🎮 Interactive Features & 3D Tilt Experience

- **3D Isometric Tilt Mode**: Click the **"3D Perspective"** button in the top header to pitch the map at 32 degrees with isometric depth!
- **Animated Water Pulse Flows**: Glowing cyan water pulses travel continuously along the pipelines showing the live movement of water from the riverbed wells into the elevated tanks.
- **🦅 3D Drone Flyover**: Automated aerial inspection along 7 checkpoints with live HUD telemetry tracking altitude and flow rates.
- **🚴 Commute Flow**: Animated transit tracking water and livestock courier transport across the historic Pennar Bridge.
- **1-Click Google 3D Earth**: Click any tank, well, or hospital to inspect ground perspectives directly in Google Maps.

---

## 🔄 Two-Way QGIS Desktop Synchronization

Edits made in desktop QGIS automatically synchronize with the WebGIS dashboard:
1. Open QGIS and run `qgis/load_nellore_health_gis.py` in the Python Console (`Ctrl + Alt + P`).
2. Digitize new pipelines, hand pumps, or market stalls using the pencil tool (✏️).
3. Save edits in QGIS (edits save directly to `data/*.geojson`).
4. Run `python3 src/compile_bundle.py` in your terminal.
5. Refresh your browser — your newly drawn features appear instantly in the live WebGIS dashboard!

---

## 👤 Author Profile

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
