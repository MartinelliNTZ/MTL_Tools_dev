# -*- coding: utf-8 -*-
from ..core.config.LogUtils import LogUtils
from .IconManager import IconManager as im


class HtmlInstructionsProvider:
    logger = None
    logo = ""
    author_info = """"""

    def __init__(self, tool_key: str):
        self.logger = LogUtils(
            tool=tool_key, class_name="HtmlInstructionsProvider", level="DEBUG"
        )
        self.logger.debug(f"HtmlInstructionsProvider initialized for tool: {tool_key}")
        self.author_info = f"""
            {self.transform_h(' Autor')}
            <h2 style="color:#ffffff;">
            Matheus A.S. Martinelli
            </h2>"""
        self.logo = f"{self._get_image(im.CADMUS_PNG, width=80)}"

    def _get_image(self, image_name: str, width: int = 100) -> str:
        path = im.icon_path(image_name)

        return f'<img src="{path}" alt="Cadmus Logo" width="{width}" style="display:block;margin-left:auto;margin-right:auto;align:center;">'

    def get_instructions(self, algorithm_name: str) -> str:
        method_name = f"get_{algorithm_name}_help"
        if hasattr(HtmlInstructionsProvider, method_name):
            method = getattr(HtmlInstructionsProvider, method_name)
            self.logger.debug(f"Encontrado método de instruções: {method_name}")
            return method(self)
        else:
            self.logger.warning(f"Método de instruções não encontrado: {method_name}")
            return "Instruções não disponíveis para este algoritmo."

    def transform_h(self, text="", level=2):
        return f'<h{level} style="color:#ffffff;">{text}</h{level}>'

    def transform_alert(self, text=""):
        return f'<h3 style="background-color:#ffcccc;color:#990000;padding:10px;border-radius:5px;margin:10px 0;">⚠️{text}</h3>'

    def get_raster_difference_statistics_help(self):
        return f"""
            {self.logo}
            Ferramenta do pacote Cadmus para cálculo de diferença entre múltiplos rasters,
            com geração automática de estatísticas e relatório consolidado em HTML.

            {self.transform_h('🎯 Objetivo')}
            Calcular diferenças entre todos os pares possíveis de rasters
            Identificar variações entre superfícies (ex: DSM, DTM, modelos temporais)
            Gerar estatísticas automáticas para cada comparação
            Consolidar resultados em relatório único

            {self.transform_h('🛠️ Como usar')}
            1. Abra a ferramenta
            Menu → Cadmus → Raster → Diferença de Rasters (Pasta/Camadas)
            2. Defina a entrada
            Opção A: Informe uma pasta com rasters (busca recursiva)
            Opção B: Selecione rasters já carregados no QGIS
            3. Defina saída (opcional)
            Caso não informado, será criada pasta temporária
            4. Execute
            O sistema irá gerar todas as combinações possíveis entre rasters

            {self.transform_h('⚙️ Comportamento')}
            Gera combinações 2 a 2 (nC2)
            Calcula: Raster A - Raster B
            Mantém NoData consistente
            Processa apenas rasters com sobreposição espacial
            Usa resolução e extent do primeiro raster do par
            Ignora automaticamente pares sem interseção

            {self.transform_h('🧾 Saídas')}
            Para cada par:
            DIF_rasterA_rasterB.tif

            Estatísticas individuais:
            DIF_rasterA_rasterB_stats.html

            Relatório consolidado:
            raster_difference_stats_summary.html

            Estatísticas incluem:
            MIN
            MAX
            INTERVALO (MAX - MIN)
            MEAN
            STD_DEV

            {self.transform_h('⚠️ Atenções')}
            Número de combinações cresce rapidamente (n²)
            Pode gerar muitos arquivos em grandes volumes
            Rasters devem ter alinhamento razoável (resolução/CRS)
            Diferenças usam apenas banda 1
            Extents diferentes podem gerar recorte implícito

            {self.transform_h('✅ Boas práticas')}
            Trabalhar com rasters já alinhados
            Evitar grandes volumes sem necessidade
            Testar com poucos arquivos primeiro
            Validar NoData antes do processamento
            Usar nomes curtos para evitar caminhos longos

            {self.author_info}
        """

    def get_difference_fields_help(self):
        return f"""
            {self.logo}
            Ferramenta do pacote Cadmus para gerar campos de diferença entre um campo base e outros campos numéricos da camada.

            {self.transform_h('🎯 Objetivo')}
            Calcular a diferença entre varios atributos numéricos de uma camada de pontos, usando um campo base como referência.
            Ideal para análises comparativas e detecção de variações.
            O resultado é uma nova camada com campos adicionais contendo as diferenças calculadas.
            O resultado pode ser usado pelo Estatisticas de Atributo para calcular estatísticas sobre as diferenças.

            {self.transform_h('🛠️ Como usar')}
            1. Abra a ferramenta
            Menu → Cadmus → Estatística → Gerador de Diferenças entre Campos
            2. Selecione a camada
            Escolha uma camada de pontos
            3. Defina o campo base
            Campo usado como referência para subtração
            4. Defina exclusões (opcional)
            Campos que NÃO participarão do cálculo
            Se vazio: todos os campos numéricos serão usados
            5. Configure prefixo
            Define o nome dos novos campos gerados
            6. Defina precisão
            Quantidade de casas decimais
            7. Execute
            Acompanhe o processamento até finalizar

            {self.transform_h('⚙️ Comportamento')}
            Opera apenas em campos numéricos
            Ignora valores nulos automaticamente
            Mantém atributos originais
            Adiciona novos campos ao final da tabela

            {self.transform_h('🧾 Saídas')}
            Campos adicionados com prefixo definido
            Exemplo:
            diff_altura
            diff_peso
            diff_temperatura

            {self.transform_h('⚠️ Atenções')}
            Campos não numéricos são ignorados
            Valores nulos geram saída nula
            Muitos campos podem aumentar o tamanho da tabela

            {self.transform_h('✅ Boas práticas')}
            Revisar campos antes de executar
            Evitar excesso de campos desnecessários
            Usar prefixos claros
            Testar com subconjunto de dados
            {self.author_info}"""

    def get_raster_mass_clipper_help(self):
        return f"""
            {self.logo}
            Ferramenta do pacote Cadmus para recorte em lote de rasters usando uma camada poligonal como máscara,
            com suporte a processamento por feição e correção automática de bordas.

            {self.transform_h('🎯 Objetivo')}
            Recortar múltiplos rasters em uma única execução
            Permitir recorte por camada inteira ou por feição
            Aplicar correção de borda baseada no tamanho do pixel
            Manter resolução original dos rasters
            Executar processamento em paralelo

            {self.transform_h('🛠️ Como usar')}
            1. Abra a ferramenta
            Menu → Cadmus → Raster → Recorte Massivo de Rasters
            2. Defina a máscara
            Selecione uma camada poligonal para recorte
            3. Selecione os rasters
            Adicione um ou mais rasters
            4. Configure o modo
            Recortar por cada polígono
            Ativado: gera um raster por feição
            Desativado: usa a camada inteira
            5. Ajuste correção
            Aplica pixel * 1.1 para evitar cortes serrilhados
            6. Pasta de saída
            A pasta será criada automaticamente se não existir
            7. Execute
            Acompanhe o progresso e aguarde a finalização

            {self.transform_h('⚙️ Comportamento')}
            Usa GDAL (cliprasterbymasklayer)
            Reprojeta máscara automaticamente
            Mantém resolução original
            Processamento multi-core

            {self.transform_h('🧾 Saídas')}
            Modo normal
            raster1_clip.tif
            raster2_clip.tif

            Modo por feição
            raster1_feat_1.tif
            raster1_feat_2.tif
            raster2_feat_1.tif

            {self.transform_h('⚠️ Atenções')}
            Modo por feição pode gerar muitos arquivos
            Buffer aumenta levemente a área recortada
            Alto uso de CPU e disco em grandes volumes

            {self.transform_h('✅ Boas práticas')}
            Testar com poucos dados antes
            Usar modo por feição apenas quando necessário
            Garantir CRS correto
            Usar pasta de saída limpa
            {self.author_info}"""

    def get_geometry_difference_line_help(self):
        return f"""
            {self.logo}
            Ferramenta do pacote Cadmus para criação de linhas entre pontos,
            calculando a distância entre pares com base em agrupamento por atributos.

            {self.transform_h('🎯 Objetivo')}
            Gerar linhas conectando 2 ou mais pontos relacionados
            Calcular distância entre pares de pontos
            Permitir análise espacial entre conjuntos de pontos
            Suportar comparação entre uma ou duas camadas

            {self.transform_h('🛠️ Como usar')}
            1. Abra a ferramenta
            Menu → Cadmus → Vetorial → Linha de Diferença entre Pontos
            2. Selecione a camada A
            Camada principal de pontos
            3. (Opcional) Selecione camada B
            Usada apenas no modo com duas camadas
            4. Escolha o modo
            Ativar "Usar segunda camada" para modo 2
            5. Defina campos de agrupamento
            Campo A: obrigatório
            Campo B: obrigatório no modo 2
            6. Execute
            Acompanhe o processamento até finalizar

            {self.transform_h('⚙️ Comportamento')}
            Modo 1 (uma camada)
            Agrupa por atributo
            Cria linhas entre pontos sequenciais

            Modo 2 (duas camadas)
            Relaciona pontos entre A e B pelo mesmo valor de campo
            Gera linha para cada correspondência

            Geometrias não pontuais usam centróide automaticamente
            Ignora feições inválidas
            Garante ordem consistente por ID

            {self.transform_h('🧾 Saídas')}
            Camada de linhas com atributos

            Campos gerados:
            group_key
            feature_a
            feature_b
            distance

            {self.transform_h('⚠️ Atenções')}
            Modo 2 exige camada B e campo correspondente
            Campos devem possuir valores compatíveis
            Geometrias vazias são ignoradas
            Grande volume pode impactar desempenho

            {self.transform_h('✅ Boas práticas')}
            Garantir consistência nos campos de agrupamento
            Evitar valores nulos
            Testar com subconjunto antes
            Verificar CRS das camadas

            {self.author_info}
        """

    def get_raster_mass_sampler_help(self):
        return f"""
            {self.logo}
            Ferramenta do pacote Cadmus para amostragem massiva de pontos de múltiplos rasters em pontos,
            gerando uma nova camada com os valores extraídos como atributos.


            {self.transform_h('🎯 Objetivo')}
            Extrair valores de vários rasters em pontos de forma automatizada
            Gerar uma tabela com valores amostrados por ponto
            Permitir análise cruzada entre diferentes superfícies raster
            Preparar dados para estatística, modelagem e validação
            {self.transform_alert('Imprescindível que o nome do raster seja claro e único, pois será usado para nomear os campos de saída.')}

            {self.transform_h('🛠️ Como usar')}
            1. Abra a ferramenta
            Menu → Cadmus → Raster → Amostragem Massiva de Rasters
            2. Selecione os pontos
            Escolha uma camada de pontos de entrada
            3. Selecione os rasters
            Adicione um ou mais rasters para amostragem
            4. Defina CRS de saída (opcional)
            Caso informado, a camada resultante será reprojetada
            5. Execute
            Acompanhe o processamento até finalizar

            {self.transform_h('⚙️ Comportamento')}
            Amostra valores usando dataProvider.sample()
            Reprojeta automaticamente pontos para o CRS de cada raster
            Mantém atributos originais dos pontos
            Cria novos campos com valores de cada raster
            Garante nomes de campos válidos e únicos

            {self.transform_h('🧾 Saídas')}
            Nova camada de pontos com atributos adicionais
            Cada raster gera um novo campo

            Exemplo:
            elevacao
            ndvi
            temperatura

            {self.transform_h('⚠️ Atenções')}
            Rasters devem possuir dados válidos na área dos pontos
            Diferenças de CRS são tratadas, mas podem impactar precisão
            Grande volume de pontos e rasters aumenta tempo de processamento
            Valores fora da extensão retornam nulo

            {self.transform_h('✅ Boas práticas')}
            Verificar CRS dos dados antes de executar
            Evitar rasters desnecessários
            Usar nomes claros para rasters
            Testar com subconjunto de pontos

            {self.author_info}
        """

    def get_attribute_statistics_help(self):
        return f"""
            {self.logo}
            Ferramenta do pacote Cadmus para calcular estatísticas descritivas de atributos numéricos de uma camada vetorial,
            gerando um arquivo CSV com os resultados consolidados.

            {self.transform_h('🎯 Objetivo')}
            Calcular média, mediana, desvio padrão, percentis e outras estatísticas para campos numéricos
            Permitir análise exploratória de dados (EDA) de forma rápida e configurável
            Exportar resultados para CSV, facilitando integração com outras ferramentas
            Auxiliar na validação e caracterização de dados antes de processamentos avançados

            {self.transform_h('🛠️ Como usar')}
            1. Abra a ferramenta
            Menu → Cadmus → Estatística → Estatísticas de Atributos
            2. Selecione a camada de entrada
            Escolha uma camada vetorial (pontos, linhas ou polígonos)
            3. (Opcional) Defina campos a excluir
            Selecione campos que não devem ser analisados
            4. Ajuste a precisão decimal
            Número de casas decimais nos resultados
            5. Escolha as estatísticas desejadas
            Marque/desmarque os checkboxes na seção avançada
            6. Configure a saída
            Defina o caminho e nome do arquivo CSV
            7. Opções avançadas
            - Forçar formato PT-BR (separador ; e vírgula decimal)
            - Carregar CSV automaticamente após execução
            8. Execute
            Acompanhe o progresso até a conclusão

            {self.transform_h('⚙️ Comportamento')}
            Identifica automaticamente campos numéricos (inteiros e decimais)
            Ignora valores nulos (NULL) no cálculo das estatísticas
            Calcula apenas as estatísticas selecionadas pelo usuário
            Ordena os campos alfabeticamente no CSV gerado
            Suporta grandes volumes de dados com uso eficiente de memória
            O arquivo CSV é salvo com codificação UTF-8

            {self.transform_h('🧾 Saídas')}
            Arquivo CSV contendo uma linha por campo analisado

            Colunas presentes:
            - Campo: nome do atributo
            - Contagem: número de valores válidos
            - Estatísticas selecionadas (ex: Média, Mediana, Desvio Padrão, etc.)

            Exemplo de linhas:
            "altura";150;1.75;1.80;0.05
            "peso";150;70.2;71.0;5.3

            {self.transform_h('⚠️ Atenções')}
            Apenas campos numéricos são considerados; campos texto ou data são ignorados
            Valores nulos são excluídos das estatísticas (podem reduzir a contagem)
            O arquivo CSV pode ficar extenso se muitos campos forem selecionados
            A opção "Forçar PT-BR" altera separadores e pode afetar a leitura em outros softwares

            {self.transform_h('✅ Boas práticas')}
            Revise os campos disponíveis antes de executar para evitar inclusões desnecessárias
            Utilize a exclusão de campos para focar nas variáveis de interesse
            Teste com um subconjunto de dados para verificar a adequação das estatísticas escolhidas
            Prefira nomes de campos sem caracteres especiais para facilitar a leitura do CSV

            {self.author_info}
        """
