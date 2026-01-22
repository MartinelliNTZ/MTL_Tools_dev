# 📘 Gerar Rastro Implemento – Manual de Utilização  

Ferramenta do pacote **MTL Tools** para geração automática do **rastro (largura efetiva)** de implementos agrícolas a partir de camadas lineares.

---

## 📌 O que esta ferramenta faz?

Esta ferramenta recebe uma **camada de linhas** (ex.: trajetórias, linhas de plantio, passadas de máquina) e gera:

- Um **polígono representando o rastro do implemento**
- Com largura definida pelo usuário
- Salvando o resultado como:
  - **Camada temporária**, ou
  - **Arquivo em disco**
- Opcionalmente aplicando um **estilo QML**

As configurações do usuário são **salvas automaticamente** e reaproveitadas nas próximas execuções.

---

## 🧩 Componentes da ferramenta

### ✔ Camada de Linhas (INPUT)
Selecione a **camada vetorial de linhas** que representa o deslocamento do implemento.

> Apenas camadas vetoriais compatíveis são listadas.

---

### ✔ Tamanho do implemento
Define a **largura total do implemento**, utilizada para gerar o rastro.

- Unidade: mesma unidade do SRC da camada
- Valor padrão: `16.0`

---

### ✔ Salvar em arquivo
Quando marcado:

- O resultado será salvo em um **arquivo físico**
- Caso desmarcado:
  - O resultado será criado como **camada temporária**

---

### ✔ Caminho do arquivo de saída
Disponível apenas quando **Salvar em arquivo** estiver marcado.

Permite escolher o formato final, como:

- Shapefile (`.shp`)
- GeoPackage (`.gpkg`)
- GeoJSON (`.geojson`)
- KML (`.kml`)
- CSV (`.csv`)

O formato final é definido automaticamente pela extensão escolhida.

---

### ✔ Aplicar estilo (QML)
Se marcado:

- Um **arquivo QML** será aplicado automaticamente ao resultado
- Caso nenhum QML seja informado:
  - O plugin utilizará o estilo padrão:
    ```
    styles/Rastro_Implemento.qml
    ```

---

### ✔ Arquivo QML (opcional)
Permite selecionar um **arquivo de estilo personalizado (.qml)** para o resultado.

Se vazio, o estilo padrão do plugin será utilizado (caso a opção esteja marcada).

---

## ▶ Como usar

### 1️⃣ Abrir a ferramenta
Menu → **MTL Tools** → **Gerar Rastro Implemento**

---

### 2️⃣ Selecionar a camada de entrada
Escolha a camada de **linhas** que representa o trajeto do implemento.

---

### 3️⃣ Definir o tamanho do implemento
Informe a largura total do implemento (ex.: 12, 16, 24 metros).

---

### 4️⃣ Escolher saída
- Camada temporária  
ou  
- Arquivo em disco (marcando *Salvar em arquivo*)

---

### 5️⃣ (Opcional) Aplicar estilo
- Marque **Aplicar estilo (QML)**
- Informe um arquivo QML personalizado ou utilize o padrão do plugin

---

### 6️⃣ Executar
Clique em **Executar**.

O resultado será:

- Adicionado automaticamente ao projeto
- Registrado no **Histórico de Processamento**
- Estilizado (se configurado)

---

## 💾 Salvamento de preferências

A ferramenta armazena automaticamente:

- Última camada utilizada
- Último tamanho de implemento
- Opção de salvar em arquivo
- Caminho do último arquivo
- Opção de aplicar estilo
- Caminho do último QML

Essas informações são carregadas automaticamente na próxima abertura.

---

## 🔑 Chave de preferências

A ferramenta utiliza a seguinte chave interna:

