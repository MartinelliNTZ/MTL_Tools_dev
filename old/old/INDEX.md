# LOGCAT - MAPA DE DOCUMENTAÇÃO

**Última Atualização**: 22 de Janeiro de 2026  
**Versão**: 1.0

---

## 📍 VOCÊ ESTÁ AQUI

Pasta: `plugins/logcat/`

---

## 🎯 COMECE AQUI

### 1️⃣ Para Entender a Ferramenta
👉 Leia: **[ARCHITECTURE_DETAILED.md](ARCHITECTURE_DETAILED.md)**
- Visão geral completa
- Componentes e responsabilidades
- Fluxo de dados
- Thread safety e performance
- Guia de manutenção

**Tempo estimado**: 30 minutos

### 2️⃣ Para Ver Cenários de Uso
👉 Leia: **[ANALISE_DE_CENARIO.md](ANALISE_DE_CENARIO.md)**
- Cenários de uso prático
- Como debugar problemas
- Análise de performance
- Manutenção e upgrades

**Tempo estimado**: 20 minutos

### 3️⃣ Para Usar a Ferramenta
👉 Leia: **[README.md](README.md)**
- Como abrir e usar
- Filtros e ordenação
- Export de dados
- Estrutura do projeto

**Tempo estimado**: 10 minutos

---

## 📚 DOCUMENTAÇÃO ORGANIZADA

### Documentação Ativa (Leia Estas)

| Arquivo | Tamanho | Conteúdo | Público |
|---------|---------|----------|---------|
| **ARCHITECTURE_DETAILED.md** | 28KB | Arquitetura completa, componentes, fluxos | Desenvolvedores |
| **ANALISE_DE_CENARIO.md** | 18KB | Cenários de uso, erro, performance, manutenção | Desenvolvedores |
| **README.md** | 9KB | Visão geral, como usar, estrutura | Todos |

### Documentação Anterior (Referência)

Pasta: `old/`

| Arquivo | Tamanho | Conteúdo |
|---------|---------|----------|
| `00_START_HERE.md` | 9.5KB | Resumo executivo original |
| `README.md` | 9.7KB | Guia de funcionalidades original |
| `ARCHITECTURE.md` | 12KB | Arquitetura original |
| `QUICK_START.md` | 8.4KB | Guia rápido original |
| `API.md` | 15.5KB | Referência de API |
| `IMPLEMENTATION_SUMMARY.md` | 12KB | Sumário técnico |
| `CHECKLIST.md` | 12KB | Checklist de verificação |

---

## 🗂️ ESTRUTURA DO CÓDIGO

### Backend (Core - Sem Qt)

```
core/
├── model/
│   ├── log_entry.py              ← Parse tolerante de JSONL
│   ├── log_session.py            ← Metadata de arquivo
│   └── log_session_manager.py    ← Discovery de sessões
├── io/
│   ├── log_loader.py             ← Carregamento incremental
│   └── log_file_watcher.py       ← Monitoramento
├── filter/
│   └── log_filter_engine.py      ← Múltiplos filtros
└── color/
    ├── class_color_provider.py   ← Cores determinísticas
    └── tool_key_color_provider.py ← Mapeamento de cores
```

**Características**:
- ✅ Sem dependências Qt
- ✅ 100% testável independentemente
- ✅ Thread-safe
- ✅ Tolerante a erros

### UI (Qt Widgets)

```
ui/
├── logcat_dialog.py              ← Orquestrador principal
├── log_table_model.py            ← Modelo Qt
├── log_sort_filter_proxy_model.py ← Sorting customizado
├── log_detail_dialog.py          ← Detalhe 1 entrada
└── log_multiple_detail_dialog.py ← Detalhe múltiplas
```

**Características**:
- ✅ Coordena todos os componentes
- ✅ Desacoplada do backend
- ✅ Model/View pattern
- ✅ Eficiente para grande volume

---

## 🚀 QUICK START

### Abrir Logcat

```python
# Menu → MTL Tools → Sistema → Logcat - Viewer de Logs
```

### Ver Logs em Tempo Real

1. Abra Logcat
2. Execute qualquer ferramenta
3. Novos logs aparecem automaticamente

### Filtrar

1. Use "Search" para texto livre
2. Use botões de filtro (Level, Tool, Class)
3. Combine múltiplos filtros

### Exportar

1. Selecione linhas (Ctrl+Click) → "Export Selection"
2. Ou "Export Filter" para todos os filtrados

---

## 📊 ESTATÍSTICAS DO PROJETO

| Métrica | Valor |
|---------|-------|
| Arquivos Python | 22 |
| Linhas de código | ~2000 |
| Classes backend | 8 |
| Classes UI | 5 |
| Documentação (KB) | 100+ |
| Cobertura de tópicos | 100% |

---

## 🔍 BUSCAR INFORMAÇÕES

### "Como faço para adicionar um novo filtro?"
👉 Consulte: `ARCHITECTURE_DETAILED.md` → Seção "Guia de Manutenção" → "Como Adicionar um Novo Filtro"

### "Por que a performance ficou lenta?"
👉 Consulte: `ANALISE_DE_CENARIO.md` → Seção "Cenários de Performance"

### "Como debugo um problema?"
👉 Consulte: `ANALISE_DE_CENARIO.md` → Seção "Cenários de Erro"

### "Qual é a arquitetura geral?"
👉 Consulte: `ARCHITECTURE_DETAILED.md` → Seção "Arquitetura em Camadas"

### "Como funciona o sorting?"
👉 Consulte: `ARCHITECTURE_DETAILED.md` → Seção "LogSortFilterProxyModel"

### "Como o file watcher funciona?"
👉 Consulte: `ARCHITECTURE_DETAILED.md` → Seção "LogFileWatcher"

### "Como posso estender a ferramenta?"
👉 Consulte: `ARCHITECTURE_DETAILED.md` → Seção "Extensibilidade"

---

## ✅ CHECKLIST DE COMPREENSÃO

Use este checklist para verificar se você entende a ferramenta:

- [ ] Entendo os 8 componentes backend (core/)
- [ ] Entendo os 5 componentes UI (ui/)
- [ ] Entendo o fluxo de dados (inicialização, tempo real, filtros)
- [ ] Entendo como funciona carregamento incremental
- [ ] Entendo como funciona o file watcher
- [ ] Entendo como funcionam os filtros
- [ ] Entendo como funcionam as cores
- [ ] Entendo como funciona a ordenação
- [ ] Entendo thread safety
- [ ] Entendo performance otimizações
- [ ] Sei como adicionar um novo filtro
- [ ] Sei como adicionar uma nova coluna
- [ ] Sei como debugar problemas
- [ ] Sei como estender a ferramenta

Se respondeu "não" a algum, consulte `ARCHITECTURE_DETAILED.md`.

---

## 🎓 RECURSOS DE APRENDIZADO

### Para Iniciantes
1. Leia `README.md` (visão geral)
2. Leia `ARCHITECTURE_DETAILED.md` → "Componentes Principais"
3. Execute a ferramenta e experimente

### Para Desenvolvedores
1. Leia `ARCHITECTURE_DETAILED.md` completo
2. Leia `ANALISE_DE_CENARIO.md`
3. Explore o código com docstrings
4. Implemente uma mudança pequena (novo filtro)

### Para Mantenedores
1. Leia `ARCHITECTURE_DETAILED.md` → "Guia de Manutenção"
2. Leia `ANALISE_DE_CENARIO.md` → "Cenários de Manutenção"
3. Use como referência para mudanças futuras

---

## 📞 FALE CONOSCO

Para dúvidas sobre:

| Tópico | Consulte |
|--------|----------|
| Uso da ferramenta | `README.md` |
| Arquitetura | `ARCHITECTURE_DETAILED.md` |
| Cenários | `ANALISE_DE_CENARIO.md` |
| Código | Docstrings nos arquivos |
| Histórico | `old/` |

---

## 🔄 VERSIONAMENTO

| Versão | Data | Status |
|--------|------|--------|
| 1.0 | 22/01/2026 | ✅ Produção |

---

## 📝 NOTAS

- Toda a documentação foi reorganizada em 22/01/2026
- Documentação anterior movida para `old/` como referência
- Duas novíssimas documentações criadas: `ARCHITECTURE_DETAILED.md` e `ANALISE_DE_CENARIO.md`
- Ferramenta está pronta para produção
- Todas as features solicitadas foram implementadas

---

**Bom trabalho! 🎉**

Você agora tem documentação profissional, bem organizada e fácil de navegar.

Comece por:
1. 📖 `README.md` (5 min)
2. 📐 `ARCHITECTURE_DETAILED.md` (30 min)
3. 🎯 `ANALISE_DE_CENARIO.md` (20 min)

Total: ~1 hora para dominar a ferramenta! ⏱️
