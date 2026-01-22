# Análise de Cenário – Ferramenta Coordenadas por Clique

## Visão Geral

A ferramenta **Coordenadas por Clique** foi desenvolvida para permitir a obtenção imediata de informações geoespaciais completas a partir de um clique do usuário no mapa do QGIS.

Ela integra:
- cálculo de coordenadas em diferentes sistemas,
- conversão entre formatos,
- consulta de altimetria,
- geocodificação reversa para identificação administrativa do local.

A ferramenta atua de forma **não destrutiva**, sem alterar camadas ou dados do projeto, e está totalmente integrada ao fluxo do plugin **MTL Tools**, utilizando tarefas assíncronas para garantir desempenho e fluidez da interface.

---

## Objetivo da Ferramenta

A ferramenta resolve situações comuns em que:
- é necessário identificar coordenadas precisas de um ponto no mapa,
- converter coordenadas entre WGS84 e UTM SIRGAS 2000,
- obter latitude e longitude em formatos decimal e DMS,
- consultar altitude aproximada do terreno,
- identificar município, estado, região e país de um ponto específico.

O foco é fornecer **informação espacial confiável, rápida e centralizada**, sem a necessidade de múltiplas ferramentas externas ou consultas manuais.

---

## Cenários de Uso

### 1️⃣ Clique simples no mapa

**Situação**
- O usuário ativa a ferramenta e realiza um clique no mapa.

**Comportamento**
- O ponto clicado é identificado, respeitando o sistema de snapping ativo.
- As coordenadas são calculadas imediatamente.
- Um diálogo é exibido com as informações básicas do ponto.

**Resultado**
- O usuário visualiza instantaneamente as coordenadas WGS84 e UTM do local selecionado.

---

### 2️⃣ Cliques sucessivos no mapa

**Situação**
- O usuário realiza vários cliques consecutivos no mapa.

**Comportamento**
- O diálogo permanece aberto.
- As informações são atualizadas dinamicamente a cada novo clique.
- Tarefas assíncronas anteriores são canceladas automaticamente.

**Resultado**
- Evita concorrência de tarefas.
- Garante que apenas os dados do último ponto sejam exibidos.

---

### 3️⃣ Consulta de geocodificação reversa

**Situação**
- O ponto selecionado possui cobertura de dados administrativos.

**Comportamento**
- Uma tarefa assíncrona consulta a API de geocodificação reversa.
- Os dados são processados sem bloquear a interface.
- O resultado é exibido no diálogo.

**Resultado**
- Exibição de município, região intermediária, estado, região e país.
- Caso a API não retorne dados, o usuário é informado.

---

### 4️⃣ Consulta de altimetria

**Situação**
- O ponto selecionado possui cobertura de dados altimétricos.

**Comportamento**
- Uma tarefa assíncrona consulta a API de altimetria (SRTM 90m).
- A altitude aproximada é exibida ao término da consulta.

**Resultado**
- O usuário obtém a elevação do terreno de forma automática.
- Em caso de falha, o campo é marcado como indisponível.

---

### 5️⃣ Cancelamento automático de tarefas

**Situação**
- O usuário clica em um novo ponto antes do término das consultas anteriores.

**Comportamento**
- As tarefas em execução são canceladas com segurança.
- Nenhuma tentativa de atualização de UI ocorre após o cancelamento.

**Resultado**
- Evita erros, vazamento de recursos e dados inconsistentes na interface.

---

## Tipos de Dados Considerados

A ferramenta trabalha corretamente com:
- coordenadas em qualquer CRS do projeto,
- transformação automática para WGS84 (EPSG:4326),
- conversão para UTM SIRGAS 2000 conforme a zona do ponto,
- cálculo de coordenadas em hemisfério norte e sul.

Pontos fora do limite UTM padrão são tratados de forma segura.

---

## Impactos nos Dados

### O que é preservado
- Camadas do projeto
- Dados vetoriais e raster
- Sistema de referência das camadas
- Estado do projeto QGIS

### O que é alterado
- Nenhum dado do projeto é modificado
- Apenas informações temporárias são exibidas ao usuário

---

## Riscos e Controles

| Risco Potencial | Mitigação |
|-----------------|-----------|
| Bloqueio da interface | Uso de QgsTask assíncrono |
| Concorrência de tarefas | Cancelamento automático de tasks |
| Dados incompletos de API | Tratamento de erro e mensagens ao usuário |
| Uso excessivo de requisições | Execução apenas sob ação do usuário |

---

## Diferença em Relação a Abordagens Simples

Diferente de ferramentas básicas de identificação, esta ferramenta:
- centraliza múltiplos cálculos em um único clique,
- utiliza tarefas assíncronas para operações externas,
- separa claramente Model, View e Controller,
- evita qualquer modificação nos dados do projeto,
- oferece funções de cópia direta para diferentes formatos de coordenadas.

---

## Possíveis Evoluções Futuras

- Cache local de consultas de geocodificação
- Suporte a múltiplos provedores de altimetria
- Exportação automática das informações para arquivo
- Histórico de pontos clicados
- Integração com outras ferramentas do MTL Tools

---

## Conclusão

A ferramenta **Coordenadas por Clique** oferece uma solução robusta, segura e altamente produtiva para obtenção de informações espaciais detalhadas no QGIS.

Seu uso de tarefas assíncronas, separação clara de responsabilidades e integração com o ecossistema **MTL Tools** a torna adequada para ambientes profissionais, evitando riscos aos dados e garantindo excelente experiência ao usuário.
