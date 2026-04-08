# ESTRUTURA_PROJETO.md

## 0) Mapa Rapido (Funcao de Cada Classe/Arquivo)
1. `main.py`: orquestra todo o pipeline (carrega config, processa imagens, agrega e renderiza).
2. `config.yaml`: define thresholds e mensagens de classificacao dos indicadores.
3. `core2/template.html`: estrutura visual do relatorio HTML final.
4. `core2/Field.py` (`Field`): estrutura base de um metacampo catalogado.
5. `core2/MetadataFields.py` (`MetadataFields`): catalogo central e unico dos metacampos (chaves, labels, atributos, descricao).
6. `core2/StringAdapter.py` (`StringAdapter`): utilitarios de normalizacao/listagem para metacampos.
7. `core2/JSONUtil.py` (`JSONUtil`): leitura de JSON e normalizacao de registros (json2 e legado).
8. `core2/RangeMetadataManager.py` (`RangeMetadataManager`): gerencia configuracao e classificacao de niveis (N1..N5).
9. `core2/IMGMetadata.py` (`IMGMetadata`): modelo principal de imagem com campos catalogados, score e serializacao.
10. `core2/AggregateAnalyzer.py` (`AggregateAnalyzer`): gera agregados, alertas, metricas avancadas e agrupamento por voo.
11. `core2/RenderEngine.py` (`RenderEngine`): monta charts/mapa, renderiza template e salva `relatorio.html`.
12. `core2/MetadataRecord.py` (`MetadataRecord`, `RecordFactory`): modelo auxiliar legado de registro; hoje fora do fluxo principal.
13. `core2/CustomPhotosFieldsUtil.py` (`CustomPhotosFieldsUtil`): utilitario de enriquecimento de campos custom no pipeline externo.
14. `core2/json2.json`: base de metadados usada como entrada no fluxo atual.

---

## 1) Fluxo Atual
1. `main.py` chama `range_metadata_manager.load()`.
2. `main.py` carrega registros com `JSONUtil.load_records(...)`.
3. Cada registro vira `IMGMetadata(record).score()`.
4. `AggregateAnalyzer.analyze(results)` consolida os resultados.
5. `RenderEngine` gera payload visual, renderiza e salva `relatorio.html`.

---

## 2) Estado de Simplificacao
- `MetadataFields` e a unica fonte de metacampos.
- Classificacao de ranges foi unificada em `RangeMetadataManager`.
- Scoring foi incorporado ao `IMGMetadata` (metodo `score()`).
- A orquestracao de diagnostico foi consolidada no `main.py`.

---

## 3) Arquivos Legacy (em branco, prontos para remocao)
- `core2/scoring.py`
- `core2/diagnostic_engine.py`
- `core2/diagnosis_result.py`
- `core2/config_manager.py`
- `core2/reference_ranges.py`
- `core2/loader.py`
- `core2/analytics.py`

---

## 4) Execucao
```bash
python main.py
```
Gera/atualiza `relatorio.html`.
