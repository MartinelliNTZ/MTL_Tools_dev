# 📘 Copiar Atributos – Manual de Utilização

Ferramenta do pacote **MTL Tools** para copiar atributos (campos) de uma camada vetorial de **origem** para uma camada vetorial de **destino**, com controle fino sobre seleção de campos e resolução de conflitos.

---

## 📌 O que esta ferramenta faz?

A ferramenta **Copiar Atributos** permite:

- Copiar atributos entre duas camadas vetoriais
- Escolher manualmente quais campos serão copiados
- Usar todos os atributos automaticamente, se desejado
- Resolver conflitos de nomes de campos durante a cópia
- Trabalhar diretamente sobre a camada destino
- Manter controle total sobre salvar ou descartar alterações

---

## 🧩 Componentes da Interface

### ✔ Camada destino
Camada vetorial que **receberá os atributos**.

- Por padrão, a camada vetorial ativa é selecionada automaticamente
- É possível:
  - Escolher manualmente
  - Arrastar uma camada do painel de camadas e soltar no campo
  - Atualizar a lista clicando no campo

---

### ✔ Camada origem
Camada vetorial de onde os atributos serão copiados.

- A lista é atualizada automaticamente
- Pode receber camadas via **drag & drop**
- Ao alterar a camada de origem, a lista de atributos é atualizada

---

### ✔ Usar todos os atributos
Quando marcado:

- Todos os campos da camada de origem serão copiados
- A lista de atributos fica desativada
- Nenhuma seleção manual é necessária

---

### ✔ Lista de atributos
Exibe todos os campos da camada de origem.

- Cada campo possui um checkbox
- Por padrão, todos vêm marcados
- É possível:
  - Marcar/desmarcar individualmente
  - Usar seleção múltipla com **Ctrl** ou **Shift**
  - Aplicar ações em lote usando os botões auxiliares

---

### ✔ Botões de atributos

#### ✔ Selecionar
- Marca os atributos selecionados na lista
- Se nenhum item estiver selecionado, marca **todos**

#### ✖ Desselecionar
- Desmarca os atributos selecionados na lista
- Se nenhum item estiver selecionado, desmarca **todos**

Esse comportamento é similar ao padrão do QGIS para seleção de feições e atributos.

---

## ▶ Como usar

### 1️⃣ Abrir a ferramenta
Menu → **MTL Tools** → *Copiar Atributos*

---

### 2️⃣ Definir camadas
- Escolha a **camada destino**
- Escolha a **camada origem**
- Opcionalmente, arraste camadas diretamente para os campos

---

### 3️⃣ Definir atributos
- Marque **Usar todos os atributos**  
  **OU**
- Selecione manualmente os campos desejados

---

### 4️⃣ Executar
Clique em **Executar**.

- Em caso de conflito de nomes de campos, a ferramenta solicitará confirmação
- As alterações **não são salvas automaticamente**

---

## 💾 Salvamento das alterações
Após a execução:

- As alterações permanecem abertas na camada destino
- O usuário decide se deseja:
  - Salvar as alterações
  - Descartar as alterações

---

## ℹ️ Observações importantes

- Apenas **camadas vetoriais** são listadas
- A ferramenta não cria camadas temporárias
- A cópia respeita a estrutura original da camada destino
- Nenhuma alteração é aplicada sem confirmação do usuário

---

## 🔑 Chave interna da ferramenta
Esta ferramenta utiliza a chave interna:

"copy_attributes"

para controle de logs e identificação no sistema.
