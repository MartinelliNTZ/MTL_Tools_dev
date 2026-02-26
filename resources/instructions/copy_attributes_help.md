# 📘 Copiar Atributos — Guia Rápido e Intuitivo

Breve: copia campos (atributos) de uma camada origem para uma camada destino com escolha de campos e controle de conflitos. 🧾

---

## ▶ Passo a passo (rápido) ✅

1. Abra: Menu → **MTL Tools** → **Copiar Atributos**
2. Selecione a **camada destino** (onde os campos serão inseridos). 🎯
3. Selecione a **camada origem** (de onde os campos serão copiados). 🗂️
4. Escolha os campos:
   - Marque **Usar todos os atributos** para copiar tudo, ou
   - Selecione manualmente os campos desejados da lista. ✅
5. Clique em **Executar** ▶️. Em caso de conflito, confirme a ação quando solicitado.

---

## ℹ️ O que acontece por trás (resumido)

- Os campos escolhidos são copiados para a camada destino; os valores são mapeados por feição.
- A operação age diretamente na camada destino (alterações ficam abertas para salvar/descartar). 🔁
- A ferramenta não cria camadas temporárias por padrão; preserve um backup se necessário. 💾

---

## 💡 Dicas rápidas

- Verifique compatibilidade de tipos entre campos (ex.: número → número, texto → texto). 🔍
- Selecione apenas os campos necessários para evitar sobrecarga da camada destino. ✂️
- Faça backup da camada destino antes de operações em massa, especialmente em ambientes de produção. 🧰

---

## ⚠️ Problemas comuns e solução

- Conflito de nomes: ferramenta pedirá confirmação; escolha sobrescrever, renomear ou pular. ⚠️
- Tipos incompatíveis: valores podem ficar vazios ou truncados — prefira campos compatíveis. 🔄
- Não é possível editar a camada destino: verifique se a camada está desbloqueada e se você tem permissão de escrita. 🔐

---

## ✅ Checklist rápido pós-execução

- Campos esperados presentes na `camada destino`? ✔️
- Valores copiados corretamente (ex.: amostra visual)? ✔️
- Salvou as alterações (se desejado)? ✔️

---

## 🔧 Preferências e suporte

- A ferramenta usa a chave interna `copy_attributes` para logs e rastreamento.
- Em caso de erro, verifique o painel de logs do plugin e reporte com: tipo da camada, número de feições e campos selecionados. 🐞

