# 🧩 Replace Text in Layouts — Guia Completo de Uso

Bem-vindo à ferramenta **Replace Text in Layouts** do pacote **MTL Tools**!  
Ela foi desenvolvida para automatizar substituições em massa dentro dos *Layouts* do QGIS, permitindo atualizar dezenas ou centenas de rótulos em questão de segundos e com total segurança.

---

## 🎯 Objetivo da Ferramenta

Esta ferramenta localiza ocorrências de texto dentro de **QgsLayoutItemLabel** (rótulos/textos nos layouts) e substitui automaticamente por outro texto definido pelo usuário.

Use quando precisar:

- Atualizar anos em documentos (ex.: “2023” → “2025”)
- Corrigir nomes de órgãos, clientes, setores ou responsáveis
- Padronizar grafias (“Km” → “KM”)
- Remover textos obsoletos
- Atualizar versões de mapas e plantas
- Fazer substituições repetitivas sem risco de esquecer algum item

---

## 🛠️ Como usar

### 1️⃣ Acessando a Ferramenta
No menu do QGIS:

**MTL Tools → Replace Text in Layouts**

A janela principal será exibida com os campos necessários.

---

### 2️⃣ Preenchendo os Campos

- **Texto a buscar**  
  O texto presente nos layouts que você deseja localizar.  
  Exemplo: `SEINFRA 2023`

- **Texto a substituir (novo)**  
  O texto que entrará no lugar do antigo.  
  Exemplo: `SEINFRA 2024`

- **Case Sensitive**  
  - **Marcado:** diferencia letras maiúsculas/minúsculas  
  - **Desmarcado:** ignora diferença (recomenda-se para a maioria dos casos)

- **Modo Chave (opcional)**  
  Quando ativado, substitui **todo o conteúdo do rótulo** se o texto buscado for encontrado, em vez de substituir apenas a parte correspondente.  
  Útil para rótulos com textos completos variáveis.

---

## 🗄️ Backup Automático

Sempre que o projeto estiver salvo, antes de qualquer modificação o plugin criará um **backup completo do .qgz**:

📁 `nome_do_projeto/backup/nomedoprojeto_YYYYMMDDHHMMSS.qgz`

Isso garante que você pode reverter qualquer modificação, mesmo que múltiplos layouts sejam alterados.

Se o projeto **não estiver salvo**, você será avisado e poderá continuar se desejar — porém sem backup automático.

---

## 📓 Arquivo de Log

Toda execução gera um arquivo de log na mesma pasta de backup:

📄 `backup/replace_log_YYYYMMDDHHMMSS.txt`

O log registra:

- Número total de substituições aplicadas  
- Lista dos layouts alterados  
- Conteúdo antigo e novo de cada rótulo modificado  
- Nome do arquivo de backup criado  
- Data e hora completas da operação  
- Confirmação de término bem-sucedido

Esse registro é essencial para auditoria e rastreabilidade.

---

## 🚀 Boas práticas de uso

Para garantir substituições seguras e previsíveis:

- Salve o projeto antes de usar a ferramenta  
- Use buscas específicas para evitar substituições indesejadas  
- Evite termos muito genéricos (ex.: “KM”)  
- Prefira expressões completas (“KM 123+500”)  
- Revise o log após a execução para confirmar todas as alterações  
- Utilize o modo chave apenas quando realmente necessário

---

## ❤️ Criado por

**Matheus A.S. Martinelli**  
Ferramentas práticas para acelerar fluxos reais de cartografia e geoprocessamento no QGIS.
