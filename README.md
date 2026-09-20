<div align="center">

# 🛰️ Nellore City & Kovur Mandal: 3D Digital Twin & Water Sentinel
### **Dual-Engine WebGIS (Leaflet 2D + Mapbox GL 3D Terrain DEM) • Copernicus Sentinel-2 Studio • SCADA Hydraulic Simulator**
#### **Nellore Municipal Corporation (NMC) & Kovur Mandal • SPSR Nellore District, Andhra Pradesh, India**

<br/>

[![Live WebGIS Demo](https://img.shields.io/badge/🌐_Explore_Live_WebGIS-3D_Digital_Twin-0ea5e9?style=for-the-badge&logo=google-chrome&logoColor=white)](https://virahitvin8.github.io/nellore-health-gis/)
[![Download Shapefiles](https://img.shields.io/badge/📦_Download-ESRI_Shapefiles_(.ZIP)-f59e0b?style=for-the-badge&logo=esotericsoftware&logoColor=white)](https://virahitvin8.github.io/nellore-health-gis/data/shapefiles/nellore_kovur_gis_shapefiles.zip)
[![GitHub Stars](https://img.shields.io/github/stars/virahitvin8/nellore-health-gis?style=for-the-badge&color=ffd700)](https://github.com/virahitvin8/nellore-health-gis/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald?style=for-the-badge)](LICENSE)

<p align="center">
  <img src="https://img.shields.io/badge/Dual_Engine-Leaflet_2D_+_Mapbox_GL_3D-0284c7?style=flat-square&logo=mapbox&logoColor=white" alt="Dual Engine"/>
  <img src="https://img.shields.io/badge/3D_Elevation-1.5x_DEM_Terrain_Mesh-38bdf8?style=flat-square" alt="3D DEM"/>
  <img src="https://img.shields.io/badge/Copernicus_CDSE-Sentinel--2_MSI_Tile_44NNC-0ea5e9?style=flat-square&logo=european-space-agency&logoColor=white" alt="Sentinel-2"/>
  <img src="https://img.shields.io/badge/SCADA_Sandbox-Hydraulic_Plume_Simulator-10b981?style=flat-square" alt="SCADA"/>
  <img src="https://img.shields.io/badge/ESRI_Shapefiles-.SHP_.DBF_.PRJ-005E95?style=flat-square&logo=esri&logoColor=white" alt="Shapefiles"/>
  <img src="https://img.shields.io/badge/Strict_AOI-Nellore_NMC_&_Kovur_Only-orange?style=flat-square" alt="Strict AOI"/>
</p>

**A next-generation Geospatial AI & Smart Water Infrastructure Digital Twin. Featuring a Dual-Engine architecture (Leaflet 2D Tactical GIS + Mapbox GL JS 3D WebGL Digital Twin with actual 3D DEM elevation relief), live Copernicus Sentinel-2 Remote Sensing Studio, SCADA Hydraulic sandbox with cross-contamination breach plume modeling, and downloadable ESRI Shapefiles.**

[Explore Live Map 🗺️](https://virahitvin8.github.io/nellore-health-gis/) • [Download Shapefiles (.ZIP) 📦](https://virahitvin8.github.io/nellore-health-gis/data/shapefiles/nellore_kovur_gis_shapefiles.zip) • [API Credentials Guide 🔑](API_KEYS_GUIDE.md) • [QGIS Loader 🐍](qgis/load_nellore_health_gis.py)

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

## 📦 ESRI Shapefiles Package Included

Pre-packaged genuine ESRI Shapefiles (`.shp`, `.shx`, `.dbf`, `.prj` in WGS84 EPSG:4326):

Download: **[nellore_kovur_gis_shapefiles.zip](https://virahitvin8.github.io/nellore-health-gis/data/shapefiles/nellore_kovur_gis_shapefiles.zip)**

1. `nellore_city_boundary` — Exact Nellore Municipal Corporation boundary polygon
2. `kovur_mandal_boundary` — Exact Kovur Mandal boundary polygon
3. `water_distribution_pipelines` — Conduits with diameter, material, and discharge
4. `overhead_storage_tanks` — ELSR/OHT tanks with staging heights & capacity
5. `underground_wells_sources` — Infiltration galleries & borewells with yields

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
