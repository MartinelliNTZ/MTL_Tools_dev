# 🧾 Coord Click — User Guide

Coord Click is a tool from the **Cadmus** suite that allows you to click on the map and instantly retrieve detailed information about a location, including coordinates, projection data, address, and altitude.

---

## 🎯 Purpose

Provide fast inspection of any point on the map with:

* WGS84 coordinates (decimal and DMS)
* UTM coordinates (SIRGAS 2000)
* Zone and EPSG information
* Approximate altitude (OpenTopoData)
* Reverse geocoded address (OpenStreetMap)

---

## 🛠️ How to Use

### 1️⃣ Activate the tool

Menu → Cadmus → Coord Click

### 2️⃣ Click on the map

Click anywhere on the map canvas.

### 3️⃣ View the results

A dialog will open (or update) displaying:

* **WGS84**

  * Latitude/Longitude (decimal)
  * Latitude/Longitude (DMS)

* **UTM**

  * Easting (X)
  * Northing (Y)
  * Zone, hemisphere, and EPSG

* **Altimetry**

  * Automatically loaded approximate value

* **Address**

  * Municipality
  * Intermediate region
  * State
  * Region
  * Country

---

## ⚙️ Internal Workflow

The tool uses an asynchronous pipeline:

* Parallel execution of:

  * Reverse geocoding
  * Altimetry query
* Engine: `AsyncPipelineEngine`
* Steps:

  * `ReverseGeocodeStep`
  * `AltimetryStep`

If the pipeline fails:

* Automatic fallback to `QgsTask`

---

## 🔎 Dependencies

* OpenStreetMap (reverse geocoding)
* OpenTopoData (altitude)

An internet connection is required.

---

## 🧾 Available Actions

* **Copy full WGS data**
* **Copy full UTM data**
* **Copy full location (dedicated button)**
* Automatic updates when clicking new points

---

## 🧠 Important Behaviors

* If the dialog is already open → it will be reused
* Previous tasks are automatically canceled
* Snapping is respected when enabled
* Asynchronous data (address/altitude) may take a few seconds

---

## ⚠️ Limitations

* Altitude is approximate (external model)
* Address depends on OSM coverage
* Without internet → only coordinates are shown


---

## Created by

Matheus A.S. Martinelli
