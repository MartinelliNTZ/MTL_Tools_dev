from qgis.PyQt.QtCore import QCoreApplication


class Strings_pt_BR:
    """ "Strings for Brazilian Portuguese (pt-BR)"""

    # General
    APP_NAME = "Cadmus"

    # About
    ABOUT_CADMUS = "Sobre o Cadmus"
    VERSION = "Versão"
    UPDATED_ON = "Atualizada em"
    CREATED_ON = "Criado em"
    CREATOR = "Criador"
    LOCATION = "Local"

    # Buttons
    CLOSE = "Fechar"
    SAVE = "Salvar"
    EXPORT = "Exportar"
    CANCEL = "Cancelar"
    EXECUTE = "Executar"
    COPIED = "Copiado"

    # Common labels
    OPTIONS = "Opções"
    SAVING = "Salvamento"
    STYLES = "Estilos"
    WARNING = "Aviso"
    ERROR = "Erro"
    ADVANCED_PARAMETERS = "Parâmetros Avançados"
    APP_PREFERENCES = "Preferências do Aplicativo"
    OPEN_PREFERENCES_FOLDER = "Abrir Pasta de Preferências"
    FILE_TYPES = "Tipos de Arquivo"
    ROOT_FOLDER = "Pasta raiz:"
    OUTPUT_FOLDER = "Pasta de saída:"
    INPUT_LINE_LAYER = "Camada de Linhas (INPUT):"
    SOURCE_LAYER = "Camada de Origem:"
    TARGET_LAYER = "Camada de Destino:"
    IMPLEMENT_SIZE = "Tamanho implemento: (sempre em metros)"
    VECTOR_CALCULATION_METHOD = "Método de Cálculo Vetorial"
    VECTOR_FIELDS_PRECISION = "Precisão de campos vetoriais (casas decimais):"
    ASYNC_THRESHOLD = "Limiar assíncrono (nº de feições):"
    CALCULATION_METHOD_LABEL = "Método de cálculo vetorial:"
    SEARCH_TEXT = "Texto a buscar:"
    REPLACE_WITH_NEW_TEXT = "Texto a substituir (novo):"
    SOURCE_LAYER_ATTRIBUTES = "Atributos da camada origem"
    EXPORT_OPTIONS = "Opções de Exportação"
    MAX_WIDTH_PNG = "Max Width para PNG (px):"
    USE_PROJECT_FOLDER = "Usar pasta do projeto"
    EXPORT_PDF = "Exportar PDF"
    EXPORT_PNG = "Exportar PNG"
    MERGE_PDFS_FINAL = "Unir PDFs em PDF final"
    MERGE_PNGS_FINAL = "Unir PNGs em PDF final"
    REPLACE_EXISTING_FILES = "Substituir arquivos existentes"
    WGS84_EPSG4326 = "WGS 84 (EPSG:4326)"
    UTM_SIRGAS_2000 = "UTM SIRGAS 2000"
    ALTIMETRY_OPENTOPO = "Altimetria (OpenTopoData)"
    APPROX_ALTITUDE_METERS = "Altitude aproximada (m)"
    LATITUDE_DECIMAL = "Latitude (Decimal)"
    LONGITUDE_DECIMAL = "Longitude (Decimal)"
    LATITUDE_DMS = "Latitude (DMS)"
    LONGITUDE_DMS = "Longitude (DMS)"
    EASTING_X = "Easting (X)"
    NORTHING_Y = "Northing (Y)"
    ADDRESS_OSM = "Endereço (OSM):"
    COPY_WGS84_FULL = "Copiar WGS 84 (Completo)"
    COPY_UTM_FULL = "Copiar UTM (Completo)"
    COPY_LOCATION_FULL = "Copiar Localização (Completo)"
    POINT_COORDINATES = "Coordenadas do Ponto"
    ZONE = "Zona"
    HEMISPHERE = "Hemisfério"
    CITY = "Município"
    INTERMEDIATE_REGION = "Região Intermediária"
    STATE = "Estado"
    REGION = "Região"
    COUNTRY = "País"
    LOADING = "Carregando..."
    LOADING_LOWER = "carregando..."
    UNAVAILABLE = "Indisponível"

    # Common option labels
    CASE_SENSITIVE = "Diferenciar maiúsculas/minúsculas"
    FULL_LABEL_REPLACE = "Substituir o label inteiro quando encontrar o texto"
    LOAD_ONLY_MISSING_FILES = (
        "Carregar apenas arquivos ainda NÃO carregados no projeto"
    )
    PRESERVE_FOLDER_STRUCTURE = (
        "Criar grupos conforme estrutura de pastas/subpastas"
    )
    DO_NOT_GROUP_LAST_FOLDER = "Não agrupar a última pasta"
    CREATE_PROJECT_BACKUP_IF_SAVED = (
        "Criar backup do projeto antes de carregar (somente se salvo)"
    )

    # Common messages
    SUCCESS_MESSAGE = "Processamento executado com sucesso."
    ERROR_LAYER_NOT_FOUND = "Erro: Camada não encontrada."
    SELECT_VALID_FOLDER = "Selecione uma pasta válida."
    SELECT_AT_LEAST_ONE_FILE_TYPE = "Selecione pelo menos um tipo de arquivo."
    SELECT_AT_LEAST_ONE_EXPORT_FORMAT = "Selecione pelo menos um formato (PDF ou PNG)"
    SELECT_VALID_LINE_LAYER = "Selecione uma camada de linhas válida."
    INVALID_SOURCE_LAYER = "Camada de origem inválida"
    INVALID_TARGET_LAYER = "Camada de destino inválida"
    INVALID_INPUT_LAYER = "Camada de entrada inválida."
    FINAL_LAYER_NOT_FOUND = "Erro: camada final não encontrada no contexto."
    BUFFER_CANNOT_BE_ZERO = "Buffer não pode ser 0"
    ASYNC_STARTED = "Execução em background iniciada. Verifique o log para progresso."
    ASYNC_START_ERROR = "Erro iniciando execução assíncrona:"
    ASYNC_FINISHED = "Execução assíncrona concluída."
    ASYNC_EXECUTION_ERROR = "Erro na execução assíncrona:"
    FILES_LOADED_PREFIX = "Foram carregados"
    FILES_SUFFIX = "arquivos."
    SETTINGS_SAVED_TITLE = "Configurações Salvas"
    SETTINGS_SAVED_MESSAGE = "As configurações foram salvas com sucesso."
    PREFERENCES_FOLDER_NOT_FOUND = "Pasta de preferências não encontrada:"
    ENTER_TEXT_TO_SEARCH = "Informe o texto a buscar."
    CONFIRM_REPLACEMENTS = "Confirme substituições"
    SEARCH_LABEL = "Buscar:"
    REPLACE_WITH_LABEL = "Substituir por:"
    DESTRUCTIVE_OPERATION_WARNING = "Atenção - operação destrutiva"
    LAYOUTS_ANALYZED = "Layouts analisados:"
    CHANGES_APPLIED = "Substituições aplicadas:"
    REPLACEMENT_COMPLETED_TITLE = "Substituição concluída"
    PROJECT_BACKUP_INFO = (
        "Backup: será criada uma cópia do projeto (.qgz) na pasta backup ao lado do arquivo do projeto."
    )
    LAYER_MUST_BE_EDITABLE = "A camada precisa estar em edição"
    NO_ATTRIBUTE_SELECTED = "Nenhum atributo selecionado"
    ATTRIBUTES_COPIED_SUCCESS = "Atributos copiados com sucesso (alterações não salvas)"
    REQUIRED_LIBRARY = "Biblioteca necessária"
    PYPDF2_REQUIRED_MESSAGE = (
        "Para unir PDFs é necessário instalar o pacote PyPDF2.\n\nDeseja instalar agora?"
    )
    PILLOW_REQUIRED_MESSAGE = (
        "Para unir PNGs em PDF é necessário instalar o pacote Pillow.\n\nDeseja instalar agora?"
    )
    EXPORTING_LAYOUTS = "Exportando layouts..."
    FAILED_EXPORT_PDF = "Falha ao exportar PDF:"
    FAILED_EXPORT_PNG = "Falha ao exportar PNG:"
    ERROR_EXPORTING = "Erro exportando"
    FAILED_MERGE_PDFS = "Falha ao unir PDFs:"
    FAILED_MERGE_PNGS = "Falha ao unir PNGs:"
    ERRORS_FOUND = "Erros encontrados:"
    LAYOUTS_EXPORTED_SUCCESS = "layout(s) exportado(s) com sucesso!"
    PDFS_MERGED = "PDFs unidos"
    PNGS_MERGED = "PNGs unidos"
    EXPORT_LAYOUTS_COMPLETED = "Exportação de Layouts Concluída"
    LOCATION_COPIED_TO_CLIPBOARD = "Localização copiada para a área de transferência"
    ADDRESS_COPIED_TO_CLIPBOARD = "Endereço copiado para a área de transferência"

    # plugins/DroneCoordinates.py
    DRONE_COORDINATES_TITLE = "Coordenadas de Drone"
    DRONE_COORDINATES_TOOLTIP = (
        "Le arquivos MRK de drone para gerar pontos das fotos e o rastro do voo.\n"
        "Pode cruzar os pontos com metadados das imagens,\n"
        "salvar os resultados em arquivo e aplicar estilos QML\n"
        "aos pontos e ao trajeto gerados."
    )
    RECURSIVE_SEARCH = "Vasculhar subpastas"
    PHOTOS_METADATA = "Cruzar com metadados das fotos"
    MRK_FOLDER = "Pasta MRK:"
    SAVE_POINTS_CHECKBOX = "Salvar pontos MRK em arquivo?"
    SAVE_IN = "Salvar em:"
    SAVE_TRACK_CHECKBOX = "Salvar rastro em arquivo?"
    APPLY_STYLE_POINTS = "Aplicar estilo (QML) nos pontos?"
    QML_POINTS = "QML pontos:"
    APPLY_STYLE_TRACK = "Aplicar estilo (QML) no rastro?"
    QML_TRACK = "QML:"

    # plugins/SettingsPlugin.py
    SETTINGS_TITLE = "Configurações Cadmus"
    SETTINGS_TOOLTIP = (
        "Abre as configurações globais do Cadmus.\n"
        "Permite definir o método padrão de cálculo vetorial,\n"
        "a precisão dos campos vetoriais e o limiar de feições\n"
        "usado para processamento assíncrono."
    )
    SETTINGS_CALCULATION_METHOD_ELLIPSOIDAL = "Elipsoidal"
    SETTINGS_CALCULATION_METHOD_CARTESIAN = "Cartesiana"
    SETTINGS_CALCULATION_METHOD_BOTH = "Ambos"

    # plugins/ReplaceInLayouts.py
    REPLACE_IN_LAYOUTS_TITLE = "Substituir Texto em Layouts"
    REPLACE_IN_LAYOUTS_TOOLTIP = (
        "Procura textos nos labels dos layouts do projeto\n"
        "e substitui pelo novo valor informado.\n"
        "Pode fazer substituição parcial ou trocar o conteúdo\n"
        "inteiro do label quando houver correspondência."
    )
    REPLACE_IN_LAYOUTS_SWAP = "Inverter"
    REPLACE_IN_LAYOUTS_RUN = "Executar substituição"

    # plugins/LoadFolderLayers.py
    LOAD_FOLDER_LAYERS_TITLE = "Carregar Pasta de Arquivos"
    LOAD_FOLDER_LAYERS_TOOLTIP = (
        "Carrega em lote arquivos vetoriais e raster de uma pasta\n"
        "e de suas subpastas para o projeto QGIS.\n"
        "Pode filtrar por tipo de arquivo, evitar duplicados\n"
        "e organizar as camadas conforme a estrutura de pastas."
    )
    LOAD_FOLDER_LAYERS_RUN = "Carregar Arquivos"

    # plugins/GenerateTrailPlugin.py
    GENERATE_TRAIL_TITLE = "Gerar Rastro de Máquinas"
    GENERATE_TRAIL_TOOLTIP = (
        "Gera a faixa ocupada por um implemento a partir de uma camada de linhas.\n"
        "Converte a largura informada para a unidade da camada,\n"
        "aplica buffer usando metade desse valor e cria\n"
        "uma nova camada com o rastro resultante."
    )

    # plugins/CopyAttributesPlugin.py
    COPY_ATTRIBUTES_TITLE = "Copiar Atributos de Vetor"
    COPY_ATTRIBUTES_TOOLTIP = (
        "Copia a estrutura de campos de uma camada vetorial de origem\n"
        "para uma camada vetorial de destino.\n"
        "Permite selecionar quais atributos criar e tratar conflitos\n"
        "de nome quando um campo já existe na camada destino."
    )

    # plugins/ExportAllLayouts.py
    EXPORT_ALL_LAYOUTS_TITLE = "Exportar Todos os Layouts"
    EXPORT_ALL_LAYOUTS_TOOLTIP = (
        "Exporta todos os layouts do projeto em PDF, PNG ou ambos.\n"
        "Pode unir os PDFs gerados em um arquivo final,\n"
        "converter os PNGs em PDF e controlar sobrescrita\n"
        "dos arquivos na pasta de saída."
    )

    # plugins/VectorMultipartPlugin.py
    CONVERTER_MULTIPART_TOOLTIP = (
        "Processa feições multipart da camada vetorial ativa\n"
        "e separa cada parte em feições simples.\n"
        "Pode atuar apenas nas feições selecionadas\n"
        "ou em toda a camada, preservando os atributos."
    )

    # plugins/CoordClickTool.py
    COORD_CLICK_TOOL_TOOLTIP = (
        "Permite clicar no mapa para consultar coordenadas do ponto.\n"
        "Abre um dialogo com WGS84, UTM, altitude aproximada\n"
        "e endereco estimado, alem de opcoes de copia\n"
        "para a area de transferencia."
    )
