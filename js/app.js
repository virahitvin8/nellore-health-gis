/**
 * Main WebGIS Application Controller - Enhanced Infrastructure Edition
 * Nellore City (NMC) & Kovur Mandal Water Supply Flow, Overhead Tanks & Strict AOI
 */

let map;
let allData = null;

// Layer Groups
let layerMask;
let layerBoundaries;
let layerRiver;
let layerDrainage;
let layerFlowNetwork;
let layerTanks;
let layerSources;
let layerWaterPoints;
let layerVegMarkets;
let layerMarkets;
let layerHospitals;

// 3D & Animation States
let is3DTilt = false;
let isDroneMode = false;
let droneStep = 0;
let droneTimer = null;
let droneMarker = null;

let isCommuteMode = false;
let commuteTimer = null;
let commuteMarker = null;
let commuteStep = 0;

// Strict Bounding Box for Nellore City & Kovur Mandal
const STRICT_BOUNDS = L.latLngBounds(
  [14.3600, 79.9100], // Southwest
  [14.5600, 80.0500]  // Northeast
);

// Drone Checkpoints along Water Flow & Major Landmarks
const DRONE_CHECKPOINTS = [
  { name: "Pennar River Infiltration Gallery (Source)", lat: 14.4640, lon: 79.9700, zoom: 16, alt: "180m AGL", rate: "18.0 MLD", note: "Riverbed sand aquifer extraction supplying NMC central headworks." },
  { name: "Nellore Municipal Central Headworks & Treatment", lat: 14.4600, lon: 79.9750, zoom: 17, alt: "120m AGL", rate: "32.0 MLD", note: "Rapid sand filtration & primary chlorination distribution hub." },
  { name: "Stonehousepet Overhead Tank (ELSR-NMC-01)", lat: 14.4500, lon: 79.9910, zoom: 17, alt: "90m AGL", rate: "1.8 MLD", note: "18m staging height; gravity feed to 42,000 ward consumers & Rythu Bazaar." },
  { name: "Santhapet Central Municipal Water Tower", lat: 14.4390, lon: 79.9810, zoom: 17, alt: "100m AGL", rate: "2.2 MLD", note: "20m elevated reservoir supplying historic central commercial bazaar." },
  { name: "Historic Pennar River Bridge Crossing", lat: 14.4650, lon: 79.9848, zoom: 15, alt: "220m AGL", rate: "River Corridor", note: "Inter-mandal transit connecting Nellore City with Kovur Mandal." },
  { name: "Kovur Gram Panchayat Overhead Tank (ELSR-KVR-01)", lat: 14.4945, lon: 79.9785, zoom: 17, alt: "90m AGL", rate: "1.4 MLD", note: "18m elevated reservoir supplying Kovur Main Bazaar & surrounding wards." },
  { name: "Inamadugu Rural Elevated Reservoir (ELSR-KVR-03)", lat: 14.4910, lon: 80.0035, zoom: 16, alt: "130m AGL", rate: "0.6 MLD", note: "Solar-assisted overhead tank serving agricultural & livestock community." }
];

const COMMUTE_ROUTE = [
  [14.4640, 79.9700], // Pennar Infiltration
  [14.4600, 79.9750], // Headworks
  [14.4550, 79.9810],
  [14.4500, 79.9910], // Stonehousepet ELSR
  [14.4508, 79.9918], // Stonehousepet Rythu Bazaar
  [14.4535, 79.9875], // Ranganayakulapet
  [14.4650, 79.9848], // Pennar Bridge
  [14.4755, 79.9840], // Padugupadu
  [14.4945, 79.9785]  // Kovur Bazaar ELSR
];

document.addEventListener("DOMContentLoaded", () => {
  initDataAndMap();
  setupEventListeners();
  loadSavedAPIKeys();
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
        alert("Spatial data loading. Please refresh.");
      }
    }, 400);
  }
}

function buildWebGIS() {
  // 1. Initialize Map with strict bounds
  map = L.map("map", {
    center: [14.460, 79.982],
    zoom: 13,
    minZoom: 12,
    maxZoom: 18,
    maxBounds: STRICT_BOUNDS,
    maxBoundsViscosity: 0.9,
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

  const esriSatellite = L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", {
    attribution: 'Tiles &copy; Esri &mdash; DigitalGlobe, GeoEye',
    maxZoom: 18
  });

  const positron = L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
    attribution: '&copy; CARTO &copy; OSM',
    subdomains: "abcd",
    maxZoom: 19
  });

  const baseMaps = {
    "CartoDB Dark Theme (Default)": darkMatter,
    "Esri World Satellite Imagery": esriSatellite,
    "CartoDB Light Theme": positron
  };
  L.control.layers(baseMaps, null, { position: "topright" }).addTo(map);

  // 3. Initialize Vectors & Mask
  initVectorLayers();

  // 4. Update Header Stats
  updateStats();

  // 5. Initialize Charts
  if (typeof initAnalyticsCharts === "function") {
    initAnalyticsCharts(allData);
  }
}

function initVectorLayers() {
  // A. Inverted Mask (Dims out everything outside Nellore & Kovur)
  layerMask = L.geoJSON(allData.inverted_mask, {
    style: {
      color: "transparent",
      fillColor: "#090d16",
      fillOpacity: 0.72,
      interactive: false
    }
  }).addTo(map);

  // B. Boundaries (Nellore NMC & Kovur Mandal)
  layerBoundaries = L.geoJSON(allData.aoi, {
    style: (feature) => {
      const isNellore = feature.properties.name.includes("Nellore");
      return {
        color: isNellore ? "#38bdf8" : "#0284c7",
        weight: 2.5,
        dashArray: "6, 6",
        fillColor: isNellore ? "#0284c7" : "#0ea5e9",
        fillOpacity: 0.05
      };
    },
    onEachFeature: (feature, layer) => {
      const p = feature.properties;
      layer.bindTooltip(`<strong>${p.name}</strong><br>${p.type} • Pop: ${p.population_est.toLocaleString()}`, { sticky: true });
    }
  }).addTo(map);

  // C. Pennar River Basin & Canals
  layerRiver = L.geoJSON(allData.waterbodies, {
    style: (feature) => {
      const isRiver = feature.geometry.type === "Polygon";
      return {
        color: "#0077b6",
        weight: isRiver ? 1.5 : 3.5,
        fillColor: "#0284c7",
        fillOpacity: 0.35,
        dashArray: isRiver ? "" : "4, 4"
      };
    },
    onEachFeature: (feature, layer) => {
      const p = feature.properties;
      layer.bindTooltip(`<strong>${p.name}</strong><br>${p.category} (${p.status})`, { sticky: true });
    }
  }).addTo(map);

  // D. Open Sullage & Sewage Outfalls (Red dashed)
  layerDrainage = L.geoJSON(allData.drainage, {
    style: {
      color: "#ef4444",
      weight: 3.2,
      dashArray: "5, 5",
      opacity: 0.95
    },
    onEachFeature: (feature, layer) => {
      const p = feature.properties;
      layer.bindTooltip(`
        <div style="font-size:12px;">
          <strong style="color:#ef4444;">🚨 ${p.drain_name}</strong><br>
          Type: ${p.drain_type}<br>
          Hazard: ${p.bio_hazard_rating}
        </div>
      `, { sticky: true });
    }
  }).addTo(map);

  // E. Animated Water Flow Network (Pipelines with pulses)
  layerFlowNetwork = L.geoJSON(allData.flow_network, {
    style: (feature) => {
      const p = feature.properties;
      const isIntake = p.flow_hierarchy.includes("Intake");
      const isPumping = p.flow_hierarchy.includes("Pumping");
      return {
        color: isIntake ? "#38bdf8" : isPumping ? "#0ea5e9" : "#0284c7",
        weight: Math.max(3, p.diameter_mm / 100),
        className: "animated-water-pipe",
        opacity: 0.95
      };
    },
    onEachFeature: (feature, layer) => {
      const p = feature.properties;
      layer.bindTooltip(`
        <div style="font-size:12px;">
          <strong style="color:#38bdf8;">💧 ${p.name}</strong><br>
          From: <em>${p.from_node}</em><br>
          To: <strong>${p.to_node}</strong><br>
          Discharge: <strong>${p.discharge_mld} MLD</strong> • Dia: ${p.diameter_mm}mm (${p.material})
        </div>
      `, { sticky: true });
      layer.on("click", () => inspectFlowPipe(p));
    }
  }).addTo(map);

  // F. Overhead Storage Reservoirs (ELSR / OHT)
  layerTanks = L.geoJSON(allData.overhead_tanks, {
    pointToLayer: (feature, latlng) => {
      const p = feature.properties;
      const html = `
        <div class="tank-marker-icon" style="width:28px; height:28px;" title="${p.name}">
          <i class="fa-solid fa-monument"></i>
        </div>
      `;
      return L.marker(latlng, {
        icon: L.divIcon({ html: html, className: "", iconSize: [28, 28], iconAnchor: [14, 14] })
      });
    },
    onEachFeature: (feature, layer) => {
      const p = feature.properties;
      layer.bindTooltip(`<strong>🏰 ${p.name}</strong><br>Capacity: ${p.capacity_mld} MLD • Height: ${p.staging_height_m}m`, { sticky: true });
      layer.on("click", () => inspectTank(p));
    }
  }).addTo(map);

  // G. Underground Wells & River Infiltration Sources
  layerSources = L.geoJSON(allData.underground_sources, {
    pointToLayer: (feature, latlng) => {
      const p = feature.properties;
      const html = `
        <div class="source-marker-icon" style="width:26px; height:26px;" title="${p.name}">
          <i class="fa-solid fa-water"></i>
        </div>
      `;
      return L.marker(latlng, {
        icon: L.divIcon({ html: html, className: "", iconSize: [26, 26], iconAnchor: [13, 13] })
      });
    },
    onEachFeature: (feature, layer) => {
      const p = feature.properties;
      layer.bindTooltip(`<strong>🌊 ${p.name}</strong><br>Yield: ${p.yield_lph.toLocaleString()} LPH • Aquifer: ${p.aquifer_source}`, { sticky: true });
      layer.on("click", () => inspectSource(p));
    }
  }).addTo(map);

  // H. Mineral Water RO Plants & Public Hand Pumps
  layerWaterPoints = L.geoJSON(allData.water_points, {
    pointToLayer: (feature, latlng) => {
      const p = feature.properties;
      const isCritical = p.risk.includes("CRITICAL");
      const html = `
        <div class="water-marker-icon" style="background:${isCritical ? '#ef4444' : '#38bdf8'}; width:22px; height:22px;">
          <i class="fa-solid ${p.type.includes('RO') ? 'fa-glass-water-droplet' : 'fa-faucet'}" style="font-size:10px;"></i>
        </div>
      `;
      return L.marker(latlng, {
        icon: L.divIcon({ html: html, className: "", iconSize: [22, 22], iconAnchor: [11, 11] })
      });
    },
    onEachFeature: (feature, layer) => {
      const p = feature.properties;
      layer.on("click", () => inspectWaterPoint(p));
    }
  }).addTo(map);

  // I. Vegetable Markets & Rythu Bazaars
  layerVegMarkets = L.geoJSON(allData.veg_markets, {
    pointToLayer: (feature, latlng) => {
      const html = `
        <div class="veg-marker-icon" style="width:24px; height:24px;">
          <i class="fa-solid fa-carrot" style="font-size:11px;"></i>
        </div>
      `;
      return L.marker(latlng, {
        icon: L.divIcon({ html: html, className: "", iconSize: [24, 24], iconAnchor: [12, 12] })
      });
    },
    onEachFeature: (feature, layer) => {
      const p = feature.properties;
      layer.on("click", () => inspectVegMarket(p));
    }
  }).addTo(map);

  // J. Wet Meat/Fish Markets
  layerMarkets = L.geoJSON(allData.markets, {
    pointToLayer: (feature, latlng) => {
      const p = feature.properties;
      const html = `
        <div class="market-marker-icon" style="background:${p.marker_color}; width:20px; height:20px;">
          <i class="fa-solid fa-store" style="font-size:9px;"></i>
        </div>
      `;
      return L.marker(latlng, {
        icon: L.divIcon({ html: html, className: "", iconSize: [20, 20], iconAnchor: [10, 10] })
      });
    },
    onEachFeature: (feature, layer) => {
      const p = feature.properties;
      layer.on("click", () => inspectMarket(p.shop_id));
    }
  }).addTo(map);

  // K. Hospitals
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
}

// ---------------- Inspector Detail Renderers ---------------- //

window.inspectFlowPipe = function(p) {
  const inspector = document.getElementById("inspector-content");
  inspector.innerHTML = `
    <div class="market-detail-card">
      <div class="md-header">
        <div>
          <div class="md-title">${p.name}</div>
          <div class="md-id">Conduit ID: ${p.pipe_id} • ${p.flow_hierarchy}</div>
        </div>
        <span class="risk-badge" style="background:#0ea5e9;">Water Main</span>
      </div>

      <div class="flow-connectivity-box">
        <div class="flow-node-title"><i class="fa-solid fa-diagram-project"></i> Supply Connectivity Route:</div>
        <div class="flow-arrow-display">
          <span>${p.from_node}</span>
          <i class="fa-solid fa-arrow-right-long"></i>
          <span>${p.to_node}</span>
        </div>
      </div>

      <table class="detail-table">
        <tr><td>Flow Direction:</td><td>${p.flow_direction}</td></tr>
        <tr><td>Daily Discharge:</td><td><strong>${p.discharge_mld} MLD</strong></td></tr>
        <tr><td>Pipe Diameter:</td><td><strong>${p.diameter_mm} mm</strong></td></tr>
        <tr><td>Conduit Material:</td><td>${p.material}</td></tr>
        <tr><td>Operating Pressure:</td><td>${p.pressure_bar} Bar</td></tr>
      </table>

      <div class="intervention-alert">
        <strong><i class="fa-solid fa-faucet-drip"></i> Municipal Water Grid Role:</strong>
        Maintains positive pressure distribution from source treatment headworks directly into elevated service reservoirs.
      </div>
    </div>
  `;
};

window.inspectTank = function(p) {
  const inspector = document.getElementById("inspector-content");
  inspector.innerHTML = `
    <div class="market-detail-card">
      <div class="md-header">
        <div>
          <div class="md-title">${p.name}</div>
          <div class="md-id">${p.id} • ${p.zone}</div>
        </div>
        <span class="risk-badge" style="background:#0284c7;">Overhead Tank</span>
      </div>

      <div class="flow-connectivity-box">
        <div class="flow-node-title"><i class="fa-solid fa-arrow-down-up-across-line"></i> Storage & Staging:</div>
        <div class="flow-arrow-display">
          <span>Fed By: ${p.fed_by}</span>
          <i class="fa-solid fa-arrow-down"></i>
          <span>Gravity Supply to Wards</span>
        </div>
      </div>

      <table class="detail-table">
        <tr><td>Storage Capacity:</td><td><strong>${p.capacity_mld} MLD</strong></td></tr>
        <tr><td>Staging Elevation Height:</td><td><strong>${p.staging_height_m} meters</strong></td></tr>
        <tr><td>Consumer Population:</td><td>${p.supply_population.toLocaleString()} citizens</td></tr>
        <tr><td>Operational Schedule:</td><td>${p.operational_status}</td></tr>
      </table>

      <div class="action-buttons-row">
        <button class="btn-card-action" onclick="openStreetView(${p.lat}, ${p.lon}, '${p.name.replace(/'/g, "\\'")}', 'Overhead Tank')">
          <i class="fa-solid fa-person-walking"></i> Ground Perspective
        </button>
        <a class="btn-card-action btn-google-maps" href="https://www.google.com/maps/search/?api=1&query=${p.lat},${p.lon}" target="_blank">
          <i class="fa-brands fa-google"></i> Google 3D
        </a>
      </div>
    </div>
  `;
  map.setView([p.lat, p.lon], 16, { animate: true });
};

window.inspectSource = function(p) {
  const inspector = document.getElementById("inspector-content");
  inspector.innerHTML = `
    <div class="market-detail-card">
      <div class="md-header">
        <div>
          <div class="md-title">${p.name}</div>
          <div class="md-id">${p.id} • ${p.zone}</div>
        </div>
        <span class="risk-badge" style="background:#0ea5e9;">Water Origin</span>
      </div>

      <div class="flow-connectivity-box">
        <div class="flow-node-title"><i class="fa-solid fa-water"></i> Raw Extraction Destination:</div>
        <div class="flow-arrow-display">
          <span>Underground Aquifer</span>
          <i class="fa-solid fa-arrow-right-long"></i>
          <span>${p.supplies_to}</span>
        </div>
      </div>

      <table class="detail-table">
        <tr><td>Extraction Type:</td><td>${p.type}</td></tr>
        <tr><td>Aquifer Formation:</td><td>${p.aquifer_source}</td></tr>
        <tr><td>Wellfield Yield:</td><td><strong>${p.yield_lph.toLocaleString()} Liters/Hour</strong></td></tr>
        <tr><td>Depth:</td><td>${p.depth_m} meters</td></tr>
      </table>

      <div class="action-buttons-row">
        <a class="btn-card-action btn-google-maps" href="https://www.google.com/maps/search/?api=1&query=${p.lat},${p.lon}" target="_blank">
          <i class="fa-brands fa-google"></i> Google 3D
        </a>
      </div>
    </div>
  `;
  map.setView([p.lat, p.lon], 16, { animate: true });
};

window.inspectWaterPoint = function(p) {
  const inspector = document.getElementById("inspector-content");
  inspector.innerHTML = `
    <div class="market-detail-card">
      <div class="md-header">
        <div>
          <div class="md-title">${p.name}</div>
          <div class="md-id">${p.id} • ${p.ward}</div>
        </div>
        <span class="risk-badge" style="background:#38bdf8; color:#090d16;">${p.type}</span>
      </div>

      <table class="detail-table">
        <tr><td>Facility Type:</td><td>${p.type}</td></tr>
        <tr><td>Capacity:</td><td>${p.capacity_lph} LPH</td></tr>
        <tr><td>TDS Reading:</td><td><strong>${p.tds_ppm} ppm</strong></td></tr>
        <tr><td>Potability:</td><td>${p.potability}</td></tr>
        <tr><td>Drain Proximity:</td><td>${p.drain_dist_m} meters</td></tr>
      </table>

      <div class="action-buttons-row">
        <a class="btn-card-action btn-google-maps" href="https://www.google.com/maps/search/?api=1&query=${p.lat},${p.lon}" target="_blank">
          <i class="fa-brands fa-google"></i> Google 3D
        </a>
      </div>
    </div>
  `;
  map.setView([p.lat, p.lon], 16, { animate: true });
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
        <span class="risk-badge" style="background:#10b981;">Produce Hub</span>
      </div>

      <table class="detail-table">
        <tr><td>Market Type:</td><td>${p.type}</td></tr>
        <tr><td>Farmer Stalls:</td><td><strong>${p.stalls_count} stalls</strong></td></tr>
        <tr><td>Daily Footfall:</td><td>${p.daily_footfall.toLocaleString()} consumers/day</td></tr>
        <tr><td>Produce Origin:</td><td>${p.produce_origin}</td></tr>
      </table>

      <div class="action-buttons-row">
        <a class="btn-card-action btn-google-maps" href="https://www.google.com/maps/search/?api=1&query=${p.lat},${p.lon}" target="_blank">
          <i class="fa-brands fa-google"></i> Google 3D
        </a>
      </div>
    </div>
  `;
  map.setView([p.lat, p.lon], 16, { animate: true });
};

window.inspectHospital = function(p) {
  const inspector = document.getElementById("inspector-content");
  inspector.innerHTML = `
    <div class="market-detail-card">
      <div class="md-header">
        <div>
          <div class="md-title">${p.name}</div>
          <div class="md-id">${p.sector} • ${p.category}</div>
        </div>
        <span class="risk-badge" style="background:#f43f5e;">Healthcare</span>
      </div>

      <table class="detail-table">
        <tr><td>Category:</td><td>${p.category}</td></tr>
        <tr><td>Bed Capacity:</td><td><strong>${p.beds} Beds</strong></td></tr>
        <tr><td>Emergency / ICU:</td><td>${p.emergency_icu}</td></tr>
      </table>

      <div class="action-buttons-row">
        <a class="btn-card-action btn-google-maps" href="https://www.google.com/maps/search/?api=1&query=${p.lat},${p.lon}" target="_blank">
          <i class="fa-brands fa-google"></i> Google 3D
        </a>
      </div>
    </div>
  `;
  map.setView([p.lat, p.lon], 16, { animate: true });
};

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
          <div class="md-id">${p.shop_id} • ${p.mandal_zone}</div>
        </div>
        <span class="risk-badge" style="background:${p.marker_color}">${p.category.split(' ')[0]}</span>
      </div>

      <table class="detail-table">
        <tr><td>Commodity:</td><td>${p.category}</td></tr>
        <tr><td>Supply Origin:</td><td>${p.animal_origin}</td></tr>
        <tr><td>Daily Throughput:</td><td>${p.daily_animals_handled} units/day</td></tr>
        <tr><td>Drain Proximity:</td><td>${p.distance_to_drain_m} meters</td></tr>
      </table>

      <div class="action-buttons-row">
        <a class="btn-card-action btn-google-maps" href="https://www.google.com/maps/search/?api=1&query=${lat},${lon}" target="_blank">
          <i class="fa-brands fa-google"></i> Google 3D
        </a>
      </div>
    </div>
  `;
  map.setView([lat, lon], 16, { animate: true });
};

// ---------------- 3D Perspective & Flyover Modes ---------------- //

function toggle3DTilt() {
  const viewport = document.getElementById("map-viewport");
  is3DTilt = !is3DTilt;
  const btn = document.getElementById("btn-3d-tilt");

  if (is3DTilt) {
    viewport.classList.add("perspective-3d");
    btn.classList.add("active");
  } else {
    viewport.classList.remove("perspective-3d");
    btn.classList.remove("active");
  }
}

function startDroneFlyover() {
  if (isDroneMode) return;
  stopCommuteFlow();

  isDroneMode = true;
  droneStep = 0;
  document.getElementById("btn-drone-mode").classList.add("active");

  const hud = document.getElementById("hud-panel");
  hud.classList.remove("hidden");
  document.getElementById("hud-mode-title").innerHTML = '<i class="fa-solid fa-helicopter"></i> Drone 3D Flyover Active';

  droneMarker = L.marker([DRONE_CHECKPOINTS[0].lat, DRONE_CHECKPOINTS[0].lon], {
    icon: L.divIcon({
      html: '<div class="source-marker-icon" style="background:#0ea5e9; width:28px; height:28px;"><i class="fa-solid fa-helicopter"></i></div>',
      className: "",
      iconSize: [28, 28],
      iconAnchor: [14, 14]
    })
  }).addTo(map);

  flyToNextCheckpoint();
}

function flyToNextCheckpoint() {
  if (!isDroneMode) return;
  const cp = DRONE_CHECKPOINTS[droneStep];

  document.getElementById("hud-checkpoint-text").textContent = `${droneStep + 1}/${DRONE_CHECKPOINTS.length}: ${cp.name}`;
  document.getElementById("hud-alt-val").textContent = cp.alt;
  document.getElementById("hud-speed-val").textContent = cp.rate;

  droneMarker.setLatLng([cp.lat, cp.lon]);
  map.flyTo([cp.lat, cp.lon], cp.zoom, { duration: 3.5 });

  droneStep = (droneStep + 1) % DRONE_CHECKPOINTS.length;
  droneTimer = setTimeout(flyToNextCheckpoint, 5500);
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

function startCommuteFlow() {
  if (isCommuteMode) return;
  stopDroneFlyover();

  isCommuteMode = true;
  commuteStep = 0;
  document.getElementById("btn-commute-mode").classList.add("active");

  const hud = document.getElementById("hud-panel");
  hud.classList.remove("hidden");
  document.getElementById("hud-mode-title").innerHTML = '<i class="fa-solid fa-motorcycle"></i> Commute Flow Active';
  document.getElementById("hud-checkpoint-text").textContent = 'Tracking Water Distribution Corridor across Pennar River...';

  commuteMarker = L.marker(COMMUTE_ROUTE[0], {
    icon: L.divIcon({
      html: '<div class="tank-marker-icon" style="background:#f59e0b; width:28px; height:28px;"><i class="fa-solid fa-motorcycle"></i></div>',
      className: "",
      iconSize: [28, 28],
      iconAnchor: [14, 14]
    })
  }).addTo(map);

  advanceCommuteStep();
}

function advanceCommuteStep() {
  if (!isCommuteMode) return;
  if (commuteStep >= COMMUTE_ROUTE.length - 1) {
    commuteStep = 0;
  } else {
    commuteStep++;
  }

  const coord = COMMUTE_ROUTE[commuteStep];
  commuteMarker.setLatLng(coord);
  map.panTo(coord, { animate: true, duration: 1.5 });

  document.getElementById("hud-alt-val").textContent = `Point ${commuteStep + 1}/${COMMUTE_ROUTE.length}`;
  document.getElementById("hud-speed-val").textContent = "32 km/h";

  commuteTimer = setTimeout(advanceCommuteStep, 2000);
}

function stopCommuteFlow() {
  isCommuteMode = false;
  clearTimeout(commuteTimer);
  document.getElementById("btn-commute-mode").classList.remove("active");
  document.getElementById("hud-panel").classList.add("hidden");
  if (commuteMarker) {
    map.removeLayer(commuteMarker);
    commuteMarker = null;
  }
}

// ---------------- API Keys Config ---------------- //

function loadSavedAPIKeys() {
  const gKey = localStorage.getItem("nellore_google_key");
  const sKey = localStorage.getItem("nellore_sentinel_key");
  const mToken = localStorage.getItem("nellore_mapbox_token");

  if (gKey && document.getElementById("input-google-key")) document.getElementById("input-google-key").value = gKey;
  if (sKey && document.getElementById("input-sentinel-key")) document.getElementById("input-sentinel-key").value = sKey;
  if (mToken && document.getElementById("input-mapbox-token")) document.getElementById("input-mapbox-token").value = mToken;
}

function saveAPIKeys() {
  const gKey = document.getElementById("input-google-key").value.trim();
  const sKey = document.getElementById("input-sentinel-key").value.trim();
  const mToken = document.getElementById("input-mapbox-token").value.trim();

  if (gKey) localStorage.setItem("nellore_google_key", gKey);
  if (sKey) localStorage.setItem("nellore_sentinel_key", sKey);
  if (mToken) localStorage.setItem("nellore_mapbox_token", mToken);

  alert("Credentials saved securely in your browser! Satellite and 3D services configured.");
  document.getElementById("keys-modal").classList.add("hidden");
}

// ---------------- Event Listeners & Filters ---------------- //

function setupEventListeners() {
  // 3D Tilt
  document.getElementById("btn-3d-tilt").addEventListener("click", toggle3DTilt);

  // Drone & Commute
  document.getElementById("btn-drone-mode").addEventListener("click", () => {
    if (isDroneMode) stopDroneFlyover();
    else startDroneFlyover();
  });

  document.getElementById("btn-commute-mode").addEventListener("click", () => {
    if (isCommuteMode) stopCommuteFlow();
    else startCommuteFlow();
  });

  document.getElementById("btn-hud-close").addEventListener("click", () => {
    stopDroneFlyover();
    stopCommuteFlow();
  });

  document.getElementById("btn-hud-stop").addEventListener("click", () => {
    stopDroneFlyover();
    stopCommuteFlow();
  });

  document.getElementById("btn-hud-next").addEventListener("click", () => {
    if (isDroneMode) flyToNextCheckpoint();
    else if (isCommuteMode) advanceCommuteStep();
  });

  // Layer toggles
  document.getElementById("layer-water-flow").addEventListener("change", (e) => toggleLayer(layerFlowNetwork, e.target.checked));
  document.getElementById("layer-tanks").addEventListener("change", (e) => toggleLayer(layerTanks, e.target.checked));
  document.getElementById("layer-sources").addEventListener("change", (e) => toggleLayer(layerSources, e.target.checked));
  document.getElementById("layer-water-points").addEventListener("change", (e) => toggleLayer(layerWaterPoints, e.target.checked));
  document.getElementById("layer-river").addEventListener("change", (e) => toggleLayer(layerRiver, e.target.checked));
  document.getElementById("layer-drainage").addEventListener("change", (e) => toggleLayer(layerDrainage, e.target.checked));
  document.getElementById("layer-veg-markets").addEventListener("change", (e) => toggleLayer(layerVegMarkets, e.target.checked));
  document.getElementById("layer-markets").addEventListener("change", (e) => toggleLayer(layerMarkets, e.target.checked));
  document.getElementById("layer-hospitals").addEventListener("change", (e) => toggleLayer(layerHospitals, e.target.checked));
  document.getElementById("layer-boundaries").addEventListener("change", (e) => toggleLayer(layerBoundaries, e.target.checked));

  // Mask toggle
  document.getElementById("filter-mask").addEventListener("change", (e) => {
    if (e.target.value === "DARK") {
      layerMask.setStyle({ fillOpacity: 0.72 });
    } else {
      layerMask.setStyle({ fillOpacity: 0.15 });
    }
  });

  // Network Focus Filter
  document.getElementById("filter-network-focus").addEventListener("change", (e) => {
    const focus = e.target.value;
    if (focus === "WATER_FLOW") {
      map.addLayer(layerFlowNetwork);
      map.addLayer(layerTanks);
      map.addLayer(layerSources);
      map.removeLayer(layerMarkets);
      map.removeLayer(layerVegMarkets);
      map.removeLayer(layerHospitals);
    } else if (focus === "STORAGE_TANKS") {
      map.addLayer(layerTanks);
      map.removeLayer(layerMarkets);
      map.removeLayer(layerFlowNetwork);
    } else if (focus === "ALL") {
      map.addLayer(layerFlowNetwork);
      map.addLayer(layerTanks);
      map.addLayer(layerSources);
      map.addLayer(layerWaterPoints);
      map.addLayer(layerMarkets);
      map.addLayer(layerVegMarkets);
      map.addLayer(layerHospitals);
    }
  });

  // Search
  document.getElementById("search-input").addEventListener("input", (e) => {
    const query = e.target.value.toLowerCase().trim();
    if (!query) return;

    const tankMatch = allData.overhead_tanks.features.find(f => f.properties.name.toLowerCase().includes(query));
    if (tankMatch) {
      inspectTank(tankMatch.properties);
      return;
    }

    const srcMatch = allData.underground_sources.features.find(f => f.properties.name.toLowerCase().includes(query));
    if (srcMatch) {
      inspectSource(srcMatch.properties);
      return;
    }

    const pipeMatch = allData.flow_network.features.find(f => f.properties.name.toLowerCase().includes(query));
    if (pipeMatch) {
      inspectFlowPipe(pipeMatch.properties);
    }
  });

  // API Keys Modal
  document.getElementById("btn-api-keys").addEventListener("click", () => {
    document.getElementById("keys-modal").classList.remove("hidden");
  });
  document.getElementById("btn-close-keys").addEventListener("click", () => {
    document.getElementById("keys-modal").classList.add("hidden");
  });
  document.getElementById("btn-save-keys").addEventListener("click", saveAPIKeys);

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

  // Shapefile & GeoJSON export buttons
  document.getElementById("btn-dl-flow-network").addEventListener("click", () => {
    downloadFile(JSON.stringify(allData.flow_network, null, 2), "water_distribution_flow_network.geojson", "application/json");
  });

  document.getElementById("btn-dl-tanks").addEventListener("click", () => {
    downloadFile(JSON.stringify(allData.overhead_tanks, null, 2), "overhead_storage_reservoirs_elsr.geojson", "application/json");
  });

  document.getElementById("btn-dl-boundaries").addEventListener("click", () => {
    downloadFile(JSON.stringify(allData.aoi, null, 2), "nellore_kovur_exact_boundaries.geojson", "application/json");
  });
}

function toggleLayer(layer, isChecked) {
  if (isChecked) map.addLayer(layer);
  else map.removeLayer(layer);
}

function updateStats() {
  // Reserved for live telemetry
}

function downloadFile(content, fileName, contentType) {
  const a = document.createElement("a");
  const file = new Blob([content], { type: contentType });
  a.href = URL.createObjectURL(file);
  a.download = fileName;
  a.click();
  URL.revokeObjectURL(a.href);
}
