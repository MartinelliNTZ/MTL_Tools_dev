import os
import re

# Lista de arquivos e classes
files_to_update = [
    ("utils/vector/VectorLayerSource.py", "VectorLayerSource"),
    ("utils/vector/VectorLayerProjection.py", "VectorLayerProjection"),
    ("utils/vector/VectorLayerGeometry.py", "VectorLayerGeometry"),
    ("utils/vector/VectorLayerMetrics.py", "VectorLayerMetrics"),
    ("utils/vector/VectorLayerAttributes.py", "VectorLayerAttributes"),
    ("utils/raster/RasterLayerSource.py", "RasterLayerSource"),
    ("utils/raster/RasterLayerProjection.py", "RasterLayerProjection"),
    ("utils/raster/RasterLayerProcessing.py", "RasterLayerProcessing"),
    ("utils/raster/RasterLayerMetrics.py", "RasterLayerMetrics"),
    ("utils/raster/RasterVectorBridge.py", "RasterVectorBridge"),
    ("utils/raster/RasterLayerRendering.py", "RasterLayerRendering"),
]

base_path = r"c:\Users\LINES-COLAB\AppData\Roaming\QGIS\QGIS3\profiles\mtl_msi\python\plugins\MTL_Tools"

for relative_path, class_name in files_to_update:
    file_path = os.path.join(base_path, relative_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Padrão para encontrar definições de método e adicionar o parâmetro
    # Procura por: def nome_metodo(self, ... ):
    # E adiciona: , external_tool_key="untraceable" antes de ):
    
    pattern = r'def (\w+)\(self,\s*(.*?)\s*\):'
    
    def replace_method_signature(match):
        method_name = match.group(1)
        params = match.group(2)
        
        # Se já tem external_tool_key, não faz nada
        if 'external_tool_key' in params:
            return match.group(0)
        
        # Se params está vazio, adiciona direto
        if not params or params.strip() == '':
            return f'def {method_name}(self, external_tool_key="untraceable"):'
        
        # Caso contrário, adiciona antes do fechamento
        return f'def {method_name}(self, {params}, external_tool_key="untraceable"):'
    
    # Aplicar a substituição
    updated_content = re.sub(pattern, replace_method_signature, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✓ Atualizado: {relative_path}")

print("\nTodas as classes foram atualizadas com external_tool_key=\"untraceable\"")
