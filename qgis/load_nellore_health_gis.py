"""
QGIS Automated Layer Loader & Symbology Script
Health GIS: Nellore City & Kovur Mandal Wet Market Geo-Risk Analytics

Instructions for QGIS:
1. Open QGIS (version 3.16+ / 3.28+ / 3.34+).
2. Go to: Plugins -> Python Console (or press Ctrl + Alt + P).
3. Click the 'Show Editor' icon (the notepad icon in the Python Console).
4. Open this script or paste this code into the editor.
5. Update PROJECT_DIR below to match the folder where you cloned/downloaded this project.
6. Click the Green 'Run Script' button (or press F5).
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

# EDIT THIS PATH TO YOUR LOCAL REPOSITORY FOLDER:
# e.g., "C:/Users/YourName/Documents/interactive-project" or "/home/user/interactive-project"
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_DIR, "data")

print(f"Loading Health GIS Layers from: {DATA_DIR}")

project = QgsProject.instance()

# 1. Administrative Boundaries
boundary_path = os.path.join(DATA_DIR, "boundaries", "nellore_kovur_aoi.geojson")
boundary_layer = QgsVectorLayer(boundary_path, "Administrative Boundaries (Nellore & Kovur)", "ogr")
if boundary_layer.isValid():
    sym = QgsSymbol.defaultSymbol(boundary_layer.geometryType())
    sym.symbolLayer(0).setStrokeColor(QColor(56, 189, 248))
    sym.symbolLayer(0).setStrokeWidth(0.8)
    sym.symbolLayer(0).setStrokeStyle(5) # Dash line
    sym.symbolLayer(0).setFillColor(QColor(56, 189, 248, 20)) # Translucent
    boundary_layer.setRenderer(QgsCategorizedSymbolRenderer())
    boundary_layer.renderer().setSourceSymbol(sym)
    project.addMapLayer(boundary_layer)
    print("✓ Loaded Boundaries Layer")

# 2. Waterbodies & Pennar River
water_path = os.path.join(DATA_DIR, "infrastructure", "pennar_river_waterbodies.geojson")
water_layer = QgsVectorLayer(water_path, "Pennar River Basin & Canals", "ogr")
if water_layer.isValid():
    sym = QgsSymbol.defaultSymbol(water_layer.geometryType())
    sym.setColor(QColor(2, 132, 199, 140))
    water_layer.renderer().setSourceSymbol(sym)
    project.addMapLayer(water_layer)
    print("✓ Loaded Waterbodies Layer")

# 3. Open Drainage & Sewage Network (Biohazard Vector)
drain_path = os.path.join(DATA_DIR, "infrastructure", "open_drainage_sewage_network.geojson")
drain_layer = QgsVectorLayer(drain_path, "Open Drainage & Sullage Lines (Hazard Vector)", "ogr")
if drain_layer.isValid():
    sym = QgsSymbol.defaultSymbol(drain_layer.geometryType())
    sym.setColor(QColor(239, 68, 68))
    sym.setWidth(1.2)
    sym.symbolLayer(0).setStrokeStyle(2) # Dash line
    drain_layer.renderer().setSourceSymbol(sym)
    project.addMapLayer(drain_layer)
    print("✓ Loaded Open Drainage Network Layer")

# 4. 250m Risk Buffers
buffer_path = os.path.join(DATA_DIR, "risk_analysis", "market_risk_buffers_250m.geojson")
buffer_layer = QgsVectorLayer(buffer_path, "250m Bio-Aerosol Hazard Buffers", "ogr")
if buffer_layer.isValid():
    sym = QgsSymbol.defaultSymbol(buffer_layer.geometryType())
    sym.setColor(QColor(217, 4, 41, 45))
    sym.symbolLayer(0).setStrokeColor(QColor(217, 4, 41, 180))
    sym.symbolLayer(0).setStrokeWidth(0.5)
    buffer_layer.renderer().setSourceSymbol(sym)
    project.addMapLayer(buffer_layer)
    print("✓ Loaded 250m Buffers Layer")

# 5. Healthcare Facilities
hosp_path = os.path.join(DATA_DIR, "infrastructure", "healthcare_facilities.geojson")
hosp_layer = QgsVectorLayer(hosp_path, "Hospitals & Primary Health Centres", "ogr")
if hosp_layer.isValid():
    sym = QgsSymbol.defaultSymbol(hosp_layer.geometryType())
    sym.setColor(QColor(0, 119, 182))
    sym.setSize(4.5)
    hosp_layer.renderer().setSourceSymbol(sym)
    project.addMapLayer(hosp_layer)
    print("✓ Loaded Healthcare Facilities Layer")

# 6. Classified Wet Markets (Risk-Categorized Symbology)
market_path = os.path.join(DATA_DIR, "risk_analysis", "market_geo_risk_classified.geojson")
market_layer = QgsVectorLayer(market_path, "Wet Markets (Geo-Risk Classified)", "ogr")
if market_layer.isValid():
    categories = []
    
    risk_styling = [
        ("Very High Risk", QColor(217, 4, 41), 4.2),   # Crimson Red
        ("High Risk", QColor(247, 127, 0), 3.8),        # Amber Orange
        ("Moderate Risk", QColor(255, 209, 102), 3.2),  # Golden Yellow
        ("Low Risk", QColor(6, 214, 160), 2.8)          # Emerald Green
    ]

    for val, color, size in risk_styling:
        sym = QgsSymbol.defaultSymbol(market_layer.geometryType())
        sym.setColor(color)
        sym.setSize(size)
        sym.symbolLayer(0).setStrokeColor(QColor(255, 255, 255))
        sym.symbolLayer(0).setStrokeWidth(0.5)
        category = QgsRendererCategory(val, sym, val)
        categories.append(category)

    renderer = QgsCategorizedSymbolRenderer("risk_level", categories)
    market_layer.setRenderer(renderer)
    project.addMapLayer(market_layer)
    print("✓ Loaded and Styled Wet Markets Layer")

# Zoom map canvas to Area of Interest
if boundary_layer.isValid():
    from qgis.utils import iface
    iface.mapCanvas().setExtent(boundary_layer.extent())
    iface.mapCanvas().refresh()
    print("Successfully zoomed to Nellore & Kovur AOI!")
