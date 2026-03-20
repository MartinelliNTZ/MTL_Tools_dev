# 🧾 Coord Click — Guia de Uso

Coord Click é uma ferramenta do pacote **Cadmus** para capturar coordenadas diretamente no mapa, exibindo informações completas do ponto clicado, incluindo localização, projeção, endereço e altitude.

---

## 🎯 Objetivo

Permitir inspeção rápida de um ponto no mapa com:

* Coordenadas em WGS84 (decimal e DMS)
* Coordenadas UTM (SIRGAS 2000)
* Informações de zona e EPSG
* Altitude aproximada (OpenTopoData)
* Endereço reverso (OpenStreetMap)

---

## 🛠️ Como usar

### 1️⃣ Ative a ferramenta

Menu → Cadmus → Coord Click

### 2️⃣ Clique no mapa

Clique em qualquer ponto do canvas.

### 3️⃣ Visualize os dados

Um diálogo será aberto (ou atualizado) com:

* **WGS84**

  * Latitude/Longitude decimal
  * Latitude/Longitude em DMS

* **UTM**

  * Easting (X)
  * Northing (Y)
  * Zona, hemisfério e EPSG

* **Altimetria**

  * Valor aproximado carregado automaticamente

* **Endereço**

  * Município
  * Região intermediária
  * Estado
  * Região
  * País

---

## ⚙️ Funcionamento interno

A ferramenta utiliza um pipeline assíncrono:

* Execução paralela de:

  * Geocodificação reversa
  * Consulta de altitude
* Engine: `AsyncPipelineEngine`
* Steps:

  * `ReverseGeocodeStep`
  * `AltimetryStep`

Caso o pipeline falhe:

* fallback automático para `QgsTask`

---

## 🔎 Dependências

* OpenStreetMap (geocodificação reversa)
* OpenTopoData (altitude)

Requer conexão com internet.

---

## 🧾 Interações disponíveis

* **Copiar WGS completo**
* **Copiar UTM completo**
* **Copiar localização completa (botão dedicado)**
* Atualização automática ao clicar em novos pontos

---

## 🧠 Comportamentos importantes

* Se o diálogo já estiver aberto → ele é reutilizado
* Tasks anteriores são canceladas automaticamente
* Clique com snapping ativo respeita feições próximas
* Dados assíncronos (endereço/altitude) podem demorar alguns segundos

---

## ⚠️ Limitações

* Altitude é aproximada (modelo externo)
* Endereço depende da cobertura do OSM
* Sem internet → apenas coordenadas são exibidas

---

##  Criado por

Matheus A.S. Martinelli
