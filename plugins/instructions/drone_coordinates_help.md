# 📘 Coordenadas de Drone (MRK) – Manual de Utilização  
Ferramenta do pacote **MTL Tools** para geração de **pontos e trajetos de voo de drone** a partir de arquivos **MRK**.

---

## 📌 O que esta ferramenta faz?

Esta ferramenta lê arquivos **MRK gerados por drones DJI** e permite:

- Gerar **pontos das fotos** do voo
- Gerar o **trajeto (linha)** do drone
- Opcionalmente **cruzar os pontos com metadados das fotos JPG**
- Salvar resultados em arquivo ou criar **camadas temporárias**
- Aplicar **estilos QML** automaticamente
- Processar grandes volumes sem travar o QGIS

---

## 🧩 Componentes principais

### ✔ Pasta dos MRK
Define a pasta onde estão os arquivos `.mrk`.

- Pode conter **subpastas**
- Pode haver **vários MRKs**

---

### ✔ Vasculhar subpastas
Quando marcado, a ferramenta procura arquivos MRK em todas as subpastas da pasta selecionada.

---

### ✔ Unir todos os MRK
Quando ativado, todos os arquivos MRK encontrados são tratados como **um único voo**, gerando:

- Um único conjunto de pontos
- Um único trajeto

---

### ✔ Cruzar com metadados das fotos
Permite enriquecer os pontos MRK com informações extraídas das fotos JPG, como:

- Nome do arquivo
- Tamanho
- Datas
- Dimensões da imagem
- ISO, abertura, distância focal, etc.

⚠ **Atenção:**  
Não recomendado para **grandes volumes de fotos**, pois o processamento é mais pesado.

---

## 📍 Pontos MRK

### ✔ Salvar pontos em arquivo
Permite salvar os pontos em:

- Shapefile (`.shp`)
- GeoPackage (`.gpkg`)
- GeoJSON (`.geojson`)
- KML (`.kml`)

Se desmarcado, os pontos serão criados como **camada temporária**.

---

### ✔ Aplicar estilo (QML) nos pontos
Permite selecionar um arquivo `.qml` para estilizar automaticamente a camada de pontos.

---

## 🧭 Trajeto do Drone (Linha)

### ✔ Salvar trajeto em arquivo
Permite salvar o trajeto do drone em:

- Shapefile
- GeoPackage
- GeoJSON
- KML
- CSV

Se desmarcado, o trajeto será criado como **camada temporária**.

---

### ✔ Aplicar estilo (QML) no trajeto
Permite aplicar um estilo `.qml` ao rastro do drone.

Se nenhum QML for informado, a ferramenta pode aplicar um **estilo padrão do plugin**.

---

## ▶ Como usar

### 1. Abrir a ferramenta  
Menu → **MTL Tools** → **Agricultura de Precisão** → *Obter Coordenadas de Drone*

---

### 2. Selecionar a pasta dos MRK
Clique em **…** e escolha a pasta onde estão os arquivos `.mrk`.

---

### 3. Definir opções desejadas
Marque conforme sua necessidade:

- Vasculhar subpastas
- Unir MRKs
- Cruzar com fotos
- Salvar pontos
- Salvar trajeto
- Aplicar estilos

---

### 4. Definir caminhos de saída (opcional)
Caso opte por salvar em arquivo:

- Escolha o local e formato
- Selecione QMLs, se desejar

---

### 5. Clique em **Executar**
A ferramenta irá:

1. Ler todos os MRKs encontrados  
2. Criar os pontos  
3. Criar o trajeto  
4. Cruzar com fotos (se ativado)  
5. Adicionar as camadas ao projeto  

O progresso e mensagens são registrados automaticamente.

---

## 🔄 Salvamento de preferências

Todas as opções escolhidas são salvas automaticamente.  
Na próxima abertura da ferramenta, os campos serão preenchidos com as últimas configurações usadas.

---

## ℹ️ Observações importantes

- Para arquivos **KML**, a reprojeção para **EPSG:4326** é feita automaticamente
- Camadas temporárias não são salvas no disco
- Grandes volumes de fotos podem levar mais tempo para processar

---

## 🔑 Chave interna da ferramenta

Esta ferramenta utiliza a seguinte chave para salvar preferências:

`drone_coordinates`
