


class ToolKey:
    # plugins/
    MTL_TOOLS_PLUGIN  = "mtl_tools_plugin"
    EXPORT_ALL_LAYOUTS = "export_all_layouts"
    DRONE_COORDINATES = "drone_coordinates"
    LOAD_FOLDER_LAYERS = "load_folder_layers"
    REPLACE_IN_LAYOUTS = "replace_in_layouts"
    RESTART_QGIS = "restart_qgis"
    GERAR_RASTRO_IMPLEMENTO = "gerar_rastro_implemento"
    COORD_CLICK_TOOL = "coord_click_tool"    
    BASE_TOOL = "base_tool"
    COPY_ATTRIBUTES = "copy_attributes"

    # model3 / panel tool
    # processing/
    ATTRIBUTE_STATISTICS = "attribute_statistics"
    DIFFERENCE_FIELDS = "difference_fields_algorithm"
    MY_ALGORITHM = "my_algorithm"
    PROVIDER = "provider"
    RASTER_MASS_SAMPLER = "raster_mass_sampler"
    ELEVATION_ANALISYS = "elevation_analisys"

    # Cores por tool_key (toolbar-first, semântica)
    TOOL_KEY_COLORS = {
        # === Toolbar / ações principais ===
        MTL_TOOLS_PLUGIN: "#804E0A",  # laranja claro → plugin principal
        EXPORT_ALL_LAYOUTS: "#4ECDC4",  # turquesa → exportação / layout
        DRONE_COORDINATES: "#45B7D1",  # azul → coordenadas / espacial
        LOAD_FOLDER_LAYERS: "#96CEB4",  # verde → carga de dados
        REPLACE_IN_LAYOUTS: "#F8C471",  # laranja → alteração / replace
        RESTART_QGIS: "#FF6B6B",  # vermelho → ação crítica
        GERAR_RASTRO_IMPLEMENTO: "#82E0AA",  # verde limão → geração geométrica
        COORD_CLICK_TOOL: "#85C1E9",  # azul céu → map tool
        BASE_TOOL: "#AED6F1",  # azul gelo → base / neutro
        COPY_ATTRIBUTES: "#DDA0DD",  # plum → dados / atributos

        # === Processing / análises ===
        ATTRIBUTE_STATISTICS: "#F7DC6F",  # amarelo → estatística
        DIFFERENCE_FIELDS: "#BB8FCE",  # roxo → comparação
        MY_ALGORITHM: "#98D8C8",  # verde água → genérico
        PROVIDER: "#BFC9CA",  # cinza → infraestrutura
        RASTER_MASS_SAMPLER: "#F1948A",  # coral → raster pesado
        ELEVATION_ANALISYS: "#5DADE2",  # azul médio → relevo
    }


