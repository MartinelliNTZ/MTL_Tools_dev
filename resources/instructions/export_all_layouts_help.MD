# 📘 Export All Layouts – Manual de Utilização  
Ferramenta do pacote **MTL Tools** para exportação automatizada de *layouts* do QGIS.

---

## 📌 O que esta ferramenta faz?

Esta ferramenta percorre **todos os layouts do projeto atual** do QGIS e permite exportá-los:

- Em **PDF**
- Em **PNG**
- Com opção de **unificar todos os PDFs** exportados em um arquivo final
- Com opção de **unificar PNGs em um único PDF**
- Respeitando ou não a substituição de arquivos já existentes

Ela também grava **preferências do usuário**, para manter as escolhas entre execuções.

---

## 🧩 Componentes principais

### ✔ Formatos de exportação  
Você pode ativar/desativar:

- **Exportar PDF**
- **Exportar PNG**

---

### ✔ Opções adicionais  
- **Unir PDFs exportados** → Gera um único PDF contendo todos os layouts.
- **Unir PNGs em um PDF** → Converte todos os PNGs exportados para um único documento.
- **Substituir arquivos existentes** → Caso desativado, arquivos repetidos ganham sufixos _001, _002…_

---

### ✔ Max Width para união de PNG  
Define a largura máxima dos PNGs ao gerar o PDF unificado.  
Útil para manter proporção/dimensionamento em grandes formatos.

---

### ✔ Seleção da pasta de saída

Você pode:

- Informar manualmente
- Selecionar via botão
- Usar automaticamente a pasta do projeto → `…/exports/`

Caso a pasta não exista, ela será criada.

---

## ▶ Como usar

### 1. Abra o diálogo  
Menu → *MTL Tools* → **Export All Layouts**

---

### 2. Escolha os formatos

Marque se deseja exportar:

- PDF  
- PNG  

Você pode escolher os dois.

---

### 3. Configure opções extras

Se desejar:

- Gerar um único PDF final (união dos PDFs)
- Unir todos PNGs em um PDF
- Forçar substituição dos arquivos existentes
- Ajustar o *Max Width* da união dos PNGs

---

### 4. Defina um diretório de saída  

Use:

- **Selecionar pasta**  
ou  
- **Usar pasta do projeto**

---

### 5. Clique em **Exportar**

A ferramenta:

1. Lista todos os layouts do projeto  
2. Exporta um por um  
3. Exibe um **diálogo de progresso**  
4. Registra erros individuais (se houver)  
5. Mostra um resumo final com link clicável para a pasta

---

## 🔄 Salvamento de preferências

Cada execução grava automaticamente as opções escolhidas.  
Na próxima abertura, tudo é carregado do arquivo `.prefs` da ferramenta.

## 📦 Bibliotecas necessárias

Algumas funcionalidades desta ferramenta dependem de bibliotecas Python externas:

- **PyPDF2** → necessária para **unir PDFs**  
- **Pillow (PIL)** → necessária para **unir PNGs em um PDF**

Se essas bibliotecas não estiverem instaladas, a ferramenta exibirá um aviso e permitirá abrir um instalador automático:

- `install_pypdf2.bat`
- `install_pillow.cmd`

⚠ **Importante:** após instalar qualquer uma dessas bibliotecas, é **obrigatório reiniciar o QGIS** para que elas sejam reconhecidas pelo Python interno do QGIS.

---

## 🔑 Chave de preferências da ferramenta

A ferramenta utiliza a seguinte chave interna para salvar e carregar configurações:

`export_all_layouts`

