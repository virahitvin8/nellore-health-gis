/**
 * Main WebGIS Application Controller
 * Health GIS & Geo-Risk Analytics: Nellore City & Kovur Mandal
 */

let map;
let allData = null;

// Layer Groups
let layerBoundaries;
let layerRiver;
let layerDrainage;
let layerHospitals;
let layerMarkets;
let layerBuffers250;
let layerBuffers500;
let simMarker = null;
let isSimulationMode = false;

// Active filtered markers array
let activeMarketMarkers = [];

document.addEventListener("DOMContentLoaded", () => {
  initDataAndMap();
  setupEventListeners();
});

function initDataAndMap() {
  // Use embedded data bundle
  if (typeof HEALTH_GIS_DATA !== "undefined") {
    allData = HEALTH_GIS_DATA;
    buildWebGIS();
  } else {
    // Fallback: Fetch from data/embedded_data.js
    console.warn("Embedded data variable not immediately found, waiting...");
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

  // Zoom control top-right
  L.control.zoom({ position: "topright" }).addTo(map);

  // Scale bar
  L.control.scale({ position: "bottomleft", metric: true, imperial: false }).addTo(map);

  // 2. Base Tile Layers
  const darkMatter = L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
    attribution: '&copy; <a href="https://carto.com/">CARTO</a> &copy; <a href="https://openstreetmap.org">OSM</a>',
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
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
    maxZoom: 18
  });

  const baseMaps = {
    "CartoDB Dark Theme": darkMatter,
    "CartoDB Light Theme": positron,
    "OpenStreetMap Standard": osmStandard,
    "Esri Satellite Imagery": esriSatellite
  };

  L.control.layers(baseMaps, null, { position: "topright" }).addTo(map);

  // 3. Initialize Feature Layers
  initVectorLayers();

  // 4. Update Header KPI Badges
  updateHeaderKPIs();

  // 5. Initialize Analytics
  initAnalyticsCharts(allData);
}

function initVectorLayers() {
  // A. Boundaries Layer
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
      layer.bindTooltip(`<strong>${p.name}</strong><br>${p.type} • Est Pop: ${p.population_est.toLocaleString()}`, {
        sticky: true
      });
    }
  }).addTo(map);

  // B. River Basin & Canals Layer
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

  // C. Open Drainage & Sewage Network
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

  // D. Healthcare Facilities Layer
  layerHospitals = L.geoJSON(allData.hospitals, {
    pointToLayer: (feature, latlng) => {
      const p = feature.properties;
      const html = `<div class="hospital-marker-icon" title="${p.name}"><i class="fa-solid fa-plus"></i></div>`;
      const icon = L.divIcon({
        html: html,
        className: "",
        iconSize: [24, 24],
        iconAnchor: [12, 12]
      });
      return L.marker(latlng, { icon: icon });
    },
    onEachFeature: (feature, layer) => {
      const p = feature.properties;
      layer.bindPopup(`
        <div style="color:#f8fafc; font-size:12px;">
          <strong style="font-size:13px; color:#38bdf8;">🏥 ${p.name}</strong><br>
          Facility Type: <em>${p.facility_type}</em><br>
          Beds: <strong>${p.bed_capacity}</strong><br>
          Emergency: ${p.emergency_service}
        </div>
      `);
    }
  }).addTo(map);

  // E. Risk Exposure Buffers (250m & 500m)
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
    },
    onEachFeature: (feature, layer) => {
      const p = feature.properties;
      layer.bindTooltip(`<strong>${p.shop_name}</strong><br>${p.exposure_zone}`, { sticky: true });
    }
  }); // Unchecked by default

  layerBuffers500 = L.geoJSON(allData.buffers_500, {
    style: {
      color: "#f59e0b",
      weight: 1,
      fillColor: "#f59e0b",
      fillOpacity: 0.08,
      dashArray: "4, 6"
    },
    onEachFeature: (feature, layer) => {
      const p = feature.properties;
      layer.bindTooltip(`<strong>${p.shop_name}</strong><br>${p.exposure_zone}`, { sticky: true });
    }
  }); // Unchecked by default

  // F. Wet Markets Layer (Dynamic)
  layerMarkets = L.layerGroup().addTo(map);
  renderMarketMarkers(allData.markets.features);
}

function renderMarketMarkers(features) {
  layerMarkets.clearLayers();
  activeMarketMarkers = [];

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

    // Popup content
    const popupHtml = `
      <div style="font-size:12px; min-width:180px;">
        <div class="custom-popup-title" style="color:${p.marker_color};">${p.shop_name}</div>
        <div class="custom-popup-sub">ID: ${p.shop_id} • ${p.category}</div>
        <div>Risk Score: <strong>${p.composite_geo_risk_score} / 100</strong></div>
        <div>Drain Distance: <strong>${p.distance_to_drain_m}m</strong></div>
        <button class="btn-popup-inspect" onclick="inspectMarket('${p.shop_id}')">Inspect Market</button>
      </div>
    `;

    marker.bindPopup(popupHtml);
    marker.on("click", () => inspectMarket(p.shop_id));

    layerMarkets.addLayer(marker);
    activeMarketMarkers.push({ feature: feat, marker: marker });
  });

  document.getElementById("stat-total-markets").textContent = features.length;
}

window.inspectMarket = function(shopId) {
  const item = allData.markets.features.find(f => f.properties.shop_id === shopId);
  if (!item) return;

  const p = item.properties;
  const inspector = document.getElementById("inspector-content");

  // Determine badge class
  let riskBadgeColor = p.marker_color;

  inspector.innerHTML = `
    <div class="market-detail-card">
      <div class="md-header">
        <div>
          <div class="md-title">${p.shop_name}</div>
          <div class="md-id">${p.shop_id} • ${p.mandal_zone} (${p.cluster_hub})</div>
        </div>
        <span class="risk-badge" style="background:${riskBadgeColor}">${p.risk_level}</span>
      </div>

      <div class="score-meter">
        <div class="meter-label">
          <span>Geo-Risk Index Score</span>
          <span style="color:${riskBadgeColor}">${p.composite_geo_risk_score} / 100</span>
        </div>
        <div class="progress-bar-bg">
          <div class="progress-bar-fill" style="width:${p.composite_geo_risk_score}%; background:${riskBadgeColor};"></div>
        </div>
        <div class="ai-prediction-pill">
          <i class="fa-solid fa-robot"></i> AI Prediction: <strong>${p.ai_predicted_risk}</strong> (${p.ai_prediction_confidence}% Conf.)
        </div>
      </div>

      <table class="detail-table">
        <tr>
          <td>Commodity:</td>
          <td>${p.category}</td>
        </tr>
        <tr>
          <td>Daily Animals/Fish:</td>
          <td>${p.daily_animals_handled} units/day</td>
        </tr>
        <tr>
          <td>Animal Supply Origin:</td>
          <td>${p.animal_origin}</td>
        </tr>
        <tr>
          <td>Destination Flow:</td>
          <td>${p.animal_destination}</td>
        </tr>
        <tr>
          <td>On-Premise Live Slaughter:</td>
          <td><strong style="color:${p.slaughter_on_site === 'Yes' ? '#f87171' : '#4ade80'}">${p.slaughter_on_site}</strong></td>
        </tr>
        <tr>
          <td>Cold Storage Refrigeration:</td>
          <td><strong style="color:${p.refrigeration_available === 'Yes' ? '#4ade80' : '#f87171'}">${p.refrigeration_available}</strong></td>
        </tr>
        <tr>
          <td>Waste Disposal:</td>
          <td>${p.waste_disposal_method}</td>
        </tr>
        <tr>
          <td>Distance to Open Drain:</td>
          <td><strong style="color:${p.distance_to_drain_m < 50 ? '#ef4444' : '#e2e8f0'}">${p.distance_to_drain_m} meters</strong></td>
        </tr>
        <tr>
          <td>Nearest Healthcare Centre:</td>
          <td>${p.distance_to_hospital_m} meters</td>
        </tr>
        <tr>
          <td>Market Crowd Intensity:</td>
          <td>${p.market_crowd_index} / 10</td>
        </tr>
      </table>

      <div class="intervention-alert">
        <strong><i class="fa-solid fa-triangle-exclamation"></i> Municipal Action Required:</strong>
        ${p.recommended_intervention}
      </div>
    </div>
  `;

  // Pan to marker
  const [lon, lat] = item.geometry.coordinates;
  map.setView([lat, lon], 16, { animate: true });
};

function updateHeaderKPIs() {
  const features = allData.markets.features;
  const critical = features.filter(f => f.properties.risk_level === "Very High Risk" || f.properties.risk_level === "High Risk").length;
  document.getElementById("stat-total-markets").textContent = features.length;
  document.getElementById("stat-critical-markets").textContent = critical;

  // Modal KPI
  const veryHigh = features.filter(f => f.properties.risk_level === "Very High Risk").length;
  const drainDumping = features.filter(f => f.properties.waste_disposal_method === "Direct Open Drain Discharge").length;
  
  if (document.getElementById("kpi-total")) document.getElementById("kpi-total").textContent = features.length;
  if (document.getElementById("kpi-very-high")) document.getElementById("kpi-very-high").textContent = veryHigh;
  if (document.getElementById("kpi-drain-dumping")) document.getElementById("kpi-drain-dumping").textContent = drainDumping;
  if (document.getElementById("kpi-ai-acc") && allData.ai_metrics) {
    document.getElementById("kpi-ai-acc").textContent = (allData.ai_metrics.test_accuracy * 100).toFixed(1) + "%";
  }
}

function setupEventListeners() {
  // Layer Toggles
  document.getElementById("layer-markets").addEventListener("change", (e) => {
    if (e.target.checked) map.addLayer(layerMarkets);
    else map.removeLayer(layerMarkets);
  });

  document.getElementById("layer-buffers-250").addEventListener("change", (e) => {
    if (e.target.checked) map.addLayer(layerBuffers250);
    else map.removeLayer(layerBuffers250);
  });

  document.getElementById("layer-buffers-500").addEventListener("change", (e) => {
    if (e.target.checked) map.addLayer(layerBuffers500);
    else map.removeLayer(layerBuffers500);
  });

  document.getElementById("layer-drainage").addEventListener("change", (e) => {
    if (e.target.checked) map.addLayer(layerDrainage);
    else map.removeLayer(layerDrainage);
  });

  document.getElementById("layer-river").addEventListener("change", (e) => {
    if (e.target.checked) map.addLayer(layerRiver);
    else map.removeLayer(layerRiver);
  });

  document.getElementById("layer-hospitals").addEventListener("change", (e) => {
    if (e.target.checked) map.addLayer(layerHospitals);
    else map.removeLayer(layerHospitals);
  });

  document.getElementById("layer-boundaries").addEventListener("change", (e) => {
    if (e.target.checked) map.addLayer(layerBoundaries);
    else map.removeLayer(layerBoundaries);
  });

  // Filter triggers
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
  const analyticsModal = document.getElementById("analytics-modal");
  document.getElementById("btn-toggle-analytics").addEventListener("click", () => {
    analyticsModal.classList.remove("hidden");
  });
  document.getElementById("btn-close-analytics").addEventListener("click", () => {
    analyticsModal.classList.add("hidden");
  });

  const exportModal = document.getElementById("export-modal");
  document.getElementById("btn-export-data").addEventListener("click", () => {
    exportModal.classList.remove("hidden");
  });
  document.getElementById("btn-close-export").addEventListener("click", () => {
    exportModal.classList.add("hidden");
  });

  // Simulation Mode Toggle
  const simBanner = document.getElementById("simulation-banner");
  document.getElementById("btn-simulate-shop").addEventListener("click", () => {
    isSimulationMode = true;
    simBanner.classList.remove("hidden");
    map.getContainer().style.cursor = "crosshair";
  });

  document.getElementById("btn-cancel-sim").addEventListener("click", () => {
    exitSimulationMode();
  });

  map.on("click", (e) => {
    if (!isSimulationMode) return;
    evaluateSimulatedLocation(e.latlng);
  });

  document.getElementById("btn-close-sim").addEventListener("click", () => {
    document.getElementById("sim-result-modal").classList.add("hidden");
  });

  // Export actions
  document.getElementById("btn-dl-geojson").addEventListener("click", () => {
    downloadFile(JSON.stringify(allData.markets, null, 2), "nellore_kovur_wet_markets_georisk.geojson", "application/json");
  });

  document.getElementById("btn-dl-buffers").addEventListener("click", () => {
    downloadFile(JSON.stringify(allData.buffers_250, null, 2), "market_risk_buffers_250m.geojson", "application/json");
  });

  document.getElementById("btn-dl-csv").addEventListener("click", exportCSV);
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

    if (search) {
      const matchName = p.shop_name.toLowerCase().includes(search);
      const matchId = p.shop_id.toLowerCase().includes(search);
      const matchHub = p.cluster_hub.toLowerCase().includes(search);
      if (!matchName && !matchId && !matchHub) return false;
    }

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

  // Approximate distance to drains
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

  // River distance (approx lat 14.463)
  const riverDist = Math.round(Math.abs(lat - 14.463) * 110574);

  // Calculate synthetic score based on standard default assumptions
  const normDrain = Math.max(0, Math.min(1, (300 - minDrainDist) / 280));
  const normSlaughter = 1.0; // default assuming wet market live slaughter
  const normWaste = minDrainDist < 50 ? 1.0 : 0.4;
  const normCrowd = 0.7;
  const normColdchain = 0.9;
  const normVolume = 0.5;
  const normWater = Math.max(0, Math.min(1, (2500 - riverDist) / 2300));

  const score = Math.round((
    (0.25 * normDrain) +
    (0.15 * normSlaughter) +
    (0.20 * normWaste) +
    (0.15 * normCrowd) +
    (0.10 * normColdchain) +
    (0.10 * normVolume) +
    (0.05 * normWater)
  ) * 100);

  let recommendation;
  let statusClass;
  let permitDecision;

  if (score >= 72 || minDrainDist < 30) {
    statusClass = "danger";
    permitDecision = "🚨 PERMIT REJECTED (High Zoonotic Risk)";
    recommendation = `Location is only <strong>${minDrainDist}m</strong> from an open municipal sullage drain. Mandate 100m bio-setback distance or relocate to formal NMC abattoir zone.`;
  } else if (score >= 56) {
    statusClass = "warning";
    permitDecision = "⚠️ CONDITIONAL PERMIT (Sanitary Covenants Required)";
    recommendation = `Permit contingent on closed bio-waste traps, mandatory zero-discharge into nearby drainage (${minDrainDist}m), and verified cold storage refrigeration.`;
  } else {
    statusClass = "info";
    permitDecision = "✅ PERMIT APPROVED (Standard Food Safety Protocol)";
    recommendation = `Adequate spatial separation from open drainage lines (${minDrainDist}m). Standard municipal sanitation inspection schedule applies.`;
  }

  // Add or update simulation marker
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

// Distance helper
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

// Download helper
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
  const rows = features.map(f => {
    return headers.map(h => {
      const val = f.properties[h] !== undefined ? f.properties[h] : "";
      return `"${String(val).replace(/"/g, '""')}"`;
    }).join(",");
  });

  const csvContent = [headers.join(","), ...rows].join("\n");
  downloadFile(csvContent, "nellore_kovur_wet_markets_classified.csv", "text/csv;charset=utf-8;");
}
