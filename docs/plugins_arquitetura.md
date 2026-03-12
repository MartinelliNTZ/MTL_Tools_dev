# Plugins do MTL Tools — Arquitetura, Contratos e Boas Práticas

Data: 2026/03/12

Resumo
------
Este documento descreve de forma técnica o subsistema de plugins do MTL Tools:
- Estrutura, contratos, padrões de implementação, integração com QGIS
- Regras obrigatórias, armadilhas, recomendações operacionais
- Tabela detalhada dos plugins


Componentes Principais
----------------------
- **BasePluginMTL**: Classe base obrigatória para todos os plugins. Garante padronização, persistência, logging e integração.
- **WidgetFactory**: Fábrica central de widgets, layouts e componentes UI. Plugins devem construir UI exclusivamente via WidgetFactory, garantindo padronização, modularidade e compatibilidade.
- **MainLayout**: Layout principal dos dialogs, encapsula scroll, bordas, AppBar.
- **AppBarWidget**: Barra superior com título, botões de ação (Executar, Info, Fechar).
- **BottomActionButtonsWidget**: Botões inferiores padronizados (Executar, Fechar, Info).
- **AttributeSelectorWidget**: Widget exclusivo para seleção de atributos/campos.
- **Styles**: Centraliza temas visuais, define estilos globais, checkbox, radio, label, etc.
- **InfoDialog**: Diálogo padronizado para exibir instruções técnicas, renderiza Markdown nativamente ou converte para HTML.
- **ToolKey**: Enum de identificação de cada ferramenta/plugin.
- **Preferences**: API para salvar/carregar preferências de cada plugin.
- **ProjectUtils**: Responsável por operações com projeto QGIS (carregar, salvar, manipular camadas). Plugins não devem acessar QgsProject/QgsApplication diretamente.
- **AsyncPipelineEngine**: Plugins não criam tasks diretamente; usam steps/pipeline para processamento assíncrono.

Integração com Resources
-----------------------
Plugins devem usar recursos padronizados para UI, estilos e instruções:
- WidgetFactory: construção de UI modular, compatível e padronizada
- Styles: aplicação de temas visuais
- InfoDialog: exibição de instruções técnicas, Markdown/HTML
- resources/widgets: widgets exclusivos para cada função
- resources/icons: ícones padronizados
- resources/instructions: arquivos de instruções para cada plugin

Recomendações técnicas:
- Plugins devem construir UI exclusivamente via WidgetFactory
- Estilos devem ser aplicados via Styles
- InfoDialog deve ser usado para exibir instruções técnicas
- Widgets devem ser modulares, reutilizáveis e compatíveis
- Arquivos de instruções devem ser mantidos e atualizados para cada plugin

Para detalhes, consulte [docs/resources_arquitetura.md](docs/resources_arquitetura.md)

Integração com Utils
--------------------
Plugins dependem fortemente dos utilitários (utils) para delegar operações técnicas:
- **DependenciesManager**: Garantia de dependências externas antes de operações (ex.: PDF, imagens)
- **ExplorerUtils**: Entrada de dados, varredura de diretórios, identificação de arquivos
- **FormatUtils**: Conversão e exibição de valores técnicos (bytes, duração, velocidade)
- **LayoutsUtils**: Processamento de layouts, substituição de textos
- **PDFUtils**: Manipulação de PDFs/imagens, logging
- **Preferences**: Persistência de estado/configuração
- **ProjectUtils**: Backup, manipulação de camadas, clipboard
- **QgisMessageUtil**: Exibição de mensagens, feedback ao usuário
- **StringUtils**: Filtros, drivers, nomes padronizados
- **ToolKeys**: Enum de identificação, cores, integração com logging

Recomendações técnicas:
- Plugins devem delegar operações técnicas para utils sempre que possível
- Utils devem ser documentados, modulares e compatíveis
- Plugins devem registrar logs via LogUtils e exibir feedback via QgisMessageUtil
- Preferências e estado devem ser persistidos via Preferences
- Operações de projeto/camadas devem ser feitas via ProjectUtils

Para detalhes, consulte [docs/utils_arquitetura.md](docs/utils_arquitetura.md)

Contratos e Regras Obrigatórias
-------------------------------
- Todos os plugins devem:
  - Herdar de BasePluginMTL
  - Usar WidgetFactory para UI (não acessar /QWidget/QPushButton etc. diretamente)
  - Declarar ToolKey único
  - Salvar preferências via Preferences
  - Integrar ProjectUtils para manipulação de projeto/camadas
  - Ter arquivo de instruções em resources/instructions
  - Ter análise de cenário em docs/analisecenario
  - Ser declarados em mtl_tools_plugin.py
  - Implementar método de abertura padrão (exemplo):
    ```python
    def run_copy_attributes(iface):
        dlg = CopyAttributes(iface)
        dlg.setModal(False)
        dlg.show()
        return dlg
    ```
  - Seguir Clean Code e boas práticas
  - Garantir compatibilidade QGIS 3.16 a 4.0
  - Não adicionar tasks diretamente; usar AsyncPipelineEngine

Fluxo de Execução
-----------------
1. Plugin é instanciado via método run padrão
2. UI é construída via WidgetFactory (se aplicável)
3. Preferências são carregadas/salvas automaticamente
4. Operações de projeto/camadas são delegadas a ProjectUtils
5. Processamento pesado é feito via steps/pipeline (AsyncPipelineEngine)
6. Logging é feito via LogUtils
7. Resultados, erros e mensagens são exibidos via QgisMessageUtil

Padrões de Implementação
------------------------
- Plugins de janela devem implementar _build_ui() usando WidgetFactory
- Plugins instantâneos podem omitir UI, mas devem exibir mensagens de status
- Plugins devem evitar dependências diretas de QGIS widgets/core
- Plugins devem persistir estado da janela, opções e preferências
- Plugins devem ter instruções e análise de cenário documentadas

Erros Comuns e Armadilhas
-------------------------
- Acessar widgets/core(possivel mas tente evitar) do QGIS diretamente (violação de contrato)
- Não usar WidgetFactory para UI
- Não persistir preferências corretamente
- Adicionar tasks diretamente (deve usar pipeline)
- Falta de compatibilidade com versões antigas do QGIS
- Não documentar instruções ou análise de cenário

Boas Práticas de Uso
--------------------
- Seguir padrões de BasePluginMTL e WidgetFactory
- Documentar contratos de entrada/saída de cada plugin
- Usar ToolKey para identificação e logging
- Persistir preferências e estado de UI
- Delegar operações de projeto/camadas para ProjectUtils
- Garantir compatibilidade máxima
- Manter documentação técnica e instruções atualizadas

Tabela Detalhada dos Plugins
----------------------------
| Nº  | Nome                          | Tipo                        | Classe Plugin              | Usa Task | Tipo de Entrada | Tipo de Saída | Risco |
|-----|-------------------------------|-----------------------------|----------------------------|----------|-----------------|---------------|-------|
| 01  | Exportar Todos os Layouts     | Janela                      | ExportAllLayoutsDialog     | Não      | Projeto QGIS    | PDF/PNG       | Substituir produtos antigos |
| 02  | Substituir Textos nos Layouts | Janela                      | ReplaceInLayoutsDialog     | Não      | Layouts QGIS    | Layouts QGIS  | Crítico/alteração QGZ |
| 03  | Salvar, Fechar e Reabrir      | Instantânea                 | _RestartExecutor           | Não      | Projeto QGIS    | Projeto QGIS  | Crítico/alteração QGZ |
| 04  | Carregar Pasta de Arquivos    | Janela                      | LoadFolderLayersDialog     | Sim      | Arquivos        | Camadas QGIS  | Alteração QGZ |
| 05  | Gerar Rastro de Implemento    | Janela                      | GenerateTrailPlugin        | Sim      | Camada Vetorial | Camada Vetorial| Nenhum |
| 06  | Sobre o MTL Tools             | Janela                      | AboutDialog                | Não      | Nenhum          | Informações   | Nenhum |
| 07  | Capturar Coordenadas          | Instantânea+Resultado        | CoordClickTool             | Sim      | Canvas QGIS     | Diálogo       | Travamento da task |
| 08  | Calcular Campos Vetoriais     | Instantânea                 | VectorFieldsCalculationPlugin | Sim  | Camada Vetorial | Camada Vetorial| Manipulação de vetores |
| 09  | Obter Coordenadas de Drone    | Janela                      | DroneCordinates            | Sim      | Arquivos MRK    | Camada Vetorial| Travamento por excesso de dados |
| 10  | Converter Multipart           | Instantânea                 | VectorMultipartPlugin      | Não      | Camada Vetorial | Camada Vetorial| Manipulação de vetores |
| 11  | Copiar Atributos de Vetores   | Janela                      | CopyAttributes             | Não      | Camada Vetorial | Camada Vetorial| Manipulação de vetores |
| 12  | LogCat Viewer                 | Janela (multithread)        | LogcatDialog               | Não      | Logs            | Diálogo       | Nenhum |
| 13  | SettingsPlugin                | Janela                      | SettingsPlugin             | Não      | Preferências    | Preferências  | Nenhum |

Recomendações Finais
--------------------
1. Seguir contratos de BasePluginMTL, WidgetFactory, ProjectUtils, Preferences
2. Garantir documentação técnica, instruções e análise de cenário
3. Manter compatibilidade máxima com QGIS
4. Evitar dependências diretas de widgets/core QGIS
5. Usar pipeline para processamento assíncrono
6. Persistir preferências e estado de UI
7. Documentar riscos e contratos de cada plugin
