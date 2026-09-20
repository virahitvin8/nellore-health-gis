"""
Data Generation Pipeline for Health GIS: Nellore City & Kovur Mandal
Wet Market Inventory, Environmental Vectors, Drainage, and Administrative Boundaries.
"""

import json
import csv
import math
import random
import os

# Set random seed for reproducibility
random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# 1. Geographic Boundaries
# Nellore City Center ~ 14.4426 N, 79.9865 E
# Kovur Mandal Center ~ 14.4950 N, 79.9780 E
# Pennar River flows between 14.455 N and 14.470 N

def create_boundaries():
    # Nellore Municipal Corporation Polygon (South of Pennar River)
    nellore_coords = [
        [79.9450, 14.4600],
        [79.9650, 14.4620],
        [79.9900, 14.4580],
        [80.0150, 14.4520],
        [80.0250, 14.4300],
        [80.0150, 14.4050],
        [79.9800, 14.3950],
        [79.9500, 14.4080],
        [79.9350, 14.4300],
        [79.9450, 14.4600]
    ]

    # Kovur Mandal Boundary (North of Pennar River)
    kovur_coords = [
        [79.9400, 14.4680],
        [79.9700, 14.4710],
        [80.0050, 14.4690],
        [80.0300, 14.4850],
        [80.0200, 14.5250],
        [79.9800, 14.5400],
        [79.9450, 14.5200],
        [79.9350, 14.4850],
        [79.9400, 14.4680]
    ]

    nellore_feat = {
        "type": "Feature",
        "properties": {
            "name": "Nellore Municipal Corporation",
            "type": "Urban Local Body (NMC)",
            "district": "SPSR Nellore",
            "state": "Andhra Pradesh",
            "area_sq_km": 150.4,
            "population_est": 600000
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [nellore_coords]
        }
    }

    kovur_feat = {
        "type": "Feature",
        "properties": {
            "name": "Kovur Mandal",
            "type": "Rural/Peri-Urban Mandal",
            "district": "SPSR Nellore",
            "state": "Andhra Pradesh",
            "area_sq_km": 112.8,
            "population_est": 125000
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [kovur_coords]
        }
    }

    aoi_geojson = {
        "type": "FeatureCollection",
        "features": [nellore_feat, kovur_feat]
    }

    with open(os.path.join(DATA_DIR, "boundaries", "nellore_corporation_boundary.geojson"), "w") as f:
        json.dump({"type": "FeatureCollection", "features": [nellore_feat]}, f, indent=2)

    with open(os.path.join(DATA_DIR, "boundaries", "kovur_mandal_boundary.geojson"), "w") as f:
        json.dump({"type": "FeatureCollection", "features": [kovur_feat]}, f, indent=2)

    with open(os.path.join(DATA_DIR, "boundaries", "nellore_kovur_aoi.geojson"), "w") as f:
        json.dump(aoi_geojson, f, indent=2)

    print("Created Boundary GeoJSONs")

def create_environmental_features():
    # Pennar River Corridor
    river_coords = [
        [79.9200, 14.4620],
        [79.9400, 14.4635],
        [79.9650, 14.4650],
        [79.9850, 14.4640],
        [80.0050, 14.4610],
        [80.0350, 14.4580],
        [80.0550, 14.4550]
    ]

    pennar_polygon = [
        [79.9200, 14.4600],
        [79.9400, 14.4615],
        [79.9650, 14.4630],
        [79.9850, 14.4620],
        [80.0050, 14.4590],
        [80.0350, 14.4560],
        [80.0550, 14.4530],
        [80.0550, 14.4600],
        [80.0350, 14.4630],
        [80.0050, 14.4660],
        [79.9850, 14.4690],
        [79.9650, 14.4700],
        [79.9400, 14.4685],
        [79.9200, 14.4670],
        [79.9200, 14.4600]
    ]

    # Buckingham Canal & Sarvepalli Canal branches
    canal_sarvepalli = [
        [79.9550, 14.4550],
        [79.9600, 14.4350],
        [79.9650, 14.4150],
        [79.9700, 14.3950]
    ]

    canal_buckingham_branch = [
        [80.0100, 14.4700],
        [80.0120, 14.4450],
        [80.0140, 14.4200],
        [80.0160, 14.4000]
    ]

    waterbodies_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "name": "Pennar River Basin (Penna)",
                    "category": "Major River",
                    "status": "Seasonal Flow / Sandbed / Urban Discharge Sink"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [pennar_polygon]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "Sarvepalli Irrigation Canal",
                    "category": "Primary Canal",
                    "status": "Active Agricultural / Runoff Carrier"
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": canal_sarvepalli
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "Buckingham Canal Feeder Channel",
                    "category": "Coastal Drainage & Canal",
                    "status": "High Silt & Urban Waste Effluent"
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": canal_buckingham_branch
                }
            }
        ]
    }

    with open(os.path.join(DATA_DIR, "infrastructure", "pennar_river_waterbodies.geojson"), "w") as f:
        json.dump(waterbodies_geojson, f, indent=2)

    # Open Sewage & Major Municipal Drains
    drain_lines = [
        {
            "name": "Stonehousepet - Pennar Main Open Outfall Drain",
            "type": "Open Masonry Drain (High Sullage)",
            "coords": [
                [79.9880, 14.4510],
                [79.9895, 14.4560],
                [79.9910, 14.4625]
            ]
        },
        {
            "name": "Santhapet - Trunk Road Central Municipal Drain",
            "type": "Semi-Covered Heavy Effluent Drain",
            "coords": [
                [79.9780, 14.4370],
                [79.9820, 14.4420],
                [79.9850, 14.4490],
                [79.9870, 14.4580]
            ]
        },
        {
            "name": "Ranganayakulapet Riverbank Open Sewer Line",
            "type": "Unlined Open Ditch",
            "coords": [
                [79.9800, 14.4530],
                [79.9840, 14.4570],
                [79.9870, 14.4620]
            ]
        },
        {
            "name": "Vedayapalem - Ramalingapuram Stormwater & Wastewater Channel",
            "type": "Open Storm Drain with Sludge",
            "coords": [
                [79.9600, 14.4120],
                [79.9670, 14.4220],
                [79.9720, 14.4310]
            ]
        },
        {
            "name": "Kovur Padugupadu Rail-Line Open Sullage Drain",
            "type": "Open Earthen Sullage Channel",
            "coords": [
                [79.9820, 14.4720],
                [79.9840, 14.4760],
                [79.9850, 14.4810]
            ]
        },
        {
            "name": "Kovur Main Bazaar Central Open Gutter",
            "type": "Open Roadside Sludge Drain",
            "coords": [
                [79.9740, 14.4920],
                [79.9780, 14.4950],
                [79.9820, 14.4980]
            ]
        },
        {
            "name": "Inamadugu Village Bypass Open Drain",
            "type": "Rural Runoff and Animal Waste Channel",
            "coords": [
                [79.9980, 14.4880],
                [80.0030, 14.4920],
                [80.0090, 14.4970]
            ]
        }
    ]

    drainage_features = []
    for d in drain_lines:
        drainage_features.append({
            "type": "Feature",
            "properties": {
                "drain_name": d["name"],
                "drain_type": d["type"],
                "bio_hazard_rating": "High (Stagnant Organic Waste)"
            },
            "geometry": {
                "type": "LineString",
                "coordinates": d["coords"]
            }
        })

    with open(os.path.join(DATA_DIR, "infrastructure", "open_drainage_sewage_network.geojson"), "w") as f:
        json.dump({"type": "FeatureCollection", "features": drainage_features}, f, indent=2)

    # Healthcare Facilities (Hospitals, CHCs, UPHCs)
    hospitals = [
        {"name": "Government General Hospital (GGH / DSR Hospital)", "lat": 14.4445, "lon": 79.9860, "type": "Tertiary Referral Hospital", "beds": 750},
        {"name": "ACSR Government Medical College & Hospital", "lat": 14.4380, "lon": 79.9720, "type": "Medical College Hospital", "beds": 500},
        {"name": "Kovur Community Health Centre (CHC)", "lat": 14.4930, "lon": 79.9790, "type": "Community Health Centre", "beds": 50},
        {"name": "Stonehousepet Urban Primary Health Centre (UPHC)", "lat": 14.4505, "lon": 79.9915, "type": "Urban Primary Health Centre", "beds": 10},
        {"name": "Santhapet Municipal Dispensary / UPHC", "lat": 14.4390, "lon": 79.9810, "type": "Urban Dispensary", "beds": 6},
        {"name": "Ranganayakulapet Ward Health Post", "lat": 14.4540, "lon": 79.9870, "type": "Health Wellness Centre", "beds": 4},
        {"name": "Vedayapalem Area Hospital / UPHC", "lat": 14.4170, "lon": 79.9670, "type": "Urban Primary Health Centre", "beds": 15},
        {"name": "Padugupadu Primary Health Sub-Centre", "lat": 14.4760, "lon": 79.9830, "type": "Primary Health Sub-Centre", "beds": 4},
        {"name": "Inamadugu Rural Health Clinic", "lat": 14.4910, "lon": 80.0040, "type": "Rural Clinic", "beds": 2}
    ]

    hosp_features = []
    for h in hospitals:
        hosp_features.append({
            "type": "Feature",
            "properties": {
                "name": h["name"],
                "facility_type": h["type"],
                "bed_capacity": h["beds"],
                "emergency_service": "Available" if h["beds"] > 20 else "Day OPD Only"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [h["lon"], h["lat"]]
            }
        })

    with open(os.path.join(DATA_DIR, "infrastructure", "healthcare_facilities.geojson"), "w") as f:
        json.dump({"type": "FeatureCollection", "features": hosp_features}, f, indent=2)

    print("Created Environmental & Healthcare GeoJSONs")

def haversine_distance_m(lat1, lon1, lat2, lon2):
    R = 6371000 # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def dist_point_to_segment_m(px, py, x1, y1, x2, y2):
    # px, py is lon, lat of market
    # approximate flat distance in meters around Nellore (lat ~14.45)
    cos_lat = math.cos(math.radians(14.45))
    mx = (px - x1) * 111320 * cos_lat
    my = (py - y1) * 110574
    sx = (x2 - x1) * 111320 * cos_lat
    sy = (y2 - y1) * 110574

    seg_len_sq = sx*sx + sy*sy
    if seg_len_sq == 0:
        return math.sqrt(mx*mx + my*my)

    t = max(0, min(1, (mx * sx + my * sy) / seg_len_sq))
    proj_x = t * sx
    proj_y = t * sy
    dx = mx - proj_x
    dy = my - proj_y
    return math.sqrt(dx*dx + dy*dy)

def dist_to_linestrings(lon, lat, lines):
    min_dist = float('inf')
    for line in lines:
        for i in range(len(line) - 1):
            x1, y1 = line[i]
            x2, y2 = line[i+1]
            d = dist_point_to_segment_m(lon, lat, x1, y1, x2, y2)
            if d < min_dist:
                min_dist = d
    return min_dist

def generate_wet_markets():
    # Load drainage lines to compute realistic distance to open drainage
    with open(os.path.join(DATA_DIR, "infrastructure", "open_drainage_sewage_network.geojson")) as f:
        drainage_data = json.load(f)
    drain_lines = [feat["geometry"]["coordinates"] for feat in drainage_data["features"]]

    with open(os.path.join(DATA_DIR, "infrastructure", "healthcare_facilities.geojson")) as f:
        hosp_data = json.load(f)
    hosp_pts = [(feat["geometry"]["coordinates"][1], feat["geometry"]["coordinates"][0]) for feat in hosp_data["features"]]

    # Key Hotspot clusters in Nellore & Kovur
    clusters = [
        # Stonehousepet - famous dense fish and meat wholesale market right near Pennar
        {"name": "Stonehousepet Fish & Mutton Hub", "zone": "Nellore Urban (NMC)", "center_lat": 14.4495, "center_lon": 79.9910, "count": 16, "types": ["Fish & Seafood", "Mutton / Sheep / Goat", "Poultry (Broiler/Country Chicken)", "Mixed Live Meat & Fish"], "crowd_base": 8.5},
        # Santhapet - historic central city commercial bazaar
        {"name": "Santhapet Central Meat Market", "zone": "Nellore Urban (NMC)", "center_lat": 14.4395, "center_lon": 79.9805, "count": 14, "types": ["Mutton / Sheep / Goat", "Poultry (Broiler/Country Chicken)"], "crowd_base": 7.5},
        # Ranganayakulapet - old riverside settlements with live poultry stalls
        {"name": "Ranganayakulapet Riverside Stalls", "zone": "Nellore Urban (NMC)", "center_lat": 14.4535, "center_lon": 79.9875, "count": 10, "types": ["Poultry (Broiler/Country Chicken)", "Fish & Seafood"], "crowd_base": 7.0},
        # Vedayapalem - southern high-growth suburban corridor
        {"name": "Vedayapalem - Ramalingapuram Meat Cluster", "zone": "Nellore Urban (NMC)", "center_lat": 14.4175, "center_lon": 79.9675, "count": 10, "types": ["Poultry (Broiler/Country Chicken)", "Mutton / Sheep / Goat"], "crowd_base": 6.0},
        # Kovur Main Bazaar - bus stand and commercial nerve center of Kovur
        {"name": "Kovur Main Bazaar & Daily Market", "zone": "Kovur Mandal", "center_lat": 14.4945, "center_lon": 79.9785, "count": 14, "types": ["Poultry (Broiler/Country Chicken)", "Mutton / Sheep / Goat", "Fish & Seafood", "Mixed Live Meat & Fish"], "crowd_base": 8.0},
        # Padugupadu - bridge entry point connecting Nellore & Kovur
        {"name": "Padugupadu Railway & Bridge Junction Stalls", "zone": "Kovur Mandal", "center_lat": 14.4755, "center_lon": 79.9840, "count": 9, "types": ["Fish & Seafood", "Poultry (Broiler/Country Chicken)"], "crowd_base": 6.5},
        # Inamadugu - rural mandal shandy and live poultry hub
        {"name": "Inamadugu Rural Livestock & Poultry Market", "zone": "Kovur Mandal", "center_lat": 14.4910, "center_lon": 80.0035, "count": 8, "types": ["Mutton / Sheep / Goat", "Poultry (Broiler/Country Chicken)"], "crowd_base": 5.5}
    ]

    animal_origins = {
        "Poultry (Broiler/Country Chicken)": ["Local Nellore Poultry Farms (Podalakur Road)", "Allur Broiler Breeding Units", "Chittoor Hatcheries Supply"],
        "Mutton / Sheep / Goat": ["Kadapa / Badvel Livestock Shandy", "Atmakur Cattle & Sheep Market", "Nellore Local Herders (Pennar Basin)"],
        "Fish & Seafood": ["Pennar River Catchment", "Krishnapatnam Deep Sea Port Landing", "Mypadu Coastal Aquaculture Farms", "Pulicat Lake Brackish Water Source"],
        "Mixed Live Meat & Fish": ["Combined Regional Traders & Local Shandy", "Multi-Source Livestock Distributors"]
    }

    destinations = [
        "Local Ward Neighborhood Households",
        "Trunk Road & Gandhi Nagar Restaurants",
        "Hotel & Catering Aggregators",
        "Local Street Food Vendors",
        "Inter-Mandal Retail Stalls"
    ]

    shops = []
    shop_id_counter = 1

    for c in clusters:
        for i in range(c["count"]):
            shop_id = f"NLR-HLTH-{shop_id_counter:03d}"
            shop_id_counter += 1

            # Scatter around cluster center with slight jitter (~100 - 450m)
            lat = c["center_lat"] + random.gauss(0, 0.0018)
            lon = c["center_lon"] + random.gauss(0, 0.0022)

            cat = random.choice(c["types"])
            origin = random.choice(animal_origins[cat])
            dest = random.choice(destinations)

            # Proximity to open drainage
            drain_dist = dist_to_linestrings(lon, lat, drain_lines)
            drain_dist = max(5.0, round(drain_dist, 1))

            # Proximity to nearest hospital
            hosp_dists = [haversine_distance_m(lat, lon, hlat, hlon) for hlat, hlon in hosp_pts]
            min_hosp_dist = round(min(hosp_dists), 1)

            # River distance (river is ~14.463 latitude)
            river_dist = round(abs(lat - 14.463) * 110574, 1)

            # Shop operational attributes
            daily_vol = random.randint(25, 420)
            slaughter_on_site = random.choices(["Yes", "No"], weights=[0.72, 0.28])[0]
            refrigeration = random.choices(["Yes", "No"], weights=[0.35, 0.65])[0]

            # Waste disposal correlation with drain distance
            if drain_dist < 40:
                waste_disp = random.choices(["Direct Open Drain Discharge", "Open Dumping on Ground", "Municipal Waste Bin"], weights=[0.65, 0.25, 0.10])[0]
                drainage_cond = "Open Stagnant Drain"
            elif drain_dist < 120:
                waste_disp = random.choices(["Direct Open Drain Discharge", "Municipal Waste Bin", "Open Dumping on Ground"], weights=[0.35, 0.50, 0.15])[0]
                drainage_cond = "Semi-Covered Municipal Drain"
            else:
                waste_disp = random.choices(["Municipal Waste Bin", "Closed Bin Collection", "Open Dumping on Ground"], weights=[0.60, 0.30, 0.10])[0]
                drainage_cond = "Underground Closed Drain"

            water_src = random.choices(["Borewell / Groundwater", "Piped Municipal Supply", "Stored Tank Water (Untreated)"], weights=[0.45, 0.40, 0.15])[0]

            crowd_score = min(10.0, max(1.0, round(c["crowd_base"] + random.gauss(0, 1.2), 1)))

            # Naming
            prefixes = ["Sri Venkateswara", "Nellore Fresh", "Pennar Quality", "Kovur Royal", "Annapurna", "Amma", "Al-Madina", "Coastal Choice", "Balaji", "Gouthami", "Sai Krupa", "National", "Star"]
            shop_name = f"{random.choice(prefixes)} {cat.split()[0]} Stall ({c['name'].split()[0]})"

            shops.append({
                "shop_id": shop_id,
                "shop_name": shop_name,
                "cluster_hub": c["name"],
                "mandal_zone": c["zone"],
                "latitude": round(lat, 6),
                "longitude": round(lon, 6),
                "category": cat,
                "animal_origin": origin,
                "animal_destination": dest,
                "daily_animals_handled": daily_vol,
                "slaughter_on_site": slaughter_on_site,
                "refrigeration_available": refrigeration,
                "waste_disposal_method": waste_disp,
                "water_source": water_src,
                "drainage_condition": drainage_cond,
                "distance_to_drain_m": drain_dist,
                "distance_to_waterbody_m": river_dist,
                "distance_to_hospital_m": min_hosp_dist,
                "market_crowd_index": crowd_score
            })

    # Save to CSV and GeoJSON
    csv_file = os.path.join(DATA_DIR, "markets", "wet_markets_inventory.csv")
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(shops[0].keys()))
        writer.writeheader()
        writer.writerows(shops)

    geojson_features = []
    for s in shops:
        geojson_features.append({
            "type": "Feature",
            "properties": s,
            "geometry": {
                "type": "Point",
                "coordinates": [s["longitude"], s["latitude"]]
            }
        })

    geojson_file = os.path.join(DATA_DIR, "markets", "wet_markets_inventory.geojson")
    with open(geojson_file, "w") as f:
        json.dump({"type": "FeatureCollection", "features": geojson_features}, f, indent=2)

    print(f"Generated {len(shops)} wet markets in Nellore City and Kovur Mandal.")

if __name__ == "__main__":
    create_boundaries()
    create_environmental_features()
    generate_wet_markets()
