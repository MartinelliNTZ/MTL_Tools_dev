# Plugins do MTL Tools

## Tabela Resumida

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


## Análise dos Plugins

### 01. Exportar Todos os Layouts
- Tipo: Janela
- Classe: ExportAllLayoutsDialog
- Usa Task: Não
- Entrada: Projeto QGIS
- Saída: PDF/PNG
- Risco: Substituir produtos antigos

### 02. Substituir Textos nos Layouts
- Tipo: Janela
- Classe: ReplaceInLayoutsDialog
- Usa Task: Não
- Entrada: Layouts QGIS
- Saída: Layouts QGIS
- Risco: Crítico/alteração QGZ

### 03. Salvar, Fechar e Reabrir Projeto
- Tipo: Instantânea
- Classe: _RestartExecutor
- Usa Task: Não
- Entrada: Projeto QGIS
- Saída: Projeto QGIS
- Risco: Crítico/alteração QGZ

### 04. Carregar Pasta de Arquivos
- Tipo: Janela
- Classe: LoadFolderLayersDialog
- Usa Task: Sim (AsyncPipelineEngine)
- Entrada: Arquivos
- Saída: Camadas QGIS
- Risco: Alteração QGZ

### 05. Gerar Rastro de Implemento
- Tipo: Janela
- Classe: GenerateTrailPlugin
- Usa Task: Sim (AsyncPipelineEngine)
- Entrada: Camada Vetorial
- Saída: Camada Vetorial
- Risco: Nenhum

### 06. Sobre o MTL Tools
- Tipo: Janela
- Classe: AboutDialog
- Usa Task: Não
- Entrada: Nenhum
- Saída: Informações
- Risco: Nenhum

### 07. Capturar Coordenadas
- Tipo: Instantânea+Resultado
- Classe: CoordClickTool
- Usa Task: Sim (ReverseGeocodeTask, AltimetriaTask)
- Entrada: Canvas QGIS
- Saída: Diálogo de resultado
- Risco: Travamento da task

### 08. Calcular Campos Vetoriais
- Tipo: Instantânea
- Classe: VectorFieldsCalculationPlugin
- Usa Task: Sim (AsyncPipelineEngine)
- Entrada: Camada Vetorial
- Saída: Camada Vetorial
- Risco: Manipulação de vetores

### 09. Obter Coordenadas de Drone
- Tipo: Janela
- Classe: DroneCordinates
- Usa Task: Sim (AsyncPipelineEngine)
- Entrada: Arquivos MRK
- Saída: Camada Vetorial
- Risco: Travamento por excesso de dados

### 10. Converter Multipart
- Tipo: Instantânea
- Classe: VectorMultipartPlugin
- Usa Task: Não
- Entrada: Camada Vetorial
- Saída: Camada Vetorial
- Risco: Manipulação de vetores

### 11. Copiar Atributos de Vetores
- Tipo: Janela
- Classe: CopyAttributes
- Usa Task: Não
- Entrada: Camada Vetorial
- Saída: Camada Vetorial
- Risco: Manipulação de vetores

### 12. LogCat Viewer
- Tipo: Janela (multithread)
- Classe: LogcatDialog
- Usa Task: Não
- Entrada: Logs
- Saída: Diálogo
- Risco: Nenhum

### 13. SettingsPlugin
- Tipo: Janela
- Classe: SettingsPlugin
- Usa Task: Não
- Entrada: Preferências
- Saída: Preferências
- Risco: Nenhum


## Tipos de Ferramentas (atualizado)

- **Instantânea**: Executa automaticamente, pode exibir mensagens de confirmação/sucesso/erro/info, tem análise de cenário.
- **Instantânea+Resultado**: Executa automaticamente, exibe resultado em janela/dialog, pode exibir mensagens de confirmação/sucesso/erro/info, tem análise de cenário.
- **Janela**: Abre janela ao executar, pode ter widgets, salvar preferências, botão de instruções, pode obter dados do explorador de arquivos, pode salvar QGZ como backup, exige ação do usuário para executar.
- **Janela (multithread)**: Abre janela, processa dados em paralelo, exibe logs em tempo real.


> Plugins de Processing não foram incluídos nesta análise.
