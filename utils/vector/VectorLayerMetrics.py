class VectorLayerMetrics:
    """
    Responsável pela leitura e cálculos espaciais de camadas vetoriais.
    
    Escopo:
    - Calcular métricas geométricas (área, comprimento, perímetro)
    - Gerar estatísticas espaciais
    - Medir distâncias e ângulos
    - Analisar distribuição de feições
    - Cálculos de densidade e concentração
    
    Responsabilidade Principal:
    - Fornecer cálculos e análises espaciais precisas
    - Garantir acurácia em medições
    - NÃO alterar dados
    
    NÃO é Responsabilidade:
    - Transformar geometrias (use VectorLayerGeometry)
    - Reprojetar (use VectorLayerProjection)
    - Manipular atributos (use VectorLayerAttributes)
    - Carregar ou salvar (use VectorLayerSource)
    """

    def calculate_feature_area(self, feature, external_tool_key="untraceable"):
        """Calcula a área total de uma feição em unidades do CRS."""
        pass

    def calculate_feature_length(self, feature, external_tool_key="untraceable"):
        """Calcula o comprimento total de uma feição em unidades do CRS."""
        pass

    def calculate_feature_perimeter(self, feature, external_tool_key="untraceable"):
        """Calcula o perímetro de uma feição em unidades do CRS."""
        pass

    def get_layer_total_area(self, layer, external_tool_key="untraceable"):
        """Calcula a área total de todas as feições da camada."""
        pass

    def get_layer_total_length(self, layer, external_tool_key="untraceable"):
        """Calcula o comprimento total de todas as feições da camada."""
        pass

    def get_layer_extent_area(self, layer, external_tool_key="untraceable"):
        """Calcula a área do retângulo envolvente (extent) da camada."""
        pass

    def calculate_feature_count_by_area(self, layer, area_ranges, external_tool_key="untraceable"):
        """Agrupa e conta feições por intervalos de área especificados."""
        pass

    def get_feature_centroid(self, feature, external_tool_key="untraceable"):
        """Calcula o centroide de uma feição."""
        pass

    def get_layer_centroid(self, layer, external_tool_key="untraceable"):
        """Calcula o centroide geral de todas as feições da camada."""
        pass

    def calculate_distance_between_features(self, feature1, feature2, external_tool_key="untraceable"):
        """Calcula a distância entre duas feições."""
        pass

    def get_layer_density_statistics(self, layer, grid_size, external_tool_key="untraceable"):
        """Calcula estatísticas de densidade de feições em uma grade."""
        pass

    def analyze_spatial_distribution(self, layer, external_tool_key="untraceable"):
        """Analisa o padrão de distribuição espacial das feições."""
        pass
