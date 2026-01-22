class VectorLayerGeometry:
    """
    Responsável pelas transformações geométricas de camadas vetoriais.
    
    Escopo:
    - Aplicar operações geométricas (buffer, dissolve, merge, explode)
    - Transformar geometrias (simplificar, suavizar, validar)
    - Operações topológicas (union, intersection, difference)
    - Alterar estrutura geométrica das feições
    - Converter entre tipos de geometria
    
    Responsabilidade Principal:
    - Orquestrar transformações que ALTERAM as geometrias
    - Garantir validade após transformações
    - Manter coerência topológica
    
    NÃO é Responsabilidade:
    - Ler ou calcular métricas (use VectorLayerMetrics)
    - Reprojetar (use VectorLayerProjection)
    - Manipular atributos (use VectorLayerAttributes)
    - Carregar ou salvar (use VectorLayerSource)
    """

    def create_buffer_geometry(self, layer, distance, segments, external_tool_key="untraceable"):
        """Cria buffer ao redor das geometrias com distância e número de segmentos especificados."""
        pass

    def dissolve_geometries_by_attribute(self, layer, dissolve_field, external_tool_key="untraceable"):
        """Dissolve geometrias agrupadas por um atributo específico."""
        pass

    def merge_geometries(self, geometries_list, external_tool_key="untraceable"):
        """Combina múltiplas geometrias em uma única geometria multipart."""
        pass

    def explode_multipart_features(self, layer, external_tool_key="untraceable"):
        """Divide feições multipart em múltiplas feições simples."""
        pass

    def simplify_geometry(self, layer, tolerance, external_tool_key="untraceable"):
        """Simplifica geometrias reduzindo vértices mantendo forma geral."""
        pass

    def smooth_geometry(self, layer, smoothing_iterations, external_tool_key="untraceable"):
        """Suaviza geometrias através de algoritmo iterativo."""
        pass

    def validate_geometry(self, geometry, external_tool_key="untraceable"):
        """Verifica se uma geometria é válida e sem problemas topológicos."""
        pass

    def fix_invalid_geometry(self, geometry, external_tool_key="untraceable"):
        """Tenta corrigir automaticamente uma geometria inválida."""
        pass

    def get_geometry_intersection(self, geometry1, geometry2, external_tool_key="untraceable"):
        """Calcula a interseção entre duas geometrias."""
        pass

    def get_geometry_union(self, geometry1, geometry2, external_tool_key="untraceable"):
        """Calcula a união entre duas geometrias."""
        pass

    def get_geometry_difference(self, geometry1, geometry2, external_tool_key="untraceable"):
        """Calcula a diferença entre duas geometrias."""
        pass

    def convert_geometry_type(self, layer, target_type, external_tool_key="untraceable"):
        """Converte geometrias para um tipo diferente quando possível."""
        pass
