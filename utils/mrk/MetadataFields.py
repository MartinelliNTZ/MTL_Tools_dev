# -*- coding: utf-8 -*-

from typing import Dict, Iterable, List, Optional

from ...core.model.Field import Field
from ..adapter.StringAdapter import StringAdapter


class MetadataFields:
    REQUIRED_FIELDS = {
        "file": Field(
            normalized="file",
            core="os",
            label="File",
            attribute="File",
            description="Nome do arquivo de imagem. [File]",
            level=3,
        ),
        "path": Field(
            normalized="path",
            core="os",
            label="Path",
            attribute="Path",
            description="Caminho completo do arquivo de imagem. [Path]",
            level=3,
        ),
        "format": Field(
            normalized="format",
            core="os",
            label="Format",
            attribute="FormatMod",
            description="Formato e modo de cor da imagem. [FormatMod]",
            level=3,
        ),
        "size_mb": Field(
            normalized="size_mb",
            core="os",
            label="Size MB",
            attribute="SizeMB",
            description="Tamanho do arquivo em megabytes. [SizeMB]",
            level=3,
        ),
        "GPSMapDatum": Field(
            normalized="EXIF:GPSInfo:GPSMapDatum",
            core="EXIF",
            label="GPS Map Datum",
            attribute="GPSDatum",
            description="Datum geodesico usado nas coordenadas GPS. [GPSDatum]",
            level=3,
        ),
        "Model": Field(
            normalized="EXIF:Model",
            core="EXIF",
            label="Model",
            attribute="Model",
            description="Modelo da camera que capturou a imagem. [Model]",
            level=3,
        ),
        "Software": Field(
            normalized="EXIF:Software",
            core="EXIF",
            label="Software",
            attribute="Firmware",
            description="Software ou firmware gravado no metadado. [Firmware]",
            level=3,
        ),
        "XResolution": Field(
            normalized="EXIF:XResolution",
            core="EXIF",
            label="X Resolution",
            attribute="DPIWidth",
            description="Resolucao horizontal informada no EXIF (DPI). [DPIWidth]",
            level=3,
        ),
        "YResolution": Field(
            normalized="EXIF:YResolution",
            core="EXIF",
            label="Y Resolution",
            attribute="DPIHeight",
            description="Resolucao vertical informada no EXIF (DPI). [DPIHeight]",
            level=3,
        ),
        "ShutterSpeedValue": Field(
            normalized="EXIF:ShutterSpeedValue",
            core="EXIF",
            label="Shutter Speed Value",
            attribute="ShutterSp",
            description="Velocidade do obturador registrada no EXIF. [ShutterSp]",
            level=3,
        ),
        "DateTimeOriginal": Field(
            normalized="EXIF:DateTimeOriginal",
            core="EXIF",
            label="Date Time Original",
            attribute="DateTime",
            description="Data e hora original da captura. [DateTime]",
            level=3,
        ),
        "ApertureValue": Field(
            normalized="EXIF:ApertureValue",
            core="EXIF",
            label="Aperture Value",
            attribute="ApertureV",
            description="Valor de abertura usado na captura. [ApertureV]",
            level=3,
        ),
        "MaxApertureValue": Field(
            normalized="EXIF:MaxApertureValue",
            core="EXIF",
            label="Max Aperture Value",
            attribute="MaxApertV",
            description="Maior abertura disponivel da lente. [MaxApertV]",
            level=3,
        ),
        "LightSource": Field(
            normalized="EXIF:LightSource",
            core="EXIF",
            label="Light Source",
            attribute="LightSour",
            description="Codigo da fonte de iluminacao da cena. [LightSour]",
            level=3,
        ),
        "FocalLength": Field(
            normalized="EXIF:FocalLength",
            core="EXIF",
            label="Focal Length",
            attribute="FocalLeng",
            description="Distancia focal da lente em mm. [FocalLeng]",
            level=3,
        ),
        "ExifImageWidth": Field(
            normalized="EXIF:ExifImageWidth",
            core="EXIF",
            label="EXIF Image Width",
            attribute="WidthPX",
            description="Largura da imagem em pixels (EXIF). [WidthPX]",
            level=3,
        ),
        "ExifImageHeight": Field(
            normalized="EXIF:ExifImageHeight",
            core="EXIF",
            label="EXIF Image Height",
            attribute="HeightPX",
            description="Altura da imagem em pixels (EXIF). [HeightPX]",
            level=3,
        ),
        "ExposureTime": Field(
            normalized="EXIF:ExposureTime",
            core="EXIF",
            label="Exposure Time",
            attribute="ExpTime",
            description="Tempo de exposicao da foto em segundos. [ExpTime]",
            level=3,
        ),
        "FNumber": Field(
            normalized="EXIF:FNumber",
            core="EXIF",
            label="F Number",
            attribute="FNumber",
            description="Numero f usado na captura. [FNumber]",
            level=3,
        ),
        "ExposureProgram": Field(
            normalized="EXIF:ExposureProgram",
            core="EXIF",
            label="Exposure Program",
            attribute="ExpProg",
            description="Programa de exposicao selecionado pela camera. [ExpProg]",
            level=3,
        ),
        "ISOSpeedRatings": Field(
            normalized="EXIF:ISOSpeedRatings",
            core="EXIF",
            label="ISO Speed Ratings",
            attribute="ISOSpeed",
            description="Sensibilidade ISO usada na captura. [ISOSpeed]",
            level=3,
        ),
        "ExposureMode": Field(
            normalized="EXIF:ExposureMode",
            core="EXIF",
            label="Exposure Mode",
            attribute="ExpMode",
            description="Modo de exposicao configurado na camera. [ExpMode]",
            level=3,
        ),
        "LensSpecification": Field(
            normalized="EXIF:LensSpecification",
            core="EXIF",
            label="Lens Specification",
            attribute="Lens",
            description="Faixa focal e de abertura da lente. [Lens]",
            level=3,
        ),
        "DigitalZoomRatio": Field(
            normalized="EXIF:DigitalZoomRatio",
            core="EXIF",
            label="Digital Zoom Ratio",
            attribute="ZoomRatio",
            description="Razao de zoom digital aplicada na captura. [ZoomRatio]",
            level=3,
        ),
        "GpsStatus": Field(
            normalized="EXIF:GPSInfo:GPSStatus",
            core="xmp_bloco_1",
            label="GPS Status",
            attribute="GpsStatus",
            description="Status do GPS no momento da foto. [GpsStatus]",
            level=3,
        ),
        "AltitudeType": Field(
            normalized="xmp_bloco_1:drone-dji:AltitudeType",
            core="xmp_bloco_1",
            label="Altitude Type",
            attribute="Ytype",
            description="Tipo de altitude registrado pelo drone. [Ytype]",
            level=3,
        ),
        "GpsLatitude": Field(
            normalized="EXIF:GPSInfo:GPSLatitude",
            core="xmp_bloco_1",
            label="GPS Latitude",
            attribute="GpsLat",
            description="Latitude GPS da aeronave na captura. [GpsLat]",
            level=3,
        ),
        "GpsLongitude": Field(
            normalized="EXIF:GPSInfo:GPSLongitude",
            core="xmp_bloco_1",
            label="GPS Longitude",
            attribute="GPSLong",
            description="Longitude GPS da aeronave na captura. [GPSLong]",
            level=3,
        ),
        "AbsoluteAltitude": Field(
            normalized="xmp_bloco_1:drone-dji:AbsoluteAltitude",
            core="xmp_bloco_1",
            label="Absolute Altitude",
            attribute="AbsY",
            description="Altitude absoluta da aeronave. [AbsY]",
            level=3,
        ),
        "RelativeAltitude": Field(
            normalized="xmp_bloco_1:drone-dji:RelativeAltitude",
            core="xmp_bloco_1",
            label="Relative Altitude",
            attribute="RelativeY",
            description="Altitude relativa ao ponto de decolagem. [RelativeY]",
            level=3,
        ),
        "GimbalRollDegree": Field(
            normalized="xmp_bloco_1:drone-dji:GimbalRollDegree",
            core="xmp_bloco_1",
            label="Gimbal Roll Degree",
            attribute="GimbRoll",
            description="Angulo de rolagem do gimbal em graus. [GimbRoll]",
            level=3,
        ),
        "GimbalYawDegree": Field(
            normalized="xmp_bloco_1:drone-dji:GimbalYawDegree",
            core="xmp_bloco_1",
            label="Gimbal Yaw Degree",
            attribute="GimbYaw",
            description="Angulo de yaw do gimbal em graus. [GimbYaw]",
            level=3,
        ),
        "GimbalPitchDegree": Field(
            normalized="xmp_bloco_1:drone-dji:GimbalPitchDegree",
            core="xmp_bloco_1",
            label="Gimbal Pitch Degree",
            attribute="GimbPitch",
            description="Angulo de pitch do gimbal em graus. [GimbPitch]",
            level=3,
        ),
        "FlightRollDegree": Field(
            normalized="xmp_bloco_1:drone-dji:FlightRollDegree",
            core="xmp_bloco_1",
            label="Flight Roll Degree",
            attribute="DroneRoll",
            description="Angulo de rolagem da aeronave em graus. [DroneRoll]",
            level=3,
        ),
        "FlightYawDegree": Field(
            normalized="xmp_bloco_1:drone-dji:FlightYawDegree",
            core="xmp_bloco_1",
            label="Flight Yaw Degree",
            attribute="DroneYaw",
            description="Angulo de yaw da aeronave em graus. [DroneYaw]",
            level=3,
        ),
        "FlightPitchDegree": Field(
            normalized="xmp_bloco_1:drone-dji:FlightPitchDegree",
            core="xmp_bloco_1",
            label="Flight Pitch Degree",
            attribute="DronePitc",
            description="Angulo de pitch da aeronave em graus. [DronePitc]",
            level=3,
        ),
        "FlightXSpeed": Field(
            normalized="xmp_bloco_1:drone-dji:FlightXSpeed",
            core="xmp_bloco_1",
            label="Flight X Speed",
            attribute="XSpeed",
            description="Velocidade da aeronave no eixo X. [XSpeed]",
            level=3,
        ),
        "FlightYSpeed": Field(
            normalized="xmp_bloco_1:drone-dji:FlightYSpeed",
            core="xmp_bloco_1",
            label="Flight Y Speed",
            attribute="YSpeed",
            description="Velocidade da aeronave no eixo Y. [YSpeed]",
            level=3,
        ),
        "FlightZSpeed": Field(
            normalized="xmp_bloco_1:drone-dji:FlightZSpeed",
            core="xmp_bloco_1",
            label="Flight Z Speed",
            attribute="ZSpeed",
            description="Velocidade da aeronave no eixo Z. [ZSpeed]",
            level=3,
        ),
        "RtkFlag": Field(
            normalized="xmp_bloco_1:drone-dji:RtkFlag",
            core="xmp_bloco_1",
            label="RTK Flag",
            attribute="RtkFlag",
            description="Indicador de qualidade/correcao RTK. [RtkFlag]",
            level=3,
        ),
        "RtkStdLon": Field(
            normalized="xmp_bloco_1:drone-dji:RtkStdLon",
            core="xmp_bloco_1",
            label="RTK Std Lon",
            attribute="RtkStdLon",
            description="Desvio padrao RTK na longitude. [RtkStdLon]",
            level=3,
        ),
        "RtkStdLat": Field(
            normalized="xmp_bloco_1:drone-dji:RtkStdLat",
            core="xmp_bloco_1",
            label="RTK Std Lat",
            attribute="RtkStdLat",
            description="Desvio padrao RTK na latitude. [RtkStdLat]",
            level=3,
        ),
        "RtkStdHgt": Field(
            normalized="xmp_bloco_1:drone-dji:RtkStdHgt",
            core="xmp_bloco_1",
            label="RTK Std Hgt",
            attribute="RtkStdHgt",
            description="Desvio padrao RTK na altitude. [RtkStdHgt]",
            level=3,
        ),
        "RtkDiffAge": Field(
            normalized="xmp_bloco_1:drone-dji:RtkDiffAge",
            core="xmp_bloco_1",
            label="RTK Diff Age",
            attribute="RtkDifAge",
            description="Tempo desde a ultima correcao RTK. [RtkDifAge]",
            level=3,
        ),
        "DewarpFlag": Field(
            normalized="xmp_bloco_1:drone-dji:DewarpFlag",
            core="xmp_bloco_1",
            label="Dewarp Flag",
            attribute="Dewarp",
            description="Estado da correcao de distorcao (dewarp). [Dewarp]",
            level=3,
        ),
        "UTCAtExposure": Field(
            normalized="xmp_bloco_1:drone-dji:UTCAtExposure",
            core="xmp_bloco_1",
            label="UTC At Exposure",
            attribute="UTCTime",
            description="Horario UTC exato do momento da exposicao. [UTCTime]",
            level=3,
        ),
        "ShutterCount": Field(
            normalized="xmp_bloco_1:drone-dji:ShutterCount",
            core="xmp_bloco_1",
            label="Shutter Count",
            attribute="ShotCount",
            description="Total de disparos acumulados da camera. [ShotCount]",
            level=3,
        ),
        "FocusDistance": Field(
            normalized="xmp_bloco_1:drone-dji:FocusDistance",
            core="xmp_bloco_1",
            label="Focus Distance",
            attribute="FocusDist",
            description="Distancia de foco usada na captura. [FocusDist]",
            level=3,
        ),
        "CameraSerialNumber": Field(
            normalized="xmp_bloco_1:drone-dji:CameraSerialNumber",
            core="xmp_bloco_1",
            label="Camera Serial Number",
            attribute="CameraID",
            description="Numero serial da camera. [CameraID]",
            level=3,
        ),
        "DroneModel": Field(
            normalized="xmp_bloco_1:drone-dji:DroneModel",
            core="xmp_bloco_1",
            label="Drone Model",
            attribute="DronModel",
            description="Modelo da aeronave/drone. [DronModel]",
            level=3,
        ),
        "DroneSerialNumber": Field(
            normalized="xmp_bloco_1:drone-dji:DroneSerialNumber",
            core="xmp_bloco_1",
            label="Drone Serial Number",
            attribute="DroneID",
            description="Numero serial da aeronave/drone. [DroneID]",
            level=3,
        ),
        "CaptureUUID": Field(
            normalized="xmp_bloco_1:drone-dji:CaptureUUID",
            core="xmp_bloco_1",
            label="Capture UUID",
            attribute="CaptureID",
            description="Identificador unico do conjunto de captura. [CaptureID]",
            level=3,
        ),
        "PictureQuality": Field(
            normalized="xmp_bloco_1:drone-dji:PictureQuality",
            core="xmp_bloco_1",
            label="Picture Quality",
            attribute="ImgQualit",
            description="Nivel de qualidade/compressao da imagem. [ImgQualit]",
            level=3,
        ),
        "segmentos_total": Field(
            normalized="JPEG:segmentos_total",
            core="xmp_bloco_1",
            label="Segmentos Total",
            attribute="Segments",
            description="Quantidade total de segmentos JPEG lidos. [Segments]",
            level=3,
        ),
        "SensorTemperature": Field(
            normalized="xmp_bloco_1:drone-dji:SensorTemperature",
            core="xmp_bloco_1",
            label="Sensor Temperature",
            attribute="SensTemp",
            description="Temperatura do sensor da camera. [SensTemp]",
            level=3,
        ),
        "LRFStatus": Field(
            normalized="xmp_bloco_1:drone-dji:LRFStatus",
            core="xmp_bloco_1",
            label="LRF Status",
            attribute="LRFStatus",
            description="Status do laser range finder (LRF). [LRFStatus]",
            level=3,
        ),
        "LRFTargetDistance": Field(
            normalized="xmp_bloco_1:drone-dji:LRFTargetDistance",
            core="xmp_bloco_1",
            label="LRF Target Distance",
            attribute="LRFDist",
            description="Distancia medida pelo LRF ate o alvo central. [LRFDist]",
            level=3,
        ),
        "LRFTargetLon": Field(
            normalized="xmp_bloco_1:drone-dji:LRFTargetLon",
            core="xmp_bloco_1",
            label="LRF Target Lon",
            attribute="LRFLong",
            description="Longitude do alvo medida pelo LRF. [LRFLong]",
            level=3,
        ),
        "LRFTargetLat": Field(
            normalized="xmp_bloco_1:drone-dji:LRFTargetLat",
            core="xmp_bloco_1",
            label="LRF Target Lat",
            attribute="LRFLati",
            description="Latitude do alvo medida pelo LRF. [LRFLati]",
            level=3,
        ),
        "LRFTargetAlt": Field(
            normalized="xmp_bloco_1:drone-dji:LRFTargetAlt",
            core="xmp_bloco_1",
            label="LRF Target Alt",
            attribute="LRFY",
            description="Altitude relativa do alvo medida pelo LRF. [LRFY]",
            level=3,
        ),
        "LRFTargetAbsAlt": Field(
            normalized="xmp_bloco_1:drone-dji:LRFTargetAbsAlt",
            core="xmp_bloco_1",
            label="LRF Target Abs Alt",
            attribute="LrfAbsAlt",
            description="Altitude absoluta do alvo medida pelo LRF. [LrfAbsAlt]",
            level=3,
        ),
        "WhiteBalanceCCT": Field(
            normalized="xmp_bloco_1:drone-dji:WhiteBalanceCCT",
            core="xmp_bloco_1",
            label="White Balance CCT",
            attribute="WhiteBlc",
            description="Temperatura de cor (Kelvin) no balanco de branco. [WhiteBlc]",
            level=3,
        ),
        "SensorFPS": Field(
            normalized="xmp_bloco_1:drone-dji:SensorFPS",
            core="xmp_bloco_1",
            label="Sensor FPS",
            attribute="SensorFPS",
            description="Taxa de amostragem do sensor em FPS. [SensorFPS]",
            level=3,
        ),
        "RecommendedExposureIndex": Field(
            normalized="EXIF:RecommendedExposureIndex",
            core="xmp_bloco_1",
            label="Recommended Exposure Index",
            attribute="REI",
            description="Indice de exposicao recomendado (REI). [REI]",
            level=3,
        ),
        "LensPosition": Field(
            normalized="xmp_bloco_1:drone-dji:LensPosition",
            core="xmp_bloco_1",
            label="Lens Position",
            attribute="LensPosit",
            description="Posicao da lente no momento da captura. [LensPosit]",
            level=3,
        ),
        "LensTemperature": Field(
            normalized="xmp_bloco_1:drone-dji:LensTemperature",
            core="xmp_bloco_1",
            label="Lens Temperature",
            attribute="LensTemp",
            description="Temperatura da lente no momento da captura. [LensTemp]",
            level=3,
        ),
    }

    CUSTOM_FIELDS = {
        "FileType": Field(
            normalized="Custom:FileType",
            core="custom",
            label="File Type",
            attribute="FileType",
            description="Tipo/Extensao do arquivo de imagem (ex.: .JPG). [FileType]",
            level=5,
        ),
        "dt_full": Field(
            normalized="Custom:dt_full",
            core="custom",
            label="Date Time Full",
            attribute="DateTimeFull",
            description="Data/hora compacta no formato YYYYMMDDHHMM. [DateTimeFull]",
            level=5,
        ),
        "dt_date": Field(
            normalized="Custom:dt_date",
            core="custom",
            label="Date Only",
            attribute="DateOnly",
            description="Data compacta no formato YYYYMMDD. [DateOnly]",
            level=5,
        ),
        "dt_time": Field(
            normalized="Custom:dt_time",
            core="custom",
            label="Time Only",
            attribute="TimeOnly",
            description="Horario compacto no formato HHMM. [TimeOnly]",
            level=5,
        ),
        "FlightNumber": Field(
            normalized="Custom:FlightNumber",
            core="custom",
            label="Flight Number",
            attribute="FlightNum",
            description="Numero do voo derivado do MRK. [FlightNum]",
            level=5,
        ),
        "FlightName": Field(
            normalized="Custom:FlightName",
            core="custom",
            label="Flight Name",
            attribute="FlightName",
            description="Nome do voo derivado do MRK. [FlightName]",
            level=5,
        ),
        "FolderLevel1": Field(
            normalized="Custom:FolderLevel1",
            core="custom",
            label="Folder Level 1",
            attribute="FolderL1",
            description="Primeiro nivel de pasta do voo. [FolderL1]",
            level=5,
        ),
        "FolderLevel2": Field(
            normalized="Custom:FolderLevel2",
            core="custom",
            label="Folder Level 2",
            attribute="FolderL2",
            description="Segundo nivel de pasta do voo. [FolderL2]",
            level=5,
        ),
        "GimbalOffset": Field(
            normalized="xmp_bloco_1:drone-dji:GimbalOffset",
            core="custom",
            label="Gimbal Offset",
            attribute="GimOffset",
            description="Deslocamento angular mínimo do gimbal em relação à aeronave em graus (GimbalYawDegree - FlightYawDegree - 180, normalizado para menor ângulo). Valores: 0-180°. Valor referência: <1°. [GimOffset]",
            level=5,
        ),
        "3DSpeed": Field(
            normalized="Custom:3DSpeed",
            core="custom",
            label="3 D Speed",
            attribute="3DSpeed",
            description="Velocidade total 3D da aeronave em m/s, calculada como sqrt(FlightXSpeed² + FlightYSpeed² + FlightZSpeed²). Valores: 0-50 m/s. Valor referência: <10 m/s para voos estáveis. [3DSpeed]",
            level=5,
        ),
        "time_since_previous": Field(
            normalized="Custom:time_since_previous",
            core="custom",
            label="Time Since Previous",
            attribute="TimePrv",
            description="Tempo em segundos desde a foto anterior. Valores: 0-120 s. Valor referência: 2-5 s para cadência ideal. [TimePrv]",
            level=5,
        ),
        "geodesic_distance_previous": Field(
            normalized="Custom:geodesic_distance_previous",
            core="custom",
            label="Geodesic Distance Previous",
            attribute="GeoDstP",
            description="Distância horizontal em metros entre posições GPS consecutivas (fórmula Haversine). Valores: 0-100 m. Valor referência: 20-50 m para sobreposição adequada. [GeoDstP]",
            level=5,
        ),
        "distance_3d_previous": Field(
            normalized="Custom:distance_3d_previous",
            core="custom",
            label="Distance 3 D Previous",
            attribute="Dist3DP",
            description="Distância 3D em metros entre posições consecutivas (horizontal + altitude). Valores: 0-100 m. Valor referência: 20-50 m. [Dist3DP]",
            level=5,
        ),
        "avg_velocity_between_photos": Field(
            normalized="Custom:avg_velocity_between_photos",
            core="custom",
            label="Avg Velocity Between Photos",
            attribute="AvgVelB",
            description="Velocidade média em m/s entre fotos consecutivas. Valores: 0-20 m/s. Valor referência: 5-10 m/s. [AvgVelB]",
            level=5,
        ),
        "linear_velocity_instant": Field(
            normalized="Custom:linear_velocity_instant",
            core="custom",
            label="Linear Velocity Instant",
            attribute="LinVelI",
            description="Velocidade instantânea 3D em m/s. Valores: 0-50 m/s. Valor referência: <10 m/s. [LinVelI]",
            level=5,
        ),
        "displacement_direction": Field(
            normalized="Custom:displacement_direction",
            core="custom",
            label="Displacement Direction",
            attribute="DirDispl",
            description="Azimute do deslocamento em graus (0=Norte). Valores: 0-360°. Valor referência: varia por missão. [DirDispl]",
            level=5,
        ),
        "incidence_angle": Field(
            normalized="Custom:incidence_angle",
            core="custom",
            label="Incidence Angle",
            attribute="IncAngle",
            description="Ângulo de incidência em graus (ângulo entre câmera e vertical). Valores: 0-180°. Valor referência: <5° para nadir. [IncAngle]",
            level=5,
        ),
        "estimated_coverage": Field(
            normalized="Custom:estimated_coverage",
            core="custom",
            label="Estimated Coverage",
            attribute="EstCover",
            description="Tupla (largura, altura) em metros da cobertura estimada no solo. Valores: (0-200, 0-150) m. Valor referência: depende altitude. [EstCover]",
            level=5,
        ),
        "predicted_overlap": Field(
            normalized="Custom:predicted_overlap",
            core="custom",
            label="Predicted Overlap",
            attribute="PredOver",
            description="Percentual de sobreposição longitudinal com foto anterior. Valores: 0-100%. Valor referência: >60%. [PredOver]",
            level=5,
        ),
        "rtk_effective_precision": Field(
            normalized="Custom:rtk_effective_precision",
            core="custom",
            label="RTK Effective Precision",
            attribute="RTKPrec",
            description="Classificação textual da precisão RTK. Valores: Alta, Média, Baixa, Sem RTK. Valor referência: Alta. [RTKPrec]",
            level=5,
        ),
        "is_ideal_overlap": Field(
            normalized="Custom:is_ideal_overlap",
            core="custom",
            label="Is Ideal Overlap",
            attribute="IdealOvl",
            description="Booleano indicando se sobreposição >=60%. Valores: True/False. Valor referência: True. [IdealOvl]",
            level=5,
        ),
        "abrupt_change_flag": Field(
            normalized="Custom:abrupt_change_flag",
            core="custom",
            label="Abrupt Change Flag",
            attribute="AbrChgF",
            description="Flag de mudança brusca (tempo ou distância >2x mediana). Valores: True/False. Valor referência: False. [AbrChgF]",
            level=5,
        ),
        "gimbal_angular_velocity": Field(
            normalized="Custom:gimbal_angular_velocity",
            core="custom",
            label="Gimbal Angular Velocity",
            attribute="GimAngV",
            description="Variação angular do gimbal em °/s. Valores: 0-100 °/s. Valor referência: <1 °/s. [GimAngV]",
            level=5,
        ),
        "orthorectification_potential": Field(
            normalized="Custom:orthorectification_potential",
            core="custom",
            label="Orthorectification Potential",
            attribute="OrtoPot",
            description="Score de potencial para ortorretificação (0-100). Valores: 0-100. Valor referência: >80. [OrtoPot]",
            level=5,
        ),
        "shutter_life_pct": Field(
            normalized="Custom:shutter_life_pct",
            core="custom",
            label="Shutter Life Pct",
            attribute="ShutPct",
            description="% de vida útil do obturador. Valores: 0-100%. Valor referência: <50%. [ShutPct]",
            level=5,
        ),
        "ground_sample_distance_cm": Field(
            normalized="Custom:ground_sample_distance_cm",
            core="custom",
            label="Ground Sample Distance Cm",
            attribute="GsdCmPx",
            description="GSD em cm/pixel. Valores: 0-10 cm. Valor referência: <2 cm. [GsdCmPx]",
            level=5,
        ),
        "total_heat_index": Field(
            normalized="Custom:total_heat_index",
            core="custom",
            label="Total Heat Index",
            attribute="HeatIdx",
            description="Índice térmico médio em °C. Valores: 20-60 °C. Valor referência: <40 °C. [HeatIdx]",
            level=5,
        ),
        "speed_3d_kmh": Field(
            normalized="Custom:speed_3d_kmh",
            core="custom",
            label="Speed 3 D Kmh",
            attribute="SpdKmH",
            description="Velocidade 3D do drone em km/h. Valores: 0-180 km/h. Valor referência: <36 km/h. [SpdKmH]",
            level=5,
        ),
        "yaw_alignment_error": Field(
            normalized="Custom:yaw_alignment_error",
            core="custom",
            label="Yaw Alignment Error",
            attribute="YawErr",
            description="Erro de alinhamento yaw em graus. Valores: 0-180°. Valor referência: <5°. [YawErr]",
            level=5,
        ),
        "motion_blur_risk": Field(
            normalized="Custom:motion_blur_risk",
            core="custom",
            label="Motion Blur Risk",
            attribute="BlurRisk",
            description="Risco de motion blur em pixels. Valores: 0-5. Valor referência: <0.5. [BlurRisk]",
            level=5,
        ),
        "exposure_value_ev": Field(
            normalized="Custom:exposure_value_ev",
            core="custom",
            label="Exposure Value EV",
            attribute="EV",
            description="Valor de exposição EV. Valores: 8-16. Valor referência: 12-14. [EV]",
            level=5,
        ),
        "light_source_classification": Field(
            normalized="Custom:light_source_classification",
            core="custom",
            label="Light Source Classification",
            attribute="LSrcClass",
            description="Classificação textual da fonte de luz EXIF. Valores: Daylight, Fluorescent, etc. Valor referência: Daylight. [LSrcClass]",
            level=5,
        ),
        "light_consistency": Field(
            normalized="Custom:light_consistency",
            core="custom",
            label="Light Consistency",
            attribute="LightCons",
            description="Consistência entre LightSource e CCT. Valores: Consistent, Inconsistent, Unknown. Valor referência: Consistent. [LightCons]",
            level=5,
        ),
        "vertical_stability": Field(
            normalized="Custom:vertical_stability",
            core="custom",
            label="Vertical Stability",
            attribute="VertStb",
            description="Variação vertical em metros. Valores: 0-10 m. Valor referência: <1 m. [VertStb]",
            level=5,
        ),
        "trajectory_smoothness": Field(
            normalized="Custom:trajectory_smoothness",
            core="custom",
            label="Trajectory Smoothness",
            attribute="TrajSmt",
            description="Diferença angular de direção em graus. Valores: 0-180°. Valor referência: <10°. [TrajSmt]",
            level=5,
        ),
        "speed_variation_index": Field(
            normalized="Custom:speed_variation_index",
            core="custom",
            label="Speed Variation Index",
            attribute="SpdVar",
            description="Índice de variação de velocidade (coeficiente de variação). Valores: 0-1. Valor referência: <0.1. [SpdVar]",
            level=5,
        ),
        "rtk_stability_score": Field(
            normalized="Custom:rtk_stability_score",
            core="custom",
            label="RTK Stability Score",
            attribute="RtkStab",
            description="Score de estabilidade RTK (0-100). Valores: 0-100. Valor referência: >90. [RtkStab]",
            level=5,
        ),
        "capture_efficiency": Field(
            normalized="Custom:capture_efficiency",
            core="custom",
            label="Capture Efficiency",
            attribute="CapEff",
            description="Eficiência de captura (distância/cobertura). Valores: 0-1. Valor referência: 0.5-0.8. [CapEff]",
            level=5,
        ),
        "photogrammetry_quality_index": Field(
            normalized="Custom:photogrammetry_quality_index",
            core="custom",
            label="Photogrammetry Quality Index",
            attribute="PQI",
            description="Índice de qualidade fotogramétrica (0-100). Valores: 0-100. Valor referência: >80. [PQI]",
            level=5,
        ),
        "strip_id": Field(
            normalized="Custom:strip_id",
            core="custom",
            label="Strip ID",
            attribute="StripID",
            description="ID da faixa de voo. Valores: 1+. Valor referência: incremental. [StripID]",
            level=5,
        ),
    }

    MRK_FIELDS = {
        "foto": Field(
            normalized="MRK:foto",
            core="mrk",
            label="Photo Number",
            attribute="PhotoNum",
            description="Numero sequencial da foto vindo do MRK. [PhotoNum]",
            level=5,
        ),
        "lat": Field(
            normalized="MRK:lat",
            core="mrk",
            label="Latitude",
            attribute="Latitude",
            description="Latitude extraida do arquivo MRK. [Latitude]",
            level=5,
        ),
        "lon": Field(
            normalized="MRK:lon",
            core="mrk",
            label="Longitude",
            attribute="Longitude",
            description="Longitude extraida do arquivo MRK. [Longitude]",
            level=5,
        ),
        "alt": Field(
            normalized="MRK:alt",
            core="mrk",
            label="Altitude",
            attribute="Altitude",
            description="Altitude extraida do arquivo MRK. [Altitude]",
            level=5,
        ),
        "date_name": Field(
            normalized="MRK:date_name",
            core="mrk",
            label="Date Name",
            attribute="DateName",
            description="Data identificada a partir do nome do MRK. [DateName]",
            level=5,
        ),
        "mrk_file": Field(
            normalized="MRK:mrk_file",
            core="mrk",
            label="MRK File",
            attribute="MrkFile",
            description="Nome do arquivo MRK de origem. [MrkFile]",
            level=5,
        ),
        "mrk_path": Field(
            normalized="MRK:mrk_path",
            core="mrk",
            label="MRK Path",
            attribute="MrkPath",
            description="Caminho completo do arquivo MRK de origem. [MrkPath]",
            level=5,
        ),
        "mrk_folder": Field(
            normalized="MRK:mrk_folder",
            core="mrk",
            label="MRK Folder",
            attribute="MrkFolder",
            description="Pasta absoluta de origem do ponto MRK. [MrkFolder]",
            level=5,
        ),
        "flight_number": Field(
            normalized="MRK:flight_number",
            core="mrk",
            label="Flight Number",
            attribute="FlightNumber",
            description="Numero do voo identificado no MRK. [FlightNumber]",
            level=5,
        ),
        "flight_name": Field(
            normalized="MRK:flight_name",
            core="mrk",
            label="Flight Name",
            attribute="FlightName",
            description="Nome do voo identificado no MRK. [FlightName]",
            level=5,
        ),
        "folder_level1": Field(
            normalized="MRK:folder_level1",
            core="mrk",
            label="Folder Level 1",
            attribute="Folder1",
            description="Primeiro nivel de pasta no caminho do MRK. [FolderLevel1]",
            level=5,
        ),
        "folder_level2": Field(
            normalized="MRK:folder_level2",
            core="mrk",
            label="Folder Level 2",
            attribute="Folder2",
            description="Segundo nivel de pasta no caminho do MRK. [FolderLevel2]",
            level=5,
        ),
    }

    @classmethod
    def all_fields(cls) -> Dict[str, Field]:
        fields: Dict[str, Field] = {}
        fields.update(cls.REQUIRED_FIELDS)
        fields.update(cls.CUSTOM_FIELDS)
        fields.update(cls.MRK_FIELDS)
        return fields

    @classmethod
    def required_keys(cls) -> List[str]:
        return list(cls.REQUIRED_FIELDS.keys())

    @classmethod
    def custom_keys(cls) -> List[str]:
        return list(cls.CUSTOM_FIELDS.keys())

    @classmethod
    def mrk_keys(cls) -> List[str]:
        return list(cls.MRK_FIELDS.keys())

    @classmethod
    def key_to_attribute_map(cls) -> Dict[str, str]:
        return {key: field.attribute for key, field in cls.all_fields().items()}

    @classmethod
    def attribute_to_key_map(cls) -> Dict[str, str]:
        return {field.attribute: key for key, field in cls.all_fields().items()}

    @classmethod
    def get_field(cls, key: str) -> Optional[Field]:
        return cls.all_fields().get(key)

    @classmethod
    def get_attribute(cls, key: str, default: Optional[str] = None) -> Optional[str]:
        field = cls.get_field(key)
        if field is None:
            return default
        return field.attribute

    @classmethod
    def resolve_key(cls, key_or_attribute: str) -> str:
        if not key_or_attribute:
            return key_or_attribute

        if key_or_attribute in cls.all_fields():
            return key_or_attribute

        return cls.attribute_to_key_map().get(key_or_attribute, key_or_attribute)

    @classmethod
    def resolve_output_name(cls, key_or_attribute: str) -> str:
        if not key_or_attribute:
            return key_or_attribute

        if key_or_attribute in cls.all_fields():
            return cls.all_fields()[key_or_attribute].attribute

        if key_or_attribute in cls.attribute_to_key_map():
            return key_or_attribute

        return key_or_attribute

    @classmethod
    def resolve_output_names(cls, names: Iterable[str]) -> List[str]:
        resolved = [cls.resolve_output_name(name) for name in (names or [])]
        return StringAdapter.unique_preserve_order(resolved)

    @classmethod
    def normalize_selected_keys(
        cls,
        names: Iterable[str],
        *,
        allowed_keys: Optional[Iterable[str]] = None,
    ) -> List[str]:
        normalized = [cls.resolve_key(name) for name in (names or [])]
        normalized = StringAdapter.unique_preserve_order(normalized)
        if allowed_keys is None:
            return StringAdapter.filter_known_keys(normalized, cls.all_fields())

        allowed_set = set(allowed_keys)
        return [name for name in normalized if name in allowed_set]

    @classmethod
    def normalize_record_to_keys(cls, record: Dict[str, object]) -> Dict[str, object]:
        """
        Converte um registro com nomes de atributos de camada para chaves internas de metadata.
        Campos nao catalogados sao mantidos inalterados.
        """
        normalized = {}
        for key, value in (record or {}).items():
            normalized[cls.resolve_key(key)] = value
        return normalized

    @classmethod
    def map_record_to_output_attributes(
        cls,
        record: Dict[str, object],
        *,
        exclude_keys: Optional[Iterable[str]] = None,
    ) -> Dict[str, object]:
        """
        Converte um registro baseado em chaves internas para nomes de atributos finais.
        """
        excluded = set(exclude_keys or [])
        mapped = {}
        for key, value in (record or {}).items():
            if key in excluded:
                continue
            mapped[cls.resolve_output_name(key)] = value
        return mapped

    @classmethod
    def default_track_attribute_keys(cls) -> List[str]:
        """
        Chaves canonicas para atributos da camada de trilha.
        """
        return ["date_name", "folder", "mrk_file", "mrk_path", "flight_number", "flight_name"]

