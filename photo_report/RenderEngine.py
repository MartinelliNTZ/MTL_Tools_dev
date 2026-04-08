from math import cos, sin, pi
from typing import Any, Dict, List

import jinja2


class RenderEngine:
    """Render HTML + charts + mapa."""

    def __init__(self):
        """Inicializa ambiente Jinja2 e carrega o template principal do relatorio."""
        loader = jinja2.FileSystemLoader("core2")
        self.env = jinja2.Environment(
            loader=loader,
            autoescape=jinja2.select_autoescape(["html", "xml"]),
        )
        self.template = self.env.get_template("template.html")

    @staticmethod
    def generate_charts(agg_data: Dict[str, Any]) -> Dict[str, Any]:
        """Monta payload de graficos consumido pelo template (Chart.js)."""
        charts: Dict[str, Any] = {}

        dist = agg_data.get("level_distribution", {})
        total = sum(dist.values())
        labels = ["Critical (1)", "Poor (2)", "OK (3)", "Good (4)", "Excellent (5)"]
        if total == 0:
            pie_data = [0, 0, 0, 0, 0]
        else:
            pie_data = [round(dist.get(i, 0) / total * 100, 2) for i in range(1, 6)]

        charts["level_pie"] = {
            "type": "pie",
            "labels": labels,
            "data": pie_data,
            "title": "Level Distribution (%)",
        }

        ind_means = {k: v["mean"] for k, v in agg_data.get("per_indicator", {}).items()}
        bar_labels = list(ind_means.keys())[:10]
        charts["indicator_bar"] = {
            "type": "bar",
            "labels": bar_labels,
            "data": [ind_means[k] for k in bar_labels],
            "title": "Average Level per Indicator",
        }

        return charts

    @staticmethod
    def generate_map_data(results: List[Any]) -> Dict[str, Any]:
        """Gera snippet Leaflet com marcadores sinteticos para visualizacao no relatorio."""
        markers = []
        center_lat, center_lon = -10.217, -48.359

        for i, result in enumerate(results):
            angle = (2 * pi * i) / max(len(results), 1)
            radius = 0.00015 + (i % 7) * 0.00003
            lat = center_lat + cos(angle) * radius
            lon = center_lon + sin(angle) * radius
            popup = (
                f"<b>{result.filename}</b><br>"
                f"Score: {result.overall_score}<br>"
                f"GSD nivel: {result.levels.get('gsd_cm', '?')}"
            )
            markers.append({"lat": lat, "lon": lon, "popup": popup})

        leaflet_lines = [
            '<div id="map" style="height:220px;border-radius:8px"></div>',
            '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>',
            '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>',
            "<script>",
            f'var map = L.map("map").setView([{center_lat}, {center_lon}], 18);',
            'L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {maxZoom: 21}).addTo(map);',
        ]

        for marker in markers:
            leaflet_lines.append(
                f'L.marker([{marker["lat"]}, {marker["lon"]}]).addTo(map).bindPopup(`{marker["popup"]}`);'
            )

        leaflet_lines.append("</script>")

        return {
            "leaflet_snippet": "".join(leaflet_lines),
            "markers_count": len(markers),
        }

    def render_report(
        self,
        *,
        results: List[Any],
        agg: Dict[str, Any],
        charts: Dict[str, Any],
        map_data: Dict[str, Any],
    ) -> str:
        """Renderiza o HTML final do relatorio com dados agregados e detalhes por imagem."""
        total_images = len(results)
        mean_overall = agg.get("mean_overall", 0)
        per_indicator = agg.get("per_indicator", {})

        return self.template.render(
            results=results,
            agg=agg,
            charts=charts,
            map_snippet=map_data.get("leaflet_snippet", ""),
            total_images=total_images,
            mean_overall=mean_overall,
            per_indicator=per_indicator,
        )

    @staticmethod
    def save_report(html: str, output_path: str = "relatorio.html") -> None:
        """Salva o HTML renderizado no caminho de saida definido."""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Relatorio salvo: {output_path}")
