# 📘 Análise de Cenário – Ferramenta Copiar Atributos

## Visão Geral
A ferramenta **Copiar Atributos** foi desenvolvida para transferir campos entre camadas vetoriais de forma segura, previsível e integrada ao fluxo do **MTL Tools**, atuando diretamente sobre a camada destino e mantendo controle explícito sobre edição e salvamento.

---

## Objetivo da Ferramenta
Resolver cenários em que:

- É necessário replicar atributos entre camadas semelhantes
- Camadas possuem estruturas parcialmente compatíveis
- O usuário precisa decidir manualmente quais campos copiar
- Conflitos de nomes de campos precisam ser tratados de forma interativa

A ferramenta evita duplicações de camadas e operações irreversíveis.

---

## Cenários de Uso

### 1️⃣ Execução com seleção manual de atributos

**Situação**
- O usuário desmarca a opção “Usar todos os atributos”
- Seleciona manualmente os campos desejados

**Comportamento**
- Apenas os campos marcados são copiados
- A ordem e o tipo dos campos são preservados

**Resultado**
- Controle total sobre os dados transferidos
- Evita poluição de atributos desnecessários

---

### 2️⃣ Execução usando todos os atributos

**Situação**
- A opção “Usar todos os atributos” está marcada

**Comportamento**
- Todos os campos da camada origem são copiados
- A lista de atributos é ignorada

**Resultado**
- Execução mais rápida
- Ideal para camadas com estruturas compatíveis

---

### 3️⃣ Conflito de nomes de campos

**Situação**
- Um campo da origem já existe na camada destino

**Comportamento**
- A ferramenta solicita ao usuário uma decisão
- A resolução é feita campo a campo

**Resultado**
- Evita sobrescritas acidentais
- Garante previsibilidade da estrutura final

---

### 4️⃣ Camada destino já em modo de edição

**Situação**
- A camada destino já estava em edição

**Comportamento**
- A ferramenta respeita o estado atual
- Nenhuma tentativa automática de salvamento é feita

**Resultado**
- Integração segura com fluxos manuais de edição

---

### 5️⃣ Camada destino fora do modo de edição

**Situação**
- A camada destino não estava em edição

**Comportamento**
- A ferramenta inicia a edição
- O usuário decide salvar ou descartar ao final

**Resultado**
- Proteção contra alterações não intencionais

---

## Comportamento da Interface (UI)

### Seleção de camadas
- Camada ativa é automaticamente sugerida como destino
- Drag & drop permite troca rápida de camadas
- Clique no campo atualiza dinamicamente a lista

---

### Seleção de atributos
- Lista suporta seleção múltipla (Ctrl / Shift)
- Botões de seleção seguem padrão do QGIS:
  - Ação aplicada apenas aos itens selecionados
  - Caso nenhum esteja selecionado, aplica a todos

Essa abordagem melhora significativamente a usabilidade em listas extensas.

---

## Impactos nos Dados

### O que é preservado
- Geometrias
- Sistema de referência espacial
- Campos existentes da camada destino
- Estado de edição da camada

### O que é alterado
- Estrutura de campos da camada destino
- Conteúdo dos atributos copiados

---

## Riscos e Controles

| Risco Potencial | Mitigação |
|----------------|-----------|
| Sobrescrita de campos | Confirmação interativa |
| Alteração indesejada | Alterações não salvas automaticamente |
| Erro de seleção | UI com feedback visual |
| Listas grandes | Controles de seleção em lote |

---

## Diferença em Relação a Abordagens Simples

Diferente de scripts diretos ou cópias automáticas, esta ferramenta:

- Permite seleção manual e visual de campos
- Trata conflitos de forma controlada
- Integra drag & drop de camadas
- Mantém compatibilidade com QGIS 3.16+

---

## Possíveis Evoluções Futuras

- Exibição de prévia dos dados copiados
- Execução em background para grandes volumes
- Relatório detalhado de campos copiados
- Persistência de seleção de atributos por camada

---

## Conclusão

A ferramenta **Copiar Atributos** oferece um fluxo robusto, seguro e alinhado às práticas profissionais do QGIS, equilibrando automação e controle manual.  
Sua arquitetura e UI foram projetadas para reutilização em futuras ferramentas do **MTL Tools**, especialmente aquelas que envolvem seleção de camadas e campos.
