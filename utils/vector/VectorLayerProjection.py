class VectorLayerProjection:
    """
    Responsável pelo CRS, reprojeção e unidades de camadas vetoriais.
    
    Escopo:
    - Gerenciar sistemas de referência de coordenadas
    - Reprojetar camadas entre CRS diferentes
    - Converter unidades de medida
    - Validar compatibilidade de CRS
    - Gerenciar transformações de coordenadas
    
    Responsabilidade Principal:
    - Orquestrar operações de reprojeção e conversão de CRS
    - Garantir consistência espacial entre camadas
    - Converter entre sistemas de unidades
    
    NÃO é Responsabilidade:
    - Alterar atributos da camada (use VectorLayerAttributes)
    - Calcular métricas espaciais (use VectorLayerMetrics)
    - Transformar geometria além de reprojeção (use VectorLayerGeometry)
    - Carregar ou salvar camadas (use VectorLayerSource)
    """

    def get_layer_crs(self, layer, external_tool_key="untraceable"):
        """Obtém o CRS atual da camada."""
        pass

    def set_layer_crs(self, layer, target_crs, external_tool_key="untraceable"):
        """Define o CRS da camada sem reprojetar (apenas muda a definição)."""
        pass

    def reproject_layer_to_crs(self, layer, target_crs, external_tool_key="untraceable"):
        """Reprojeta a camada para um CRS diferente, transformando todas as geometrias."""
        pass

    def validate_crs_compatibility(self, layer1, layer2, external_tool_key="untraceable"):
        """Verifica se duas camadas possuem CRS compatíveis ou próximos."""
        pass

    def get_layer_unit_type(self, layer, external_tool_key="untraceable"):
        """Obtém o tipo de unidade de medida do CRS da camada (metros, graus, etc)."""
        pass

    def convert_distance_unit(self, distance_value, from_unit, to_unit, external_tool_key="untraceable"):
        """Converte um valor de distância entre diferentes unidades de medida."""
        pass

    def convert_area_unit(self, area_value, from_unit, to_unit, external_tool_key="untraceable"):
        """Converte um valor de área entre diferentes unidades de medida."""
        pass

    def get_layer_extent_in_different_crs(self, layer, target_crs, external_tool_key="untraceable"):
        """Calcula a extensão da camada quando projetada em um CRS diferente."""
        pass

    def check_layer_is_geographic_crs(self, layer, external_tool_key="untraceable"):
        """Verifica se a camada usa sistema de coordenadas geográficas (lat/lon)."""
        pass

    def check_layer_is_projected_crs(self, layer, external_tool_key="untraceable"):
        """Verifica se a camada usa sistema de coordenadas projetado."""
        pass

    def get_crs_axis_order(self, crs, external_tool_key="untraceable"):
        """Obtém a ordem de eixos do CRS (XY ou YX)."""
        pass

    def list_common_crs_for_region(self, region_code, external_tool_key="untraceable"):
        """Lista os CRS mais comuns e apropriados para uma região geográfica."""
        pass
