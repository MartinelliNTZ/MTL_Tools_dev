# Cadmus — QGIS Automation Suite

![Canopy](resources/images/canopy.svg)

![Cadmus Icon](resources/icons/cadmus_icon.png) ![TMLAgro Logo](resources/images/tmlagro.png)

## Sobre

Cadmus é um plugin modular para QGIS (compatível 3.16+ e 4.x) desenvolvido pela TML Agro.
Proporciona automação de workflows cartográficos, processamento de dados vetoriais/raster,
instrumentos de análise e logging integrado.

## Arquitetura

- core/: engine assíncrona, tasks/steps, config e log.
- plugins/: plugins individuais (ExportAllLayouts, ReplaceInLayouts, etc.)
- utils/: utilitários transversais (ProjectUtils, Preferences, StringUtils).
- 
esources/: ícones, imagens, estilos e instruções de cada plugin.
- docs/arquitetura: documentação de projeto e contratos técnicos.

## Principais componentes

- BasePluginMTL + WidgetFactory + AppBarWidget
- AsyncPipelineEngine, BaseStep, BaseTask
- LogUtils/LogCleanupUtils, Logcat UI
- ProjectUtils (manipulação segura de camadas/projeto)

## Funcionalidades principais

1. Exportação de layouts em lote (PDF/PNG)
2. Substituição de textos em layouts
3. Reinício seguro do QGIS (Salvar/Fechar/Reabrir)
4. Carregamento de pastas recursivo (vetor/raster)
5. Geração de rastro de implemento agrícola
6. Estatísticas e diferenças de atributos
7. Logcat com filtro em tempo real

## Instalação

1. Copie a pasta Cadmus para <QGIS>/python/plugins/.
2. Ative em Plugins > Gerenciar e Instalar Plugins.
3. Acesse Cadmus no menu principal.

## Uso GitHub

- Clone o repositório, mantenha módulos separados e adicione testes para cada plugin.
- Utilize docs/arquitetura como fonte de verdade de contratos entre classes.

## Contribuição

- Siga os padrões do projeto (PEP8, Clean Code, SOLID)
- Registre alterações em docs/ia/changelog.txt
- Mantenha documentação atualizada em docs/arquitetura

## Licença

MIT
