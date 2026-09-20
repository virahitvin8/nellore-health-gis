/**
 * Chart.js Visualizations for Health GIS: Nellore City & Kovur Mandal
 */

let riskDistChart = null;
let categoryChart = null;
let featureImpChart = null;
let clusterChart = null;

function initAnalyticsCharts(data) {
  if (!window.Chart) {
    console.warn("Chart.js not loaded.");
    return;
  }

  const markets = data.markets.features.map(f => f.properties);
  const metrics = data.ai_metrics;
  const featImp = data.feature_importance;

  // 1. Risk Distribution
  const riskCounts = {
    "Very High Risk": 0,
    "High Risk": 0,
    "Moderate Risk": 0,
    "Low Risk": 0
  };

  markets.forEach(m => {
    if (riskCounts[m.risk_level] !== undefined) {
      riskCounts[m.risk_level]++;
    }
  });

  const ctxRisk = document.getElementById("chart-risk-dist");
  if (ctxRisk) {
    if (riskDistChart) riskDistChart.destroy();
    riskDistChart = new Chart(ctxRisk, {
      type: "doughnut",
      data: {
        labels: ["Very High Risk", "High Risk", "Moderate Risk", "Low Risk"],
        datasets: [{
          data: [
            riskCounts["Very High Risk"],
            riskCounts["High Risk"],
            riskCounts["Moderate Risk"],
            riskCounts["Low Risk"]
          ],
          backgroundColor: ["#d90429", "#f77f00", "#ffd166", "#06d6a0"],
          borderWidth: 2,
          borderColor: "#0f172a"
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "bottom",
            labels: { color: "#cbd5e1", font: { size: 11 } }
          }
        }
      }
    });
  }

  // 2. Category Breakdown
  const catCounts = {};
  markets.forEach(m => {
    const shortCat = m.category.split(" ")[0];
    catCounts[shortCat] = (catCounts[shortCat] || 0) + 1;
  });

  const ctxCat = document.getElementById("chart-categories");
  if (ctxCat) {
    if (categoryChart) categoryChart.destroy();
    categoryChart = new Chart(ctxCat, {
      type: "bar",
      data: {
        labels: Object.keys(catCounts),
        datasets: [{
          label: "Number of Stalls",
          data: Object.values(catCounts),
          backgroundColor: "#3b82f6",
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: { ticks: { color: "#94a3b8" }, grid: { color: "#334155" } },
          x: { ticks: { color: "#94a3b8" }, grid: { display: false } }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }

  // 3. AI Feature Importance
  const ctxFeat = document.getElementById("chart-feature-imp");
  if (ctxFeat && featImp) {
    if (featureImpChart) featureImpChart.destroy();

    const featureLabelMap = {
      "distance_to_drain_m": "Proximity to Drain",
      "distance_to_waterbody_m": "Distance to River/Canal",
      "daily_animals_handled": "Daily Animals Volume",
      "distance_to_hospital_m": "Distance to Hospital",
      "waste_severity_score": "Waste Disposal Method",
      "market_crowd_index": "Crowd Density Index",
      "slaughter_flag": "Live On-Site Slaughter",
      "refrig_flag": "Refrigeration Status",
      "category_code": "Commodity Type"
    };

    featureImpChart = new Chart(ctxFeat, {
      type: "bar",
      indexAxis: "y",
      data: {
        labels: featImp.map(f => featureLabelMap[f.feature] || f.feature),
        datasets: [{
          label: "Random Forest Importance (%)",
          data: featImp.map(f => (f.importance * 100).toFixed(1)),
          backgroundColor: "#ec4899",
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        scales: {
          x: { ticks: { color: "#94a3b8" }, grid: { color: "#334155" } },
          y: { ticks: { color: "#94a3b8" }, grid: { display: false } }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }

  // 4. Top Geographic Clusters by Mean Geo-Risk Score
  const clusterScores = {};
  const clusterCounts = {};
  markets.forEach(m => {
    const hub = m.cluster_hub.split(" ")[0];
    clusterScores[hub] = (clusterScores[hub] || 0) + m.composite_geo_risk_score;
    clusterCounts[hub] = (clusterCounts[hub] || 0) + 1;
  });

  const clusterMeans = Object.keys(clusterScores).map(h => ({
    hub: h,
    avgScore: (clusterScores[h] / clusterCounts[h]).toFixed(1)
  })).sort((a, b) => b.avgScore - a.avgScore);

  const ctxClusters = document.getElementById("chart-clusters");
  if (ctxClusters) {
    if (clusterChart) clusterChart.destroy();
    clusterChart = new Chart(ctxClusters, {
      type: "bar",
      data: {
        labels: clusterMeans.map(c => c.hub),
        datasets: [{
          label: "Average Geo-Risk Score (0-100)",
          data: clusterMeans.map(c => c.avgScore),
          backgroundColor: clusterMeans.map(c => c.avgScore >= 65 ? "#d90429" : c.avgScore >= 50 ? "#f77f00" : "#ffd166"),
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: { min: 0, max: 100, ticks: { color: "#94a3b8" }, grid: { color: "#334155" } },
          x: { ticks: { color: "#94a3b8" }, grid: { display: false } }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }
}
