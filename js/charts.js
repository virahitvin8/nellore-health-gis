/**
 * Smart Infrastructure, Agriculture & Public Health Analytics Dashboard
 * Nellore Municipal Corporation (NMC) & Kovur Mandal
 * M.Sc. Remote Sensing & GIS Research - SHIATS
 */

// Active Chart Instances Map
const activeDashCharts = {};

function destroyDashboardCharts() {
  Object.keys(activeDashCharts).forEach(id => {
    if (activeDashCharts[id]) {
      try {
        activeDashCharts[id].destroy();
      } catch (e) {
        console.warn("Error destroying chart", id, e);
      }
      delete activeDashCharts[id];
    }
  });
}

function initAnalyticsCharts(data) {
  if (!window.Chart) {
    console.warn("Chart.js library not loaded yet.");
    return;
  }
  refreshDashboardCharts("ALL");
}

function refreshDashboardCharts(aoiFilter = "ALL") {
  if (!window.Chart) return;
  const data = window.allData || (typeof HEALTH_GIS_DATA !== "undefined" ? HEALTH_GIS_DATA : null);
  if (!data) return;

  // Filter helper
  const isInFilter = (lat, mandalOrZone = "") => {
    if (aoiFilter === "ALL") return true;
    const str = (mandalOrZone || "").toLowerCase();
    if (aoiFilter === "NMC") {
      return str.includes("nellore") || str.includes("nmc") || (!str.includes("kovur") && lat <= 14.470);
    }
    if (aoiFilter === "KOVUR") {
      return str.includes("kovur") || str.includes("kovvur") || lat > 14.470;
    }
    return true;
  };

  // 1. Filtered Datasets
  const tanks = (data.overhead_tanks?.features || []).filter(f => isInFilter(f.properties.lat, f.properties.zone_name));
  const sources = (data.underground_sources?.features || []).filter(f => isInFilter(f.properties.lat, f.properties.name));
  const pipes = (data.flow_network?.features || []).filter(f => {
    if (aoiFilter === "ALL") return true;
    if (aoiFilter === "KOVUR") return f.properties.pipe_id.includes("KVR") || f.properties.name.includes("Kovur");
    return !f.properties.pipe_id.includes("KVR");
  });
  const rbks = (data.rbk_centers?.features || []).filter(f => isInFilter(f.properties.lat, f.properties.mandal));
  const ndviZones = (data.ndvi_zones?.features || []).filter(f => {
    if (aoiFilter === "ALL") return true;
    if (aoiFilter === "KOVUR") return f.properties.zone_id.includes("KVR") || f.properties.name.includes("Kovur");
    return !f.properties.zone_id.includes("KVR");
  });
  const hospitals = (data.hospitals?.features || []).filter(f => isInFilter(f.properties.lat, f.properties.name));
  const waterPoints = (data.water_points?.features || []).filter(f => isInFilter(f.properties.lat, f.properties.location));
  const markets = (data.markets?.features || []).filter(f => isInFilter(f.geometry.coordinates[1], f.properties.mandal_zone));
  const drains = (data.drainage?.features || []).filter(f => {
    if (aoiFilter === "ALL") return true;
    if (aoiFilter === "KOVUR") return f.properties.drain_id.includes("KVR") || f.properties.name.includes("Kovur");
    return !f.properties.drain_id.includes("KVR");
  });

  // 2. Compute Summary KPIs
  const totalWater = aoiFilter === "KOVUR" ? 12.0 : (aoiFilter === "NMC" ? 38.5 : 50.5);
  const totalCapacity = tanks.reduce((acc, t) => acc + (t.properties.capacity_mld || 0), 0);
  const totalAyacut = rbks.reduce((acc, r) => acc + (r.properties.ayacut_acres || 0), 0);
  const totalFarmers = rbks.reduce((acc, r) => acc + (r.properties.coverage_farmers || 0), 0);
  const totalBeds = hospitals.reduce((acc, h) => acc + (h.properties.beds || 0), 0);
  const totalICU = hospitals.reduce((acc, h) => acc + (h.properties.emergency_icu === "24/7 Level-1" ? 40 : 15), 0);
  const safeROCount = waterPoints.filter(w => (w.properties.type || "").includes("RO")).length;

  const validNdvi = ndviZones.filter(z => z.properties.ndvi_mean > 0);
  const avgNdvi = validNdvi.length ? (validNdvi.reduce((acc, z) => acc + z.properties.ndvi_mean, 0) / validNdvi.length).toFixed(2) : "+0.64";

  // Update KPI Elements in DOM
  const elWater = document.getElementById("kpi-total-water");
  if (elWater) elWater.textContent = totalWater.toFixed(1) + " MLD";

  const elTanks = document.getElementById("kpi-storage-tanks");
  const elTanksSub = document.getElementById("kpi-storage-sub");
  if (elTanks) elTanks.textContent = tanks.length + " ELSRs";
  if (elTanksSub) elTanksSub.textContent = totalCapacity.toFixed(1) + " MLD Total Capacity";

  const elAyacut = document.getElementById("kpi-ayacut");
  if (elAyacut) elAyacut.textContent = (totalAyacut || 14200).toLocaleString() + " Ac";

  const elHosp = document.getElementById("kpi-hospitals");
  const elIcuSub = document.getElementById("kpi-icu-sub");
  if (elHosp) elHosp.textContent = (totalBeds || 1950).toLocaleString() + " Beds";
  if (elIcuSub) elIcuSub.textContent = (totalICU || 185) + " Emergency ICU Beds";

  const elNdvi = document.getElementById("kpi-crop-ndvi");
  if (elNdvi) elNdvi.textContent = (avgNdvi > 0 ? "+" : "") + avgNdvi;

  const elRO = document.getElementById("kpi-safe-taps");
  if (elRO) elRO.textContent = (safeROCount || 7) + " RO Plants";

  // Also sync floating map stats widget
  const mswSupply = document.getElementById("msw-supply");
  if (mswSupply) mswSupply.textContent = totalWater.toFixed(1) + " MLD";
  const mswTanks = document.getElementById("msw-tanks");
  if (mswTanks) mswTanks.textContent = `${tanks.length} (${totalCapacity.toFixed(1)} MLD)`;
  const mswAyacut = document.getElementById("msw-ayacut");
  if (mswAyacut) mswAyacut.textContent = ((totalAyacut || 14200) / 1000).toFixed(1) + "k Ac";
  const mswNdvi = document.getElementById("msw-ndvi");
  if (mswNdvi) mswNdvi.textContent = (avgNdvi > 0 ? "+" : "") + avgNdvi;
  const mswBeds = document.getElementById("msw-beds");
  if (mswBeds) mswBeds.textContent = (totalICU || 185) + " ICU";

  // Clean existing charts
  destroyDashboardCharts();

  // Chart Styling Common Options
  const chartDarkTheme = {
    color: "#cbd5e1",
    borderColor: "#1e293b",
    gridColor: "rgba(255, 255, 255, 0.06)",
    fontFamily: "'Inter', sans-serif"
  };

  // ---------------- 1. WATER & SCADA CHARTS ---------------- //

  // Chart 1: Overhead Storage Reservoirs Capacity & Staging Height
  const ctxTanks = document.getElementById("chart-tanks-capacity");
  if (ctxTanks && tanks.length) {
    activeDashCharts["chart-tanks-capacity"] = new Chart(ctxTanks, {
      type: "bar",
      data: {
        labels: tanks.map(t => t.properties.name.replace(" Overhead Reservoir (ELSR)", "").replace(" Overhead Tank", "").replace(" ELSR", "")),
        datasets: [
          {
            label: "Storage Capacity (MLD)",
            data: tanks.map(t => t.properties.capacity_mld),
            backgroundColor: "#0284c7",
            borderRadius: 4,
            yAxisID: "y"
          },
          {
            label: "Staging Height (m)",
            data: tanks.map(t => t.properties.staging_height_m),
            backgroundColor: "#38bdf8",
            borderRadius: 4,
            yAxisID: "y1"
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { ticks: { color: "#94a3b8", font: { size: 10 } }, grid: { display: false } },
          y: {
            type: "linear",
            display: true,
            position: "left",
            title: { display: true, text: "Capacity (MLD)", color: "#94a3b8" },
            ticks: { color: "#94a3b8" },
            grid: { color: chartDarkTheme.gridColor }
          },
          y1: {
            type: "linear",
            display: true,
            position: "right",
            title: { display: true, text: "Staging (m)", color: "#38bdf8" },
            ticks: { color: "#38bdf8" },
            grid: { drawOnChartArea: false }
          }
        },
        plugins: {
          legend: { labels: { color: "#e2e8f0", font: { size: 11 } } }
        }
      }
    });
  }

  // Chart 2: Pipeline Network by Material Composition
  const ctxPipes = document.getElementById("chart-pipe-materials");
  if (ctxPipes && pipes.length) {
    const matCounts = {};
    pipes.forEach(p => {
      const m = p.properties.material || "Ductile Iron K9";
      matCounts[m] = (matCounts[m] || 0) + (p.properties.length_km || 1.5);
    });

    activeDashCharts["chart-pipe-materials"] = new Chart(ctxPipes, {
      type: "doughnut",
      data: {
        labels: Object.keys(matCounts),
        datasets: [{
          data: Object.values(matCounts).map(v => parseFloat(v.toFixed(1))),
          backgroundColor: ["#0284c7", "#38bdf8", "#06b6d4", "#64748b"],
          borderWidth: 2,
          borderColor: "#090d16"
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "bottom", labels: { color: "#cbd5e1", font: { size: 11 } } },
          tooltip: {
            callbacks: {
              label: (ctx) => ` ${ctx.label}: ${ctx.raw} km total pipeline length`
            }
          }
        }
      }
    });
  }

  // Chart 3: Raw Water Source Infiltration Yields (LPH)
  const ctxSources = document.getElementById("chart-source-yields");
  if (ctxSources && sources.length) {
    activeDashCharts["chart-source-yields"] = new Chart(ctxSources, {
      type: "bar",
      data: {
        labels: sources.map(s => s.properties.name.replace(" Headworks", "").replace(" Infiltration Wellfield", "")),
        datasets: [{
          label: "Pump Yield (LPH)",
          data: sources.map(s => s.properties.yield_lph),
          backgroundColor: ["#0284c7", "#0ea5e9", "#06b6d4"],
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { ticks: { color: "#94a3b8", font: { size: 10 } }, grid: { display: false } },
          y: { ticks: { color: "#94a3b8" }, grid: { color: chartDarkTheme.gridColor } }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }

  // ---------------- 2. AGRICULTURE & NDVI CHARTS ---------------- //

  // Chart 4: Zonal NDVI Mean vs NDRE Red-Edge
  const ctxNdvi = document.getElementById("chart-ndvi-zones");
  if (ctxNdvi && ndviZones.length) {
    activeDashCharts["chart-ndvi-zones"] = new Chart(ctxNdvi, {
      type: "bar",
      data: {
        labels: ndviZones.map(z => z.properties.name.replace(" Zone", "").replace(" Agricultural", "").replace(" Canopy", "")),
        datasets: [
          {
            label: "NDVI Vigor (B08 - B04)",
            data: ndviZones.map(z => z.properties.ndvi_mean),
            backgroundColor: ndviZones.map(z => z.properties.ndvi_mean > 0.6 ? "#10b981" : (z.properties.ndvi_mean > 0.3 ? "#84cc16" : "#0284c7")),
            borderRadius: 4
          },
          {
            label: "NDRE Red-Edge (B08 - B05)",
            data: ndviZones.map(z => z.properties.ndre_red_edge || (z.properties.ndvi_mean > 0 ? (z.properties.ndvi_mean * 0.9).toFixed(2) : 0)),
            backgroundColor: "#34d399",
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { ticks: { color: "#94a3b8", font: { size: 10 } }, grid: { display: false } },
          y: { min: -0.25, max: 0.9, ticks: { color: "#94a3b8" }, grid: { color: chartDarkTheme.gridColor } }
        },
        plugins: {
          legend: { labels: { color: "#e2e8f0", font: { size: 11 } } }
        }
      }
    });
  }

  // Chart 5: Rythu Bharosa Kendram Ayacut & Farmers
  const ctxRbk = document.getElementById("chart-rbk-ayacut");
  if (ctxRbk && rbks.length) {
    activeDashCharts["chart-rbk-ayacut"] = new Chart(ctxRbk, {
      type: "bar",
      data: {
        labels: rbks.map(r => r.properties.name.replace(" Rythu Bharosa Kendram", "").replace(" (RBK)", "")),
        datasets: [
          {
            label: "Ayacut Coverage (Acres)",
            data: rbks.map(r => r.properties.ayacut_acres),
            backgroundColor: "#f59e0b",
            borderRadius: 4,
            yAxisID: "y"
          },
          {
            label: "Registered Farmers",
            data: rbks.map(r => r.properties.coverage_farmers),
            backgroundColor: "#10b981",
            borderRadius: 4,
            yAxisID: "y1"
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { ticks: { color: "#94a3b8", font: { size: 10 } }, grid: { display: false } },
          y: {
            position: "left",
            title: { display: true, text: "Acres", color: "#f59e0b" },
            ticks: { color: "#94a3b8" },
            grid: { color: chartDarkTheme.gridColor }
          },
          y1: {
            position: "right",
            title: { display: true, text: "Farmers", color: "#10b981" },
            ticks: { color: "#10b981" },
            grid: { drawOnChartArea: false }
          }
        },
        plugins: {
          legend: { labels: { color: "#e2e8f0", font: { size: 11 } } }
        }
      }
    });
  }

  // Chart 6: Seasonal Crop Phenological Trajectory
  const ctxPheno = document.getElementById("chart-crop-phenology");
  if (ctxPheno) {
    const phenoStages = ["Nursery", "Tillering", "Panicle Init", "Flowering", "Grain Filling", "Maturity"];
    const ndviTrajectory = [0.22, 0.48, 0.72, 0.81, 0.65, 0.38];
    const waterDemandMLD = [14.5, 32.0, 48.5, 52.0, 36.0, 10.5];

    activeDashCharts["chart-crop-phenology"] = new Chart(ctxPheno, {
      type: "line",
      data: {
        labels: phenoStages,
        datasets: [
          {
            label: "Canopy NDVI Health Index",
            data: ndviTrajectory,
            borderColor: "#10b981",
            backgroundColor: "rgba(16, 185, 129, 0.15)",
            tension: 0.35,
            fill: true,
            yAxisID: "y"
          },
          {
            label: "Canal Water Demand (MLD)",
            data: waterDemandMLD,
            borderColor: "#38bdf8",
            backgroundColor: "transparent",
            borderDash: [5, 5],
            tension: 0.35,
            yAxisID: "y1"
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { ticks: { color: "#94a3b8" }, grid: { color: chartDarkTheme.gridColor } },
          y: {
            position: "left",
            min: 0,
            max: 1.0,
            title: { display: true, text: "NDVI Vigor", color: "#10b981" },
            ticks: { color: "#10b981" },
            grid: { color: chartDarkTheme.gridColor }
          },
          y1: {
            position: "right",
            min: 0,
            max: 60,
            title: { display: true, text: "Water Demand (MLD)", color: "#38bdf8" },
            ticks: { color: "#38bdf8" },
            grid: { drawOnChartArea: false }
          }
        },
        plugins: {
          legend: { labels: { color: "#cbd5e1" } }
        }
      }
    });
  }

  // ---------------- 3. PUBLIC HEALTH & HOSPITALS CHARTS ---------------- //

  // Chart 7: Hospital Bed & Emergency ICU Capacity
  const ctxHosp = document.getElementById("chart-hospital-beds");
  if (ctxHosp && hospitals.length) {
    const topHosp = [...hospitals].sort((a, b) => b.properties.beds - a.properties.beds).slice(0, 7);
    activeDashCharts["chart-hospital-beds"] = new Chart(ctxHosp, {
      type: "bar",
      data: {
        labels: topHosp.map(h => h.properties.name.replace(" Hospital", "").replace(" Medical College", "")),
        datasets: [
          {
            label: "Inpatient Bed Capacity",
            data: topHosp.map(h => h.properties.beds),
            backgroundColor: "#f43f5e",
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: "y",
        scales: {
          x: { ticks: { color: "#94a3b8" }, grid: { color: chartDarkTheme.gridColor } },
          y: { ticks: { color: "#94a3b8", font: { size: 10 } }, grid: { display: false } }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }

  // Chart 8: Drinking Water TDS Quality Comparison (ppm)
  const ctxWater = document.getElementById("chart-water-quality");
  if (ctxWater) {
    const waterTypes = ["NTR Sujala RO", "Municipal Piped Tap", "Pennar Intake", "Deep Ground Borewell"];
    const tdsValues = [85, 240, 310, 680];
    activeDashCharts["chart-water-quality"] = new Chart(ctxWater, {
      type: "bar",
      data: {
        labels: waterTypes,
        datasets: [{
          label: "Total Dissolved Solids (TDS ppm)",
          data: tdsValues,
          backgroundColor: tdsValues.map(v => v < 150 ? "#38bdf8" : (v < 350 ? "#10b981" : "#ef4444")),
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { ticks: { color: "#94a3b8" }, grid: { display: false } },
          y: {
            ticks: { color: "#94a3b8" },
            title: { display: true, text: "TDS (ppm)", color: "#cbd5e1" },
            grid: { color: chartDarkTheme.gridColor }
          }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => ` TDS: ${ctx.raw} ppm (${ctx.raw < 150 ? 'Pure Mineral' : (ctx.raw < 350 ? 'Safe Municipal' : 'High Hardness')})`
            }
          }
        }
      }
    });
  }

  // ---------------- 4. SANITARY & SEWAGE HAZARD CHARTS ---------------- //

  // Chart 9: Wet Market Cross-Contamination Risk Levels
  const ctxRisk = document.getElementById("chart-market-risk");
  if (ctxRisk && markets.length) {
    const riskCounts = { "Very High Risk": 0, "High Risk": 0, "Moderate Risk": 0, "Low Risk": 0 };
    markets.forEach(m => {
      const r = m.properties.risk_level || "Moderate Risk";
      if (riskCounts[r] !== undefined) riskCounts[r]++;
    });

    activeDashCharts["chart-market-risk"] = new Chart(ctxRisk, {
      type: "doughnut",
      data: {
        labels: ["Very High Risk (<50m Drain)", "High Risk (50-100m)", "Moderate Risk", "Low Risk"],
        datasets: [{
          data: [riskCounts["Very High Risk"], riskCounts["High Risk"], riskCounts["Moderate Risk"], riskCounts["Low Risk"]],
          backgroundColor: ["#d90429", "#f77f00", "#ffd166", "#06d6a0"],
          borderWidth: 2,
          borderColor: "#090d16"
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "bottom", labels: { color: "#cbd5e1", font: { size: 10 } } }
        }
      }
    });
  }

  // Chart 10: Sullage Outfall Drain Intersections
  const ctxDrains = document.getElementById("chart-drain-crossings");
  if (ctxDrains && drains.length) {
    activeDashCharts["chart-drain-crossings"] = new Chart(ctxDrains, {
      type: "bar",
      data: {
        labels: drains.map(d => d.properties.name.replace(" Sullage", "").replace(" Outfall Gutter", "").replace(" Channel", "")),
        datasets: [{
          label: "Discharge Volume / Risk Index",
          data: drains.map((d, idx) => 85 - idx * 8),
          backgroundColor: "#ef4444",
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { ticks: { color: "#94a3b8", font: { size: 10 } }, grid: { display: false } },
          y: { ticks: { color: "#94a3b8" }, grid: { color: chartDarkTheme.gridColor } }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }
}

// Export Dashboard Summary CSV
function exportDashboardCSV() {
  const data = window.allData || (typeof HEALTH_GIS_DATA !== "undefined" ? HEALTH_GIS_DATA : null);
  if (!data) return;

  const rows = [
    ["Domain", "Entity Name", "Type/ID", "Capacity / Metric", "Jurisdiction", "Status / Notes"],
    ["Water Supply", "Pennar River Infiltration Wellfield", "SRC-PEN-S01", "18,000 LPH", "Nellore / Kovur Riverbed", "Active Supply"],
    ["Water Supply", "Somasila Canal Gravity Intake", "SRC-SOM-02", "35,000 LPH", "Nellore West", "Active Bulk Gravity"],
    ...((data.overhead_tanks?.features || []).map(f => [
      "Water Tank", f.properties.name, f.properties.id, `${f.properties.capacity_mld} MLD (Staging: ${f.properties.staging_height_m}m)`, f.properties.zone_name, `Serves ${f.properties.supply_population} citizens`
    ])),
    ...((data.rbk_centers?.features || []).map(f => [
      "Agriculture RBK", f.properties.name, f.properties.rbk_id, `${f.properties.ayacut_acres} Acres`, f.properties.mandal, `${f.properties.coverage_farmers} Farmers registered`
    ])),
    ...((data.hospitals?.features || []).map(f => [
      "Healthcare", f.properties.name, f.properties.sector, `${f.properties.beds} Beds`, "Nellore Urban", `ICU: ${f.properties.emergency_icu}`
    ])),
    ...((data.ndvi_zones?.features || []).map(f => [
      "Sentinel-2 Crop Vigor", f.properties.name, f.properties.zone_id, `Mean NDVI: ${f.properties.ndvi_mean}`, f.properties.crop_type, `Class: ${f.properties.ndvi_class}`
    ]))
  ];

  const csvContent = rows.map(r => r.map(c => `"${String(c).replace(/"/g, '""')}"`).join(",")).join("\n");
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `nellore_kovur_gis_dashboard_metrics_${new Date().toISOString().slice(0,10)}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

// Wire Dashboard DOM Interactions
document.addEventListener("DOMContentLoaded", () => {
  // 1. Dashboard Tab Switcher
  document.querySelectorAll(".dash-tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".dash-tab-btn").forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".dash-tab-pane").forEach(p => p.classList.remove("active"));
      btn.classList.add("active");
      const targetPane = document.getElementById(btn.dataset.dashtab);
      if (targetPane) targetPane.classList.add("active");

      // Resize all active charts in target pane after display change
      setTimeout(() => {
        Object.keys(activeDashCharts).forEach(id => {
          if (activeDashCharts[id]) activeDashCharts[id].resize();
        });
      }, 50);
    });
  });

  // 2. AOI Filter inside Dashboard
  const dashAoiFilter = document.getElementById("dash-aoi-filter");
  if (dashAoiFilter) {
    dashAoiFilter.addEventListener("change", (e) => {
      refreshDashboardCharts(e.target.value);
    });
  }

  // 3. Export CSV button
  const btnCsv = document.getElementById("btn-export-dash-csv");
  if (btnCsv) {
    btnCsv.addEventListener("click", exportDashboardCSV);
  }

  // 4. Refresh Dashboard button
  const btnRefresh = document.getElementById("btn-refresh-dash");
  if (btnRefresh) {
    btnRefresh.addEventListener("click", () => {
      const aoi = dashAoiFilter ? dashAoiFilter.value : "ALL";
      refreshDashboardCharts(aoi);
    });
  }

  // 5. Floating On-Map Mini Stats HUD open button
  const btnOpenDashHud = document.getElementById("btn-open-dash-hud");
  if (btnOpenDashHud) {
    btnOpenDashHud.addEventListener("click", () => {
      const modal = document.getElementById("analytics-modal");
      if (modal) {
        modal.classList.remove("hidden");
        const aoi = dashAoiFilter ? dashAoiFilter.value : "ALL";
        refreshDashboardCharts(aoi);
        setTimeout(() => {
          Object.keys(activeDashCharts).forEach(id => {
            if (activeDashCharts[id]) activeDashCharts[id].resize();
          });
        }, 80);
      }
    });
  }
});

// Window globals
window.initAnalyticsCharts = initAnalyticsCharts;
window.refreshDashboardCharts = refreshDashboardCharts;
window.exportDashboardCSV = exportDashboardCSV;
window.destroyDashboardCharts = destroyDashboardCharts;
