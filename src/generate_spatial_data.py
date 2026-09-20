"""
Comprehensive Data Generation Pipeline for Health GIS: Nellore City & Kovur Mandal
Wet Markets, Vegetable Markets & Rythu Bazaars, Drinking Water Pipelines,
Water Points (RO Plants, Borewells, Hand Pumps), Open Drains, River & Hospitals (Govt + Private).
"""

import json
import csv
import math
import random
import os

random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

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
            "population_est": 600000,
            "wards_count": 54
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
            "population_est": 125000,
            "gram_panchayats_count": 18
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

    print("✓ Created Boundaries GeoJSONs")

def create_environmental_features():
    # Pennar River Basin Corridor
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
                    "category": "Major River Basin",
                    "status": "Infiltration Wells Source & Urban Effluent Sink"
                },
                "geometry": { "type": "Polygon", "coordinates": [pennar_polygon] }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "Sarvepalli Irrigation Canal",
                    "category": "Primary Canal",
                    "status": "Active Agricultural & Runoff Channel"
                },
                "geometry": { "type": "LineString", "coordinates": canal_sarvepalli }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "Buckingham Canal Feeder Channel",
                    "category": "Coastal Drainage & Canal",
                    "status": "High Silt & Urban Waste Effluent"
                },
                "geometry": { "type": "LineString", "coordinates": canal_buckingham_branch }
            }
        ]
    }

    with open(os.path.join(DATA_DIR, "infrastructure", "pennar_river_waterbodies.geojson"), "w") as f:
        json.dump(waterbodies_geojson, f, indent=2)

    # Open Drainage Network
    drain_lines = [
        {"name": "Stonehousepet - Pennar Main Open Outfall Drain", "type": "Open Masonry Drain (High Sullage)", "coords": [[79.9880, 14.4510], [79.9895, 14.4560], [79.9910, 14.4625]]},
        {"name": "Santhapet - Trunk Road Central Municipal Drain", "type": "Semi-Covered Heavy Effluent Drain", "coords": [[79.9780, 14.4370], [79.9820, 14.4420], [79.9850, 14.4490], [79.9870, 14.4580]]},
        {"name": "Ranganayakulapet Riverbank Open Sewer Line", "type": "Unlined Open Ditch", "coords": [[79.9800, 14.4530], [79.9840, 14.4570], [79.9870, 14.4620]]},
        {"name": "Vedayapalem - Ramalingapuram Stormwater Drain", "type": "Open Storm Drain with Sullage", "coords": [[79.9600, 14.4120], [79.9670, 14.4220], [79.9720, 14.4310]]},
        {"name": "Kovur Padugupadu Rail-Line Open Drain", "type": "Open Earthen Sullage Channel", "coords": [[79.9820, 14.4720], [79.9840, 14.4760], [79.9850, 14.4810]]},
        {"name": "Kovur Main Bazaar Central Open Gutter", "type": "Open Roadside Sludge Drain", "coords": [[79.9740, 14.4920], [79.9780, 14.4950], [79.9820, 14.4980]]},
        {"name": "Inamadugu Village Bypass Open Drain", "type": "Rural Runoff and Animal Waste Channel", "coords": [[79.9980, 14.4880], [80.0030, 14.4920], [80.0090, 14.4970]]}
    ]

    drain_features = []
    for d in drain_lines:
        drain_features.append({
            "type": "Feature",
            "properties": {
                "drain_name": d["name"],
                "drain_type": d["type"],
                "bio_hazard_rating": "High (Stagnant Organic Waste & Sullage)"
            },
            "geometry": { "type": "LineString", "coordinates": d["coords"] }
        })

    with open(os.path.join(DATA_DIR, "infrastructure", "open_drainage_sewage_network.geojson"), "w") as f:
        json.dump({"type": "FeatureCollection", "features": drain_features}, f, indent=2)

    print("✓ Created Environmental Infrastructure GeoJSONs")

def create_drinking_water_pipelines():
    """
    Creates tagged drinking water pipelines across Nellore Municipal Corporation (NMC)
    and Kovur Gram Panchayats with pipeline numbering, diameter, and cross-contamination indicators.
    """
    pipelines = [
        # Nellore NMC Water Pipelines
        {
            "pipe_id": "NMC-WTR-PL-01",
            "line_name": "Pennar Infiltration Gallery to Stonehousepet Trunk Main",
            "jurisdiction": "Nellore Municipal Corporation",
            "water_source": "Pennar River Infiltration Wells",
            "diameter_mm": 450,
            "pipe_material": "Ductile Iron (DI)",
            "operating_pressure_bar": 3.8,
            "laying_year": 2018,
            "coords": [[79.9700, 14.4640], [79.9780, 14.4580], [79.9870, 14.4520], [79.9910, 14.4490]],
            "cross_contamination_risk": "Moderate (Runs parallel to Stonehousepet masonry drain)"
        },
        {
            "pipe_id": "NMC-WTR-PL-02",
            "line_name": "Stonehousepet - Santhapet Feeder Line",
            "jurisdiction": "Nellore Municipal Corporation",
            "water_source": "Municipal Water Headworks",
            "diameter_mm": 300,
            "pipe_material": "HDPE High-Density",
            "operating_pressure_bar": 3.2,
            "laying_year": 2021,
            "coords": [[79.9910, 14.4490], [79.9860, 14.4440], [79.9810, 14.4390]],
            "cross_contamination_risk": "High (Crosses central municipal drain near Trunk Road)"
        },
        {
            "pipe_id": "NMC-WTR-PL-03",
            "line_name": "Somasila Drinking Water Scheme - Trunk Supply to Nellore South",
            "jurisdiction": "Nellore Municipal Corporation",
            "water_source": "Somasila Water Pipeline Project",
            "diameter_mm": 600,
            "pipe_material": "Mild Steel (MS)",
            "operating_pressure_bar": 4.5,
            "laying_year": 2019,
            "coords": [[79.9450, 14.4450], [79.9550, 14.4350], [79.9650, 14.4250], [79.9720, 14.4170]],
            "cross_contamination_risk": "Low (Dedicated deep utility corridor)"
        },
        {
            "pipe_id": "NMC-WTR-PL-04",
            "line_name": "Ranganayakulapet Urban Water Distribution Branch",
            "jurisdiction": "Nellore Municipal Corporation",
            "water_source": "Overhead Reservoir (ELSR)",
            "diameter_mm": 200,
            "pipe_material": "uPVC Class-4",
            "operating_pressure_bar": 2.5,
            "laying_year": 2015,
            "coords": [[79.9780, 14.4580], [79.9820, 14.4560], [79.9870, 14.4540]],
            "cross_contamination_risk": "High (Aging pipe joints near riverbank sullage)"
        },
        {
            "pipe_id": "NMC-WTR-PL-05",
            "line_name": "Vedayapalem - Ramalingapuram Sub-Trunk",
            "jurisdiction": "Nellore Municipal Corporation",
            "water_source": "Somasila Headworks Reservoir",
            "diameter_mm": 350,
            "pipe_material": "DI K9",
            "operating_pressure_bar": 3.5,
            "laying_year": 2020,
            "coords": [[79.9580, 14.4280], [79.9650, 14.4200], [79.9700, 14.4150]],
            "cross_contamination_risk": "Moderate"
        },
        # Kovur Gram Panchayat Water Pipelines
        {
            "pipe_id": "KVR-PNC-WTR-01",
            "line_name": "Kovur Gram Panchayat Pennar Infiltration Supply Line",
            "jurisdiction": "Kovur Mandal / Gram Panchayat",
            "water_source": "Pennar North Bank Infiltration Wells",
            "diameter_mm": 300,
            "pipe_material": "Ductile Iron (DI)",
            "operating_pressure_bar": 3.0,
            "laying_year": 2017,
            "coords": [[79.9720, 14.4690], [79.9760, 14.4800], [79.9780, 14.4940]],
            "cross_contamination_risk": "Moderate (Main conduit along Kovur trunk road)"
        },
        {
            "pipe_id": "KVR-PNC-WTR-02",
            "line_name": "Padugupadu Railway Colony Panchayati Pipeline",
            "jurisdiction": "Kovur Mandal / Padugupadu GP",
            "water_source": "Deep Community Borewell & GLSR",
            "diameter_mm": 160,
            "pipe_material": "HDPE PN-6",
            "operating_pressure_bar": 2.2,
            "laying_year": 2019,
            "coords": [[79.9760, 14.4720], [79.9820, 14.4750], [79.9860, 14.4780]],
            "cross_contamination_risk": "High (Intersected by open railway side drains)"
        },
        {
            "pipe_id": "KVR-PNC-WTR-03",
            "line_name": "Kovur Main Bazaar Ward Distribution Pipeline",
            "jurisdiction": "Kovur Mandal / Kovur GP",
            "water_source": "Kovur Overhead Tank (OHT)",
            "diameter_mm": 180,
            "pipe_material": "uPVC",
            "operating_pressure_bar": 2.0,
            "laying_year": 2016,
            "coords": [[79.9740, 14.4930], [79.9780, 14.4960], [79.9820, 14.4970]],
            "cross_contamination_risk": "Very High (Directly submerged under bazaar sullage gutter during monsoon)"
        },
        {
            "pipe_id": "KVR-PNC-WTR-04",
            "line_name": "Inamadugu Rural Water Supply Pipeline (RWSS)",
            "jurisdiction": "Kovur Mandal / Inamadugu GP",
            "water_source": "Inamadugu Gram Panchayat Tank",
            "diameter_mm": 140,
            "pipe_material": "HDPE PN-6",
            "operating_pressure_bar": 1.8,
            "laying_year": 2020,
            "coords": [[79.9880, 14.4880], [79.9960, 14.4900], [80.0040, 14.4920]],
            "cross_contamination_risk": "Low"
        }
    ]

    pipe_features = []
    for p in pipelines:
        pipe_features.append({
            "type": "Feature",
            "properties": {
                "pipe_id": p["pipe_id"],
                "name": p["line_name"],
                "jurisdiction": p["jurisdiction"],
                "water_source": p["water_source"],
                "diameter_mm": p["diameter_mm"],
                "material": p["pipe_material"],
                "pressure_bar": p["operating_pressure_bar"],
                "laying_year": p["laying_year"],
                "cross_contamination_risk": p["cross_contamination_risk"]
            },
            "geometry": {
                "type": "LineString",
                "coordinates": p["coords"]
            }
        })

    with open(os.path.join(DATA_DIR, "infrastructure", "drinking_water_pipelines.geojson"), "w") as f:
        json.dump({"type": "FeatureCollection", "features": pipe_features}, f, indent=2)

    print(f"✓ Created {len(pipe_features)} Drinking Water Pipeline Segments (NMC & Panchayati)")

def create_water_points():
    """
    Creates Mineral Water RO Plants, Community Drinking Water ATMs,
    Municipal Deep Borewells, and Public Hand Pumps with potability & contamination attributes.
    """
    water_points = [
        # Mineral Water Plants & RO ATMs
        {"id": "RO-NMC-01", "name": "NTR Sujala / Community RO Plant - Stonehousepet", "type": "Mineral Water RO Plant", "ward": "Stonehousepet (NMC)", "lat": 14.4502, "lon": 79.9905, "capacity_lph": 2000, "tds_ppm": 85, "potability": "Potable (Certified Safe)", "drain_dist_m": 45, "risk": "Low"},
        {"id": "RO-NMC-02", "name": "Santhapet Municipal Community RO Water Station", "type": "Mineral Water RO Plant", "ward": "Santhapet (NMC)", "lat": 14.4385, "lon": 79.9795, "capacity_lph": 1500, "tds_ppm": 92, "potability": "Potable (Certified Safe)", "drain_dist_m": 80, "risk": "Low"},
        {"id": "RO-NMC-03", "name": "Ranganayakulapet Ward RO Dispenser", "type": "Mineral Water RO Plant", "ward": "Ranganayakulapet (NMC)", "lat": 14.4542, "lon": 79.9865, "capacity_lph": 1000, "tds_ppm": 110, "potability": "Potable", "drain_dist_m": 35, "risk": "Moderate (Near Open Gutter)"},
        {"id": "RO-NMC-04", "name": "Vedayapalem Urban RO Purifier Unit", "type": "Mineral Water RO Plant", "ward": "Vedayapalem (NMC)", "lat": 14.4168, "lon": 79.9680, "capacity_lph": 2000, "tds_ppm": 78, "potability": "Potable (Certified Safe)", "drain_dist_m": 120, "risk": "Low"},
        {"id": "RO-KVR-01", "name": "Kovur Main Bazaar Gram Panchayat RO Plant", "type": "Mineral Water RO Plant", "ward": "Kovur Bazaar (GP)", "lat": 14.4948, "lon": 79.9775, "capacity_lph": 2500, "tds_ppm": 95, "potability": "Potable", "drain_dist_m": 25, "risk": "Moderate (Drainage Seepage Watch)"},
        {"id": "RO-KVR-02", "name": "Padugupadu Junction RO Water Hub", "type": "Mineral Water RO Plant", "ward": "Padugupadu (GP)", "lat": 14.4752, "lon": 79.9835, "capacity_lph": 1000, "tds_ppm": 105, "potability": "Potable", "drain_dist_m": 60, "risk": "Low"},
        {"id": "RO-KVR-03", "name": "Inamadugu Village Drinking Water Plant", "type": "Mineral Water RO Plant", "ward": "Inamadugu (GP)", "lat": 14.4915, "lon": 80.0025, "capacity_lph": 1000, "tds_ppm": 88, "potability": "Potable", "drain_dist_m": 110, "risk": "Low"},
        
        # Municipal & Public Deep Borewells
        {"id": "BW-NMC-01", "name": "Pennar South Riverbed Municipal Borewell Array", "type": "Deep Public Borewell", "ward": "Riverbank / Stonehousepet", "lat": 14.4610, "lon": 79.9750, "capacity_lph": 8000, "tds_ppm": 240, "potability": "Raw Water (Piped to Treatment)", "drain_dist_m": 180, "risk": "Low"},
        {"id": "BW-NMC-02", "name": "Santhapet Market Municipal Extraction Well", "type": "Deep Public Borewell", "ward": "Santhapet (NMC)", "lat": 14.4410, "lon": 79.9820, "capacity_lph": 4500, "tds_ppm": 420, "potability": "Moderate Hardness", "drain_dist_m": 30, "risk": "High (Microbial Intrusion Risk)"},
        {"id": "BW-KVR-01", "name": "Pennar North Bank Kovur Infiltration Borewell", "type": "Deep Public Borewell", "ward": "Pennar Basin North", "lat": 14.4670, "lon": 79.9740, "capacity_lph": 6000, "tds_ppm": 210, "potability": "Raw Water", "drain_dist_m": 220, "risk": "Low"},
        {"id": "BW-KVR-02", "name": "Inamadugu Agricultural & Public Well", "type": "Deep Public Borewell", "ward": "Inamadugu (GP)", "lat": 14.4925, "lon": 80.0060, "capacity_lph": 3500, "tds_ppm": 380, "potability": "Potable with boiling", "drain_dist_m": 90, "risk": "Moderate"},

        # Public Hand Pumps (Crucial for Low-Income Slum Risk)
        {"id": "HP-NMC-01", "name": "Stonehousepet Riverside Public Hand Pump #1", "type": "Public Hand Pump", "ward": "Stonehousepet Slum", "lat": 14.4515, "lon": 79.9920, "capacity_lph": 300, "tds_ppm": 510, "potability": "High Microbial Risk (Coliforms Detected)", "drain_dist_m": 8, "risk": "CRITICAL (8m from Open Sewer)"},
        {"id": "HP-NMC-02", "name": "Stonehousepet Fish Market Worker Hand Pump", "type": "Public Hand Pump", "ward": "Stonehousepet Market", "lat": 14.4498, "lon": 79.9912, "capacity_lph": 300, "tds_ppm": 480, "potability": "Unsafe without boiling", "drain_dist_m": 12, "risk": "CRITICAL (Direct Runoff Zone)"},
        {"id": "HP-NMC-03", "name": "Santhapet Gutter Lane Public Hand Pump", "type": "Public Hand Pump", "ward": "Santhapet (NMC)", "lat": 14.4392, "lon": 79.9808, "capacity_lph": 250, "tds_ppm": 440, "potability": "Unsafe for Drinking", "drain_dist_m": 10, "risk": "CRITICAL (Adjacent to Central Drain)"},
        {"id": "HP-NMC-04", "name": "Ranganayakulapet Fisherman Colony Hand Pump", "type": "Public Hand Pump", "ward": "Ranganayakulapet", "lat": 14.4532, "lon": 79.9882, "capacity_lph": 350, "tds_ppm": 390, "potability": "Moderate Risk", "drain_dist_m": 18, "risk": "High (Submerged in rains)"},
        {"id": "HP-KVR-01", "name": "Kovur Bazaar Lane Hand Pump", "type": "Public Hand Pump", "ward": "Kovur Main Bazaar", "lat": 14.4942, "lon": 79.9782, "capacity_lph": 300, "tds_ppm": 460, "potability": "Unsafe for Direct Drinking", "drain_dist_m": 7, "risk": "CRITICAL (7m from Open Sludge Gutter)"},
        {"id": "HP-KVR-02", "name": "Padugupadu Railway Slum Hand Pump", "type": "Public Hand Pump", "ward": "Padugupadu Rail Nagar", "lat": 14.4758, "lon": 79.9845, "capacity_lph": 300, "tds_ppm": 410, "potability": "High Microbial Risk", "drain_dist_m": 14, "risk": "CRITICAL (Open Sullage Contamination)"},
        {"id": "HP-KVR-03", "name": "Inamadugu Dalitwada Public Hand Pump", "type": "Public Hand Pump", "ward": "Inamadugu (GP)", "lat": 14.4895, "lon": 80.0042, "capacity_lph": 320, "tds_ppm": 350, "potability": "Marginal Potability", "drain_dist_m": 45, "risk": "Moderate"}
    ]

    features = []
    for w in water_points:
        features.append({
            "type": "Feature",
            "properties": w,
            "geometry": {
                "type": "Point",
                "coordinates": [w["lon"], w["lat"]]
            }
        })

    with open(os.path.join(DATA_DIR, "infrastructure", "water_points_ro_plants.geojson"), "w") as f:
        json.dump({"type": "FeatureCollection", "features": features}, f, indent=2)

    print(f"✓ Created {len(features)} Drinking Water Points (RO Plants, Borewells & Hand Pumps)")

def create_vegetable_markets():
    """
    Creates major Vegetable Markets, Rythu Bazaars (Govt of AP Marketing Dept),
    and Daily Produce Hubs across Nellore City and Kovur Mandal.
    """
    veg_markets = [
        {
            "market_id": "VEG-NMC-01",
            "market_name": "Stonehousepet Rythu Bazaar (Govt of AP)",
            "type": "Govt Rythu Bazaar",
            "jurisdiction": "Nellore Municipal Corporation",
            "stalls_count": 85,
            "daily_footfall": 4500,
            "produce_origin": "Podalakur & Allur Farmers direct supply",
            "proximity_to_meat_fish_m": 45,
            "waste_management": "Municipal Compost Truck (Daily)",
            "drain_dist_m": 35,
            "cross_contamination_rating": "High (Flies & Runoff from Adjacent Fish Stalls)",
            "lat": 14.4508,
            "lon": 79.9918
        },
        {
            "market_id": "VEG-NMC-02",
            "market_name": "Santhapet Central Wholesale & Retail Vegetable Market",
            "type": "Municipal Daily Market",
            "jurisdiction": "Nellore Municipal Corporation",
            "stalls_count": 120,
            "daily_footfall": 7500,
            "produce_origin": "Madanapalle, Bangalore & Local AP Mandis",
            "proximity_to_meat_fish_m": 60,
            "waste_management": "Open Central Dump Vats",
            "drain_dist_m": 25,
            "cross_contamination_rating": "High (Crowded Bazaar Congestion)",
            "lat": 14.4388,
            "lon": 79.9802
        },
        {
            "market_id": "VEG-NMC-03",
            "market_name": "Fateh Khan Pet Daily Vegetable Sub-Market",
            "type": "Neighborhood Municipal Market",
            "jurisdiction": "Nellore Municipal Corporation",
            "stalls_count": 45,
            "daily_footfall": 2200,
            "produce_origin": "Local Peri-Urban Vegetable Growers",
            "proximity_to_meat_fish_m": 85,
            "waste_management": "Closed Bins",
            "drain_dist_m": 70,
            "cross_contamination_rating": "Moderate",
            "lat": 14.4375,
            "lon": 79.9925
        },
        {
            "market_id": "VEG-NMC-04",
            "market_name": "Dargamitta Rythu Bazaar (Govt of AP)",
            "type": "Govt Rythu Bazaar",
            "jurisdiction": "Nellore Municipal Corporation",
            "stalls_count": 70,
            "daily_footfall": 3800,
            "produce_origin": "Nellore Rural & Kovur Horticultural Units",
            "proximity_to_meat_fish_m": 220,
            "waste_management": "Separate Bio-Degradable Processing",
            "drain_dist_m": 140,
            "cross_contamination_rating": "Low (Segregated from Meat Vendors)",
            "lat": 14.4310,
            "lon": 79.9745
        },
        {
            "market_id": "VEG-NMC-05",
            "market_name": "Vedayapalem Ramalingapuram Produce Hub",
            "type": "Commercial Daily Market",
            "jurisdiction": "Nellore Municipal Corporation",
            "stalls_count": 55,
            "daily_footfall": 2800,
            "produce_origin": "Venkatagiri & Podalakur Farms",
            "proximity_to_meat_fish_m": 75,
            "waste_management": "Municipal Collection",
            "drain_dist_m": 45,
            "cross_contamination_rating": "Moderate",
            "lat": 14.4180,
            "lon": 79.9670
        },
        {
            "market_id": "VEG-KVR-01",
            "market_name": "Kovur Main Road Vegetable Market",
            "type": "Panchayat Daily Market",
            "jurisdiction": "Kovur Mandal / Kovur GP",
            "stalls_count": 65,
            "daily_footfall": 3400,
            "produce_origin": "Pennar River Basin Fertile Silt Farms",
            "proximity_to_meat_fish_m": 30,
            "waste_management": "Roadside Open Dump",
            "drain_dist_m": 18,
            "cross_contamination_rating": "Very High (Adjacent to Broiler/Mutton Stalls & Drain)",
            "lat": 14.4952,
            "lon": 79.9780
        },
        {
            "market_id": "VEG-KVR-02",
            "market_name": "Padugupadu Railway Road Vegetable Stalls",
            "type": "Informal Street Produce Hub",
            "jurisdiction": "Kovur Mandal / Padugupadu GP",
            "stalls_count": 30,
            "daily_footfall": 1600,
            "produce_origin": "Riverbank vegetable growers",
            "proximity_to_meat_fish_m": 50,
            "waste_management": "Open Ground Dumping",
            "drain_dist_m": 22,
            "cross_contamination_rating": "High",
            "lat": 14.4762,
            "lon": 79.9838
        },
        {
            "market_id": "VEG-KVR-03",
            "market_name": "Inamadugu Weekly Sunday Shandy (Santhe)",
            "type": "Rural Weekly Shandy",
            "jurisdiction": "Kovur Mandal / Inamadugu GP",
            "stalls_count": 90,
            "daily_footfall": 4200,
            "produce_origin": "Multi-Village Rural Farmers",
            "proximity_to_meat_fish_m": 40,
            "waste_management": "Compost Clearing after Market Day",
            "drain_dist_m": 55,
            "cross_contamination_rating": "Moderate",
            "lat": 14.4905,
            "lon": 80.0030
        }
    ]

    features = []
    for v in veg_markets:
        features.append({
            "type": "Feature",
            "properties": v,
            "geometry": {
                "type": "Point",
                "coordinates": [v["lon"], v["lat"]]
            }
        })

    with open(os.path.join(DATA_DIR, "markets", "vegetable_markets.geojson"), "w") as f:
        json.dump({"type": "FeatureCollection", "features": features}, f, indent=2)

    print(f"✓ Created {len(features)} Vegetable Markets & Rythu Bazaars")

def create_expanded_healthcare():
    """
    Creates comprehensive healthcare layer including Government Hospitals,
    Medical Colleges, CHCs, UPHCs, and Major Private Super Speciality Hospitals in Nellore & Kovur.
    """
    hospitals = [
        # Government Hospitals
        {"name": "Government General Hospital (GGH / DSR Hospital)", "category": "Government Referral Hospital", "sector": "Government", "lat": 14.4445, "lon": 79.9860, "beds": 750, "emergency_icu": "24x7 Trauma & Epidemic Isolation Ward", "ambulance": "108 Base Station"},
        {"name": "ACSR Government Medical College Hospital", "category": "Government Medical College Hospital", "sector": "Government", "lat": 14.4380, "lon": 79.9720, "beds": 500, "emergency_icu": "Tertiary ICU & Pathology Laboratories", "ambulance": "Available"},
        {"name": "Kovur Community Health Centre (CHC)", "category": "Government CHC", "sector": "Government", "lat": 14.4930, "lon": 79.9790, "beds": 50, "emergency_icu": "24x7 Emergency & Inpatient Care", "ambulance": "108 Available"},
        {"name": "Stonehousepet Urban Primary Health Centre (UPHC)", "category": "Government UPHC", "sector": "Government", "lat": 14.4505, "lon": 79.9915, "beds": 10, "emergency_icu": "Day OPD & Immunization Unit", "ambulance": "On Call"},
        {"name": "Santhapet Municipal Dispensary / UPHC", "category": "Government UPHC", "sector": "Government", "lat": 14.4390, "lon": 79.9810, "beds": 6, "emergency_icu": "OPD & Communicable Disease Screening", "ambulance": "On Call"},
        {"name": "Ranganayakulapet Ward Health Wellness Post", "category": "Government UPHC", "sector": "Government", "lat": 14.4540, "lon": 79.9870, "beds": 4, "emergency_icu": "Primary Wellness Clinic", "ambulance": "On Call"},
        {"name": "Vedayapalem Area Hospital / UPHC", "category": "Government UPHC", "sector": "Government", "lat": 14.4170, "lon": 79.9670, "beds": 15, "emergency_icu": "General OPD & Maternal Health", "ambulance": "Available"},
        {"name": "Padugupadu Primary Health Sub-Centre", "category": "Government Sub-Centre", "sector": "Government", "lat": 14.4760, "lon": 79.9830, "beds": 4, "emergency_icu": "Rural Sub-Centre OPD", "ambulance": "On Call"},
        {"name": "Inamadugu Rural Primary Health Centre", "category": "Government PHC", "sector": "Government", "lat": 14.4910, "lon": 80.0040, "beds": 6, "emergency_icu": "Rural Primary Health Center", "ambulance": "On Call"},
        
        # Major Private & Super Speciality Hospitals (Nellore & Kovur)
        {"name": "Narayana Medical College & Super Speciality Hospital", "category": "Private Medical College & Research", "sector": "Private Super Speciality", "lat": 14.4250, "lon": 80.0210, "beds": 1400, "emergency_icu": "Level-1 Trauma & State Zoonotic Research ICU", "ambulance": "Dedicated Advanced Fleet"},
        {"name": "Medicover Hospitals (formerly KIMS Al Shifa)", "category": "Private Multi-Speciality Hospital", "sector": "Private Super Speciality", "lat": 14.4265, "lon": 79.9725, "beds": 250, "emergency_icu": "24x7 Critical Care & Infectious Disease Unit", "ambulance": "Advanced Life Support"},
        {"name": "Apollo Speciality Hospital Nellore", "category": "Private Super Speciality Hospital", "sector": "Private Super Speciality", "lat": 14.4215, "lon": 79.9790, "beds": 200, "emergency_icu": "Tertiary Critical Care & Emergency Wing", "ambulance": "24x7 ALS Ambulance"},
        {"name": "Simhapuri Hospital (NH16 Bypass)", "category": "Private Multi-Speciality Hospital", "sector": "Private Super Speciality", "lat": 14.4120, "lon": 79.9540, "beds": 300, "emergency_icu": "Trauma, Toxicology & Infectious Care", "ambulance": "Available"},
        {"name": "Rainbow Children's & Maternity Clinic", "category": "Private Speciality Clinic", "sector": "Private Speciality", "lat": 14.4420, "lon": 79.9840, "beds": 80, "emergency_icu": "Pediatric ICU & Neonatal Care", "ambulance": "Available"},
        {"name": "Kovur Medicare Nursing Home", "category": "Private Community Hospital", "sector": "Private Community", "lat": 14.4960, "lon": 79.9765, "beds": 35, "emergency_icu": "Inpatient Medicine & Minor Surgery", "ambulance": "Local Ambulance"}
    ]

    hosp_features = []
    for h in hospitals:
        hosp_features.append({
            "type": "Feature",
            "properties": h,
            "geometry": {
                "type": "Point",
                "coordinates": [h["lon"], h["lat"]]
            }
        })

    with open(os.path.join(DATA_DIR, "infrastructure", "healthcare_facilities.geojson"), "w") as f:
        json.dump({"type": "FeatureCollection", "features": hosp_features}, f, indent=2)

    print(f"✓ Created {len(hosp_features)} Comprehensive Healthcare Facilities (Govt + Private)")

def dist_point_to_segment_m(px, py, x1, y1, x2, y2):
    cos_lat = math.cos(math.radians(14.45))
    mx = (px - x1) * 111320 * cos_lat
    my = (py - y1) * 110574
    sx = (x2 - x1) * 111320 * cos_lat
    sy = (y2 - y1) * 110574

    seg_len_sq = sx*sx + sy*sy
    if seg_len_sq == 0:
        return math.sqrt(mx*mx + my*my)

    t = max(0, min(1, (mx * sx + my * sy) / seg_len_sq))
    dx = mx - (t * sx)
    dy = my - (t * sy)
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

def haversine_distance_m(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def generate_wet_markets():
    with open(os.path.join(DATA_DIR, "infrastructure", "open_drainage_sewage_network.geojson")) as f:
        drainage_data = json.load(f)
    drain_lines = [feat["geometry"]["coordinates"] for feat in drainage_data["features"]]

    with open(os.path.join(DATA_DIR, "infrastructure", "healthcare_facilities.geojson")) as f:
        hosp_data = json.load(f)
    hosp_pts = [(feat["geometry"]["coordinates"][1], feat["geometry"]["coordinates"][0]) for feat in hosp_data["features"]]

    clusters = [
        {"name": "Stonehousepet Fish & Mutton Hub", "zone": "Nellore Urban (NMC)", "center_lat": 14.4495, "center_lon": 79.9910, "count": 16, "types": ["Fish & Seafood", "Mutton / Sheep / Goat", "Poultry (Broiler/Country Chicken)", "Mixed Live Meat & Fish"], "crowd_base": 8.5},
        {"name": "Santhapet Central Meat Market", "zone": "Nellore Urban (NMC)", "center_lat": 14.4395, "center_lon": 79.9805, "count": 14, "types": ["Mutton / Sheep / Goat", "Poultry (Broiler/Country Chicken)"], "crowd_base": 7.5},
        {"name": "Ranganayakulapet Riverside Stalls", "zone": "Nellore Urban (NMC)", "center_lat": 14.4535, "center_lon": 79.9875, "count": 10, "types": ["Poultry (Broiler/Country Chicken)", "Fish & Seafood"], "crowd_base": 7.0},
        {"name": "Vedayapalem - Ramalingapuram Meat Cluster", "zone": "Nellore Urban (NMC)", "center_lat": 14.4175, "center_lon": 79.9675, "count": 10, "types": ["Poultry (Broiler/Country Chicken)", "Mutton / Sheep / Goat"], "crowd_base": 6.0},
        {"name": "Kovur Main Bazaar & Daily Market", "zone": "Kovur Mandal", "center_lat": 14.4945, "center_lon": 79.9785, "count": 14, "types": ["Poultry (Broiler/Country Chicken)", "Mutton / Sheep / Goat", "Fish & Seafood", "Mixed Live Meat & Fish"], "crowd_base": 8.0},
        {"name": "Padugupadu Railway & Bridge Junction Stalls", "zone": "Kovur Mandal", "center_lat": 14.4755, "center_lon": 79.9840, "count": 9, "types": ["Fish & Seafood", "Poultry (Broiler/Country Chicken)"], "crowd_base": 6.5},
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

            lat = c["center_lat"] + random.gauss(0, 0.0018)
            lon = c["center_lon"] + random.gauss(0, 0.0022)

            cat = random.choice(c["types"])
            origin = random.choice(animal_origins[cat])
            dest = random.choice(destinations)

            drain_dist = dist_to_linestrings(lon, lat, drain_lines)
            drain_dist = max(5.0, round(drain_dist, 1))

            hosp_dists = [haversine_distance_m(lat, lon, hlat, hlon) for hlat, hlon in hosp_pts]
            min_hosp_dist = round(min(hosp_dists), 1)
            river_dist = round(abs(lat - 14.463) * 110574, 1)

            daily_vol = random.randint(25, 420)
            slaughter_on_site = random.choices(["Yes", "No"], weights=[0.72, 0.28])[0]
            refrigeration = random.choices(["Yes", "No"], weights=[0.35, 0.65])[0]

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

    print(f"✓ Generated {len(shops)} wet markets in Nellore City and Kovur Mandal.")

if __name__ == "__main__":
    create_boundaries()
    create_environmental_features()
    create_drinking_water_pipelines()
    create_water_points()
    create_vegetable_markets()
    create_expanded_healthcare()
    generate_wet_markets()
