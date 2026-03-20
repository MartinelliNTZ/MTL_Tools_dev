# 🧾 Coord Click — Guía de Uso

Coord Click es una herramienta del paquete **Cadmus** que permite hacer clic en el mapa y obtener información detallada del punto, incluyendo coordenadas, proyección, dirección y altitud.

---

## 🎯 Objetivo

Permitir una inspección rápida de cualquier punto en el mapa con:

* Coordenadas WGS84 (decimal y DMS)
* Coordenadas UTM (SIRGAS 2000)
* Información de zona y EPSG
* Altitud aproximada (OpenTopoData)
* Dirección mediante geocodificación inversa (OpenStreetMap)

---

## 🛠️ Cómo usar

### 1️⃣ Activar la herramienta

Menú → Cadmus → Coord Click

### 2️⃣ Hacer clic en el mapa

Haz clic en cualquier punto del canvas.

### 3️⃣ Ver los resultados

Se abrirá (o actualizará) un diálogo con:

* **WGS84**

  * Latitud/Longitud en decimal
  * Latitud/Longitud en DMS

* **UTM**

  * Easting (X)
  * Northing (Y)
  * Zona, hemisferio y EPSG

* **Altimetría**

  * Valor aproximado cargado automáticamente

* **Dirección**

  * Municipio
  * Región intermedia
  * Estado
  * Región
  * País

---

## ⚙️ Funcionamiento interno

La herramienta utiliza un pipeline asíncrono:

* Ejecución en paralelo de:

  * Geocodificación inversa
  * Consulta de altitud
* Motor: `AsyncPipelineEngine`
* Pasos:

  * `ReverseGeocodeStep`
  * `AltimetryStep`

Si el pipeline falla:

* Se utiliza fallback automático con `QgsTask`

---

## 🔎 Dependencias

* OpenStreetMap (geocodificación inversa)
* OpenTopoData (altitud)

Se requiere conexión a internet.

---

## 🧾 Acciones disponibles

* **Copiar datos completos WGS**
* **Copiar datos completos UTM**
* **Copiar ubicación completa (botón dedicado)**
* Actualización automática al hacer clic en nuevos puntos

---

## 🧠 Comportamientos importantes

* Si el diálogo ya está abierto → se reutiliza
* Las tareas anteriores se cancelan automáticamente
* El snapping es respetado si está activo
* Los datos asíncronos (dirección/altitud) pueden tardar algunos segundos

---

## ⚠️ Limitaciones

* La altitud es aproximada (modelo externo)
* La dirección depende de la cobertura de OSM
* Sin internet → solo se muestran coordenadas

---

## ❤️ Creado por

Matheus A.S. Martinelli
