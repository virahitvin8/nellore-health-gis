# 🔑 API Credentials & Spatial Intelligence Guide
## Dual-Engine 3D Digital Twin, Sentinel-2 Studio & Google 3D Earth
### **Nellore City (NMC) & Kovur Mandal Smart Infrastructure Platform**

This guide documents the API integrations and credentials powering the **GeoHealth Sentinel & 3D Digital Twin** platform.

---

### 🛰️ Pre-Configured & Authenticated Spatial Services

| Spatial Engine | Credential / Identifier | Role in Platform | Status |
| :--- | :--- | :--- | :--- |
| **Mapbox GL JS 3D Engine** | Public Access Token (Configured & Verified) | Real 3D Terrain DEM (`mapbox-terrain-dem-v1` at 1.5x exaggeration), 3D building extrusions, sky atmosphere & retina satellite tiles | <span style="color:#10b981;">**ACTIVE & VERIFIED ✅**</span> |
| **ESA Copernicus CDSE** | Client ID: `sh-3320f912-93af-440f-ad9f-794d96326b5b` | 10m Sentinel-2 MSI multispectral imagery (Tile `T44NNC`), false-color composites (CIR, NDWI, SWIR), and 12-band spectral reflectance | <span style="color:#10b981;">**OAUTH AUTHENTICATED ✅**</span> |
| **Google Cloud & Maps** | Project ID: `braided-analyst-500314-c5`<br>Key: `AIzaSyCtrj5JuGv2Um8_lq2trgqbDBjNI0I1oBE` | Ground-level Google Street View inspection, 3D Photorealistic Earth views for overhead tanks and hospitals | <span style="color:#10b981;">**CONFIGURED ✅**</span> |
| **Research Institution** | `25msrsgis001@shiats.edu.in` | Sam Higginbottom University of Agriculture, Technology and Sciences (SHIATS) Remote Sensing & GIS Lab | <span style="color:#38bdf8;">**LAB CERTIFIED 🎓**</span> |

---

### 1. Mapbox GL JS 3D Digital Twin Engine

**Features enabled by your Mapbox Token**:
1. **WebGL 3D Digital Twin**: Switch effortlessly between the 2D Tactical Leaflet map and the Mapbox GL 3D Digital Twin view with one click.
2. **Dynamic 3D Terrain Mesh (`mapbox-dem`)**: Renders actual 3D elevation relief of the Pennar River delta, coastal sand dunes, and Kovur agricultural topography.
3. **Atmospheric Lighting & Fog**: Horizon haze, deep sky atmosphere, and celestial stars rendered in real-time.
4. **3D Building Extrusions**: Realistic building heights for Nellore City core (Stonehousepet, Trunk Road, Vedayapalem).
5. **360° Cinematic Orbital Flyaround**: Rotates the 3D camera smoothly around key municipal infrastructure.

---

### 2. ESA Copernicus Sentinel-2 Remote Sensing Studio

**Features enabled by your CDSE Client Credentials (`sh-3320...`)**:
1. **Granule Telemetry**:
   - Satellite: ESA Sentinel-2A / Sentinel-2B Multi-Spectral Instrument (MSI)
   - Granule Tile ID: `T44NNC` (EPSG:32644 - SPSR Nellore District)
   - Orbit: Relative Orbit `R062`
   - Revisit Cycle: Every 5 days
2. **Multispectral False-Color Band Composites**:
   - **Natural True Color (RGB: B04, B03, B02)**: Visual surface features.
   - **Color Infrared (CIR: B08, B04, B03)**: Highlights crop vigor in Kovur paddy fields in vivid red/magenta.
   - **Normalized Difference Water Index (NDWI: $(B03 - B08)/(B03 + B08)$)**: High-contrast water extraction of Pennar River and Kanigiri irrigation canals.
   - **Short-Wave Infrared (SWIR: B12, B8A, B04)**: Measures soil water content and discriminates riverbed moisture.
3. **Interactive 12-Band Spectral Reflectance Profile Chart**:
   - Compares bottom-of-atmosphere (BOA) spectral reflectance curves from B01 (443nm Coastal Aerosol) to B12 (2190nm SWIR) for Water, Paddy Crop, Urban Concrete, and Riverbed Sand.

---

### 3. Google Cloud & Maps 3D Earth Integration

**Features enabled by your Google Key (`AIzaSy...`) & Project (`braided-analyst-500314-c5`)**:
1. **1-Click Google 3D Earth Navigation**: Inspect any of the 8 Elevated Storage Reservoirs (ELSR), Pennar riverbed infiltration wells, or hospitals in Google Earth 3D.
2. **Ground-Level Street View Inspection**: Direct modal launch into 360° ground panoramas around Stonehousepet, Trunk Road, and Kovur Bazaar.

---

### 4. Updating Credentials

To update credentials at any time:
1. Click the **"Credentials"** button in the WebGIS top navigation bar.
2. Edit your Mapbox token, Copernicus Client ID, or Google key.
3. Click **"Update Credentials"** — changes are instantly saved in your browser's `localStorage` and applied across all map engines without code changes!
