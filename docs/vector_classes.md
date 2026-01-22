# 📐 Vector Utils – Arquitetura de Camadas Vetoriais (QGIS Plugin)

Este documento define o **conjunto mínimo e escalável de utils** para manipulação de camadas vetoriais
em um plugin QGIS de grande porte, orientado a múltiplas ferramentas.

O design é **funcional**, evita herança excessiva e privilegia **pipelines de processamento**.

---

## 1️⃣ VectorLayerIO

### Escopo e Responsabilidade
Responsável por **entrada, saída e estado** de camadas vetoriais.  
Não executa transformações geométricas nem cálculos espaciais.

Tudo que envolve **carregar, salvar, clonar ou validar** uma camada passa por aqui.

### Métodos Conceituais
- carregar camada a partir de arquivo
- salvar camada em formato definido
- validar se a camada é vetorial e utilizável
- verificar se a camada possui feições
- clonar camada em memória
- criar camada vazia baseada em outra
- garantir que a camada esteja carregada corretamente
- verificar provider e tipo de fonte
- resolver caminhos de saída
- remover camada temporária

---

## 2️⃣ VectorLayerCrs

### Escopo e Responsabilidade
Centraliza **CRS, reprojeção e unidades**.  
Evita que regras de CRS fiquem espalhadas pelo código.

Não realiza análises, apenas **transforma sistemas de referência**.

### Métodos Conceituais
- obter CRS da camada
- verificar se a camada está projetada
- reprojetar camada para CRS alvo
- reprojetar geometria individual
- detectar unidade linear da camada
- converter distâncias entre unidades
- alinhar CRS de múltiplas camadas
- validar compatibilidade de CRS
- obter CRS do projeto
- forçar CRS em camada sem definição

---

## 3️⃣ VectorLayerGeometry

### Escopo e Responsabilidade
Executa **transformações geométricas** que **alteram a geometria** da camada.

Aqui acontecem buffers, merges, dissolves e outras operações espaciais.

### Métodos Conceituais
- aplicar buffer fixo
- aplicar buffer baseado em atributo
- dissolver feições por campo
- unir múltiplas camadas
- explodir geometrias múltiplas
- simplificar geometria
- gerar geometria de contorno
- criar centroides
- corrigir geometrias inválidas
- recortar camada por máscara

---

## 4️⃣ VectorLayerMetrics

### Escopo e Responsabilidade
Responsável por **medidas e métricas geométricas**, sem modificar dados.

Tudo aqui é **leitura e cálculo**, nunca transformação.

### Métodos Conceituais
- calcular área de feição
- calcular comprimento de feição
- calcular área total da camada
- calcular comprimento total
- obter centroide
- calcular bounding box
- estatísticas básicas de campo numérico
- somar valores por atributo
- calcular densidade espacial
- gerar resumo geométrico da camada

---

## 5️⃣ VectorLayerAttributes

### Escopo e Responsabilidade
Gerencia **campos, valores e expressões** de atributos.

É a ponte entre **dados espaciais** e **dados tabulares**, muito usada pela UI.

### Métodos Conceituais
- listar todos os campos da camada
- listar campos numéricos
- listar campos textuais
- obter valores de um campo
- adicionar novo campo
- remover campo
- calcular campo por expressão
- renomear campo
- copiar atributos entre camadas
- validar existência de campo

---

## 🧭 Princípios de Uso

- Nenhuma dessas classes conhece UI ou widgets
- Nenhuma decide fluxo de ferramenta
- Todas podem ser chamadas pelo `PluginService`
- Todas são reutilizáveis por múltiplas ferramentas
- Cada classe tem **um único motivo para mudar**

---

## 📌 Observação Final

Este conjunto de 5 utils representa o **núcleo vetorial mínimo** para um plugin QGIS grande.
Novas capacidades devem **estender métodos**, não criar novas hierarquias de classes.

> Preferir sempre crescimento horizontal (novos métodos) a crescimento vertical (novas classes).

