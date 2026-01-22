# 📘 Ferramenta: Carregar Pasta de Arquivos
Bem-vindo(a)! Esta ferramenta foi criada para agilizar o processo de carregar grandes volumes de arquivos no QGIS, mantendo organização, evitando duplicações e permitindo automações úteis no dia a dia.  

---

## 🎯 Objetivo
Permitir que você selecione uma pasta raiz e carregue automaticamente **todos os layers encontrados dentro dela**, incluindo subpastas, respeitando filtros, estrutura e evitando arquivos já carregados no projeto.

---

## 🚀 Como usar

### 1️⃣ Selecione a Pasta Raiz
Clique no botão `...` ao lado do campo de pasta e escolha onde estão seus arquivos.

A ferramenta pesquisa recursivamente dentro de **todas as subpastas**.

---

## 📂 Tipos de arquivos suportados
Você pode marcar os tipos que deseja incluir:

- Shapefile (`.shp`)
- GeoJSON / JSON
- KML e KMZ
- TIFF / GeoTIFF
- ECW
- JPEG2000 (`.jp2`)
- ASCII Grid (`.asc`)
- GPX
- CSV
- TAB (MapInfo)
- LAS / LAZ
- e outros formatos vetoriais compatíveis com o QGIS

---

## 🧠 Opções Inteligentes

### ✔ **Carregar apenas arquivos ainda NÃO carregados**
Evita duplicações automaticamente.  
Se um arquivo já está no projeto → ele será ignorado.

### ✔ **Preservar estrutura de pastas**
Cria no QGIS a mesma organização da sua pasta, com grupos e subgrupos.

### ✔ **Criar backup do projeto**
Antes de carregar, o plugin cria um backup automático na pasta `backup/`  
(ativo apenas se o projeto já estiver salvo).

---

## 📊 Resultado
Ao finalizar, o QGIS mostrará:

- Quantos arquivos foram carregados
- Caminho do backup (se ativado)

---

## ❤️ Dicas de Uso

- Ideal para quem recebe *pastas enormes de shapefiles* e precisa carregar tudo organizado.
- Perfeito para cargas iniciais de projetos SIG corporativos.
- Ótimo para comparar pastas ou atualizar lotes de arquivos sem duplicar facilmente.

---

## 🔧 Observação técnica
A ferramenta usa normalização completa de paths e leitura absoluta dos arquivos, garantindo que:
- caminhos relativos não causem duplicação,
- formatos compactados (KMZ, JP2 etc.) sejam tratados corretamente,
- raster e vetores tenham suas origens identificadas sem ambiguidades.

---

Se desejar expandir a ferramenta com filtros avançados, carregamento assíncrono ou integração com banco de dados PostGIS, entre em contato! 😄
