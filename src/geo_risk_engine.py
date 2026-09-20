"""
Spatial Geo-Risk Index Engine for Health GIS: Nellore City & Kovur Mandal
Implements Multi-Criteria Spatial Decision Analysis (MCSDA) and Buffer Generation.
Formula: Geo-Risk Score = SUM(Weight_i * Normalized_Indicator_i) * 100
"""

import json
import csv
import math
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def calculate_geo_risk():
    input_file = os.path.join(DATA_DIR, "markets", "wet_markets_inventory.json")
    # Read from the generated GeoJSON
    with open(os.path.join(DATA_DIR, "markets", "wet_markets_inventory.geojson")) as f:
        data = json.load(f)

    classified_features = []
    summary_counts = {"Low Risk": 0, "Moderate Risk": 0, "High Risk": 0, "Very High Risk": 0}

    # Weight definitions (sum = 1.00)
    W_DRAIN = 0.25      # Proximity to open drainage/sewage
    W_SLAUGHTER = 0.15  # On-site live slaughter
    W_WASTE = 0.20      # Waste disposal practice
    W_CROWD = 0.15      # Crowd index (human-animal contact)
    W_COLDCHAIN = 0.10  # Absence of refrigeration
    W_VOLUME = 0.10     # Daily animal volume
    W_WATERBODY = 0.05  # Distance to Pennar River / Canal

    for feat in data["features"]:
        p = feat["properties"]

        # 1. Drainage proximity score (higher score = closer to drain = higher risk)
        # If distance < 20m -> 1.0, if > 300m -> 0.0
        drain_dist = p["distance_to_drain_m"]
        norm_drain = max(0.0, min(1.0, (300.0 - drain_dist) / 280.0))

        # 2. On-site slaughter
        norm_slaughter = 1.0 if p["slaughter_on_site"] == "Yes" else 0.15

        # 3. Waste disposal method
        waste_map = {
            "Direct Open Drain Discharge": 1.0,
            "Open Dumping on Ground": 0.85,
            "Municipal Waste Bin": 0.35,
            "Closed Bin Collection": 0.10
        }
        norm_waste = waste_map.get(p["waste_disposal_method"], 0.5)

        # 4. Crowd index (1 to 10 -> 0.1 to 1.0)
        norm_crowd = min(1.0, max(0.1, p["market_crowd_index"] / 10.0))

        # 5. Cold chain / Refrigeration (No refrigeration = 1.0, Has refrigeration = 0.1)
        norm_coldchain = 1.0 if p["refrigeration_available"] == "No" else 0.15

        # 6. Daily volume (0 to 450)
        norm_volume = min(1.0, p["daily_animals_handled"] / 450.0)

        # 7. River / Waterbody proximity (< 200m -> 1.0, > 2500m -> 0.0)
        riv_dist = p["distance_to_waterbody_m"]
        norm_water = max(0.0, min(1.0, (2500.0 - riv_dist) / 2300.0))

        # Composite score calculation (0 - 100)
        composite_score = (
            (W_DRAIN * norm_drain) +
            (W_SLAUGHTER * norm_slaughter) +
            (W_WASTE * norm_waste) +
            (W_CROWD * norm_crowd) +
            (W_COLDCHAIN * norm_coldchain) +
            (W_VOLUME * norm_volume) +
            (W_WATERBODY * norm_water)
        ) * 100.0

        composite_score = round(composite_score, 2)

        # Classification
        if composite_score >= 72.0:
            risk_class = "Very High Risk"
            intervention = "Immediate bio-sanitation audit; mandatory effluent interceptor; drain covering within 50m; live slaughter inspection."
            marker_color = "#d90429" # Crimson Red
        elif composite_score >= 56.0:
            risk_class = "High Risk"
            intervention = "Bi-weekly municipal disinfection; mandatory covered waste bins; offal disposal regulation; cold storage subsidy."
            marker_color = "#f77f00" # Orange Amber
        elif composite_score >= 40.0:
            risk_class = "Moderate Risk"
            intervention = "Monthly routine surveillance; water potability testing; solid waste collection compliance."
            marker_color = "#ffd166" # Golden Yellow
        else:
            risk_class = "Low Risk"
            intervention = "Quarterly standard food safety audit; maintain existing hygienic separation."
            marker_color = "#06d6a0" # Emerald Green

        summary_counts[risk_class] += 1

        p["norm_drain_risk"] = round(norm_drain, 3)
        p["norm_waste_risk"] = round(norm_waste, 3)
        p["composite_geo_risk_score"] = composite_score
        p["risk_level"] = risk_class
        p["recommended_intervention"] = intervention
        p["marker_color"] = marker_color

        classified_features.append(feat)

    output_geojson = {
        "type": "FeatureCollection",
        "features": classified_features
    }

    out_file = os.path.join(DATA_DIR, "risk_analysis", "market_geo_risk_classified.geojson")
    with open(out_file, "w") as f:
        json.dump(output_geojson, f, indent=2)

    # Also export classified CSV
    out_csv = os.path.join(DATA_DIR, "risk_analysis", "market_geo_risk_classified.csv")
    if classified_features:
        headers = list(classified_features[0]["properties"].keys())
        with open(out_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for feat in classified_features:
                writer.writerow(feat["properties"])

    print("Geo-Risk Analysis Complete!")
    print("Risk Classification Distribution:")
    for k, v in summary_counts.items():
        print(f" - {k}: {v} markets ({round(v / len(classified_features) * 100, 1)}%)")

    # Generate Buffer Polygons (250m & 500m around High and Very High risk markets)
    generate_risk_buffers(classified_features)

def create_circular_polygon(center_lon, center_lat, radius_meters, num_points=24):
    coords = []
    # Degrees approximation around 14.45N
    lat_deg_per_m = 1.0 / 110574.0
    lon_deg_per_m = 1.0 / (111320.0 * math.cos(math.radians(14.45)))

    for i in range(num_points):
        angle = (2 * math.pi * i) / num_points
        dx = radius_meters * math.cos(angle)
        dy = radius_meters * math.sin(angle)
        pt_lon = center_lon + (dx * lon_deg_per_m)
        pt_lat = center_lat + (dy * lat_deg_per_m)
        coords.append([round(pt_lon, 6), round(pt_lat, 6)])
    coords.append(coords[0]) # Close ring
    return coords

def generate_risk_buffers(features):
    high_risk_markets = [f for f in features if f["properties"]["risk_level"] in ["High Risk", "Very High Risk"]]

    buffers_250 = []
    buffers_500 = []

    for f in high_risk_markets:
        lon, lat = f["geometry"]["coordinates"]
        p = f["properties"]

        ring_250 = create_circular_polygon(lon, lat, 250)
        ring_500 = create_circular_polygon(lon, lat, 500)

        buffers_250.append({
            "type": "Feature",
            "properties": {
                "shop_id": p["shop_id"],
                "shop_name": p["shop_name"],
                "risk_level": p["risk_level"],
                "buffer_radius_m": 250,
                "exposure_zone": "Immediate Bio-Exposure & Odor Vector Zone (250m)"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [ring_250]
            }
        })

        buffers_500.append({
            "type": "Feature",
            "properties": {
                "shop_id": p["shop_id"],
                "shop_name": p["shop_name"],
                "risk_level": p["risk_level"],
                "buffer_radius_m": 500,
                "exposure_zone": "Secondary Vector & Human Transmission Reach (500m)"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [ring_500]
            }
        })

    with open(os.path.join(DATA_DIR, "risk_analysis", "market_risk_buffers_250m.geojson"), "w") as f:
        json.dump({"type": "FeatureCollection", "features": buffers_250}, f, indent=2)

    with open(os.path.join(DATA_DIR, "risk_analysis", "market_risk_buffers_500m.geojson"), "w") as f:
        json.dump({"type": "FeatureCollection", "features": buffers_500}, f, indent=2)

    print(f"Generated {len(buffers_250)} risk buffers (250m and 500m).")

if __name__ == "__main__":
    calculate_geo_risk()
