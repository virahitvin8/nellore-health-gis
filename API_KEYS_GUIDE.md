# Complete API Keys & Credentials Guide for Remote Sensing & GIS
## Google Maps 3D, Google Earth Engine, Sentinel Hub & Mapbox

This step-by-step guide explains how to get **free API keys** and credentials to connect high-resolution satellite imagery, 3D terrain, and Earth observation data directly into your **GeoHealth Sentinel** project.

---

### 1. Google Maps JavaScript API (for Google 3D Earth & Satellite Basemap)

**Where to get it**: [Google Cloud Console (console.cloud.google.com)](https://console.cloud.google.com/)

**Step-by-step process**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/) and log in with your Google account.
2. Click the top project dropdown ➔ click **"New Project"** ➔ Name it: `nellore-gis-platform` ➔ Click **Create**.
3. In the search bar at the top, type **"Maps JavaScript API"** ➔ Click on it ➔ Click the blue **"Enable"** button.
4. On the left menu, click **"Credentials"** ➔ click **"+ Create Credentials"** at the top ➔ select **"API Key"**.
5. Your API key will be displayed (e.g., `AIzaSyD...`).
6. **(Recommended Security)**: Under "API Restrictions", select "Restrict key" ➔ choose "Maps JavaScript API". Under "Website restrictions", add:
   - `https://virahitvin8.github.io/*`
   - `http://localhost:*`
7. Copy this API key and paste it into the **API Key Config modal** in your WebGIS dashboard!

---

### 2. Google Earth Engine (GEE) API & Service Account

**Where to get it**: [Google Earth Engine Signup (earthengine.google.com)](https://earthengine.google.com/signup/)

**Step-by-step process**:
1. Go to [earthengine.google.com/signup](https://earthengine.google.com/signup).
2. Choose **"Register a Non-Commercial or Academic project"** (free access for researchers and students).
3. Connect it to your Google Cloud project (`nellore-gis-platform`).
4. Once approved, you can use the Google Earth Engine Python API:
   ```bash
   pip3 install earthengine-api
   earthengine authenticate
   ```
5. You can compute NDVI, Land Surface Temperature (LST), and Flood Extent across the Pennar River basin directly using GEE cloud compute!

---

### 3. Sentinel Hub / Copernicus Data Space Ecosystem (CDSE)

**Where to get it**: [Copernicus Data Space Ecosystem (dataspace.copernicus.eu)](https://dataspace.copernicus.eu/)

**Step-by-step process**:
1. Open [dataspace.copernicus.eu](https://dataspace.copernicus.eu/) and click **"Register"** in the top-right corner.
2. Fill in your name and email to create a free European Space Agency (ESA) Copernicus account.
3. Once logged in, go to the **Copernicus Browser / API Dashboard**:
   - Go to [shapps.dataspace.copernicus.eu](https://shapps.dataspace.copernicus.eu/) ➔ Settings ➔ **OAuth Clients**.
   - Click **"Create Client"** ➔ Name it `nellore-health-sentinel`.
   - Copy the **Client ID** and **Client Secret**.
4. With this key, you can pull live 10-meter optical Sentinel-2 imagery (Bands B02, B03, B04, B08) over Nellore and Kovur without cloud interference!

---

### 4. Mapbox GL API Token (for 3D Terrain & Digital Elevation Models)

**Where to get it**: [Mapbox Signup (mapbox.com)](https://account.mapbox.com/)

**Step-by-step process**:
1. Go to [mapbox.com](https://www.mapbox.com/) and create a free account (includes 50,000 free map loads every month).
2. Go to your **Account Dashboard** (`account.mapbox.com`).
3. Under **"Default public token"**, copy your token (starts with `pk.eyJ...`).
4. Paste this token into your WebGIS Settings modal to unlock 3D building extrusions and realistic digital elevation relief!

---

### Summary Checklist

| API Service | Key Type | Best Use in Nellore Health GIS | Free Tier Limits |
| :--- | :--- | :--- | :--- |
| **Google Maps JS API** | `AIzaSy...` | 3D Street View & satellite imagery | $200 free credit monthly (~28,000 loads) |
| **Copernicus CDSE / Sentinel** | Client ID / Secret | Live 10m Sentinel-2 multispectral riverbed monitoring | Completely Free (ESA public satellite data) |
| **Google Earth Engine** | Cloud Project ID | Cloud spatial computation & water indices (MNDWI) | Free for academic/research use |
| **Mapbox GL** | `pk.eyJ...` | 3D terrain mesh & 3D building heights | 50,000 loads/month free |
