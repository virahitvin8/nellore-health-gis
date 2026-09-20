/**
 * Main WebGIS Application Controller
 * Health GIS & Urban Infrastructure Sentinel: Nellore City & Kovur Mandal
 * Features: Wet Markets, Water Pipelines, RO Plants/Hand Pumps, Vegetable Markets, Hospitals,
 * Drone Flyover, Motorcycle Delivery Commute, and Street View Integration.
 */

let map;
let allData = null;

// Layer Groups
let layerBoundaries;
let layerRiver;
let layerDrainage;
let layerHospitals;
let layerMarkets;
let layerVegMarkets;
let layerPipelines;
let layerWaterPoints;
let layerBuffers250;
let layerBuffers500;

// Simulation & Interactive Animation States
let simMarker = null;
let isSimulationMode = false;

// Drone Flyover State
let isDroneMode = false;
let droneStep = 0;
let droneTimer = null;
let droneMarker = null;

// Bike Commute State
let isBikeMode = false;
let bikeTimer = null;
let bikeMarker = null;
let bikeProgress = 0;

// Drone Flight Checkpoints
const DRONE_CHECKPOINTS = [
  { name: "Vedayapalem South Corridor (NMC)", lat: 14.4175, lon: 79.9675, zoom: 15, alt: "160m AGL", speed: "55 km/h", hazard: "MODERATE", note: "Suburban livestock stalls & southern drainage outfall channel." },
  { name: "Santhapet Central Commercial Bazaar", lat: 14.4395, lon: 79.9805, zoom: 16, alt: "110m AGL", speed: "42 km/h", hazard: "HIGH", note: "Dense bazaar congestion; water pipeline crossing under open drain." },
  { name: "Stonehousepet Fish & Mutton Wholesale Hub", lat: 14.4495, lon: 79.9910, zoom: 17, alt: "70m AGL", speed: "30 km/h", hazard: "CRITICAL", note: "Heavy live slaughter directly over open masonry outfall sewer." },
  { name: "Pennar River Infiltration Gallery & Wells", lat: 14.4635, lon: 79.9750, zoom: 15, alt: "210m AGL", speed: "65 km/h", hazard: "WATCH", note: "Primary municipal drinking water source for Nellore city." },
  { name: "Padugupadu Railway & Bridge Entry (Kovur)", lat: 14.4755, lon: 79.9840, zoom: 16, alt: "120m AGL", speed: "48 km/h", hazard: "HIGH", note: "Inter-mandal gateway; railway slum open sullage channels." },
  { name: "Kovur Main Bazaar & Gram Panchayat Market", lat: 14.4945, lon: 79.9785, zoom: 17, alt: "80m AGL", speed: "35 km/h", hazard: "CRITICAL", note: "Open roadside sludge gutter submerged directly beneath market." },
  { name: "Inamadugu Rural Livestock & Produce Shandy", lat: 14.4910, lon: 80.0035, zoom: 15, alt: "140m AGL", speed: "50 km/h", hazard: "NORMAL", note: "Multi-village rural poultry shandy & agricultural wellfield." }
];

// Bike Supply Commute Route (North bank farm to South bank Stonehousepet)
const BIKE_ROUTE = [
  [14.4945, 79.9785], // Kovur Bazaar
  [14.4880, 79.9810],
  [14.4810, 79.9830],
  [14.4755, 79.9840], // Padugupadu
  [14.4700, 79.9845], // Pennar Bridge North End
  [14.4650, 79.9848], // Crossing Pennar River
  [14.4600, 79.9850], // Pennar Bridge South End
  [14.4550, 79.9870], // Ranganayakulapet
  [14.4510, 79.9895], // Stonehousepet Entrance
  [14.4495, 79.9910]  // Stonehousepet Fish Market Hub
];

document.addEventListener("DOMContentLoaded", () => {
  initDataAndMap();
  setupEventListeners();
});

function initDataAndMap() {
  if (typeof HEALTH_GIS_DATA !== "undefined") {
    allData = HEALTH_GIS_DATA;
    buildWebGIS();
  } else {
    setTimeout(() => {
      if (typeof HEALTH_GIS_DATA !== "undefined") {
        allData = HEALTH_GIS_DATA;
        buildWebGIS();
      } else {
        alert("Unable to load spatial data. Please ensure data/embedded_data.js is present.");
      }
    }, 500);
  }
}

function buildWebGIS() {
  // 1. Initialize Map
  map = L.map("map", {
    center: [14.455, 79.985],
    zoom: 13,
    minZoom: 11,
    maxZoom: 18,
    zoomControl: false
  });

  L.control.zoom({ position: "topright" }).addTo(map);
  L.control.scale({ position: "bottomleft", metric: true, imperial: false }).addTo(map);

  // 2. Base Tile Layers
  const darkMatter = L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
    attribution: '&copy; CARTO &copy; OSM',
    subdomains: "abcd",
    maxZoom: 19
  }).addTo(map);

  const positron = L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
    attribution: '&copy; CARTO &copy; OSM',
    subdomains: "abcd",
    maxZoom: 19
  });

  const osmStandard = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 19
  });

  const esriSatellite = L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", {
    attribution: 'Tiles &copy; Esri &mdash; DigitalGlobe, GeoEye, Earthstar Geographics',
    maxZoom: 18
  });

  const baseMaps = {
    "CartoDB Dark Theme": darkMatter,
    "Esri Satellite Imagery": esriSatellite,
    "CartoDB Light Theme": positron,
    "OpenStreetMap Standard": osmStandard
  };

  L.control.layers(baseMaps, null, { position: "topright" }).addTo(map);

  // 3. Initialize Feature Layers
  initAllVectorLayers();

  // 4. Update Header KPIs
  updateHeaderKPIs();

  // 5. Initialize Charts
  if (typeof initAnalyticsCharts === "function") {
    initAnalyticsCharts(allData);
  }
}

function initAllVectorLayers() {
  // A. Boundaries
  layerBoundaries = L.geoJSON(allData.aoi, {
    style: (feature) => {
      const isNellore = feature.properties.name.includes("Nellore");
      return {
        color: isNellore ? "#38bdf8" : "#a855f7",
        weight: 2,
        dashArray: "6, 6",
        fillColor: isNellore ? "#0284c7" : "#9333ea",
        fillOpacity: 0.08
      };
    },
    onEachFeature: (feature, layer) => {
      const p = feature.properties;
      layer.bindTooltip(`<strong>${p.name}</strong><br>${p.type} • Pop: ${p.population_est.toLocaleString()}`, { sticky: true });
    }
  }).addTo(map);

  // B. River Basin & Canals
  layerRiver = L.geoJSON(allData.waterbodies, {
    style: (feature) => {
      const isRiver = feature.geometry.type === "Polygon";
      return {
        color: "#0284c7",
        weight: isRiver ? 1.5 : 3.5,
        fillColor: "#0ea5e9",
        fillOpacity: 0.35,
        dashArray: isRiver ? "" : "4, 4"
      };
    },
    onEachFeature: (feature, layer) => {
      const p = feature.properties;
      layer.bindTooltip(`<strong>${p.name}</strong><br>${p.category} (${p.status})`, { sticky: true });
    }
  }).addTo(map);

  // C. Open Drainage Network
  layerDrainage = L.geoJSON(allData.drainage, {
    style: {
      color: "#ef4444",
      weight: 3.5,
      dashArray: "5, 5",
      opacity: 0.95
    },
    onEachFeature: (feature, layer) => {
      const p = feature.properties;
      layer.bindTooltip(`
        <div style="font-size:12px;">
          <strong style="color:#ef4444;">🚨 ${p.drain_name}</strong><br>
          Type: ${p.drain_type}<br>
          Bio-Hazard: ${p.bio_hazard_rating}
        </div>
      `, { sticky: true });
    }
  }).addTo(map);

  // D. Drinking Water Pipelines (NMC & Panchayati)
  layerPipelines = L.geoJSON(allData.pipelines, {
    style: (feature) => {
      const p = feature.properties;
      const isHighRisk = p.cross_contamination_risk.includes("High");
      return {
        color: isHighRisk ? "#38bdf8" : "#0284c7",
        weight: Math.max(2.5, p.diameter_mm / 100),
        dashArray: isHighRisk ? "6, 4" : "",
        opacity: 0.9
      };
    },
    onEachFeature: (feature, layer) => {
      const p = feature.properties;
      layer.bindTooltip(`
        <div style="font-size:12px;">
          <strong style="color:#38bdf8;">💧 ${p.pipe_id}: ${p.name}</strong><br>
          Source: ${p.water_source}<br>
          Dia: <strong>${p.diameter_mm}mm</strong> (${p.material})<br>
          Contamination Risk: <em>${p.cross_contamination_risk}</em>
        </div>
      `, { sticky: true });
      layer.on("click", () => inspectPipeline(p));
    }
  }).addTo(map);

  // E. Drinking Water Points (RO Plants, Borewells, Hand Pumps)
  layerWaterPoints = L.geoJSON(allData.water_points, {
    pointToLayer: (feature, latlng) => {
      const p = feature.properties;
      const isCritical = p.risk.includes("CRITICAL");
      const iconColor = isCritical ? "#ef4444" : p.type.includes("RO") ? "#0ea5e9" : "#0284c7";
      const iconSymbol = p.type.includes("RO") ? "fa-glass-water-droplet" : p.type.includes("Pump") ? "fa-faucet" : "fa-water";

      const html = `
        <div class="water-marker-icon" style="background:${iconColor}; border-color:${isCritical ? '#fee2e2' : '#ffffff'}; width:24px; height:24px;">
          <i class="fa-solid ${iconSymbol}" style="font-size:11px;"></i>
        </div>
      `;
      return L.marker(latlng, {
        icon: L.divIcon({ html: html, className: "", iconSize: [24, 24], iconAnchor: [12, 12] })
      });
    },
    onEachFeature: (feature, layer) => {
      const p = feature.properties;
      layer.on("click", () => inspectWaterPoint(p));
    }
  }).addTo(map);

  // F. Vegetable Markets & Rythu Bazaars
  layerVegMarkets = L.geoJSON(allData.veg_markets, {
    pointToLayer: (feature, latlng) => {
      const p = feature.properties;
      const html = `
        <div class="veg-marker-icon" style="width:26px; height:26px;">
          <i class="fa-solid fa-carrot" style="font-size:12px;"></i>
        </div>
      `;
      return L.marker(latlng, {
        icon: L.divIcon({ html: html, className: "", iconSize: [26, 26], iconAnchor: [13, 13] })
      });
    },
    onEachFeature: (feature, layer) => {
      const p = feature.properties;
      layer.on("click", () => inspectVegMarket(p));
    }
  }).addTo(map);

  // G. Healthcare Facilities (Govt + Private)
  layerHospitals = L.geoJSON(allData.hospitals, {
    pointToLayer: (feature, latlng) => {
      const p = feature.properties;
      const isGovt = p.sector === "Government";
      const html = `
        <div class="hospital-marker-icon" style="background:${isGovt ? '#0284c7' : '#f43f5e'}; width:24px; height:24px;">
          <i class="fa-solid fa-hospital" style="font-size:12px;"></i>
        </div>
      `;
      return L.marker(latlng, {
        icon: L.divIcon({ html: html, className: "", iconSize: [24, 24], iconAnchor: [12, 12] })
      });
    },
    onEachFeature: (feature, layer) => {
      const p = feature.properties;
      layer.on("click", () => inspectHospital(p));
    }
  }).addTo(map);

  // H. Risk Exposure Buffers (250m & 500m)
  layerBuffers250 = L.geoJSON(allData.buffers_250, {
    style: (feature) => {
      const isVeryHigh = feature.properties.risk_level === "Very High Risk";
      return {
        color: isVeryHigh ? "#d90429" : "#f77f00",
        weight: 1.5,
        fillColor: isVeryHigh ? "#d90429" : "#f77f00",
        fillOpacity: 0.18,
        dashArray: "3, 3"
      };
    }
  });

  layerBuffers500 = L.geoJSON(allData.buffers_500, {
    style: {
      color: "#f59e0b",
      weight: 1,
      fillColor: "#f59e0b",
      fillOpacity: 0.08,
      dashArray: "4, 6"
    }
  });

  // I. Wet Markets Layer
  layerMarkets = L.layerGroup().addTo(map);
  renderMarketMarkers(allData.markets.features);
}

function renderMarketMarkers(features) {
  layerMarkets.clearLayers();

  features.forEach(feat => {
    const p = feat.properties;
    const [lon, lat] = feat.geometry.coordinates;

    const iconHtml = `
      <div class="market-marker-icon" style="background:${p.marker_color}; width:24px; height:24px;">
        <i class="fa-solid fa-store" style="font-size:10px;"></i>
      </div>
    `;

    const icon = L.divIcon({
      html: iconHtml,
      className: "",
      iconSize: [24, 24],
      iconAnchor: [12, 12]
    });

    const marker = L.marker([lat, lon], { icon: icon });

    marker.bindTooltip(`<strong>${p.shop_name}</strong><br>GRI Score: ${p.composite_geo_risk_score}/100 (${p.risk_level})`, { sticky: true });
    marker.on("click", () => inspectMarket(p.shop_id));

    layerMarkets.addLayer(marker);
  });
}

// ---------------- Inspector Functions ---------------- //

window.inspectMarket = function(shopId) {
  const item = allData.markets.features.find(f => f.properties.shop_id === shopId);
  if (!item) return;

  const p = item.properties;
  const [lon, lat] = item.geometry.coordinates;
  const inspector = document.getElementById("inspector-content");

  inspector.innerHTML = `
    <div class="market-detail-card">
      <div class="md-header">
        <div>
          <div class="md-title">${p.shop_name}</div>
          <div class="md-id">${p.shop_id} • ${p.mandal_zone} (${p.cluster_hub})</div>
        </div>
        <span class="risk-badge" style="background:${p.marker_color}">${p.risk_level}</span>
      </div>

      <div class="score-meter">
        <div class="meter-label">
          <span>Geo-Risk Index Score</span>
          <span style="color:${p.marker_color}">${p.composite_geo_risk_score} / 100</span>
        </div>
        <div class="progress-bar-bg">
          <div class="progress-bar-fill" style="width:${p.composite_geo_risk_score}%; background:${p.marker_color};"></div>
        </div>
        <div class="ai-prediction-pill">
          <i class="fa-solid fa-robot"></i> AI Prediction: <strong>${p.ai_predicted_risk}</strong> (${p.ai_prediction_confidence}% Conf.)
        </div>
      </div>

      <table class="detail-table">
        <tr><td>Commodity:</td><td>${p.category}</td></tr>
        <tr><td>Daily Throughput:</td><td>${p.daily_animals_handled} units/day</td></tr>
        <tr><td>Supply Origin:</td><td>${p.animal_origin}</td></tr>
        <tr><td>Destination:</td><td>${p.animal_destination}</td></tr>
        <tr><td>Live On-Site Slaughter:</td><td><strong style="color:${p.slaughter_on_site === 'Yes' ? '#f87171' : '#4ade80'}">${p.slaughter_on_site}</strong></td></tr>
        <tr><td>Refrigeration Available:</td><td><strong style="color:${p.refrigeration_available === 'Yes' ? '#4ade80' : '#f87171'}">${p.refrigeration_available}</strong></td></tr>
        <tr><td>Waste Disposal:</td><td>${p.waste_disposal_method}</td></tr>
        <tr><td>Distance to Open Drain:</td><td><strong style="color:${p.distance_to_drain_m < 50 ? '#ef4444' : '#e2e8f0'}">${p.distance_to_drain_m} meters</strong></td></tr>
        <tr><td>Nearest Health Centre:</td><td>${p.distance_to_hospital_m} meters</td></tr>
        <tr><td>Crowd Density Index:</td><td>${p.market_crowd_index} / 10</td></tr>
      </table>

      <div class="intervention-alert">
        <strong><i class="fa-solid fa-triangle-exclamation"></i> Municipal Action Required:</strong>
        ${p.recommended_intervention}
      </div>

      <div class="action-buttons-row">
        <button class="btn-card-action" onclick="openStreetView(${lat}, ${lon}, '${p.shop_name.replace(/'/g, "\\'")}', 'Wet Market')">
          <i class="fa-solid fa-person-walking"></i> Street Walk View
        </button>
        <a class="btn-card-action btn-google-maps" href="https://www.google.com/maps/search/?api=1&query=${lat},${lon}" target="_blank">
          <i class="fa-brands fa-google"></i> Google Maps 3D
        </a>
      </div>
    </div>
  `;

  map.setView([lat, lon], 16, { animate: true });
};

window.inspectVegMarket = function(p) {
  const inspector = document.getElementById("inspector-content");
  inspector.innerHTML = `
    <div class="market-detail-card">
      <div class="md-header">
        <div>
          <div class="md-title">${p.market_name}</div>
          <div class="md-id">${p.market_id} • ${p.jurisdiction}</div>
        </div>
        <span class="risk-badge" style="background:#10b981;">Vegetable Market</span>
      </div>

      <table class="detail-table">
        <tr><td>Market Type:</td><td>${p.type}</td></tr>
        <tr><td>Stalls Count:</td><td><strong>${p.stalls_count} farmer stalls</strong></td></tr>
        <tr><td>Daily Footfall:</td><td>${p.daily_footfall.toLocaleString()} consumers/day</td></tr>
        <tr><td>Produce Origin:</td><td>${p.produce_origin}</td></tr>
        <tr><td>Distance to Meat Stalls:</td><td><strong>${p.proximity_to_meat_fish_m} meters</strong></td></tr>
        <tr><td>Distance to Open Drain:</td><td>${p.drain_dist_m} meters</td></tr>
        <tr><td>Waste Management:</td><td>${p.waste_management}</td></tr>
      </table>

      <div class="intervention-alert" style="border-color:#10b981; background:rgba(16,185,129,0.1); color:#6ee7b7;">
        <strong style="color:#a7f3d0;"><i class="fa-solid fa-leaf"></i> Cross-Contamination Rating: ${p.cross_contamination_rating}</strong>
        Ensure physical segregation from wet meat/fish stalls and regular daily organic waste composting.
      </div>

      <div class="action-buttons-row">
        <button class="btn-card-action" onclick="openStreetView(${p.lat}, ${p.lon}, '${p.market_name.replace(/'/g, "\\'")}', 'Produce Market')">
          <i class="fa-solid fa-person-walking"></i> Street Walk View
        </button>
        <a class="btn-card-action btn-google-maps" href="https://www.google.com/maps/search/?api=1&query=${p.lat},${p.lon}" target="_blank">
          <i class="fa-brands fa-google"></i> Google Maps 3D
        </a>
      </div>
    </div>
  `;
  map.setView([p.lat, p.lon], 16, { animate: true });
};

window.inspectPipeline = function(p) {
  const inspector = document.getElementById("inspector-content");
  const isHighRisk = p.cross_contamination_risk.includes("High");

  inspector.innerHTML = `
    <div class="market-detail-card">
      <div class="md-header">
        <div>
          <div class="md-title">${p.name}</div>
          <div class="md-id">Pipeline #${p.pipe_id} • ${p.jurisdiction}</div>
        </div>
        <span class="risk-badge" style="background:${isHighRisk ? '#ef4444' : '#0284c7'};">Water Main</span>
      </div>

      <table class="detail-table">
        <tr><td>Pipeline ID:</td><td><strong>${p.pipe_id}</strong></td></tr>
        <tr><td>Water Headworks:</td><td>${p.water_source}</td></tr>
        <tr><td>Pipe Diameter:</td><td><strong>${p.diameter_mm} mm</strong></td></tr>
        <tr><td>Material:</td><td>${p.material}</td></tr>
        <tr><td>Operating Pressure:</td><td>${p.pressure_bar} Bar</td></tr>
        <tr><td>Commissioning Year:</td><td>${p.laying_year}</td></tr>
      </table>

      <div class="intervention-alert" style="border-color:${isHighRisk ? '#ef4444' : '#0284c7'};">
        <strong><i class="fa-solid fa-faucet-drip"></i> Contamination Vulnerability:</strong>
        ${p.cross_contamination_risk}. Sullage ingress can occur during low water pressure hours.
      </div>
    </div>
  `;
};

window.inspectWaterPoint = function(p) {
  const inspector = document.getElementById("inspector-content");
  const isCritical = p.risk.includes("CRITICAL");

  inspector.innerHTML = `
    <div class="market-detail-card">
      <div class="md-header">
        <div>
          <div class="md-title">${p.name}</div>
          <div class="md-id">${p.id} • ${p.ward}</div>
        </div>
        <span class="risk-badge" style="background:${isCritical ? '#ef4444' : '#0284c7'};">${p.type}</span>
      </div>

      <table class="detail-table">
        <tr><td>Facility Type:</td><td>${p.type}</td></tr>
        <tr><td>Output Capacity:</td><td>${p.capacity_lph} Liters/Hour</td></tr>
        <tr><td>TDS Level:</td><td><strong>${p.tds_ppm} ppm</strong></td></tr>
        <tr><td>Potability Status:</td><td><strong style="color:${isCritical ? '#f87171' : '#4ade80'}">${p.potability}</strong></td></tr>
        <tr><td>Distance to Open Drain:</td><td><strong style="color:${p.drain_dist_m < 15 ? '#ef4444' : '#e2e8f0'}">${p.drain_dist_m} meters</strong></td></tr>
      </table>

      <div class="intervention-alert">
        <strong><i class="fa-solid fa-biohazard"></i> Health Alert (${p.risk}):</strong>
        ${isCritical ? 'Immediate microbial testing required. Hand pump is directly vulnerable to subsurface sewage percolation.' : 'Water quality within acceptable IS 10500 drinking standards.'}
      </div>

      <div class="action-buttons-row">
        <a class="btn-card-action btn-google-maps" href="https://www.google.com/maps/search/?api=1&query=${p.lat},${p.lon}" target="_blank">
          <i class="fa-brands fa-google"></i> Google Maps 3D
        </a>
      </div>
    </div>
  `;
  map.setView([p.lat, p.lon], 16, { animate: true });
};

window.inspectHospital = function(p) {
  const inspector = document.getElementById("inspector-content");
  const isGovt = p.sector === "Government";

  inspector.innerHTML = `
    <div class="market-detail-card">
      <div class="md-header">
        <div>
          <div class="md-title">${p.name}</div>
          <div class="md-id">${p.sector} • ${p.category}</div>
        </div>
        <span class="risk-badge" style="background:${isGovt ? '#0284c7' : '#f43f5e'};">Healthcare</span>
      </div>

      <table class="detail-table">
        <tr><td>Category:</td><td>${p.category}</td></tr>
        <tr><td>Inpatient Bed Capacity:</td><td><strong>${p.beds} Beds</strong></td></tr>
        <tr><td>ICU & Emergency:</td><td>${p.emergency_icu}</td></tr>
        <tr><td>Ambulance Network:</td><td>${p.ambulance}</td></tr>
      </table>

      <div class="action-buttons-row">
        <a class="btn-card-action btn-google-maps" href="https://www.google.com/maps/search/?api=1&query=${p.lat},${p.lon}" target="_blank">
          <i class="fa-brands fa-google"></i> Google Maps 3D
        </a>
      </div>
    </div>
  `;
  map.setView([p.lat, p.lon], 16, { animate: true });
};

// ---------------- Street View Modal ---------------- //

window.openStreetView = function(lat, lon, name, type) {
  const modal = document.getElementById("street-modal");
  const content = document.getElementById("street-modal-content");

  content.innerHTML = `
    <div style="text-align:center;">
      <div style="background:#0f172a; border-radius:8px; padding:18px; border:1px solid #334155; margin-bottom:14px;">
        <i class="fa-solid fa-street-view" style="font-size:3rem; color:#38bdf8; margin-bottom:10px;"></i>
        <h3 style="font-size:1.05rem; font-weight:700; color:#fff;">${name}</h3>
        <p style="font-size:0.8rem; color:#94a3b8; margin-top:4px;">Type: ${type} • Location: ${lat.toFixed(5)}°N, ${lon.toFixed(5)}°E</p>
      </div>

      <p style="font-size:0.82rem; color:#cbd5e1; line-height:1.5; margin-bottom:16px;">
        Explore the ground-level street view, roadside drainage gutters, market vendor stalls, and underground pipeline corridors directly via Google Maps 3D Earth:
      </p>

      <a class="nav-btn" style="display:inline-flex; justify-content:center; width:100%; padding:10px; font-size:0.9rem;" href="https://www.google.com/maps/search/?api=1&query=${lat},${lon}" target="_blank">
        <i class="fa-brands fa-google"></i> Open Street View in Google Maps 3D
      </a>
    </div>
  `;

  modal.classList.remove("hidden");
};

// ---------------- Drone Flyover Mode ---------------- //

function startDroneFlyover() {
  if (isDroneMode) return;
  stopBikeCommute();

  isDroneMode = true;
  droneStep = 0;
  document.getElementById("btn-drone-mode").classList.add("active");

  const hud = document.getElementById("hud-panel");
  hud.classList.remove("hidden");
  document.getElementById("hud-mode-title").innerHTML = '<i class="fa-solid fa-helicopter"></i> Drone Flyover Active';

  // Add animated drone marker
  droneMarker = L.marker([DRONE_CHECKPOINTS[0].lat, DRONE_CHECKPOINTS[0].lon], {
    icon: L.divIcon({
      html: '<div class="drone-camera-icon" style="width:28px; height:28px;"><i class="fa-solid fa-helicopter"></i></div>',
      className: "",
      iconSize: [28, 28],
      iconAnchor: [14, 14]
    })
  }).addTo(map);

  flyToNextDroneCheckpoint();
}

function flyToNextDroneCheckpoint() {
  if (!isDroneMode) return;

  const cp = DRONE_CHECKPOINTS[droneStep];
  document.getElementById("hud-checkpoint-text").textContent = `Checkpoint ${droneStep + 1}/${DRONE_CHECKPOINTS.length}: ${cp.name}`;
  document.getElementById("hud-alt-val").textContent = cp.alt;
  document.getElementById("hud-speed-val").textContent = cp.speed;

  const bioVal = document.getElementById("hud-bio-val");
  bioVal.textContent = cp.hazard;
  bioVal.className = `hud-val ${cp.hazard === "CRITICAL" ? "alert-red" : cp.hazard === "HIGH" ? "alert-red" : "alert-green"}`;

  droneMarker.setLatLng([cp.lat, cp.lon]);
  map.flyTo([cp.lat, cp.lon], cp.zoom, { duration: 3.5 });

  droneStep = (droneStep + 1) % DRONE_CHECKPOINTS.length;
  droneTimer = setTimeout(flyToNextDroneCheckpoint, 5500);
}

function stopDroneFlyover() {
  isDroneMode = false;
  clearTimeout(droneTimer);
  document.getElementById("btn-drone-mode").classList.remove("active");
  document.getElementById("hud-panel").classList.add("hidden");
  if (droneMarker) {
    map.removeLayer(droneMarker);
    droneMarker = null;
  }
}

// ---------------- Motorcycle / Bicycle Commute Mode ---------------- //

function startBikeCommute() {
  if (isBikeMode) return;
  stopDroneFlyover();

  isBikeMode = true;
  bikeProgress = 0;
  document.getElementById("btn-commute-mode").classList.add("active");

  const hud = document.getElementById("hud-panel");
  hud.classList.remove("hidden");
  document.getElementById("hud-mode-title").innerHTML = '<i class="fa-solid fa-motorcycle"></i> Livestock Commute Simulation';
  document.getElementById("hud-checkpoint-text").textContent = 'Transporting Livestock: Kovur Rural Hatchery ➔ Stonehousepet Wholesale Market';

  bikeMarker = L.marker(BIKE_ROUTE[0], {
    icon: L.divIcon({
      html: '<div class="moving-bike-icon" style="width:30px; height:30px;"><i class="fa-solid fa-motorcycle"></i></div>',
      className: "",
      iconSize: [30, 30],
      iconAnchor: [15, 15]
    })
  }).addTo(map);

  map.setView(BIKE_ROUTE[0], 15);
  advanceBikeCommute();
}

function advanceBikeCommute() {
  if (!isBikeMode) return;

  if (bikeProgress >= BIKE_ROUTE.length - 1) {
    bikeProgress = 0; // Loop or finish
  } else {
    bikeProgress++;
  }

  const currentCoord = BIKE_ROUTE[bikeProgress];
  bikeMarker.setLatLng(currentCoord);
  map.panTo(currentCoord, { animate: true, duration: 1.5 });

  const distKm = ((bikeProgress / BIKE_ROUTE.length) * 6.5).toFixed(1);
  document.getElementById("hud-alt-val").textContent = `Ground (${distKm} km)`;
  document.getElementById("hud-speed-val").textContent = "32 km/h";

  // Bio exposure triggers when crossing Pennar bridge & entering Stonehousepet
  const bioVal = document.getElementById("hud-bio-val");
  if (bikeProgress >= 7) {
    bioVal.textContent = "CRITICAL (Near Open Sewer)";
    bioVal.className = "hud-val alert-red";
  } else if (bikeProgress >= 4) {
    bioVal.textContent = "MODERATE (Crossing River)";
    bioVal.className = "hud-val alert-green";
  } else {
    bioVal.textContent = "NORMAL";
    bioVal.className = "hud-val alert-green";
  }

  bikeTimer = setTimeout(advanceBikeCommute, 2200);
}

function stopBikeCommute() {
  isBikeMode = false;
  clearTimeout(bikeTimer);
  document.getElementById("btn-commute-mode").classList.remove("active");
  document.getElementById("hud-panel").classList.add("hidden");
  if (bikeMarker) {
    map.removeLayer(bikeMarker);
    bikeMarker = null;
  }
}

// ---------------- Event Listeners & Filter Handlers ---------------- //

function updateHeaderKPIs() {
  const features = allData.markets.features;
  const critical = features.filter(f => f.properties.risk_level === "Very High Risk" || f.properties.risk_level === "High Risk").length;
  const veryHigh = features.filter(f => f.properties.risk_level === "Very High Risk").length;

  if (document.getElementById("kpi-total")) document.getElementById("kpi-total").textContent = features.length + allData.veg_markets.features.length;
  if (document.getElementById("kpi-very-high")) document.getElementById("kpi-very-high").textContent = veryHigh;
  if (document.getElementById("kpi-ai-acc") && allData.ai_metrics) {
    document.getElementById("kpi-ai-acc").textContent = (allData.ai_metrics.test_accuracy * 100).toFixed(1) + "%";
  }
}

function setupEventListeners() {
  // Layer Toggles
  document.getElementById("layer-markets").addEventListener("change", (e) => toggleLayer(layerMarkets, e.target.checked));
  document.getElementById("layer-veg-markets").addEventListener("change", (e) => toggleLayer(layerVegMarkets, e.target.checked));
  document.getElementById("layer-pipelines").addEventListener("change", (e) => toggleLayer(layerPipelines, e.target.checked));
  document.getElementById("layer-water-points").addEventListener("change", (e) => toggleLayer(layerWaterPoints, e.target.checked));
  document.getElementById("layer-drainage").addEventListener("change", (e) => toggleLayer(layerDrainage, e.target.checked));
  document.getElementById("layer-river").addEventListener("change", (e) => toggleLayer(layerRiver, e.target.checked));
  document.getElementById("layer-hospitals").addEventListener("change", (e) => toggleLayer(layerHospitals, e.target.checked));
  document.getElementById("layer-boundaries").addEventListener("change", (e) => toggleLayer(layerBoundaries, e.target.checked));
  document.getElementById("layer-buffers-250").addEventListener("change", (e) => toggleLayer(layerBuffers250, e.target.checked));

  // Drone & Bike Modes
  document.getElementById("btn-drone-mode").addEventListener("click", () => {
    if (isDroneMode) stopDroneFlyover();
    else startDroneFlyover();
  });

  document.getElementById("btn-commute-mode").addEventListener("click", () => {
    if (isBikeMode) stopBikeCommute();
    else startBikeCommute();
  });

  document.getElementById("btn-hud-close").addEventListener("click", () => {
    stopDroneFlyover();
    stopBikeCommute();
  });

  document.getElementById("btn-hud-stop").addEventListener("click", () => {
    stopDroneFlyover();
    stopBikeCommute();
  });

  document.getElementById("btn-hud-next").addEventListener("click", () => {
    if (isDroneMode) flyToNextDroneCheckpoint();
    else if (isBikeMode) advanceBikeCommute();
  });

  // Filters
  document.getElementById("search-input").addEventListener("input", applyFilters);
  document.getElementById("filter-risk").addEventListener("change", applyFilters);
  document.getElementById("filter-zone").addEventListener("change", applyFilters);
  document.getElementById("filter-category").addEventListener("change", applyFilters);

  const drainSlider = document.getElementById("filter-drain-dist");
  drainSlider.addEventListener("input", (e) => {
    const val = e.target.value;
    document.getElementById("drain-dist-val").textContent = val >= 300 ? "All" : `≤ ${val}m`;
    applyFilters();
  });

  // Modals
  document.getElementById("btn-toggle-analytics").addEventListener("click", () => {
    document.getElementById("analytics-modal").classList.remove("hidden");
  });
  document.getElementById("btn-close-analytics").addEventListener("click", () => {
    document.getElementById("analytics-modal").classList.add("hidden");
  });

  document.getElementById("btn-export-data").addEventListener("click", () => {
    document.getElementById("export-modal").classList.remove("hidden");
  });
  document.getElementById("btn-close-export").addEventListener("click", () => {
    document.getElementById("export-modal").classList.add("hidden");
  });

  document.getElementById("btn-close-street").addEventListener("click", () => {
    document.getElementById("street-modal").classList.add("hidden");
  });

  // Simulation Tool
  document.getElementById("btn-simulate-shop").addEventListener("click", () => {
    isSimulationMode = true;
    document.getElementById("simulation-banner").classList.remove("hidden");
    map.getContainer().style.cursor = "crosshair";
  });

  document.getElementById("btn-cancel-sim").addEventListener("click", exitSimulationMode);
  document.getElementById("btn-close-sim").addEventListener("click", () => {
    document.getElementById("sim-result-modal").classList.add("hidden");
  });

  map.on("click", (e) => {
    if (!isSimulationMode) return;
    evaluateSimulatedLocation(e.latlng);
  });

  // Export handlers
  document.getElementById("btn-dl-geojson").addEventListener("click", () => {
    downloadFile(JSON.stringify(allData.markets, null, 2), "nellore_kovur_wet_markets.geojson", "application/json");
  });

  document.getElementById("btn-dl-pipelines").addEventListener("click", () => {
    downloadFile(JSON.stringify(allData.pipelines, null, 2), "drinking_water_pipelines_nmc_kovur.geojson", "application/json");
  });

  document.getElementById("btn-dl-waterpoints").addEventListener("click", () => {
    downloadFile(JSON.stringify(allData.water_points, null, 2), "water_points_ro_plants_handpumps.geojson", "application/json");
  });

  document.getElementById("btn-dl-csv").addEventListener("click", exportCSV);
}

function toggleLayer(layer, isChecked) {
  if (isChecked) map.addLayer(layer);
  else map.removeLayer(layer);
}

function exitSimulationMode() {
  isSimulationMode = false;
  document.getElementById("simulation-banner").classList.add("hidden");
  map.getContainer().style.cursor = "";
  if (simMarker) {
    map.removeLayer(simMarker);
    simMarker = null;
  }
}

function applyFilters() {
  const search = document.getElementById("search-input").value.toLowerCase().trim();
  const risk = document.getElementById("filter-risk").value;
  const zone = document.getElementById("filter-zone").value;
  const category = document.getElementById("filter-category").value;
  const maxDrain = parseInt(document.getElementById("filter-drain-dist").value, 10);

  const filtered = allData.markets.features.filter(f => {
    const p = f.properties;
    if (search && !p.shop_name.toLowerCase().includes(search) && !p.shop_id.toLowerCase().includes(search)) return false;
    if (risk !== "ALL" && p.risk_level !== risk) return false;
    if (zone !== "ALL" && p.mandal_zone !== zone) return false;
    if (category !== "ALL" && p.category !== category) return false;
    if (maxDrain < 300 && p.distance_to_drain_m > maxDrain) return false;
    return true;
  });

  renderMarketMarkers(filtered);
}

function evaluateSimulatedLocation(latlng) {
  const lat = latlng.lat;
  const lon = latlng.lng;

  const drainLines = allData.drainage.features.map(f => f.geometry.coordinates);
  let minDrainDist = 9999;

  drainLines.forEach(line => {
    for (let i = 0; i < line.length - 1; i++) {
      const [x1, y1] = line[i];
      const [x2, y2] = line[i + 1];
      const d = distPointToSegment(lon, lat, x1, y1, x2, y2);
      if (d < minDrainDist) minDrainDist = d;
    }
  });
  minDrainDist = Math.round(minDrainDist);
  const riverDist = Math.round(Math.abs(lat - 14.463) * 110574);

  const normDrain = Math.max(0, Math.min(1, (300 - minDrainDist) / 280));
  const score = Math.round(((0.25 * normDrain) + (0.15 * 1.0) + (0.20 * (minDrainDist < 50 ? 1.0 : 0.4)) + 0.15 * 0.7 + 0.10 * 0.9 + 0.10 * 0.5 + 0.05 * Math.max(0, Math.min(1, (2500 - riverDist)/2300))) * 100);

  let recommendation, permitDecision;
  if (score >= 72 || minDrainDist < 30) {
    permitDecision = "🚨 PERMIT REJECTED (High Zoonotic Risk)";
    recommendation = `Location is only <strong>${minDrainDist}m</strong> from an open municipal sullage drain. Mandate 100m bio-setback distance or relocate to formal NMC abattoir zone.`;
  } else if (score >= 56) {
    permitDecision = "⚠️ CONDITIONAL PERMIT (Sanitary Covenants Required)";
    recommendation = `Permit contingent on closed bio-waste traps, mandatory zero-discharge into nearby drainage (${minDrainDist}m), and verified cold storage refrigeration.`;
  } else {
    permitDecision = "✅ PERMIT APPROVED (Standard Food Safety Protocol)";
    recommendation = `Adequate spatial separation from open drainage lines (${minDrainDist}m). Standard municipal sanitation inspection schedule applies.`;
  }

  if (simMarker) map.removeLayer(simMarker);
  simMarker = L.circleMarker([lat, lon], {
    radius: 10,
    color: "#ffffff",
    weight: 3,
    fillColor: score >= 72 ? "#d90429" : score >= 56 ? "#f77f00" : "#06d6a0",
    fillOpacity: 0.9
  }).addTo(map);

  const content = `
    <div style="font-size:0.85rem; line-height:1.5;">
      <div style="font-size:1rem; font-weight:700; margin-bottom:8px;">${permitDecision}</div>
      <table class="detail-table">
        <tr><td>Selected Coordinates:</td><td>${lat.toFixed(5)}°N, ${lon.toFixed(5)}°E</td></tr>
        <tr><td>Distance to Open Drain:</td><td><strong>${minDrainDist} meters</strong></td></tr>
        <tr><td>Distance to Pennar River:</td><td>${riverDist} meters</td></tr>
        <tr><td>Estimated Geo-Risk Score:</td><td><strong>${score} / 100</strong></td></tr>
      </table>
      <div class="intervention-alert" style="margin-top:12px;">
        ${recommendation}
      </div>
    </div>
  `;

  document.getElementById("sim-result-content").innerHTML = content;
  document.getElementById("sim-result-modal").classList.remove("hidden");
  exitSimulationMode();
}

function distPointToSegment(px, py, x1, y1, x2, y2) {
  const cosLat = Math.cos(14.45 * Math.PI / 180);
  const mx = (px - x1) * 111320 * cosLat;
  const my = (py - y1) * 110574;
  const sx = (x2 - x1) * 111320 * cosLat;
  const sy = (y2 - y1) * 110574;

  const segLenSq = sx * sx + sy * sy;
  if (segLenSq === 0) return Math.sqrt(mx * mx + my * my);

  const t = Math.max(0, Math.min(1, (mx * sx + my * sy) / segLenSq));
  const dx = mx - t * sx;
  const dy = my - t * sy;
  return Math.sqrt(dx * dx + dy * dy);
}

function downloadFile(content, fileName, contentType) {
  const a = document.createElement("a");
  const file = new Blob([content], { type: contentType });
  a.href = URL.createObjectURL(file);
  a.download = fileName;
  a.click();
  URL.revokeObjectURL(a.href);
}

function exportCSV() {
  const features = allData.markets.features;
  if (!features.length) return;

  const headers = Object.keys(features[0].properties);
  const rows = features.map(f => headers.map(h => `"${String(f.properties[h] || '').replace(/"/g, '""')}"`).join(","));
  downloadFile([headers.join(","), ...rows].join("\n"), "health_gis_nellore_kovur_attributes.csv", "text/csv;charset=utf-8;");
}
