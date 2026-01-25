from ...resources.widget.LayerInputWidget import LayerInputWidget


class WidgetFactory:

    @staticmethod
    def create_layer_input(
            label_text,
            filters,
            *,
            allow_empty=True,
            enable_selected_checkbox=True,
            parent=None
    ) -> LayerInputWidget:
        """current_layer() -> QgsMapLayer | None
            only_selected_enabled() -> bool
            set_layer(layer)
            """

        widget = LayerInputWidget(
            label_text=label_text,
            filters=filters,
            allow_empty=allow_empty,
            enable_selected_checkbox=enable_selected_checkbox,
            parent=parent
        )

        # estilo centralizado (opcional)
        # LayerInputStyles.apply(widget)

        return widget
