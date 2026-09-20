"""
Compiles all GeoJSON layers into a self-contained JavaScript bundle (data/embedded_data.js)
so the WebGIS dashboard works instantly both over HTTP/GitHub Pages and offline via file://.
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")

def build_embedded_bundle():
    layers = {}

    # 1. Boundaries
    with open(os.path.join(DATA_DIR, "boundaries", "nellore_kovur_aoi.geojson")) as f:
        layers["aoi"] = json.load(f)

    with open(os.path.join(DATA_DIR, "boundaries", "nellore_corporation_boundary.geojson")) as f:
        layers["nellore_boundary"] = json.load(f)

    with open(os.path.join(DATA_DIR, "boundaries", "kovur_mandal_boundary.geojson")) as f:
        layers["kovur_boundary"] = json.load(f)

    # 2. Environmental & Infrastructure
    with open(os.path.join(DATA_DIR, "infrastructure", "pennar_river_waterbodies.geojson")) as f:
        layers["waterbodies"] = json.load(f)

    with open(os.path.join(DATA_DIR, "infrastructure", "open_drainage_sewage_network.geojson")) as f:
        layers["drainage"] = json.load(f)

    with open(os.path.join(DATA_DIR, "infrastructure", "healthcare_facilities.geojson")) as f:
        layers["hospitals"] = json.load(f)

    # 3. Markets & Risk
    with open(os.path.join(DATA_DIR, "risk_analysis", "market_geo_risk_classified.geojson")) as f:
        layers["markets"] = json.load(f)

    with open(os.path.join(DATA_DIR, "risk_analysis", "market_risk_buffers_250m.geojson")) as f:
        layers["buffers_250"] = json.load(f)

    with open(os.path.join(DATA_DIR, "risk_analysis", "market_risk_buffers_500m.geojson")) as f:
        layers["buffers_500"] = json.load(f)

    # 4. Model Metrics
    with open(os.path.join(MODELS_DIR, "model_evaluation_metrics.json")) as f:
        layers["ai_metrics"] = json.load(f)

    with open(os.path.join(MODELS_DIR, "feature_importance.json")) as f:
        layers["feature_importance"] = json.load(f)

    output_path = os.path.join(DATA_DIR, "embedded_data.js")
    with open(output_path, "w") as f:
        f.write("// Auto-generated Health GIS Nellore & Kovur Spatial Data Bundle\n")
        f.write(f"const HEALTH_GIS_DATA = {json.dumps(layers, indent=2)};\n")

    print(f"Generated {output_path} successfully!")

if __name__ == "__main__":
    build_embedded_bundle()
