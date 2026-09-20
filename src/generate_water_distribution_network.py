"""
Water Supply & Distribution Flow Network Engine for Nellore City & Kovur Mandal
Generates flow lines, source nodes, underground infiltration wells, overhead storage tanks (ELSR/OHT),
and an Inverted Boundary Mask to strictly focus the map on Nellore & Kovur only.
"""

import os
import json
import math
from export_shapefiles import export_boundaries_shapefiles, export_water_network_shapefile, create_shapefiles_zip

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
INFRA_DIR = os.path.join(DATA_DIR, "infrastructure")
os.makedirs(INFRA_DIR, exist_ok=True)

def generate_water_infrastructure_and_flow():
    # 1. Raw Water Origin & Underground Wells
    sources = [
        {
            "id": "SRC-PEN-S01",
            "name": "Pennar South Riverbed Infiltration Wellfield",
            "type": "Riverbed Infiltration Gallery & Deep Borewell Array",
            "zone": "Pennar River Basin (NMC)",
            "aquifer_source": "Pennar Deep Sand Alluvial Aquifer",
            "depth_m": 32,
            "yield_lph": 18000,
            "lat": 14.4640,
            "lon": 79.9700,
            "supplies_to": "Nellore Municipal Central Headworks (HW-NMC-01)"
        },
        {
            "id": "SRC-SOM-01",
            "name": "Somasila Drinking Water Scheme - West Canal Intake",
            "type": "Surface Reservoir Gravity Intake & Pipeline",
            "zone": "Somasila Pipeline Corridor",
            "aquifer_source": "Somasila Reservoir Storage Basin",
            "depth_m": 0,
            "yield_lph": 35000,
            "lat": 14.4500,
            "lon": 79.9400,
            "supplies_to": "Vedayapalem Booster Pumping Station (BST-NMC-01)"
        },
        {
            "id": "SRC-PEN-N01",
            "name": "Kovur North Bank Riverbed Infiltration Wells",
            "type": "Riverbed Radial Collector & Infiltration Wells",
            "zone": "Pennar North Bank (Kovur GP)",
            "aquifer_source": "Pennar North Alluvial Sandbed",
            "depth_m": 28,
            "yield_lph": 12000,
            "lat": 14.4690,
            "lon": 79.9720,
            "supplies_to": "Kovur Gram Panchayat Treatment Plant (HW-KVR-01)"
        }
    ]

    # 2. Municipal Treatment Plants & Booster Headworks
    headworks = [
        {
            "id": "HW-NMC-01",
            "name": "Nellore Municipal Central Water Headworks & Treatment Plant",
            "type": "Central Water Treatment & Pumping Plant",
            "zone": "Nellore Urban Local Body",
            "capacity_mld": 32.0,
            "treatment_tech": "Rapid Gravity Sand Filtration & Chlorination",
            "lat": 14.4600,
            "lon": 79.9750
        },
        {
            "id": "BST-NMC-01",
            "name": "Vedayapalem Southern Booster Pumping Station",
            "type": "Booster Pumping Station & Intermediate Sump",
            "zone": "Nellore South",
            "capacity_mld": 18.0,
            "treatment_tech": "Secondary Chlorination & Sump Balancing",
            "lat": 14.4350,
            "lon": 79.9550
        },
        {
            "id": "HW-KVR-01",
            "name": "Kovur Gram Panchayat Water Treatment Headworks",
            "type": "Panchayat Filter Bed & Primary Chlorination Plant",
            "zone": "Kovur Mandal",
            "capacity_mld": 10.5,
            "treatment_tech": "Slow Sand Filtration & In-line Gas Chlorination",
            "lat": 14.4750,
            "lon": 79.9750
        }
    ]

    # 3. Elevated Level Service Reservoirs (ELSR / OHT) & Municipal Storage Tanks
    tanks = [
        {
            "id": "ELSR-NMC-01",
            "name": "Stonehousepet Elevated Level Service Reservoir (ELSR)",
            "zone": "Stonehousepet (NMC)",
            "capacity_mld": 1.8,
            "staging_height_m": 18,
            "supply_population": 42000,
            "operational_status": "Active (Dual Daily Distribution)",
            "fed_by": "HW-NMC-01",
            "lat": 14.4500,
            "lon": 79.9910
        },
        {
            "id": "ELSR-NMC-02",
            "name": "Santhapet Central Municipal Overhead Tank",
            "zone": "Santhapet Commercial Ward (NMC)",
            "capacity_mld": 2.2,
            "staging_height_m": 20,
            "supply_population": 55000,
            "operational_status": "Active (Pressure Balanced)",
            "fed_by": "HW-NMC-01",
            "lat": 14.4390,
            "lon": 79.9810
        },
        {
            "id": "ELSR-NMC-03",
            "name": "Ranganayakulapet Riverside Overhead Reservoir",
            "zone": "Ranganayakulapet (NMC)",
            "capacity_mld": 1.2,
            "staging_height_m": 16,
            "supply_population": 28000,
            "operational_status": "Active",
            "fed_by": "HW-NMC-01",
            "lat": 14.4540,
            "lon": 79.9870
        },
        {
            "id": "ELSR-NMC-04",
            "name": "Vedayapalem - Ramalingapuram High-Level Reservoir",
            "zone": "Vedayapalem (NMC)",
            "capacity_mld": 2.5,
            "staging_height_m": 22,
            "supply_population": 62000,
            "operational_status": "Active (Supplies South Corridor)",
            "fed_by": "BST-NMC-01",
            "lat": 14.4170,
            "lon": 79.9670
        },
        {
            "id": "ELSR-NMC-05",
            "name": "Dargamitta Municipal Water Tower",
            "zone": "Dargamitta / Magunta Layout (NMC)",
            "capacity_mld": 1.5,
            "staging_height_m": 18,
            "supply_population": 36000,
            "operational_status": "Active",
            "fed_by": "BST-NMC-01",
            "lat": 14.4310,
            "lon": 79.9750
        },
        {
            "id": "ELSR-KVR-01",
            "name": "Kovur Main Bazaar Gram Panchayat Elevated Reservoir",
            "zone": "Kovur Bazaar (GP)",
            "capacity_mld": 1.4,
            "staging_height_m": 18,
            "supply_population": 32000,
            "operational_status": "Active (Gram Panchayat Core)",
            "fed_by": "HW-KVR-01",
            "lat": 14.4945,
            "lon": 79.9785
        },
        {
            "id": "ELSR-KVR-02",
            "name": "Padugupadu Railway Colony Overhead Tank",
            "zone": "Padugupadu (GP)",
            "capacity_mld": 0.9,
            "staging_height_m": 16,
            "supply_population": 19000,
            "operational_status": "Active",
            "fed_by": "HW-KVR-01",
            "lat": 14.4755,
            "lon": 79.9840
        },
        {
            "id": "ELSR-KVR-03",
            "name": "Inamadugu Rural Gram Panchayat Water Tower",
            "zone": "Inamadugu (GP)",
            "capacity_mld": 0.6,
            "staging_height_m": 15,
            "supply_population": 14000,
            "operational_status": "Active (Solar Pumping Assisted)",
            "fed_by": "HW-KVR-01",
            "lat": 14.4910,
            "lon": 80.0035
        }
    ]

    # 4. Pipeline Connectivity & Directional Flow Network
    pipelines = [
        # Segment 1: River Infiltration -> NMC Central Headworks
        {
            "pipe_id": "PL-RAW-01",
            "name": "Pennar River Infiltration Wells ➔ NMC Central Headworks",
            "from_node": "Pennar South Riverbed Infiltration Wellfield (SRC-PEN-S01)",
            "to_node": "NMC Central Water Headworks (HW-NMC-01)",
            "flow_direction": "River Infiltration ➔ Municipal Treatment",
            "flow_hierarchy": "Primary Raw Intake Main",
            "diameter_mm": 600,
            "material": "Ductile Iron (DI K9)",
            "discharge_mld": 18.0,
            "pressure_bar": 3.8,
            "coordinates": [[79.9700, 14.4640], [79.9725, 14.4620], [79.9750, 14.4600]]
        },
        # Segment 2: NMC Central Headworks -> Stonehousepet ELSR
        {
            "pipe_id": "PL-FEED-01",
            "name": "NMC Central Headworks ➔ Stonehousepet ELSR Feeder",
            "from_node": "NMC Central Water Headworks (HW-NMC-01)",
            "to_node": "Stonehousepet ELSR (ELSR-NMC-01)",
            "flow_direction": "Treatment Headworks ➔ Stonehousepet Overhead Tank",
            "flow_hierarchy": "Secondary Treated Pumping Main",
            "diameter_mm": 450,
            "material": "Ductile Iron (DI)",
            "discharge_mld": 6.5,
            "pressure_bar": 4.2,
            "coordinates": [[79.9750, 14.4600], [79.9810, 14.4550], [79.9870, 14.4520], [79.9910, 14.4500]]
        },
        # Segment 3: NMC Central Headworks -> Santhapet Central ELSR
        {
            "pipe_id": "PL-FEED-02",
            "name": "NMC Central Headworks ➔ Santhapet Central ELSR Feeder",
            "from_node": "NMC Central Water Headworks (HW-NMC-01)",
            "to_node": "Santhapet Central Municipal Overhead Tank (ELSR-NMC-02)",
            "flow_direction": "Treatment Headworks ➔ Santhapet Overhead Tank",
            "flow_hierarchy": "Secondary Treated Pumping Main",
            "diameter_mm": 500,
            "material": "Mild Steel (MS)",
            "discharge_mld": 8.0,
            "pressure_bar": 4.5,
            "coordinates": [[79.9750, 14.4600], [79.9770, 14.4520], [79.9790, 14.4450], [79.9810, 14.4390]]
        },
        # Segment 4: NMC Central Headworks -> Ranganayakulapet ELSR
        {
            "pipe_id": "PL-FEED-03",
            "name": "NMC Central Headworks ➔ Ranganayakulapet ELSR Branch",
            "from_node": "NMC Central Water Headworks (HW-NMC-01)",
            "to_node": "Ranganayakulapet Riverside Overhead Reservoir (ELSR-NMC-03)",
            "flow_direction": "Treatment Headworks ➔ Ranganayakulapet Overhead Tank",
            "flow_hierarchy": "Secondary Treated Pumping Main",
            "diameter_mm": 350,
            "material": "Ductile Iron (DI)",
            "discharge_mld": 3.5,
            "pressure_bar": 3.6,
            "coordinates": [[79.9750, 14.4600], [79.9800, 14.4580], [79.9840, 14.4560], [79.9870, 14.4540]]
        },
        # Segment 5: Somasila Canal Intake -> Vedayapalem Booster Station
        {
            "pipe_id": "PL-RAW-02",
            "name": "Somasila Canal Gravity Intake ➔ Vedayapalem Booster Station",
            "from_node": "Somasila Canal Intake (SRC-SOM-01)",
            "to_node": "Vedayapalem Booster Station (BST-NMC-01)",
            "flow_direction": "Surface Canal Intake ➔ Southern Booster Station",
            "flow_hierarchy": "Primary Raw Gravity Conduit",
            "diameter_mm": 700,
            "material": "Prestressed Concrete (PSC)",
            "discharge_mld": 15.0,
            "pressure_bar": 3.2,
            "coordinates": [[79.9400, 14.4500], [79.9480, 14.4420], [79.9550, 14.4350]]
        },
        # Segment 6: Vedayapalem Booster Station -> Vedayapalem ELSR
        {
            "pipe_id": "PL-FEED-04",
            "name": "Vedayapalem Booster Station ➔ Vedayapalem High-Level ELSR",
            "from_node": "Vedayapalem Booster Station (BST-NMC-01)",
            "to_node": "Vedayapalem High-Level Reservoir (ELSR-NMC-04)",
            "flow_direction": "Booster Pump ➔ Vedayapalem High-Level Tank",
            "flow_hierarchy": "Secondary Treated Pumping Main",
            "diameter_mm": 450,
            "material": "HDPE PN-10",
            "discharge_mld": 7.0,
            "pressure_bar": 4.0,
            "coordinates": [[79.9550, 14.4350], [79.9610, 14.4260], [79.9670, 14.4170]]
        },
        # Segment 7: Vedayapalem Booster Station -> Dargamitta Water Tower
        {
            "pipe_id": "PL-FEED-05",
            "name": "Vedayapalem Booster Station ➔ Dargamitta Municipal Tower",
            "from_node": "Vedayapalem Booster Station (BST-NMC-01)",
            "to_node": "Dargamitta Municipal Water Tower (ELSR-NMC-05)",
            "flow_direction": "Booster Pump ➔ Dargamitta Elevated Tower",
            "flow_hierarchy": "Secondary Treated Pumping Main",
            "diameter_mm": 400,
            "material": "Ductile Iron (DI)",
            "discharge_mld": 5.0,
            "pressure_bar": 3.8,
            "coordinates": [[79.9550, 14.4350], [79.9650, 14.4330], [79.9750, 14.4310]]
        },
        # Segment 8: Stonehousepet ELSR -> Ward Distribution & RO ATMs
        {
            "pipe_id": "PL-DIST-01",
            "name": "Stonehousepet ELSR ➔ Ward Distribution & RO Water ATM Points",
            "from_node": "Stonehousepet ELSR (ELSR-NMC-01)",
            "to_node": "Stonehousepet Ward Distribution & NTR Sujala RO ATMs",
            "flow_direction": "Overhead Tank ➔ Ward Street Consumer Taps",
            "flow_hierarchy": "Tertiary Reticulation Network",
            "diameter_mm": 300,
            "material": "HDPE PN-6",
            "discharge_mld": 1.8,
            "pressure_bar": 2.2,
            "coordinates": [[79.9910, 14.4500], [79.9925, 14.4480], [79.9940, 14.4450]]
        },
        # Segment 9: Kovur River Infiltration -> Kovur Treatment Headworks
        {
            "pipe_id": "PL-KVR-01",
            "name": "Kovur North Infiltration Wells ➔ Kovur Treatment Headworks",
            "from_node": "Kovur North Bank Riverbed Infiltration Wells (SRC-PEN-N01)",
            "to_node": "Kovur Treatment Headworks (HW-KVR-01)",
            "flow_direction": "River Infiltration ➔ Kovur Treatment Plant",
            "flow_hierarchy": "Primary Raw Infiltration Main",
            "diameter_mm": 350,
            "material": "Ductile Iron (DI)",
            "discharge_mld": 5.5,
            "pressure_bar": 3.0,
            "coordinates": [[79.9720, 14.4690], [79.9735, 14.4720], [79.9750, 14.4750]]
        },
        # Segment 10: Kovur Treatment Headworks -> Kovur Bazaar ELSR
        {
            "pipe_id": "PL-KVR-02",
            "name": "Kovur Treatment Headworks ➔ Kovur Main Bazaar ELSR",
            "from_node": "Kovur Treatment Headworks (HW-KVR-01)",
            "to_node": "Kovur Main Bazaar Gram Panchayat Reservoir (ELSR-KVR-01)",
            "flow_direction": "Treatment Plant ➔ Kovur Main Bazaar Tank",
            "flow_hierarchy": "Secondary Treated Pumping Main",
            "diameter_mm": 300,
            "material": "Ductile Iron (DI)",
            "discharge_mld": 3.0,
            "pressure_bar": 3.5,
            "coordinates": [[79.9750, 14.4750], [79.9765, 14.4850], [79.9785, 14.4945]]
        },
        # Segment 11: Kovur Treatment Headworks -> Padugupadu Railway OHT
        {
            "pipe_id": "PL-KVR-03",
            "name": "Kovur Treatment Headworks ➔ Padugupadu Railway OHT",
            "from_node": "Kovur Treatment Headworks (HW-KVR-01)",
            "to_node": "Padugupadu Railway Colony Overhead Tank (ELSR-KVR-02)",
            "flow_direction": "Treatment Plant ➔ Padugupadu Water Tower",
            "flow_hierarchy": "Secondary Treated Pumping Main",
            "diameter_mm": 200,
            "material": "HDPE PN-6",
            "discharge_mld": 1.8,
            "pressure_bar": 2.8,
            "coordinates": [[79.9750, 14.4750], [79.9790, 14.4752], [79.9840, 14.4755]]
        },
        # Segment 12: Kovur Treatment Headworks -> Inamadugu Rural OHT
        {
            "pipe_id": "PL-KVR-04",
            "name": "Kovur Treatment Headworks ➔ Inamadugu Rural OHT Feeder",
            "from_node": "Kovur Treatment Headworks (HW-KVR-01)",
            "to_node": "Inamadugu Rural Elevated Water Reservoir (ELSR-KVR-03)",
            "flow_direction": "Treatment Plant ➔ Inamadugu Rural Water Tower",
            "flow_hierarchy": "Secondary Rural Feeder Conduit",
            "diameter_mm": 160,
            "material": "HDPE PN-6",
            "discharge_mld": 0.9,
            "pressure_bar": 2.5,
            "coordinates": [[79.9750, 14.4750], [79.9880, 14.4840], [80.0035, 14.4910]]
        }
    ]

    # Save to GeoJSONs
    # 1. Sources GeoJSON
    src_features = []
    for s in sources:
        src_features.append({
            "type": "Feature",
            "properties": s,
            "geometry": { "type": "Point", "coordinates": [s["lon"], s["lat"]] }
        })
    with open(os.path.join(INFRA_DIR, "underground_sources_wellfields.geojson"), "w") as f:
        json.dump({"type": "FeatureCollection", "features": src_features}, f, indent=2)

    # 2. Tanks GeoJSON
    tank_features = []
    for t in tanks:
        tank_features.append({
            "type": "Feature",
            "properties": t,
            "geometry": { "type": "Point", "coordinates": [t["lon"], t["lat"]] }
        })
    with open(os.path.join(INFRA_DIR, "overhead_storage_reservoirs.geojson"), "w") as f:
        json.dump({"type": "FeatureCollection", "features": tank_features}, f, indent=2)

    # 3. Pipelines Flow GeoJSON
    pipe_features = []
    for p in pipelines:
        pipe_features.append({
            "type": "Feature",
            "properties": p,
            "geometry": { "type": "LineString", "coordinates": p["coordinates"] }
        })
    with open(os.path.join(INFRA_DIR, "water_distribution_flow_network.geojson"), "w") as f:
        json.dump({"type": "FeatureCollection", "features": pipe_features}, f, indent=2)

    # 4. Inverted AOI Mask Polygon (Hole matching exact Nellore City + Kovur Mandal)
    with open(os.path.join(DATA_DIR, "boundaries", "nellore_kovur_aoi.geojson")) as f:
        aoi_data = json.load(f)

    # World outer box
    world_ring = [
        [-180.0, -90.0],
        [180.0, -90.0],
        [180.0, 90.0],
        [-180.0, 90.0],
        [-180.0, -90.0]
    ]

    # Extract coordinates of Nellore and Kovur polygons to use as holes
    nellore_hole = aoi_data["features"][0]["geometry"]["coordinates"][0]
    kovur_hole = aoi_data["features"][1]["geometry"]["coordinates"][0]

    inverted_mask = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": { "name": "Nellore & Kovur Exclusion Mask", "purpose": "Focus display strictly on study area" },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [world_ring, nellore_hole, kovur_hole]
                }
            }
        ]
    }
    with open(os.path.join(DATA_DIR, "boundaries", "aoi_inverted_mask.geojson"), "w") as f:
        json.dump(inverted_mask, f, indent=2)

    print("✓ Created Water Flow Network, Overhead Tanks, Underground Sources, and Inverted Mask!")

    # Export Boundaries and Water Infrastructure to Shapefiles
    export_boundaries_shapefiles()
    water_network = {
        "sources": sources,
        "tanks": tanks,
        "pipelines": pipelines
    }
    export_water_network_shapefile(water_network)
    create_shapefiles_zip()

if __name__ == "__main__":
    generate_water_infrastructure_and_flow()
