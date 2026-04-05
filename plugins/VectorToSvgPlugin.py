# -*- coding: utf-8 -*-
import os
import re
from xml.sax.saxutils import escape

from qgis.PyQt.QtGui import QColor
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsFeature,
    QgsGeometry,
    QgsMapLayerProxyModel,
    QgsPointXY,
    QgsProject,
    QgsRenderContext,
    QgsSymbol,
    QgsVectorLayer,
    QgsWkbTypes,
)

from .BasePlugin import BasePluginMTL
from ..core.ui.WidgetFactory import WidgetFactory
from ..i18n.TranslationManager import STR
from ..utils.Preferences import load_tool_prefs, save_tool_prefs
from ..utils.ProjectUtils import ProjectUtils
from ..utils.QgisMessageUtil import QgisMessageUtil
from ..utils.ToolKeys import ToolKey
from ..utils.vector.VectorLayerAttributes import VectorLayerAttributes
from ..utils.vector.VectorLayerGeometry import VectorLayerGeometry


class VectorToSvgPlugin(BasePluginMTL):
    TOOL_KEY = ToolKey.VECTOR_TO_SVG
    SVG_SIZE = 2048
    MARGIN = 48
    DEFAULT_STROKE_COLOR = "#202020"
    DEFAULT_FILL_COLOR = "#4c78a8"
    DEFAULT_POINT_RADIUS = 5.0
    DEFAULT_LINE_WIDTH = 2.0
    DEFAULT_POLYGON_STROKE_WIDTH = 1.2

    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface
        self.init(
            tool_key=self.TOOL_KEY,
            class_name=self.__class__.__name__,
            load_settings_prefs=False,
            build_ui=True,
        )

    def _build_ui(self, **kwargs):
        super()._build_ui(
            title="Conversor de Vetor para SVG",
            icon_path="cadmus_icon.ico",
            enable_scroll=False,
        )

        layer_layout, self.layer_input = WidgetFactory.create_layer_input(
            "Camada Vetorial",
            QgsMapLayerProxyModel.VectorLayer,
            allow_empty=False,
            enable_selected_checkbox=True,
            parent=self,
            separator_top=False,
            separator_bottom=True,
        )

        fill_layout, self.fill_color_widget = WidgetFactory.create_color_button(
            title="Cor Fundo",
            initial_color=QColor("#ffffff"),
            tooltip="Selecione a cor de preenchimento",
            parent=self,
            separator_top=False,
            separator_bottom=False,
        )

        border_layout, self.border_color_widget = WidgetFactory.create_color_button(
            title="Cor Borda",
            initial_color=QColor("#000000"),
            tooltip="Selecione a cor da borda",
            parent=self,
            separator_top=False,
            separator_bottom=False,
        )

        label_layout, self.label_color_widget = WidgetFactory.create_color_button(
            title="Cor Rotulo",
            initial_color=QColor("#000000"),
            tooltip="Selecione a cor do rotulo",
            parent=self,
            separator_top=False,
            separator_bottom=True,
        )

        options = {
            "transparent_background": "Fundo transparente",
            "show_border": "Mostrar Borda",
            "show_label": "Mostrar Rotulo",
            "for_each_feature": "Gerar SVG para cada feicao",
        }
        options_layout, self.options_map = WidgetFactory.create_checkbox_grid(
            options,
            items_per_row=1,
            checked_by_default=False,
            title=None,
            separator_top=False,
            separator_bottom=True,
        )

        buttons_layout, self.action_buttons = (
            WidgetFactory.create_bottom_action_buttons(
                parent=self,
                run_callback=self.execute_tool,
                close_callback=self.close,
                info_callback=self.show_info_dialog,
                tool_key=self.TOOL_KEY,
            )
        )
        folder_layout, self.folder_selector = WidgetFactory.create_path_selector(
            parent=self,
            title=STR.OUTPUT_FOLDER,
            mode="folder",
            separator_top=False,
            separator_bottom=False,
        )
        self.logger.debug("Path selector de pasta de saida criado")

        btn_project_layout, self.btn_project = WidgetFactory.create_simple_button(
            text=STR.USE_PROJECT_FOLDER,
            parent=self,
        )
        self.btn_project.clicked.connect(self._set_folder_to_project)
        self.logger.debug("Botao 'Usar pasta do projeto' criado")

        self.layout.add_items(
            [
                layer_layout,
                fill_layout,
                border_layout,
                label_layout,
                options_layout,
                folder_layout,
                btn_project_layout,
                buttons_layout,
            ]
        )

    def _load_prefs(self):
        self.logger.debug("Carregando preferencias do VectorToSvg")
        self.preferences = load_tool_prefs(self.TOOL_KEY)

        self.fill_color_widget.set_color(
            QColor(self.preferences.get("fill_color", "#ffffff"))
        )
        self.border_color_widget.set_color(
            QColor(self.preferences.get("border_color", "#000000"))
        )
        self.label_color_widget.set_color(
            QColor(self.preferences.get("label_color", "#000000"))
        )

        self.options_map["transparent_background"].setChecked(
            self.preferences.get("transparent_background", False)
        )
        self.options_map["show_border"].setChecked(
            self.preferences.get("show_border", False)
        )
        self.options_map["show_label"].setChecked(
            self.preferences.get("show_label", False)
        )
        self.options_map["for_each_feature"].setChecked(
            self.preferences.get("for_each_feature", False)
        )

        project_folder = ProjectUtils.get_project_dir(
            ProjectUtils.get_project_instance()
        )
        default_folder = os.path.join(project_folder, "svgs")
        output_folder = self.preferences.get("output_folder", default_folder)
        self.folder_selector.set_paths([output_folder])

    def _save_prefs(self):
        self.logger.debug("Salvando preferencias do VectorToSvg")

        self.preferences["fill_color"] = self.fill_color_widget.get_color().name(
            QColor.HexArgb
        )
        self.preferences["border_color"] = self.border_color_widget.get_color().name(
            QColor.HexArgb
        )
        self.preferences["label_color"] = self.label_color_widget.get_color().name(
            QColor.HexArgb
        )
        self.preferences["transparent_background"] = self.options_map[
            "transparent_background"
        ].isChecked()
        self.preferences["show_border"] = self.options_map["show_border"].isChecked()
        self.preferences["show_label"] = self.options_map["show_label"].isChecked()
        self.preferences["for_each_feature"] = self.options_map[
            "for_each_feature"
        ].isChecked()

        paths = self.folder_selector.get_paths()
        project_folder = ProjectUtils.get_project_dir(
            ProjectUtils.get_project_instance()
        )
        self.preferences["output_folder"] = (
            paths[0] if paths else os.path.join(project_folder, "svgs")
        )

        self.preferences["window_width"] = self.width()
        self.preferences["window_height"] = self.height()

        save_tool_prefs(self.TOOL_KEY, self.preferences)

    def execute_tool(self):
        self.logger.info("Iniciando exportacao de SVG a partir de camada vetorial")
        layer = ProjectUtils.get_active_vector_layer(
            self.layer_input.current_layer(), self.logger
        )
        self.start_stats(layer)

        if not layer:
            QgisMessageUtil.bar_critical(self.iface, "Selecione uma camada vetorial.")
            return

        if not VectorLayerAttributes.ensure_has_features(layer, self.logger):
            QgisMessageUtil.bar_warning(self.iface, "A camada nao possui feicoes.")
            return

        output_folder = self._resolve_output_folder()
        if not output_folder:
            return

        only_selected = self.layer_input.only_selected_enabled()
        export_layer = self._resolve_export_layer(layer, only_selected)
        if not export_layer:
            return

        features = self._collect_features(export_layer)
        if not features:
            QgisMessageUtil.bar_warning(
                self.iface, "Nenhuma feicao valida foi encontrada para exportacao."
            )
            return

        style = self._build_style()
        for_each_feature = self.options_map["for_each_feature"].isChecked()

        try:
            if for_each_feature:
                generated = self._export_one_svg_per_feature(
                    layer, features, output_folder, style
                )
            else:
                generated = [
                    self._export_single_svg(layer, features, output_folder, style)
                ]
        except Exception as e:
            self.logger.error(f"Erro ao gerar SVG: {e}")
            QgisMessageUtil.modal_error(self.iface, f"Erro ao gerar SVG:\n{e}")
            return

        if not generated:
            QgisMessageUtil.bar_warning(
                self.iface, "Nenhum SVG foi gerado a partir da camada selecionada."
            )
            return

        self.finish_stats(input_obj=export_layer)
        message = f"{len(generated)} SVG(s) gerado(s) com sucesso."
        self.logger.info(message)
        QgisMessageUtil.modal_result_with_folder(
            self.iface,
            "Exportacao concluida",
            message,
            output_folder,
            parent=self,
        )

    def _resolve_output_folder(self):
        paths = self.folder_selector.get_paths()
        output_folder = paths[0].strip() if paths else ""

        if not output_folder:
            QgisMessageUtil.bar_warning(self.iface, "Selecione a pasta de saida.")
            return None

        try:
            os.makedirs(output_folder, exist_ok=True)
            self.logger.debug(f"Pasta de saida garantida: {output_folder}")
            return output_folder
        except Exception as e:
            self.logger.error(f"Erro ao preparar pasta de saida '{output_folder}': {e}")
            QgisMessageUtil.modal_error(
                self.iface, f"Nao foi possivel criar/acessar a pasta de saida.\n{e}"
            )
            return None

    def _resolve_export_layer(self, layer, only_selected):
        if not only_selected:
            self.logger.debug(
                f"Exportando todas as feicoes da camada '{layer.name()}'."
            )
            return layer

        self.logger.debug(
            f"Opcao somente feicoes selecionadas ativa. Total selecionadas: {layer.selectedFeatureCount()}"
        )
        selected_layer, error = VectorLayerGeometry.get_selected_features(
            layer, tool_key=self.TOOL_KEY
        )
        if error:
            self.logger.warning(f"Falha ao obter feicoes selecionadas: {error}")
            QgisMessageUtil.modal_error(self.iface, error)
            return None

        return selected_layer

    def _collect_features(self, layer):
        prepared = []
        wgs84 = QgsCoordinateReferenceSystem("EPSG:4326")
        transform = None

        if layer.crs().isValid() and layer.crs() != wgs84:
            try:
                transform = QgsCoordinateTransform(
                    layer.crs(),
                    wgs84,
                    QgsProject.instance().transformContext(),
                )
            except Exception as e:
                self.logger.warning(
                    f"Falha ao preparar transformacao para WGS84. Sera usado o CRS original. Erro: {e}"
                )
                transform = None

        for feature in layer.getFeatures():
            geometry = feature.geometry()
            if not geometry or geometry.isEmpty():
                continue

            geometry = QgsGeometry(geometry)
            if transform is not None:
                try:
                    geometry.transform(transform)
                except Exception as e:
                    self.logger.warning(
                        f"Falha ao reprojetar feicao {feature.id()} para WGS84: {e}"
                    )
                    continue

            prepared.append({"feature": QgsFeature(feature), "geometry": geometry})

        self.logger.debug(f"Feicoes preparadas para exportacao: {len(prepared)}")
        return prepared

    def _build_style(self):
        return {
            "background_color": self.fill_color_widget.get_color().name(QColor.HexRgb),
            "border_color": self.border_color_widget.get_color().name(QColor.HexRgb),
            "label_color": self.label_color_widget.get_color().name(QColor.HexRgb),
            "transparent_background": self.options_map[
                "transparent_background"
            ].isChecked(),
            "show_border": self.options_map["show_border"].isChecked(),
            "show_label": self.options_map["show_label"].isChecked(),
        }

    def _export_single_svg(self, layer, features, output_folder, style):
        base_name = self._sanitize_filename(layer.name())
        output_path = self._unique_svg_path(output_folder, base_name)
        label_text = layer.name()
        svg_content = self._build_svg_document(layer, features, label_text, style)
        self._write_svg(output_path, svg_content)
        self.logger.info(f"SVG unico gerado: {output_path}")
        return output_path

    def _export_one_svg_per_feature(self, layer, features, output_folder, style):
        generated = []
        for index, item in enumerate(features, start=1):
            feature = item["feature"]
            base_name = self._feature_output_base_name(layer, feature, index)
            output_path = self._unique_svg_path(output_folder, base_name)
            label_text = self._feature_label(layer, feature, index)
            svg_content = self._build_svg_document(layer, [item], label_text, style)
            self._write_svg(output_path, svg_content)
            generated.append(output_path)
            self.logger.debug(f"SVG por feicao gerado: {output_path}")
        return generated

    def _build_svg_document(self, layer, features, label_text, style):
        bounds = self._combined_bounds(features)
        min_x, min_y, max_x, max_y = bounds
        width = max(max_x - min_x, 1e-9)
        height = max(max_y - min_y, 1e-9)
        draw_size = self.SVG_SIZE - 2 * self.MARGIN
        scale = min(draw_size / width, draw_size / height)
        offset_x = min_x - (draw_size - width * scale) / (2 * scale)
        offset_y = min_y - (draw_size - height * scale) / (2 * scale)

        svg = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            (
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.SVG_SIZE}" '
                f'height="{self.SVG_SIZE}" viewBox="0 0 {self.SVG_SIZE} {self.SVG_SIZE}">'
            ),
        ]
        svg.append(self._background_svg(style))
        if style["show_border"]:
            svg.append(self._border_svg(style))

        svg.append('  <g id="features">')
        render_context = QgsRenderContext()
        for item in features:
            feature = item["feature"]
            geometry = item["geometry"]
            symbol_style = self._symbol_style_for_feature(
                layer, feature, geometry, render_context
            )
            elements = self._geometry_to_svg_elements(
                geometry, offset_x, offset_y, scale, symbol_style
            )
            svg.extend(f"    {element}" for element in elements)
        svg.append("  </g>")

        if style["show_label"]:
            svg.append(self._label_svg(label_text, style))

        svg.append("</svg>")
        return "\n".join(svg)

    def _background_svg(self, style):
        if style["transparent_background"]:
            return (
                f'  <rect width="{self.SVG_SIZE}" height="{self.SVG_SIZE}" '
                'fill="none"/>'
            )
        return (
            f'  <rect width="{self.SVG_SIZE}" height="{self.SVG_SIZE}" '
            f'fill="{style["background_color"]}"/>'
        )

    def _border_svg(self, style):
        return (
            f'  <rect x="8" y="8" width="{self.SVG_SIZE - 16}" '
            f'height="{self.SVG_SIZE - 16}" fill="none" '
            f'stroke="{style["border_color"]}" stroke-width="1.5" rx="6"/>'
        )

    def _label_svg(self, label_text, style):
        escaped = escape(label_text or "")
        return (
            f'  <text x="{self.SVG_SIZE // 2}" y="{self.SVG_SIZE - 16}" '
            f'font-family="monospace" font-size="14" '
            f'fill="{style["label_color"]}" text-anchor="middle">{escaped}</text>'
        )

    def _combined_bounds(self, features):
        min_x = None
        min_y = None
        max_x = None
        max_y = None

        for item in features:
            bbox = item["geometry"].boundingBox()
            if min_x is None:
                min_x = bbox.xMinimum()
                min_y = bbox.yMinimum()
                max_x = bbox.xMaximum()
                max_y = bbox.yMaximum()
                continue

            min_x = min(min_x, bbox.xMinimum())
            min_y = min(min_y, bbox.yMinimum())
            max_x = max(max_x, bbox.xMaximum())
            max_y = max(max_y, bbox.yMaximum())

        return min_x, min_y, max_x, max_y

    def _geometry_to_svg_elements(
        self, geometry, offset_x, offset_y, scale, symbol_style
    ):
        wkb_type = QgsWkbTypes.flatType(geometry.wkbType())
        if wkb_type == QgsWkbTypes.GeometryCollection:
            elements = []
            for sub_geometry in geometry.asGeometryCollection():
                elements.extend(
                    self._geometry_to_svg_elements(
                        sub_geometry, offset_x, offset_y, scale, symbol_style
                    )
                )
            return elements

        if wkb_type == QgsWkbTypes.Point:
            return [
                self._point_svg(
                    geometry.asPoint(), offset_x, offset_y, scale, symbol_style
                )
            ]
        if wkb_type == QgsWkbTypes.MultiPoint:
            return [
                self._point_svg(point, offset_x, offset_y, scale, symbol_style)
                for point in geometry.asMultiPoint()
            ]
        if wkb_type == QgsWkbTypes.LineString:
            return [
                self._line_svg(
                    geometry.asPolyline(), offset_x, offset_y, scale, symbol_style
                )
            ]
        if wkb_type == QgsWkbTypes.MultiLineString:
            return [
                self._line_svg(line, offset_x, offset_y, scale, symbol_style)
                for line in geometry.asMultiPolyline()
            ]
        if wkb_type == QgsWkbTypes.Polygon:
            return [
                self._polygon_svg(
                    geometry.asPolygon(), offset_x, offset_y, scale, symbol_style
                )
            ]
        if wkb_type == QgsWkbTypes.MultiPolygon:
            return [
                self._polygon_svg(polygon, offset_x, offset_y, scale, symbol_style)
                for polygon in geometry.asMultiPolygon()
            ]
        return []

    def _polygon_svg(self, polygon, offset_x, offset_y, scale, symbol_style):
        path_parts = []
        for ring in polygon:
            path_parts.append(
                self._ring_to_path(ring, offset_x, offset_y, scale, close=True)
            )
        path_data = "".join(path_parts)
        return (
            f'<path d="{path_data}" fill="{symbol_style["fill"]}" '
            'fill-rule="evenodd" '
            f'fill-opacity="{symbol_style["fill_opacity"]:.3f}" '
            f'stroke="{symbol_style["stroke"]}" '
            f'stroke-width="{symbol_style["stroke_width"]:.3f}" '
            f'stroke-opacity="{symbol_style["stroke_opacity"]:.3f}" '
            'stroke-linejoin="round"/>'
        )

    def _line_svg(self, line, offset_x, offset_y, scale, symbol_style):
        path_data = self._ring_to_path(line, offset_x, offset_y, scale, close=False)
        return (
            f'<path d="{path_data}" fill="none" '
            f'stroke="{symbol_style["stroke"]}" '
            f'stroke-width="{symbol_style["stroke_width"]:.3f}" '
            f'stroke-opacity="{symbol_style["stroke_opacity"]:.3f}" '
            'stroke-linecap="round" stroke-linejoin="round"/>'
        )

    def _point_svg(self, point, offset_x, offset_y, scale, symbol_style):
        pixel_x, pixel_y = self._to_svg_xy(point, offset_x, offset_y, scale)
        return (
            f'<circle cx="{pixel_x:.3f}" cy="{pixel_y:.3f}" '
            f'r="{symbol_style["point_radius"]:.3f}" '
            f'fill="{symbol_style["fill"]}" '
            f'fill-opacity="{symbol_style["fill_opacity"]:.3f}" '
            f'stroke="{symbol_style["stroke"]}" '
            f'stroke-width="{symbol_style["stroke_width"]:.3f}" '
            f'stroke-opacity="{symbol_style["stroke_opacity"]:.3f}"/>'
        )

    def _ring_to_path(self, ring, offset_x, offset_y, scale, close):
        commands = []
        for index, point in enumerate(ring):
            svg_x, svg_y = self._to_svg_xy(point, offset_x, offset_y, scale)
            prefix = "M" if index == 0 else "L"
            commands.append(f"{prefix}{svg_x:.3f},{svg_y:.3f}")
        if close and commands:
            commands.append("Z")
        return "".join(commands)

    def _to_svg_xy(self, point, offset_x, offset_y, scale):
        if isinstance(point, QgsPointXY):
            x_value = point.x()
            y_value = point.y()
        else:
            x_value = point.x()
            y_value = point.y()

        pixel_x = (x_value - offset_x) * scale + self.MARGIN
        pixel_y = self.SVG_SIZE - self.MARGIN - (y_value - offset_y) * scale
        return pixel_x, pixel_y

    def _symbol_style_for_feature(self, layer, feature, geometry, render_context):
        symbol = None
        renderer = layer.renderer()
        if renderer is not None:
            try:
                if hasattr(renderer, "startRender"):
                    renderer.startRender(render_context, layer.fields())
                if hasattr(renderer, "symbolForFeature"):
                    symbol = renderer.symbolForFeature(feature, render_context)
                elif hasattr(renderer, "symbol"):
                    symbol = renderer.symbol()
            except Exception as e:
                self.logger.warning(
                    f"Falha ao obter simbolo da feicao {feature.id()}: {e}"
                )
            finally:
                try:
                    if hasattr(renderer, "stopRender"):
                        renderer.stopRender(render_context)
                except Exception as e:
                    self.logger.warning(f"Falha ao finalizar render context: {e}")

        if symbol is None:
            symbol = QgsSymbol.defaultSymbol(layer.geometryType())

        if symbol is None:
            return self._default_symbol_style(geometry)

        fill_color = self._qcolor_to_svg(getattr(symbol, "color", lambda: None)())
        opacity = float(getattr(symbol, "opacity", lambda: 1.0)() or 1.0)
        stroke_color = fill_color or self.DEFAULT_STROKE_COLOR
        stroke_opacity = opacity
        stroke_width = self.DEFAULT_LINE_WIDTH
        point_radius = self.DEFAULT_POINT_RADIUS

        try:
            symbol_layer = (
                symbol.symbolLayer(0) if symbol.symbolLayerCount() > 0 else None
            )
        except Exception:
            symbol_layer = None

        if symbol_layer is not None:
            stroke_candidate = self._extract_symbol_color(
                symbol_layer,
                ("strokeColor", "outlineColor", "borderColor", "color"),
            )
            if stroke_candidate:
                stroke_color = stroke_candidate

            stroke_width = self._extract_symbol_number(
                symbol_layer,
                ("strokeWidth", "outlineWidth", "width", "borderWidth"),
                stroke_width,
            )
            point_radius = (
                self._extract_symbol_number(
                    symbol_layer,
                    ("size", "radius", "width"),
                    point_radius * 2.0,
                )
                / 2.0
            )

            fill_candidate = self._extract_symbol_color(
                symbol_layer,
                ("fillColor", "color"),
            )
            if fill_candidate:
                fill_color = fill_candidate

        if geometry.type() == QgsWkbTypes.PointGeometry:
            stroke_width = max(stroke_width, 0.5)
            point_radius = max(point_radius, 1.0)
        elif geometry.type() == QgsWkbTypes.LineGeometry:
            fill_color = "none"
            stroke_width = max(stroke_width, 0.5)
        else:
            stroke_width = max(stroke_width, 0.5)
            if fill_color in (None, "", "none"):
                fill_color = self.DEFAULT_FILL_COLOR

        return {
            "fill": fill_color or self.DEFAULT_FILL_COLOR,
            "fill_opacity": opacity if fill_color != "none" else 0.0,
            "stroke": stroke_color or self.DEFAULT_STROKE_COLOR,
            "stroke_width": stroke_width,
            "stroke_opacity": stroke_opacity,
            "point_radius": point_radius,
        }

    def _default_symbol_style(self, geometry):
        if geometry.type() == QgsWkbTypes.PointGeometry:
            return {
                "fill": self.DEFAULT_FILL_COLOR,
                "fill_opacity": 1.0,
                "stroke": self.DEFAULT_STROKE_COLOR,
                "stroke_width": 1.0,
                "stroke_opacity": 1.0,
                "point_radius": self.DEFAULT_POINT_RADIUS,
            }
        if geometry.type() == QgsWkbTypes.LineGeometry:
            return {
                "fill": "none",
                "fill_opacity": 0.0,
                "stroke": self.DEFAULT_STROKE_COLOR,
                "stroke_width": self.DEFAULT_LINE_WIDTH,
                "stroke_opacity": 1.0,
                "point_radius": self.DEFAULT_POINT_RADIUS,
            }
        return {
            "fill": self.DEFAULT_FILL_COLOR,
            "fill_opacity": 0.8,
            "stroke": self.DEFAULT_STROKE_COLOR,
            "stroke_width": self.DEFAULT_POLYGON_STROKE_WIDTH,
            "stroke_opacity": 1.0,
            "point_radius": self.DEFAULT_POINT_RADIUS,
        }

    def _extract_symbol_color(self, symbol_layer, method_names):
        for method_name in method_names:
            method = getattr(symbol_layer, method_name, None)
            if callable(method):
                try:
                    return self._qcolor_to_svg(method())
                except Exception:
                    continue
        return None

    def _extract_symbol_number(self, symbol_layer, method_names, fallback):
        for method_name in method_names:
            method = getattr(symbol_layer, method_name, None)
            if callable(method):
                try:
                    value = float(method())
                    if value > 0:
                        return value
                except Exception:
                    continue
        return fallback

    def _qcolor_to_svg(self, value):
        if isinstance(value, QColor) and value.isValid():
            return value.name(QColor.HexRgb)
        return None

    def _feature_output_base_name(self, layer, feature, index):
        field_index = feature.fields().lookupField("Name")
        if field_index != -1:
            value = feature.attribute(field_index)
            if value is not None and str(value).strip():
                return self._sanitize_filename(str(value).strip())

        return self._sanitize_filename(f"{layer.name()}_{index}")

    def _feature_label(self, layer, feature, index):
        field_index = feature.fields().lookupField("Name")
        if field_index != -1:
            value = feature.attribute(field_index)
            if value is not None and str(value).strip():
                return str(value).strip()
        return f"{layer.name()}_{index}"

    def _sanitize_filename(self, value):
        sanitized = re.sub(r'[<>:"/\\|?*]+', "_", str(value or "").strip())
        sanitized = re.sub(r"\s+", "_", sanitized)
        sanitized = re.sub(r"_+", "_", sanitized).strip("._")
        return sanitized or "svg"

    def _unique_svg_path(self, output_folder, base_name):
        candidate = os.path.join(output_folder, f"{base_name}.svg")
        counter = 1
        while os.path.exists(candidate):
            candidate = os.path.join(output_folder, f"{base_name}_{counter}.svg")
            counter += 1
        return candidate

    def _write_svg(self, output_path, svg_content):
        with open(output_path, "w", encoding="utf-8") as stream:
            stream.write(svg_content)

    def _set_folder_to_project(self):
        self.logger.debug("Definindo pasta para pasta do projeto")
        project_folder = ProjectUtils.get_project_dir(
            ProjectUtils.get_project_instance()
        )
        export_folder = os.path.join(project_folder, "svgs")
        self.folder_selector.set_paths([export_folder])
        self.logger.debug(f"Pasta definida para: {export_folder}")


def run(iface):
    dlg = VectorToSvgPlugin(iface)
    dlg.setModal(False)
    dlg.show()
    return dlg
