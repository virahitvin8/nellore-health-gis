"""
Shapefile Generator for Health GIS: Nellore City & Kovur Mandal
Exports genuine ESRI Shapefiles (.shp, .shx, .dbf, .prj in WGS84 EPSG:4326)
Contains exact boundaries, water supply network, overhead tanks, underground wells, and landmarks.
"""

import os
import json
import zipfile
import shapefile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SHP_DIR = os.path.join(DATA_DIR, "shapefiles")
os.makedirs(SHP_DIR, exist_ok=True)

# Standard WGS84 .prj content
WGS84_PRJ = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'

def write_prj(filepath):
    with open(filepath, "w") as f:
        f.write(WGS84_PRJ)

def extract_rings(geom):
    if geom["type"] == "MultiPolygon":
        rings = []
        for poly in geom["coordinates"]:
            for ring in poly:
                rings.append(ring)
        return rings
    elif geom["type"] == "Polygon":
        return geom["coordinates"]
    return []

def export_boundaries_shapefiles():
    # 1. Nellore Municipal Corporation Boundary (GADM 4.1)
    with open(os.path.join(DATA_DIR, "boundaries", "nellore_corporation_boundary.geojson")) as f:
        nellore_data = json.load(f)
    
    shp_path = os.path.join(SHP_DIR, "nellore_city_boundary")
    w = shapefile.Writer(shp_path, shapefile.POLYGON)
    w.field("NAME", "C", size=50)
    w.field("GADM_GID", "C", size=20)
    w.field("TYPE", "C", size=30)
    w.field("DISTRICT", "C", size=30)
    w.field("STATE", "C", size=30)
    w.field("SOURCE", "C", size=30)
    w.field("AREA_SQKM", "F", decimal=2)
    w.field("POP_EST", "N", size=10)

    for feat in nellore_data["features"]:
        rings = extract_rings(feat["geometry"])
        p = feat["properties"]
        w.poly(rings)
        w.record(p["name"], p.get("gadm_gid", "IND.2.7.14_1"), p["type"], p["district"], p["state"], p.get("source", "GADM 4.1"), p["area_sq_km"], p["population_est"])
    w.close()
    write_prj(shp_path + ".prj")

    # 2. Kovur Mandal Boundary (GADM 4.1)
    with open(os.path.join(DATA_DIR, "boundaries", "kovur_mandal_boundary.geojson")) as f:
        kovur_data = json.load(f)
    
    shp_path = os.path.join(SHP_DIR, "kovur_mandal_boundary")
    w = shapefile.Writer(shp_path, shapefile.POLYGON)
    w.field("NAME", "C", size=50)
    w.field("GADM_GID", "C", size=20)
    w.field("TYPE", "C", size=30)
    w.field("DISTRICT", "C", size=30)
    w.field("STATE", "C", size=30)
    w.field("SOURCE", "C", size=30)
    w.field("AREA_SQKM", "F", decimal=2)
    w.field("POP_EST", "N", size=10)

    for feat in kovur_data["features"]:
        rings = extract_rings(feat["geometry"])
        p = feat["properties"]
        w.poly(rings)
        w.record(p["name"], p.get("gadm_gid", "IND.2.7.4_1"), p["type"], p["district"], p["state"], p.get("source", "GADM 4.1"), p["area_sq_km"], p["population_est"])
    w.close()
    write_prj(shp_path + ".prj")

    print("✓ Exported GADM 4.1 Boundaries Shapefiles")

def export_water_network_shapefile(water_network):
    # Pipelines
    shp_path = os.path.join(SHP_DIR, "water_distribution_pipelines")
    w = shapefile.Writer(shp_path, shapefile.POLYLINE)
    w.field("PIPE_ID", "C", size=20)
    w.field("LINE_NAME", "C", size=60)
    w.field("FROM_NODE", "C", size=40)
    w.field("TO_NODE", "C", size=40)
    w.field("FLOW_DIR", "C", size=30)
    w.field("DIA_MM", "N", size=6)
    w.field("MATERIAL", "C", size=20)
    w.field("FLOW_MLD", "F", decimal=2)
    w.field("PRESSURE_B", "F", decimal=1)

    for p in water_network["pipelines"]:
        w.line([p["coordinates"]])
        w.record(p["pipe_id"], p["name"], p["from_node"], p["to_node"], p["flow_direction"], p["diameter_mm"], p["material"], p["discharge_mld"], p["pressure_bar"])
    w.close()
    write_prj(shp_path + ".prj")

    # Overhead Storage Tanks
    shp_path = os.path.join(SHP_DIR, "overhead_storage_tanks")
    w = shapefile.Writer(shp_path, shapefile.POINT)
    w.field("TANK_ID", "C", size=20)
    w.field("NAME", "C", size=60)
    w.field("ZONE", "C", size=40)
    w.field("CAP_MLD", "F", decimal=2)
    w.field("HEIGHT_M", "N", size=4)
    w.field("SUPPLY_POP", "N", size=10)
    w.field("STATUS", "C", size=30)

    for t in water_network["tanks"]:
        w.point(t["lon"], t["lat"])
        w.record(t["id"], t["name"], t["zone"], t["capacity_mld"], t["staging_height_m"], t["supply_population"], t["operational_status"])
    w.close()
    write_prj(shp_path + ".prj")

    # Raw Water Sources & Infiltration Wells
    shp_path = os.path.join(SHP_DIR, "underground_wells_sources")
    w = shapefile.Writer(shp_path, shapefile.POINT)
    w.field("SRC_ID", "C", size=20)
    w.field("NAME", "C", size=60)
    w.field("SRC_TYPE", "C", size=40)
    w.field("YIELD_LPH", "N", size=10)
    w.field("DEPTH_M", "N", size=5)
    w.field("AQUIFER", "C", size=40)

    for s in water_network["sources"]:
        w.point(s["lon"], s["lat"])
        w.record(s["id"], s["name"], s["type"], s["yield_lph"], s["depth_m"], s["aquifer_source"])
    w.close()
    write_prj(shp_path + ".prj")

    print("✓ Exported Water Infrastructure Shapefiles")

def export_rbk_shapefiles():
    rbk_path = os.path.join(DATA_DIR, "infrastructure", "rythu_bharosa_kendrams.geojson")
    if not os.path.exists(rbk_path):
        return
    with open(rbk_path) as f:
        data = json.load(f)

    shp_path = os.path.join(SHP_DIR, "rythu_bharosa_kendrams")
    w = shapefile.Writer(shp_path, shapefile.POINT)
    w.field("RBK_ID", "C", size=20)
    w.field("NAME", "C", size=60)
    w.field("MANDAL", "C", size=40)
    w.field("OFFICER", "C", size=50)
    w.field("PHONE", "C", size=20)
    w.field("FARMERS", "N", size=6)
    w.field("ACRES", "N", size=6)
    w.field("CROP", "C", size=50)

    for feat in data["features"]:
        p = feat["properties"]
        coords = feat["geometry"]["coordinates"]
        w.point(coords[0], coords[1])
        w.record(p["rbk_id"], p["name"], p["mandal"], p["agri_officer"], p["phone"], p["coverage_farmers"], p["ayacut_acres"], p["primary_crop"])
    w.close()
    write_prj(shp_path + ".prj")
    print("✓ Exported Rythu Bharosa Kendram (RBK) Shapefiles")

def create_shapefiles_zip():
    zip_filename = os.path.join(SHP_DIR, "nellore_kovur_gis_shapefiles.zip")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(SHP_DIR):
            for file in files:
                if file != "nellore_kovur_gis_shapefiles.zip":
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, SHP_DIR)
                    zipf.write(full_path, arcname)
    print(f"✓ Created Shapefile ZIP archive: {zip_filename}")

if __name__ == "__main__":
    export_boundaries_shapefiles()
    export_rbk_shapefiles()
    create_shapefiles_zip()
