#!/usr/bin/env python3
"""
Sistema Relatorio Fotogrametrico Completo.
Execute: python main.py
Output: relatorio.html
"""

from core2 import range_metadata_manager, JSONUtil, IMGMetadata, AggregateAnalyzer, RenderEngine


def main():
    print("Iniciando Sistema Relatorio Fotogrametrico...")

    # 1. Config + ranges
    range_metadata_manager.load()

    # 2. Diagnostico (main orquestra direto)
    raw_records = JSONUtil.load_records("core2/json2.json")
    results = [IMGMetadata(record).score() for record in raw_records]
    mean = (sum(item.overall_score for item in results) / len(results)) if results else 0.0
    print(f"Analise completa: {len(results)} resultados, media overall {mean:.1f}")

    # 3. Agregados
    agg = AggregateAnalyzer.analyze(results)

    # 4. Charts/Map + Report
    renderer = RenderEngine()
    charts = renderer.generate_charts(agg)
    map_data = renderer.generate_map_data(results)
    html = renderer.render_report(results=results, agg=agg, charts=charts, map_data=map_data)
    renderer.save_report(html)

    print("Concluido! Abra relatorio.html")


if __name__ == '__main__':
    main()
