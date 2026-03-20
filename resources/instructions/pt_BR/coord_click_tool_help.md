# Obter Coordenadas (CoordClickTool)

Descrição
---------
Ferramenta que permite obter coordenadas de um ponto no mapa com conversão para WGS84/UTM, altimetria aproximada (OpenTopoData) e tentativa de geocodificação reversa (endereço via serviços OSM).

Como usar
---------
1. Abra o plugin Cadmus e selecione a ferramenta "Obter Coordenadas" (ou o atalho/entrada correspondente).
2. Clique no mapa no local desejado.
3. Será aberto um diálogo com:
   - Coordenadas em WGS84 (decimal e DMS)
   - Coordenadas UTM (Easting/Northing) e zona
   - Altitude aproximada (pode demorar dependendo da conexão)
   - Endereço (se disponível)
4. Use os botões para copiar a localização completa ou copiar partes do endereço.

Comportamento assíncrono
------------------------
- Geocodificação reversa e consulta de altimetria são executadas de forma assíncrona para não bloquear a UI.
- O diálogo abre imediatamente com coordenadas; os campos de altitude/endereço serão preenchidos quando as tasks terminarem.

Mensagens e logs
----------------
- Se a geocodificação ou altimetria estiverem indisponíveis, os campos mostrarão "Carregando..." ou "Indisponível".
- Verifique os logs do plugin (LogUtils) para mensagens de erro detalhadas.

Permissões e requisitos
-----------------------
- A ferramenta requer conexão com internet para resolver endereço e buscar altimetria.
- Não altera camadas do projeto; apenas lê coordenadas e manipula o diálogo.

Soluções rápidas para problemas
------------------------------
- Diálogo não abre: verifique se há erros no log e se o plugin está inicializado corretamente.
- Endereço não aparece: verifique conexão de rede e possíveis bloqueios de API.
- Altitude não aparece: serviço de altimetria pode estar indisponível ou houve erro de rede.

Notas de implementação
----------------------
- A ferramenta usa `AsyncPipelineEngine` com `ReverseGeocodeStep` e `AltimetryStep` executando em paralelo.
- Se houver falha na pipeline, há um fallback que agenda tasks individuais.

Contato / Suporte
-----------------
Abra uma issue no repositório com o log do plugin e passos para reproduzir o problema.
