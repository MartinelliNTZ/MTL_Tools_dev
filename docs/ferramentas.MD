# 🧰 MTL Tools

**MTL Tools** é um conjunto de ferramentas avançadas para o QGIS voltado à **automação de layouts**, **processamento de dados vetoriais e raster** e **otimização de fluxos cartográficos** 🗺️⚙️  
O plugin reúne soluções para **exportação em lote**, **edição massiva de layouts**, **análises estatísticas**, **amostragem de rasters**, **cálculos automatizados de atributos** e **ferramentas interativas de apoio**, reduzindo etapas manuais e aumentando a produtividade no QGIS.

---

## 🚀 Ferramentas Principais

### 📤 Exportar Todos os Layouts
    Ferramenta para **exportação automática de todos os layouts do projeto** para PDF e/ou PNG.  
    Ideal para produção cartográfica em lote com controle e padronização.

    **O que ela faz:**
    - Exporta todos os layouts do projeto automaticamente
    - Permite definir pasta de saída e evitar sobrescrita
    - Opção para unir todos os PDFs em um único arquivo
    - Conversão opcional de múltiplos PNGs em PDF final
    - Controle de largura máxima na exportação
    - Exibe progresso e trata erros por layout
    - Salva preferências do usuário

---

### 🔁 Replace Text in Layouts
    Ferramenta para **substituição de textos em massa** em todos os layouts do projeto QGIS.  
    Indicada para padronização rápida de títulos, legendas e informações repetidas.

    **O que ela faz:**
    - Busca e substituição de textos em todos os layouts
    - Opção de diferenciar maiúsculas/minúsculas
    - Modo **chave**, substituindo todo o conteúdo do item
    - Cria **backup automático do projeto (.qgz)**
    - Gera **arquivo de log** das alterações
    - Salva preferências do usuário

---

### 🔄 Salvar, Fechar e Reabrir Projeto
    Ferramenta que **reinicia o QGIS mantendo o projeto atual aberto**.  
    Ideal para aplicar mudanças globais sem risco de perda de dados.

    **O que ela faz:**
    - Verifica se o projeto está salvo
    - Salva todas as alterações automaticamente
    - Fecha o QGIS de forma controlada
    - Reabre o QGIS com o mesmo projeto carregado

---

### 📂 Carregar Pasta de Arquivos
    Ferramenta para **carregamento automático de camadas a partir de pastas e subpastas**.  
    Indicada para projetos com grandes volumes de dados organizados em diretórios.

    **O que ela faz:**
    - Seleção de pasta raiz no disco
    - Suporte a múltiplos formatos vetoriais e raster
    - Opção para carregar apenas arquivos novos
    - Preserva estrutura de pastas em grupos
    - Cria backup do projeto antes da operação
    - Salva preferências de uso

---

### 🚜 Gerar Rastro de Implemento
    Ferramenta para **geração da faixa de cobertura de implementos agrícolas** a partir de linhas.  
    Indicada para planejamento agrícola e análise operacional.

    **O que ela faz:**
    - Usa camada de linhas como entrada
    - Gera o rastro com base na largura informada
    - Saída como camada temporária ou arquivo
    - Opção de aplicar estilo QML
    - Armazena preferências do usuário

---

### ℹ️ Sobre o MTL Tools
    Janela informativa com **dados técnicos, autoria, versão e links oficiais** do plugin.  
    Utilizada como referência rápida e acesso a suporte.

---

### 📍 Consulta de Coordenadas e Altimetria
    Ferramenta que permite **obter coordenadas completas e altitude por clique no mapa**.  
    Ideal para conferência rápida e apoio a levantamentos de campo.

    **O que ela faz:**
    - Clique direto no mapa com suporte a snapping
    - Coordenadas em **WGS 84 (decimal e DMS)**
    - Coordenadas **UTM SIRGAS 2000** completas
    - Consulta automática de **altitude (SRTM 90 m)**
    - Execução em background
    - Cópia individual ou completa dos valores

---



## ⚙️ Ferramentas de Processamento

### 📊 Estatísticas de Atributos
    Ferramenta para **geração de estatísticas descritivas de campos numéricos**.  
    Indicada para análises exploratórias e relatórios técnicos.

    **O que ela faz:**
    - Analisa todos os campos numéricos
    - Permite excluir campos do cálculo
    - Calcula médias, desvios, percentis, variância e mais
    - Define precisão decimal
    - Gera arquivo **CSV**
    - Suporte a formato PT-BR
    - Carrega o CSV automaticamente no projeto
    - Salva preferências do usuário

---

### ➖ Gerador de Diferenças entre Campos
    Ferramenta para **criação automática de campos com diferenças numéricas**.  
    Indicada para análises comparativas e validação de dados.

    **O que ela faz:**
    - Utiliza camada de pontos
    - Define um campo base
    - Calcula diferenças para todos os campos numéricos
    - Cria novos campos com prefixo configurável
    - Controla precisão decimal
    - Gera nova camada de saída
    - Salva preferências do usuário

---

### 🌐 Amostragem Massiva de Rasters
    Ferramenta para **extração automática de valores de múltiplos rasters** em pontos.  
    Indicada para análises ambientais, agrícolas e geoespaciais.

    **O que ela faz:**
    - Usa camada de pontos como base
    - Permite selecionar múltiplos rasters
    - Extrai valores automaticamente
    - Cria novos campos por raster
    - Gera nova camada vetorial
    - Opção de reprojeção da saída
    - Armazena preferências de saída
