# -*- coding: utf-8 -*-
from pathlib import Path
from qgis.core import (
            QgsVectorFileWriter,
            QgsProject,
            QgsVectorLayer,
            QgsCoordinateReferenceSystem,
            QgsCoordinateTransform,
            QgsFeature,
            QgsGeometry, 
            QgsPointXY,  
            QgsWkbTypes,
            QgsFeatureRequest,
            QgsField
        )
from qgis.core import (
    QgsVectorLayer,
    QgsVectorFileWriter,
    QgsProject,
    QgsCoordinateTransformContext
)
from pathlib import Path
import os
from typing import Optional
import processing


class VectorLayerAttributes:
    """
    Responsável por campos e atributos de camadas vetoriais.
    
    Escopo:
    - Gerenciar campos e estrutura de dados
    - Criar, remover, renomear campos
    - Validar dados de atributos
    - Calcular valores para campos
    - Ponte entre dados espaciais e tabulares
    
    Responsabilidade Principal:
    - Orquestrar operações de dados tabulares da camada
    - Garantir integridade estrutural de atributos
    - Facilitar acesso e modificação de dados tabulares
    
    NÃO é Responsabilidade:
    - Transformar geometrias (use VectorLayerGeometry)
    - Calcular métricas espaciais (use VectorLayerMetrics)
    - Reprojetar (use VectorLayerProjection)
    - Carregar ou salvar (use VectorLayerSource)
    """

    def get_layer_fields(self, layer, external_tool_key="untraceable"):
        """Retorna lista com todos os campos da camada e seus tipos."""
        pass

    @staticmethod
    def copy_attributes(
        target_layer,
        source_layer,
        field_names=None,
        conflict_resolver=None
    ):
        """
        Copia estrutura de atributos da camada source para target.

        conflict_resolver(field_name) -> "skip" | "rename" | "cancel"
        """

        if not target_layer.isEditable():
            target_layer.startEditing()

        for field in source_layer.fields():

            if field_names and field.name() not in field_names:
                continue

            idx = target_layer.fields().indexOf(field.name())

            # campo não existe
            if idx == -1:
                target_layer.addAttribute(QgsField(
                    field.name(),
                    field.type(),
                    field.typeName(),
                    field.length(),
                    field.precision()
                ))
                continue

            # conflito
            action = "skip"
            if conflict_resolver:
                action = conflict_resolver(field.name())

            if action == "cancel":
                return False

            if action == "rename":
                new_name = VectorLayerAttributes._generate_field_name(
                    target_layer, field.name()
                )
                target_layer.addAttribute(QgsField(
                    new_name,
                    field.type(),
                    field.typeName(),
                    field.length(),
                    field.precision()
                ))

        target_layer.updateFields()
        return True
    
    @staticmethod
    def _generate_field_name(layer, base):
        i = 1
        while layer.fields().indexOf(f"{base}_{i}") != -1:
            i += 1
        return f"{base}_{i}"



    def create_new_field(self, layer, field_name, field_type, field_width, external_tool_key="untraceable"):
        """Cria um novo campo na camada com tipo e tamanho especificados."""
        pass

    def delete_field(self, layer, field_name, external_tool_key="untraceable"):
        """Remove um campo da camada."""
        pass

    def rename_field(self, layer, old_field_name, new_field_name, external_tool_key="untraceable"):
        """Renomeia um campo existente na camada."""
        pass

    def get_field_values(self, layer, field_name, external_tool_key="untraceable"):
        """Obtém todos os valores únicos de um campo."""
        pass

    def calculate_field_statistics(self, layer, field_name, external_tool_key="untraceable"):
        """Calcula estatísticas (min, max, média, etc) para um campo numérico."""
        pass

    def validate_field_data_type(self, layer, field_name, expected_type, external_tool_key="untraceable"):
        """Verifica se os dados em um campo correspondem ao tipo esperado."""
        pass

    def update_field_values(self, layer, field_name, value_dict, external_tool_key="untraceable"):
        """Atualiza valores de um campo com base em um dicionário de mapeamento."""
        pass

    def check_for_duplicate_values(self, layer, field_name, external_tool_key="untraceable"):
        """Identifica valores duplicados em um campo."""
        pass

    def get_feature_attribute(self, feature, field_name, external_tool_key="untraceable"):
        """Obtém o valor de um atributo específico de uma feição."""
        pass

    def set_feature_attribute(self, feature, field_name, value, external_tool_key="untraceable"):
        """Define o valor de um atributo específico de uma feição."""
        pass

    def export_attributes_to_table(self, layer, output_path, external_tool_key="untraceable"):
        """Exporta todos os atributos da camada para um arquivo tabular."""
        pass
