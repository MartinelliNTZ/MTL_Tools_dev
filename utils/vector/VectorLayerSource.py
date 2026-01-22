class VectorLayerSource:
    """
    Responsável pela entrada, saída e origem de camadas vetoriais.
    
    Escopo:
    - Carregar camadas vetoriais de diferentes fontes
    - Salvar camadas em diferentes formatos
    - Validar integridade de camadas
    - Clonar camadas existentes
    - Gerenciar origem de dados (arquivo, banco, memória)
    
    Responsabilidade Principal:
    - Orquestrar operações de I/O de camadas vetoriais
    - Garantir que camadas sejam carregadas e salvas corretamente
    - Validar antes de operações críticas
    
    NÃO é Responsabilidade:
    - Reprojetar camadas (use VectorLayerProjection)
    - Calcular geometria ou métricas (use VectorLayerGeometry/VectorLayerMetrics)
    - Manipular atributos (use VectorLayerAttributes)
    - Renderizar ou exibir dados
    """

    def load_vector_layer_from_file(self, file_path, external_tool_key="untraceable"):
        """Carrega uma camada vetorial de um arquivo no disco."""
        pass

    def load_vector_layer_from_database(self, connection_string, layer_name, external_tool_key="untraceable"):
        """Carrega uma camada vetorial de um banco de dados."""
        pass

    def create_memory_layer(self, layer_name, geometry_type, crs, external_tool_key="untraceable"):
        """Cria uma camada vetorial em memória com geometria e CRS especificados."""
        pass

    def save_vector_layer_to_file(self, layer, output_path, file_format, external_tool_key="untraceable"):
        """Salva uma camada vetorial em arquivo com formato especificado."""
        pass

    def save_vector_layer_to_database(self, layer, connection_string, table_name, external_tool_key="untraceable"):
        """Salva uma camada vetorial em um banco de dados."""
        pass

    def clone_vector_layer(self, source_layer, include_features, external_tool_key="untraceable"):
        """Cria uma cópia exata de uma camada vetorial com ou sem feições."""
        pass

    def validate_layer_integrity(self, layer, external_tool_key="untraceable"):
        """Verifica se a camada está válida e íntegra para operações."""
        pass

    def get_layer_source_uri(self, layer, external_tool_key="untraceable"):
        """Obtém a URI ou caminho completo da origem da camada."""
        pass

    def check_file_format_compatibility(self, file_path, target_format, external_tool_key="untraceable"):
        """Verifica se o arquivo pode ser convertido para o formato desejado."""
        pass

    def reload_layer_from_source(self, layer, external_tool_key="untraceable"):
        """Recarrega a camada a partir de sua fonte original."""
        pass

    def export_layer_statistics(self, layer, output_path, external_tool_key="untraceable"):
        """Exporta estatísticas básicas da camada para arquivo de relatório."""
        pass

    def validate_geometry_before_save(self, layer, external_tool_key="untraceable"):
        """Valida geometrias da camada antes de salvar para evitar corrupção."""
        pass
