"""
Process GADM 4.1 Boundaries for Nellore & Kovur
Clips and structures the exact AOI boundaries, generates inverted exclusion mask,
and creates 3D extruded boundary curtain for WebGL 3D visualization.
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
BOUND_DIR = os.path.join(DATA_DIR, "boundaries")

def process_gadm():
    gadm_path = os.path.join(BOUND_DIR, "gadm_nellore_kovur.geojson")
    with open(gadm_path) as f:
        gadm_data = json.load(f)

    # 1. Create Clean AOI GeoJSON
    aoi_features = []
    holes = []

    for feat in gadm_data["features"]:
        p = feat["properties"]
        geom = feat["geometry"]
        gadm_name = p.get("NAME_3", p.get("gadm_name", ""))
        is_nellore = "nellore" in gadm_name.lower()
        
        cleaned_props = {
            "name": "Nellore Municipal Corporation" if is_nellore else "Kovur Mandal",
            "gadm_name": gadm_name,
            "gadm_gid": p.get("GID_3", "IND.2.7.14_1" if is_nellore else "IND.2.7.4_1"),
            "district": "SPSR Nellore",
            "state": "Andhra Pradesh",
            "country": "India",
            "source": "GADM 4.1 & AP Government",
            "type": "Urban Local Body (NMC)" if is_nellore else "Mandal / Taluk",
            "area_sq_km": 150.4 if is_nellore else 112.8,
            "population_est": 600000 if is_nellore else 125000,
            "wards_or_gps": 54 if is_nellore else 18,
            "clip_3d_height": 75,
            "border_color": "#38bdf8" if is_nellore else "#0284c7"
        }

        aoi_features.append({
            "type": "Feature",
            "properties": cleaned_props,
            "geometry": geom
        })

        # Collect rings for inverted mask
        if geom["type"] == "MultiPolygon":
            for poly in geom["coordinates"]:
                holes.append(poly[0])
        elif geom["type"] == "Polygon":
            holes.append(geom["coordinates"][0])

    aoi_geojson = {
        "type": "FeatureCollection",
        "name": "GADM_Nellore_Kovur_AOI",
        "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
        "features": aoi_features
    }

    with open(os.path.join(BOUND_DIR, "nellore_kovur_aoi.geojson"), "w") as f:
        json.dump(aoi_geojson, f, indent=2)

    # Separate individual files
    with open(os.path.join(BOUND_DIR, "nellore_corporation_boundary.geojson"), "w") as f:
        json.dump({"type": "FeatureCollection", "features": [aoi_features[1] if "nellore" in aoi_features[1]["properties"]["gadm_name"].lower() else aoi_features[0]]}, f, indent=2)

    with open(os.path.join(BOUND_DIR, "kovur_mandal_boundary.geojson"), "w") as f:
        json.dump({"type": "FeatureCollection", "features": [aoi_features[0] if "kov" in aoi_features[0]["properties"]["gadm_name"].lower() else aoi_features[1]]}, f, indent=2)

    # 2. Inverted Exclusion Mask (Dims everything outside GADM Nellore & Kovur)
    world_ring = [
        [-180.0, -90.0],
        [180.0, -90.0],
        [180.0, 90.0],
        [-180.0, 90.0],
        [-180.0, -90.0]
    ]

    inverted_mask = {
        "type": "FeatureCollection",
        "name": "GADM_Nellore_Kovur_Inverted_Mask",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "name": "Nellore & Kovur GADM Strict Clip Mask",
                    "source": "GADM 4.1",
                    "description": "Excludes everything outside Nellore NMC and Kovur Mandal"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [world_ring] + holes
                }
            }
        ]
    }

    with open(os.path.join(BOUND_DIR, "aoi_inverted_mask.geojson"), "w") as f:
        json.dump(inverted_mask, f, indent=2)

    # 3. 3D Boundary Extrusion Curtain GeoJSON (for WebGL 3D clipping in Mapbox GL)
    curtain_features = []
    for feat in aoi_features:
        p = feat["properties"]
        geom = feat["geometry"]
        curtain_features.append({
            "type": "Feature",
            "properties": {
                "name": f"{p['name']} 3D Perimeter Curtain",
                "height": 75,
                "base_height": 0,
                "color": p["border_color"],
                "opacity": 0.3
            },
            "geometry": geom
        })

    curtain_geojson = {
        "type": "FeatureCollection",
        "name": "GADM_3D_Boundary_Curtain",
        "features": curtain_features
    }

    with open(os.path.join(BOUND_DIR, "aoi_3d_clip_curtain.geojson"), "w") as f:
        json.dump(curtain_geojson, f, indent=2)

    print("✓ GADM 4.1 Processing complete!")
    print(f"  • Processed {len(aoi_features)} GADM features (Nellore & Kovur)")
    print(f"  • Created Inverted Mask with {len(holes)} boundary rings")
    print(f"  • Created 3D Boundary Curtain with 75m height extrusion")

if __name__ == "__main__":
    process_gadm()
