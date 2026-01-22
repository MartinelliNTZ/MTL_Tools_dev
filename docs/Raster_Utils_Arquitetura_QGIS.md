# 🛰️ Raster Utils – Arquitetura para Plugins QGIS

Este documento define a arquitetura proposta para manipulação de **rasters** em um plugin QGIS de grande porte.
O foco é **separação clara de responsabilidades**, reutilização e manutenção a longo prazo.

---

## 1️⃣ RasterLayerIO

### Escopo e Responsabilidade
Gerencia **entrada, saída, criação e validação** de rasters.
Não executa cálculos nem transformações espaciais complexas.

### Métodos Conceituais
- carregar raster de arquivo
- salvar raster em formato definido
- criar raster vazio
- clonar raster existente
- validar raster e provider
- verificar existência de bandas
- definir valor NoData
- ler valor NoData
- criar raster temporário
- remover raster temporário
- obter caminho da fonte
- verificar integridade do arquivo

---

## 2️⃣ RasterLayerCrs

### Escopo e Responsabilidade
Centraliza tudo relacionado a **CRS, resolução, extent e alinhamento espacial**.
Evita erros silenciosos de reprojeção.

### Métodos Conceituais
- obter CRS do raster
- verificar se raster está projetado
- reprojetar raster para CRS alvo
- alinhar raster a outro raster
- ajustar resolução espacial
- ajustar extent
- converter unidades lineares
- detectar tamanho do pixel
- validar compatibilidade de CRS
- forçar CRS em raster sem definição
- obter CRS do projeto
- verificar distorção de reprojeção

---

## 3️⃣ RasterLayerProcessing

### Escopo e Responsabilidade
Executa **processamentos raster destrutivos**, pixel a pixel ou banda a banda.
É o motor principal de transformação.

### Métodos Conceituais
- reclassificar valores raster
- aplicar máscara raster
- calcular raster por expressão
- normalizar valores
- combinar múltiplos rasters
- gerar raster binário
- aplicar threshold
- converter tipo de dado
- extrair banda específica
- suavizar ruído
- aplicar filtro espacial
- preencher valores NoData

---

## 4️⃣ RasterLayerMetrics

### Escopo e Responsabilidade
Executa **análises e métricas**, sem modificar o raster.
Usado para relatórios, validações e exportações.

### Métodos Conceituais
- calcular estatísticas por banda
- gerar histograma
- obter valor mínimo
- obter valor máximo
- calcular média
- calcular desvio padrão
- contar pixels válidos
- calcular área por classe
- detectar valor NoData real
- estatística por máscara
- gerar resumo estatístico
- validar qualidade dos dados

---

## 5️⃣ RasterVectorInterop

### Escopo e Responsabilidade
Responsável pela **integração raster ↔ vetor**.
Viabiliza fluxos reais de análise espacial.

### Métodos Conceituais
- recortar raster por camada vetorial
- rasterizar camada vetorial
- extrair valores raster para pontos
- gerar estatísticas zonais
- converter raster para vetor
- alinhar raster a geometria vetorial
- criar máscara raster a partir de vetor
- amostrar raster em linhas
- extrair contorno de classes
- calcular raster sob buffer
- validar compatibilidade raster-vetor
- gerar raster de apoio para vetores

---

## 📌 Princípios Gerais

- Nenhuma classe conhece UI
- Nenhuma classe controla fluxo de ferramenta
- Todas são reutilizáveis
- Todas podem ser orquestradas pelo PluginService
- Cada classe tem um único motivo para mudar

---

## ✅ Conclusão

Este conjunto fornece **potência, clareza e escalabilidade** para plugins QGIS avançados,
sem cair em superclasses ou acoplamento excessivo.
