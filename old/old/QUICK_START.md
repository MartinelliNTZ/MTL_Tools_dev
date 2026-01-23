"""
LOGCAT TOOL - QUICK START GUIDE

Guia rápido para acessar e usar a ferramenta Logcat.
"""

# ============================================================
# ACESSO RÁPIDO
# ============================================================

1. ABRIR O LOGCAT

   Menu: MTL Tools > Sistema > Logcat - Viewer de Logs
   
   Atalho: (Adicionar à toolbar para acesso rápido)

2. O QUE VER

   - Tabela com entries de log
   - Seletor de sessão (histórico)
   - Filtros em tempo real
   - Status bar com contagem

# ============================================================
# INTERFACE RÁPIDA
# ============================================================

┌─────────────────────────────────────────────────────────┐
│ Session: [Dropdown] [Refresh Sessions]                  │
├─────────────────────────────────────────────────────────┤
│ Search: [________]  Level: All  Tool: All  Class: All   │
│                     [Clear Filters]                      │
├─────────────────────────────────────────────────────────┤
│ Timestamp  │ Level │ Tool │ Class │ Message             │
├─────────────────────────────────────────────────────────┤
│ 11:28:52   │ INFO  │ syst │ LogU  │ Log session started │
│ 11:28:52   │ INFO  │ main │ MTL_  │ Plugin inicializado │
│ 11:29:01   │ WARN  │ vect │ Copy  │ Attribute mismatch  │
├─────────────────────────────────────────────────────────┤
│ Mostrando 3/50 entradas | Sessão: 2026-01-22 11:28:52   │
│                                                          │
│ [Clear Session] [Clear All Logs] [Close]                │
└─────────────────────────────────────────────────────────┘

# ============================================================
# OPERAÇÕES COMUNS
# ============================================================

## Buscar uma mensagem
1. Type in "Search" field
2. Filtro aplicado em tempo real
3. Tab atualiza automaticamente

## Ver detalhes completos
1. Duplo-clique em uma linha
2. Diálogo abre com tudo
3. Click "Copy All" para copiar

## Filtrar por nível
1. Click botão "Level"
2. Selecione níveis (DEBUG, INFO, WARNING, ERROR, CRITICAL)
3. Click OK
4. Tabela filtrada automaticamente

## Filtrar por ferramenta
1. Click botão "Tool"
2. Selecione ferramentas (system, vector_field, etc)
3. Click OK
4. Tabela filtrada automaticamente

## Filtrar por classe
1. Click botão "Class"
2. Selecione classes específicas
3. Click OK
4. Tabela filtrada automaticamente

## Limpar filtros
1. Click "Clear Filters"
2. Todos os filtros removidos
3. Tabela volta ao completo

## Limpar logs
1. Click "Clear Session" (apenas sessão atual)
   ou "Clear All Logs" (TODOS os logs)
2. Confirmação pedida
3. Logs deletados
4. UI recarregada

## Trocar de sessão
1. Dropdown "Session" mostra histórico
2. Click para selecionar outra sessão
3. Tabela recarrega com os logs daquela sessão

## Recarregar sessões
1. Click "Refresh Sessions"
2. Se novos logs foram criados, aparecerão

# ============================================================
# DICAS E TRUQUES
# ============================================================

1. **Busca Rápida**
   - Simplesmente type no campo Search
   - Funciona em todos os campos
   - Suporta regex se necessário

2. **Cores Significativas**
   - Vermelho = ERROR ou CRITICAL
   - Laranja = WARNING
   - Verde = INFO
   - Cinza = DEBUG

3. **Cópia de Informações**
   - Duplo-click > Copy All
   - Copia tudo: timestamp, stack trace, dados

4. **Histórico de Sessões**
   - Cada execução do QGIS cria um log
   - Histórico mantido em raiz/log
   - Acesso rápido via dropdown

5. **Performance**
   - Mesmo com muitos logs, UI é responsiva
   - Filtros aceleramento rapidamente
   - Scroll suave

6. **Limpeza**
   - Use "Clear Session" para atual
   - Use "Clear All Logs" para tudo
   - Confirmação sempre pedida
   - Irreversível!

# ============================================================
# CAMPOS DA TABELA
# ============================================================

Timestamp
  - Data/hora do evento (ISO format)
  - Clicável para ordem

Level
  - DEBUG (cinza)
  - INFO (verde)
  - WARNING (laranja)
  - ERROR (vermelho)
  - CRITICAL (vermelho escuro)

Tool
  - "system" (vermelho)
  - "vector_field" (roxo)
  - "coord_click" (rosa)
  - etc

Class
  - Classe que gerou o log
  - Cor automaticamente determinada
  - Mesma classe = mesma cor sempre

Message
  - Mensagem truncada (primeira 100 chars)
  - "..." se maior
  - Full message via duplo-click

# ============================================================
# TROUBLESHOOTING
# ============================================================

### Logcat não abre?
- Verificar se pasta raiz/log existe
- Tentar "Refresh Sessions"
- Verificar permissões de pasta

### Tabela vazia?
- Executar algo no plugin para gerar logs
- Clicar "Refresh Sessions"
- Verificar se há .log files em raiz/log

### Filtro não funciona?
- Verificar se valor existe nos logs
- Clicar "Clear Filters"
- Tentar novamente

### Performance lenta?
- Usar filtros para reduzir volume
- Considerar "Clear All Logs"
- Fechar e reabrir

### Cores estranhas?
- Cores normalmente autogeneradas
- Mesma classe = mesma cor SEMPRE
- Cores para tools são customizáveis (padrão)

# ============================================================
# LOCAIS IMPORTANTES
# ============================================================

Log Directory: raiz/log/

Arquivo de log: mtl_tools_YYYYMMDD_HHMMSS_pidPPPPPP.log

Exemplo: mtl_tools_20260122_112852_pid122308.log

Formato: JSONL (um JSON por linha)

# ============================================================
# TECLADO
# ============================================================

Ctrl+C - Copiar seleção (se implementado)
Escape - Fechar diálogos
Enter - Aplicar busca (se necessário)
Tab - Navegar entre campos

# ============================================================
# EXEMPLOS
# ============================================================

## Exemplo 1: Encontrar erros recentes
1. Abrir Logcat
2. No campo "Search" digitar: "ERROR"
3. Ou clicar Level > selecionar "ERROR"
4. Tabela mostra apenas erros
5. Duplo-click para ver detalhes

## Exemplo 2: Ver logs de ferramenta específica
1. Abrir Logcat
2. Clicar botão "Tool"
3. Selecionar "vector_field"
4. Tabela mostra apenas dessa ferramenta

## Exemplo 3: Ver aumento de erros em tempo real
1. Abrir Logcat
2. Nível = ERROR apenas
3. Observe tabela atualizar em tempo real
4. Novos erros aparecem conforme gerados

## Exemplo 4: Copiar stack trace completo
1. Abrir Logcat
2. Filtrar para encontrar erro
3. Duplo-click na linha
4. Clicar "Copy All"
5. Colar em editor de texto

# ============================================================
# LIMITAÇÕES CONHECIDAS
# ============================================================

- Não salva estado entre execuções
- Não export para CSV/JSON (por enquanto)
- Monitor de arquivo tem latência ~1s
- Regex busca é básica

# ============================================================
# SUPORTE E FEEDBACK
# ============================================================

Se encontrar problemas:
1. Verificar ARCHITECTURE.md para detalhes técnicos
2. Verificar README.md para uso avançado
3. Verificar IMPLEMENTATION_SUMMARY.md para overview

# ============================================================
