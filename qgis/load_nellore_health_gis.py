"""
QGIS Automated Layer Loader & Symbology Script (Comprehensive Edition)
Health GIS: Nellore City & Kovur Mandal Wet Markets, Water Pipelines, RO Plants, & Hospitals

Instructions for QGIS:
1. Open QGIS (version 3.16+ / 3.28+ / 3.34+).
2. Go to: Plugins -> Python Console (or press Ctrl + Alt + P).
3. Click the 'Show Editor' icon (the notepad icon in the Python Console).
4. Open this script or paste this code into the editor.
5. Click the Green 'Run Script' button (or press F5).
All layers will load, categorize by risk colors, and zoom into Nellore & Kovur!
"""

import os
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsSymbol,
    QgsRendererCategory,
    QgsCategorizedSymbolRenderer,
    QgsSimpleMarkerSymbolLayer,
    QgsSimpleLineSymbolLayer,
    QgsSimpleFillSymbolLayer
)
from PyQt5.QtGui import QColor

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_DIR, "data")

print(f"Loading Health GIS Layers from: {DATA_DIR}")
project = QgsProject.instance()

# 1. Administrative Boundaries (Nellore NMC & Kovur Mandal)
boundary_path = os.path.join(DATA_DIR, "boundaries", "nellore_kovur_aoi.geojson")
boundary_layer = QgsVectorLayer(boundary_path, "Administrative Boundaries (Nellore NMC & Kovur GP)", "ogr")
if boundary_layer.isValid():
    sym = QgsSymbol.defaultSymbol(boundary_layer.geometryType())
    sym.symbolLayer(0).setStrokeColor(QColor(56, 189, 248))
    sym.symbolLayer(0).setStrokeWidth(0.8)
    sym.symbolLayer(0).setStrokeStyle(5)
    sym.symbolLayer(0).setFillColor(QColor(56, 189, 248, 25))
    boundary_layer.renderer().setSourceSymbol(sym)
    project.addMapLayer(boundary_layer)
    print("✓ Loaded Administrative Boundaries Layer")

# 2. Waterbodies & Pennar River
water_path = os.path.join(DATA_DIR, "infrastructure", "pennar_river_waterbodies.geojson")
water_layer = QgsVectorLayer(water_path, "Pennar River Basin & Irrigation Canals", "ogr")
if water_layer.isValid():
    sym = QgsSymbol.defaultSymbol(water_layer.geometryType())
    sym.setColor(QColor(2, 132, 199, 140))
    water_layer.renderer().setSourceSymbol(sym)
    project.addMapLayer(water_layer)
    print("✓ Loaded River Basin Layer")

# 3. Open Drainage & Sewage Network (Biohazard Vector)
drain_path = os.path.join(DATA_DIR, "infrastructure", "open_drainage_sewage_network.geojson")
drain_layer = QgsVectorLayer(drain_path, "Open Drainage & Sullage Lines (Hazard Vector)", "ogr")
if drain_layer.isValid():
    sym = QgsSymbol.defaultSymbol(drain_layer.geometryType())
    sym.setColor(QColor(239, 68, 68))
    sym.setWidth(1.2)
    sym.symbolLayer(0).setStrokeStyle(2) # Red dashed
    drain_layer.renderer().setSourceSymbol(sym)
    project.addMapLayer(drain_layer)
    print("✓ Loaded Open Drainage Network Layer")

# 4. Drinking Water Pipelines (NMC & Panchayati)
pipe_path = os.path.join(DATA_DIR, "infrastructure", "drinking_water_pipelines.geojson")
pipe_layer = QgsVectorLayer(pipe_path, "Drinking Water Pipelines (NMC & Panchayati)", "ogr")
if pipe_layer.isValid():
    sym = QgsSymbol.defaultSymbol(pipe_layer.geometryType())
    sym.setColor(QColor(14, 165, 233))
    sym.setWidth(1.4)
    pipe_layer.renderer().setSourceSymbol(sym)
    project.addMapLayer(pipe_layer)
    print("✓ Loaded Drinking Water Pipelines Layer")

# 5. Drinking Water Points (RO Plants, Borewells, Hand Pumps)
wp_path = os.path.join(DATA_DIR, "infrastructure", "water_points_ro_plants.geojson")
wp_layer = QgsVectorLayer(wp_path, "RO Water Plants & Public Hand Pumps", "ogr")
if wp_layer.isValid():
    sym = QgsSymbol.defaultSymbol(wp_layer.geometryType())
    sym.setColor(QColor(56, 189, 248))
    sym.setSize(3.2)
    wp_layer.renderer().setSourceSymbol(sym)
    project.addMapLayer(wp_layer)
    print("✓ Loaded Drinking Water Points Layer")

# 6. Vegetable Markets & Rythu Bazaars
veg_path = os.path.join(DATA_DIR, "markets", "vegetable_markets.geojson")
veg_layer = QgsVectorLayer(veg_path, "Vegetable Markets & Rythu Bazaars (Govt of AP)", "ogr")
if veg_layer.isValid():
    sym = QgsSymbol.defaultSymbol(veg_layer.geometryType())
    sym.setColor(QColor(16, 185, 129))
    sym.setSize(4.0)
    veg_layer.renderer().setSourceSymbol(sym)
    project.addMapLayer(veg_layer)
    print("✓ Loaded Vegetable Markets Layer")

# 7. Hospitals & Healthcare (Govt + Private)
hosp_path = os.path.join(DATA_DIR, "infrastructure", "healthcare_facilities.geojson")
hosp_layer = QgsVectorLayer(hosp_path, "Hospitals (Government & Private)", "ogr")
if hosp_layer.isValid():
    sym = QgsSymbol.defaultSymbol(hosp_layer.geometryType())
    sym.setColor(QColor(244, 63, 94))
    sym.setSize(4.2)
    hosp_layer.renderer().setSourceSymbol(sym)
    project.addMapLayer(hosp_layer)
    print("✓ Loaded Hospitals Layer")

# 8. 250m Risk Buffers
buffer_path = os.path.join(DATA_DIR, "risk_analysis", "market_risk_buffers_250m.geojson")
buffer_layer = QgsVectorLayer(buffer_path, "250m Bio-Aerosol Hazard Buffers", "ogr")
if buffer_layer.isValid():
    sym = QgsSymbol.defaultSymbol(buffer_layer.geometryType())
    sym.setColor(QColor(217, 4, 41, 40))
    sym.symbolLayer(0).setStrokeColor(QColor(217, 4, 41, 160))
    sym.symbolLayer(0).setStrokeWidth(0.5)
    buffer_layer.renderer().setSourceSymbol(sym)
    project.addMapLayer(buffer_layer)
    print("✓ Loaded 250m Buffers Layer")

# 9. Classified Wet Markets (Geo-Risk Symbology)
market_path = os.path.join(DATA_DIR, "risk_analysis", "market_geo_risk_classified.geojson")
market_layer = QgsVectorLayer(market_path, "Wet Markets (Geo-Risk Classified)", "ogr")
if market_layer.isValid():
    categories = []
    risk_styling = [
        ("Very High Risk", QColor(217, 4, 41), 4.4),
        ("High Risk", QColor(247, 127, 0), 3.8),
        ("Moderate Risk", QColor(255, 209, 102), 3.2),
        ("Low Risk", QColor(6, 214, 160), 2.8)
    ]
    for val, color, size in risk_styling:
        sym = QgsSymbol.defaultSymbol(market_layer.geometryType())
        sym.setColor(color)
        sym.setSize(size)
        sym.symbolLayer(0).setStrokeColor(QColor(255, 255, 255))
        sym.symbolLayer(0).setStrokeWidth(0.6)
        category = QgsRendererCategory(val, sym, val)
        categories.append(category)

    renderer = QgsCategorizedSymbolRenderer("risk_level", categories)
    market_layer.setRenderer(renderer)
    project.addMapLayer(market_layer)
    print("✓ Loaded and Styled Wet Markets Layer")

# Zoom map canvas
if boundary_layer.isValid():
    from qgis.utils import iface
    iface.mapCanvas().setExtent(boundary_layer.extent())
    iface.mapCanvas().refresh()
    print("✓ Successfully zoomed to Nellore & Kovur AOI!")
