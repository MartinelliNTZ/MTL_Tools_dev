class Strings:
    
    {"img1":{"file":"G:\\np\\IMAGENS\\1_CERRADO (1).JPG","GPSMapDatum":"WGS-84","Software":"DJI GO 4"},
     "img2":{"file":"G:\\np\\IMAGENS\\2_CERRADO (1).JPG","GPSMapDatum":"WGS-84","Software":"DJI GO 4"}
     }
    REQUIRED_FIELDS = {
        "file": {
            "normalized": "file",
            "core": "os",
            "attribute": "File",
            "description": "",
        },
        "path": {
            "normalized": "path",
            "core": "os",
            "attribute": "Path",
            "description": "",
        },
        "format": {
            "normalized": "format",
            "core": "os",
            "attribute": "FormatMod",
            "description": "",
        },
        "size_mb": {
            "normalized": "size_mb",
            "core": "os",
            "attribute": "SizeMB",
            "description": "",
        },
        "GPSMapDatum": {
            "normalized": "EXIF:GPSInfo:GPSMapDatum",
            "core": "EXIF",
            "attribute": "GPSDatum",
            "description": "Datum da foto",
        },
        "Model": {
            "normalized": "EXIF:Model",
            "core": "EXIF",
            "attribute": "Model",
            "description": "Modelo da Camera",
        },
        "Software": {
            "normalized": "EXIF:Software",
            "core": "EXIF",
            "attribute": "Firmware",
            "description": "Versao do Firmware",
        },
        "XResolution": {
            "normalized": "EXIF:XResolution",
            "core": "EXIF",
            "attribute": "DPIWidth",
            "description": "Largura em DPI",
        },
        "YResolution": {
            "normalized": "EXIF:YResolution",
            "core": "EXIF",
            "attribute": "DPIHeight",
            "description": "Altura em DPI",
        },
        "ShutterSpeedValue": {
            "normalized": "EXIF:ShutterSpeedValue",
            "core": "EXIF",
            "attribute": "ShutterSp",
            "description": "Velocidade do Obturador",
        },
        "DateTimeOriginal": {
            "normalized": "EXIF:DateTimeOriginal",
            "core": "EXIF",
            "attribute": "DateTime",
            "description": "Data exata da foto no fuso horario",
        },
        "ApertureValue": {
            "normalized": "EXIF:ApertureValue",
            "core": "EXIF",
            "attribute": "ApertureV",
            "description": "Abertura da lente",
        },
        "MaxApertureValue": {
            "normalized": "EXIF:MaxApertureValue",
            "core": "EXIF",
            "attribute": "MaxApertV",
            "description": "Abertura maxima da lente",
        },
        "LightSource": {
            "normalized": "EXIF:LightSource",
            "core": "EXIF",
            "attribute": "LightSour",
            "description": "Luminosidade do dia",
        },
        "FocalLength": {
            "normalized": "EXIF:FocalLength",
            "core": "EXIF",
            "attribute": "FocalLeng",
            "description": "Distancia focal real da lente em milimetros",
        },
        "ExifImageWidth": {
            "normalized": "EXIF:ExifImageWidth",
            "core": "EXIF",
            "attribute": "WidthPX",
            "description": "Largura em pixels",
        },
        "ExifImageHeight": {
            "normalized": "EXIF:ExifImageHeight",
            "core": "EXIF",
            "attribute": "HeightPX",
            "description": "Altura em pixels",
        },
        "ExposureTime": {
            "normalized": "EXIF:ExposureTime",
            "core": "EXIF",
            "attribute": "ExpTime",
            "description": "Tempo de Exposicao",
        },
        "FNumber": {
            "normalized": "EXIF:FNumber",
            "core": "EXIF",
            "attribute": "FNumber",
            "description": "Numero da Abertura",
        },
        "ExposureProgram": {
            "normalized": "EXIF:ExposureProgram",
            "core": "EXIF",
            "attribute": "ExpProg",
            "description": "Programa de exposicao definido pelo drone",
        },
        "ISOSpeedRatings": {
            "normalized": "EXIF:ISOSpeedRatings",
            "core": "EXIF",
            "attribute": "ISOSpeed",
            "description": "Sensibilidade do sensor a luz",
        },
        "ExposureMode": {
            "normalized": "EXIF:ExposureMode",
            "core": "EXIF",
            "attribute": "ExpMode",
            "description": "Modo de exposicao utilizado pela camera",
        },
        "LensSpecification": {
            "normalized": "EXIF:LensSpecification",
            "core": "EXIF",
            "attribute": "Lens",
            "description": "(FocalLengthMin, FocalLengthMax, ApertureMin, ApertureMax)",
        },
        "DigitalZoomRatio": {
            "normalized": "EXIF:DigitalZoomRatio",
            "core": "EXIF",
            "attribute": "ZoomRatio",
            "description": "Zoom digital tem sempre que ta 0",
        },
        "GpsStatus": {
            "normalized": "EXIF:GPSInfo:GPSStatus",
            "core": "xmp_bloco_1",
            "attribute": "GpsStatus",
            "description": "Se RTK ou outro formato",
        },
        "AltitudeType": {
            "normalized": "xmp_bloco_1:drone-dji:AltitudeType",
            "core": "xmp_bloco_1",
            "attribute": "Ytype",
            "description": "Se RTK ou outro formato",
        },
        "GpsLatitude": {
            "normalized": "EXIF:GPSInfo:GPSLatitude",
            "core": "xmp_bloco_1",
            "attribute": "GpsLat",
            "description": "Latitude da aeronave",
        },
        "GpsLongitude": {
            "normalized": "EXIF:GPSInfo:GPSLongitude",
            "core": "xmp_bloco_1",
            "attribute": "GPSLong",
            "description": "Longitude da aeronave",
        },
        "AbsoluteAltitude": {
            "normalized": "xmp_bloco_1:drone-dji:AbsoluteAltitude",
            "core": "xmp_bloco_1",
            "attribute": "AbsY",
            "description": "Altitude absoluta da aeronave",
        },
        "RelativeAltitude": {
            "normalized": "xmp_bloco_1:drone-dji:RelativeAltitude",
            "core": "xmp_bloco_1",
            "attribute": "RelativeY",
            "description": "Altitude Relativa do ponto de decolagem",
        },
        "GimbalRollDegree": {
            "normalized": "xmp_bloco_1:drone-dji:GimbalRollDegree",
            "core": "xmp_bloco_1",
            "attribute": "GimbRoll",
            "description": "Rolagem do Gimbal(180 normal)(sim com acabeça)",
        },
        "GimbalYawDegree": {
            "normalized": "xmp_bloco_1:drone-dji:GimbalYawDegree",
            "core": "xmp_bloco_1",
            "attribute": "GimbYaw",
            "description": "Direcao do Gimbal",
        },
        "GimbalPitchDegree": {
            "normalized": "xmp_bloco_1:drone-dji:GimbalPitchDegree",
            "core": "xmp_bloco_1",
            "attribute": "GimbPitch",
            "description": "Inclinacao do Gimbal verticamente",
        },
        "FlightRollDegree": {
            "normalized": "xmp_bloco_1:drone-dji:FlightRollDegree",
            "core": "xmp_bloco_1",
            "attribute": "DroneRoll",
            "description": "Rolagem da aeronave",
        },
        "FlightYawDegree": {
            "normalized": "xmp_bloco_1:drone-dji:FlightYawDegree",
            "core": "xmp_bloco_1",
            "attribute": "DroneYaw",
            "description": "Direcao da aeronave",
        },
        "FlightPitchDegree": {
            "normalized": "xmp_bloco_1:drone-dji:FlightPitchDegree",
            "core": "xmp_bloco_1",
            "attribute": "DronePitc",
            "description": "Inclinacao da aeronave",
        },
        "FlightXSpeed": {
            "normalized": "xmp_bloco_1:drone-dji:FlightXSpeed",
            "core": "xmp_bloco_1",
            "attribute": "XSpeed",
            "description": "Velocidade de voo X",
        },
        "FlightYSpeed": {
            "normalized": "xmp_bloco_1:drone-dji:FlightYSpeed",
            "core": "xmp_bloco_1",
            "attribute": "YSpeed",
            "description": "Velocidade de voo Y",
        },
        "FlightZSpeed": {
            "normalized": "xmp_bloco_1:drone-dji:FlightZSpeed",
            "core": "xmp_bloco_1",
            "attribute": "ZSpeed",
            "description": "Velocidade de voo Z",
        },
        "RtkFlag": {
            "normalized": "xmp_bloco_1:drone-dji:RtkFlag",
            "core": "xmp_bloco_1",
            "attribute": "RtkFlag",
            "description": "Qualidade do sinal do drone",
        },
        "RtkStdLon": {
            "normalized": "xmp_bloco_1:drone-dji:RtkStdLon",
            "core": "xmp_bloco_1",
            "attribute": "RtkStdLon",
            "description": "Desvio Padrao do RTK Longitude",
        },
        "RtkStdLat": {
            "normalized": "xmp_bloco_1:drone-dji:RtkStdLat",
            "core": "xmp_bloco_1",
            "attribute": "RtkStdLat",
            "description": "Desvio Padrao do RTK Latitude",
        },
        "RtkStdHgt": {
            "normalized": "xmp_bloco_1:drone-dji:RtkStdHgt",
            "core": "xmp_bloco_1",
            "attribute": "RtkStdHgt",
            "description": "Desvio Padrao do RTK Altitude",
        },
        "RtkDiffAge": {
            "normalized": "xmp_bloco_1:drone-dji:RtkDiffAge",
            "core": "xmp_bloco_1",
            "attribute": "RtkDifAge",
            "description": "Tempo da Ultima correcao RTK",
        },
        "DewarpFlag": {
            "normalized": "xmp_bloco_1:drone-dji:DewarpFlag",
            "core": "xmp_bloco_1",
            "attribute": "Dewarp",
            "description": "Dewarp habilitado =0; desabilitado = nada",
        },
        "UTCAtExposure": {
            "normalized": "xmp_bloco_1:drone-dji:UTCAtExposure",
            "core": "xmp_bloco_1",
            "attribute": "UTCTime",
            "description": "Data e hora no GPS Time",
        },
        "ShutterCount": {
            "normalized": "xmp_bloco_1:drone-dji:ShutterCount",
            "core": "xmp_bloco_1",
            "attribute": "ShotCount",
            "description": "Numero Total de Fotos tiradas com a camera",
        },
        "FocusDistance": {
            "normalized": "xmp_bloco_1:drone-dji:FocusDistance",
            "core": "xmp_bloco_1",
            "attribute": "FocusDist",
            "description": "Distancia de foco",
        },
        "CameraSerialNumber": {
            "normalized": "xmp_bloco_1:drone-dji:CameraSerialNumber",
            "core": "xmp_bloco_1",
            "attribute": "CameraID",
            "description": "Numero Serial da Camera",
        },
        "DroneModel": {
            "normalized": "xmp_bloco_1:drone-dji:DroneModel",
            "core": "xmp_bloco_1",
            "attribute": "DronModel",
            "description": "Modelo do Drone",
        },
        "DroneSerialNumber": {
            "normalized": "xmp_bloco_1:drone-dji:DroneSerialNumber",
            "core": "xmp_bloco_1",
            "attribute": "DroneID",
            "description": "Numero Serial do Drone",
        },
        "CaptureUUID": {
            "normalized": "xmp_bloco_1:drone-dji:CaptureUUID",
            "core": "xmp_bloco_1",
            "attribute": "CaptureID",
            "description": "ID da captura para unir fotos Multespectral em drones M3M",
        },
        "PictureQuality": {
            "normalized": "xmp_bloco_1:drone-dji:PictureQuality",
            "core": "xmp_bloco_1",
            "attribute": "ImgQualit",
            "description": "Nivel de compressao da imagem",
        },
        "segmentos_total": {
            "normalized": "JPEG:segmentos_total",
            "core": "xmp_bloco_1",
            "attribute": "Segments",
            "description": "Numero de segmentos do JPG",
        },
        "SensorTemperature": {
            "normalized": "xmp_bloco_1:drone-dji:SensorTemperature",
            "core": "xmp_bloco_1",
            "attribute": "SensTemp",
            "description": "Temperatura do sensor",
        },
        "LRFStatus": {
            "normalized": "xmp_bloco_1:drone-dji:LRFStatus",
            "core": "xmp_bloco_1",
            "attribute": "LRFStatus",
            "description": "Status do Laser Range Finder",
        },
        "LRFTargetDistance": {
            "normalized": "xmp_bloco_1:drone-dji:LRFTargetDistance",
            "core": "xmp_bloco_1",
            "attribute": "LRFDist",
            "description": "Distancia do LRF(Laser Range Finder) ate o ponto central da foto no solo",
        },
        "LRFTargetLon": {
            "normalized": "xmp_bloco_1:drone-dji:LRFTargetLon",
            "core": "xmp_bloco_1",
            "attribute": "LRFLong",
            "description": "Longitude medida pelo LRF(Laser Range Finder)",
        },
        "LRFTargetLat": {
            "normalized": "xmp_bloco_1:drone-dji:LRFTargetLat",
            "core": "xmp_bloco_1",
            "attribute": "LRFLati",
            "description": "Latitude medida pelo LRF(Laser Range Finder)",
        },
        "LRFTargetAlt": {
            "normalized": "xmp_bloco_1:drone-dji:LRFTargetAlt",
            "core": "xmp_bloco_1",
            "attribute": "LRFY",
            "description": "Altitude Relativa do ponto de decolagem LRF(Laser Range Finder)",
        },
        "LRFTargetAbsAlt": {
            "normalized": "xmp_bloco_1:drone-dji:LRFTargetAbsAlt",
            "core": "xmp_bloco_1",
            "attribute": "LrfAbsAlt",
            "description": "Altitude Absoluta do ponto de decolagem LRF(Laser Range Finder)",
        },
        "WhiteBalanceCCT": {
            "normalized": "xmp_bloco_1:drone-dji:WhiteBalanceCCT",
            "core": "xmp_bloco_1",
            "attribute": "WhiteBlc",
            "description": "E um valor numerico que indica a cor da luz no ambiente onde a foto foi tirada, medida em Kelvin (K)",
        },
        "SensorFPS": {
            "normalized": "xmp_bloco_1:drone-dji:SensorFPS",
            "core": "xmp_bloco_1",
            "attribute": "SensorFPS",
            "description": "Taxa de quadros (frames por segundo)",
        },
        "RecommendedExposureIndex": {
            "normalized": "EXIF:RecommendedExposureIndex",
            "core": "xmp_bloco_1",
            "attribute": "REI",
            "description": "Indice de Exposicao Recomendado - REI",
        },
        "LensPosition": {
            "normalized": "xmp_bloco_1:drone-dji:LensPosition",
            "core": "xmp_bloco_1",
            "attribute": "LensPosit",
            "description": "Posicao da Lente",
        },
        "LensTemperature": {
            "normalized": "xmp_bloco_1:drone-dji:LensTemperature",
            "core": "xmp_bloco_1",
            "attribute": "LensTemp",
            "description": "Temperatura da Lente",
        },
    }
    
    
    CUSTOM_FIELDS = {
        "GimbalOffset": {
            "normalized": "xmp_bloco_1:drone-dji:GimbalOffset",
            "core": "Custom",
            "attribute": "GimOffset",
            "description": "Deslocamento do Gimbal em relaccao a aeronave (GimbalYawDegree - FlightYawDegree -180)"
        },
        "3DSpeed": {
            "normalized": "xmp_bloco_1:drone-dji:3DSpeed",
            "core": "Custom",
            "attribute": "3DSpeed",
            "description": "Velocidade total de deslocamento da aeronave calculada a partir das velocidades de voo X, Y e Z (FlightXSpeed, FlightYSpeed, FlightZSpeed)"
        }
    }
    
    DERIVED_INDIVIDUAL_FIELDS = {
    "tempo_desde_anterior": {
        "description": "Tempo decorrido (segundos) desde a foto anterior, calculado como diferença entre DateTimeOriginal da foto atual e da anterior. Indica a cadência de captura."
    },
    "distancia_geodesica_anterior": {
        "description": "Distância horizontal (metros) entre a posição GPS atual e a anterior, utilizando a fórmula de Haversine com as coordenadas (GPSLatitude, GPSLongitude)."
    },
    "distancia_3d_anterior": {
        "description": "Distância tridimensional (metros) entre a posição atual e a anterior, combinando a distância horizontal com a diferença de altitude (AbsoluteAltitude ou GPSAltitude)."
    },
    "velocidade_media_entre_fotos": {
        "description": "Velocidade média (m/s) no intervalo entre a foto anterior e a atual, calculada como distancia_3d_anterior / tempo_desde_anterior."
    },
    "velocidade_linear_instantanea": {
        "description": "Módulo da velocidade vetorial (m/s) fornecida pelos campos FlightXSpeed, FlightYSpeed, FlightZSpeed: sqrt(XSpeed² + YSpeed² + ZSpeed²)."
    },
    "direcao_deslocamento": {
        "description": "Azimute (graus) do deslocamento entre a posição anterior e a atual, medido a partir do norte verdadeiro. Indica a direção de movimento."
    },
    "angulo_de_incidencia": {
        "description": "Ângulo (graus) entre o eixo óptico da câmera e a vertical do terreno, combinando GimbalPitchDegree e FlightPitchDegree. Importante para fotogrametria."
    },
    "cobertura_estimada": {
        "description": "Tupla (largura_m, altura_m) estimada da área projetada no solo, baseada na altitude, campo de visão (derivado do modelo) e ângulo do gimbal."
    },
    "sobreposicao_prevista": {
        "description": "Percentual de sobreposição longitudinal com a imagem anterior, calculado como (1 - (distancia_geodesica_anterior / cobertura_estimada_largura)) * 100, limitado a [0,100]."
    },
    "precisao_rtk_efetiva": {
        "description": "Classificação textual da precisão RTK: 'Alta' (RtkFlag=50 e desvios < 0.02), 'Média' (desvios < 0.1), 'Baixa' (desvios >= 0.1), 'Sem RTK' (RtkFlag=0)."
    },
    "e_sobreposicao_ideal": {
        "description": "Booleano indicando se a sobreposição prevista é maior ou igual a um limiar (ex.: 60%). Útil para controle de qualidade do voo."
    },
    "flag_mudanca_brusca": {
        "description": "Booleano que sinaliza quando o tempo_desde_anterior ou a distancia_geodesica_anterior excede significativamente a mediana do conjunto (ex.: > 2× mediana)."
    },
    "velocidade_angular_gimbal": {
        "description": "Variação de GimbalYawDegree (graus por segundo) entre a imagem atual e a anterior, indicando se o gimbal estava girando durante a captura."
    },
    "potencial_de_ortoretificacao": {
        "description": "Score (0–100) que avalia a adequação da imagem para fotogrametria de alta precisão, combinando precisão RTK, angulo_de_incidencia, CalibratedFocalLength e DewarpFlag."
    }
}

"""
### Lista 2 – Informações do conjunto geral de dados

- **tempo_total_sequencia**: Duração total (segundos) desde a primeira até a última imagem da sequência (diferença entre DateTimeOriginal da última e da primeira).
- **integral_velocidade**: Distância total percorrida (metros) pelo drone durante toda a missão, obtida pela soma de `distancia_3d_anterior` para todas as imagens consecutivas.
- **taxa_de_obturacao**: Frequência média de captura (fotos por segundo) ao longo da sequência, calculada como (número de imagens) / tempo_total_sequencia.
- **sentido_de_voo**: Direção dominante do voo (ex.: “Norte”, “Sul”, “Nordeste”, etc.) determinada pela média dos azimutes de deslocamento (`direcao_deslocamento`).
- **altitude_relativa_media**: Média da `RelativeAltitude` (ou `AbsoluteAltitude` caso a relativa não exista) para todas as imagens, representando a altura média de voo.
- **variacao_rtk_entre_fotos**: Diferença média (ou máxima) dos desvios padrão RTK (`RtkStdLon`, `RtkStdLat`, `RtkStdHgt`) entre imagens consecutivas, indicando estabilidade da correção.
- **distribuicao_sobreposicao**: Estatísticas (mínimo, máximo, média, mediana, desvio padrão) da `sobreposicao_prevista` ao longo do conjunto, para avaliar a uniformidade da cobertura.
- **perfil_de_velocidade**: Estatísticas descritivas das velocidades (`velocidade_media_entre_fotos` e `velocidade_linear_instantanea`) – média, desvio, máximo – caracterizando o tipo de voo.
- **mapa_de_trajetoria**: Lista ordenada de coordenadas (latitude, longitude, altitude) de cada imagem, permitindo visualização do percurso completo em um mapa.
- **identificacao_de_passagens**: Detecção automática de padrões de ida e volta (linhas de voo), baseada na alternância da `direcao_deslocamento` (variação próxima a 180°).
- **falhas_ou_manobras**: Lista ou contagem de imagens onde `flag_mudanca_brusca` foi verdadeira, indicando possíveis pausas, mudanças abruptas ou falhas de comunicação.
- **percentual_de_imagens_adequadas**: Proporção de imagens com `potencial_de_ortoretificacao` acima de um limiar (ex.: > 80), útil para avaliar a qualidade geral do conjunto.
- **estimativa_de_area_coberta**: Área total aproximada (km² ou ha) varrida pelo conjunto, calculada pela união das `cobertura_estimada` de cada imagem, considerando sobreposição.
- **consistencia_de_metadados**: Percentual de imagens que possuem todos os campos críticos (GPS, atitude, RTK, etc.) preenchidos, indicando completude dos dados.
- **calibracao_do_conjunto**: Identificação se houve variação sistemática em parâmetros como `CalibratedFocalLength` ou `DewarpData` entre imagens, indicando possíveis mudanças de configuração durante o voo.
"""
    
"""
    ### 3. Novos campos derivados (informação calculada, não dados brutos)

Estes campos são computados a partir dos metadados existentes, considerando a sequência ordenada de imagens (por `DateTimeOriginal`). Eles transformam dados isolados em informação contextual.

- **tempo_desde_anterior** – intervalo em segundos entre a foto atual e a foto anterior (`DateTimeOriginal` atual – anterior). Útil para avaliar frequência de captura e sincronia.
- **distancia_geodesica_anterior** – distância em metros entre a posição GPS atual e a anterior, calculada pela fórmula de Haversine usando `GPSLatitude`, `GPSLongitude` e as altitudes (`AbsoluteAltitude` ou `GPSAltitude`). Indica o deslocamento entre pontos.
- **distancia_3d_anterior** – distância tridimensional entre a posição atual e a anterior, combinando a distância horizontal (haversine) com a diferença de altitude (`AbsoluteAltitude`). Mais realista para voos.
- **velocidade_linear_instantanea** – módulo da velocidade vetorial fornecida pelos campos `FlightXSpeed`, `FlightYSpeed`, `FlightZSpeed` (se presentes): `sqrt(XSpeed² + YSpeed² + ZSpeed²)` em m/s. Representa a velocidade total do drone no momento da captura.
- **velocidade_media_entre_fotos** – velocidade média (m/s) entre a foto anterior e a atual, calculada como `distancia_3d_anterior / tempo_desde_anterior`. Permite detectar variações de velocidade entre tomadas.
- **direcao_deslocamento** – azimute (graus) do deslocamento entre duas imagens consecutivas, derivado das coordenadas GPS. Útil para verificar se a trajetória segue um padrão (ex.: voo em linha reta).
- **angulo_de_incidencia** – ângulo entre o eixo óptico da câmera e a vertical do terreno, combinando `GimbalPitchDegree` e a inclinação do drone (`FlightPitchDegree`). Importante para análises fotogramétricas.
- **cobertura_estimada** – largura (m) e altura (m) da área capturada no solo, calculada a partir da altitude (`AbsoluteAltitude`), ângulo de gimbal, campo de visão da câmera (derivado do modelo) e formato do sensor. Permite avaliar sobreposição de imagens.
- **sobreposicao_prevista** – percentual de sobreposição longitudinal com a imagem anterior, baseada na distância percorrida e na cobertura estimada. Essencial para qualidade de ortomosaico.
- **tempo_desde_inicio_voo** – tempo decorrido desde a primeira imagem da sequência (ou desde o início do voo, se houver registro). Ajuda a sincronizar eventos.
- **precisao_rtk_efetiva** – classificação da precisão baseada nos campos `RtkFlag`, `RtkStdLon`, `RtkStdLat`, `RtkStdHgt` e `RtkDiffAge`. Exemplo: “Alta (cm)”, “Média (dm)”, “Baixa (m)”, “Sem RTK”.
- **variacao_rtk_entre_fotos** – diferença nos valores de `RtkStdLon` (ou similares) entre imagens consecutivas, indicando se a qualidade da correção se manteve estável.
- **altitude_relativa_media** – média da `RelativeAltitude` (se disponível) em uma janela de imagens, para estimar altura de voo em relação ao ponto de decolagem.
- **taxa_de_obturacao** – número de fotos por segundo no conjunto (frequência média), útil para identificar modo burst ou intervalo programado.
- **sentido_de_voo** – direção geral do voo (ex.: “Norte”, “Sul”, etc.) baseada na média dos azimutes de deslocamento.
- **integral_velocidade** – distância total percorrida pelo drone durante a missão (soma das `distancia_3d_anterior`), em metros.
- **tempo_total_sequencia** – duração total desde a primeira até a última imagem (segundos).
- **flag_mudanca_brusca** – indicador booleano que alerta quando `tempo_desde_anterior` > 2× média ou `distancia_geodesica_anterior` > 2× mediana, sinalizando possíveis falhas ou manobras não programadas.
- **e_sobreposicao_ideal** – booleano baseado na `sobreposicao_prevista` comparada com um limiar (ex.: > 60% para longitudinal), útil para controle de qualidade.
- **velocidade_angular_gimbal** – derivada da variação de `GimbalYawDegree` entre imagens consecutivas (graus/s), para verificar se o gimbal estava estável ou em movimento.
- **potencial_de_ortoretificacao** – score (0–100) que combina precisão RTK, ângulo de gimbal, distância focal calibrada (`CalibratedFocalLength`) e presença de dados de dewarp (`DewarpFlag`), indicando se a imagem é adequada para processamento fotogramétrico de alta precisão.
    """
    
