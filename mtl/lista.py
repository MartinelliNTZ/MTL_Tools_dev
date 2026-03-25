LISTA_COMENTADA = """
normalized	CHAVE_DICT	core	attribute	description
file	file		File	
path	path		Path	
format	format		FormatMod		
size_mb	size_mb		SizeMB	
EXIF:GPSInfo:GPSMapDatum	GPSMapDatum	EXIF	GPSDatum	Datum da foto
EXIF:Model	Model	EXIF	Model	Modelo da Camera
EXIF:Software	Software	EXIF	Firmware	Versao do Firmware
EXIF:XResolution	XResolution	EXIF	DPIWidth	Largura em DPI
EXIF:YResolution	YResolution	EXIF	DPIHeight	Altura em DPI
EXIF:ShutterSpeedValue	ShutterSpeedValue	EXIF	ShutterSp	Velocidade do Obturador
EXIF:DateTimeOriginal	DateTimeOriginal	EXIF	DateTime	Data exata da foto no fuso horario
EXIF:ApertureValue	ApertureValue	EXIF	ApertureV	Abertura da lente
EXIF:MaxApertureValue	MaxApertureValue	EXIF	MaxApertV	Abertura maxima da lente
EXIF:LightSource	LightSource	EXIF	LightSour	Luminosidade do dia
EXIF:FocalLength	FocalLength	EXIF	FocalLeng	Distancia focal real da lente em milimetros
EXIF:ExifImageWidth	ExifImageWidth	EXIF	WidthPX	Largura em pixels
EXIF:ExifImageHeight	ExifImageHeight	EXIF	HeightPX	Altura em pixels
EXIF:ExposureTime	ExposureTime	EXIF	ExpTime	Tempo de Exposicao
EXIF:FNumber	FNumber	EXIF	FNumber	Numero da Abertura
EXIF:ExposureProgram	ExposureProgram	EXIF	ExpProg	Programa de exposicao definido pelo drone
EXIF:ISOSpeedRatings	ISOSpeedRatings	EXIF	ISOSpeed	Sensibilidade do sensor a luz
EXIF:ExposureMode	ExposureMode	EXIF	ExpMode	Modo de exposicao utilizado pela camera
EXIF:LensSpecification	LensSpecification	EXIF	Lens	(FocalLengthMin, FocalLengthMax, ApertureMin, ApertureMax)
EXIF:DigitalZoomRatio	DigitalZoomRatio	EXIF	ZoomRatio	Zoom digital tem sempre que ta 0
EXIF:GPSInfo:GPSStatus	GpsStatus	xmp_bloco_1	GpsStatus	Se RTK ou outro formato
xmp_bloco_1:drone-dji:AltitudeType	AltitudeType	xmp_bloco_1	Ytype	Se RTK ou outro formato
EXIF:GPSInfo:GPSLatitude	GpsLatitude	xmp_bloco_1	GpsLat	Latitude da aeronave
EXIF:GPSInfo:GPSLongitude	GpsLongitude	xmp_bloco_1	GPSLong	Longitude da aeronave
xmp_bloco_1:drone-dji:AbsoluteAltitude	AbsoluteAltitude	xmp_bloco_1	AbsY	Altitude absoluta da aeronave
xmp_bloco_1:drone-dji:RelativeAltitude	RelativeAltitude	xmp_bloco_1	RelativeY	Altitude Relativa do ponto de decolagem
xmp_bloco_1:drone-dji:GimbalRollDegree	GimbalRollDegree	xmp_bloco_1	GimbRoll	Rolagem do Gimbal(180 normal)(sim com acabeça)
xmp_bloco_1:drone-dji:GimbalYawDegree	GimbalYawDegree	xmp_bloco_1	GimbYaw	Direcao do Gimbal
xmp_bloco_1:drone-dji:GimbalPitchDegree	GimbalPitchDegree	xmp_bloco_1	GimbPitch	Inclinacao do Gimbal verticamente
xmp_bloco_1:drone-dji:FlightRollDegree	FlightRollDegree	xmp_bloco_1	DroneRoll	Rolagem da aeronave
xmp_bloco_1:drone-dji:FlightYawDegree	FlightYawDegree	xmp_bloco_1	DroneYaw	Direcao da aeronave
xmp_bloco_1:drone-dji:FlightPitchDegree	FlightPitchDegree	xmp_bloco_1	DronePitc	Inclinacao da aeronave
xmp_bloco_1:drone-dji:FlightXSpeed	FlightXSpeed	xmp_bloco_1	XSpeed	Velocidade de voo X
xmp_bloco_1:drone-dji:FlightYSpeed	FlightYSpeed	xmp_bloco_1	YSpeed	Velocidade de voo Y
xmp_bloco_1:drone-dji:FlightZSpeed	FlightZSpeed	xmp_bloco_1	ZSpeed	Velocidade de voo Z
xmp_bloco_1:drone-dji:RtkFlag	RtkFlag	xmp_bloco_1	RtkFlag	Qualidade do sinal do drone
xmp_bloco_1:drone-dji:RtkStdLon	RtkStdLon	xmp_bloco_1	RtkStdLon	Desvio Padrao do RTK Longitude
xmp_bloco_1:drone-dji:RtkStdLat	RtkStdLat	xmp_bloco_1	RtkStdLat	Desvio Padrao do RTK Latitude
xmp_bloco_1:drone-dji:RtkStdHgt	RtkStdHgt	xmp_bloco_1	RtkStdHgt	Desvio Padrao do RTK Altitude
xmp_bloco_1:drone-dji:RtkDiffAge	RtkDiffAge	xmp_bloco_1	RtkDifAge	Tempo da Ultima correcao RTK
xmp_bloco_1:drone-dji:DewarpFlag	DewarpFlag	xmp_bloco_1	Dewarp	Dewarp habilitado =0; desabilitado = nada
xmp_bloco_1:drone-dji:UTCAtExposure	UTCAtExposure	xmp_bloco_1	UTCTime	Data e hora no GPS Time
xmp_bloco_1:drone-dji:ShutterCount	ShutterCount	xmp_bloco_1	ShotCount	Numero Total de Fotos tiradas com a camera
xmp_bloco_1:drone-dji:FocusDistance	FocusDistance	xmp_bloco_1	FocusDist	Distancia de foco
xmp_bloco_1:drone-dji:CameraSerialNumber	CameraSerialNumber	xmp_bloco_1	CameraID	Numero Serial da Camera
xmp_bloco_1:drone-dji:DroneModel	DroneModel	xmp_bloco_1	DronModel	Modelo do Drone
xmp_bloco_1:drone-dji:DroneSerialNumber	DroneSerialNumber	xmp_bloco_1	DroneID	Numero Serial do Drone
xmp_bloco_1:drone-dji:CaptureUUID	CaptureUUID	xmp_bloco_1	CaptureID	ID da captura para unir fotos Multespectral em drones M3M
xmp_bloco_1:drone-dji:PictureQuality	PictureQuality	xmp_bloco_1	ImgQualit	Nivel de compressao da imagem
JPEG:segmentos_total	segmentos_total	xmp_bloco_1	Segments	Numero de segmentos do JPG
xmp_bloco_1:drone-dji:SensorTemperature	SensorTemperature	xmp_bloco_1	SensTemp	Temperatura do sensor
xmp_bloco_1:drone-dji:LRFStatus	LRFStatus	xmp_bloco_1	LRFStatus	Status do Laser Range Finder
xmp_bloco_1:drone-dji:LRFTargetDistance	LRFTargetDistance	xmp_bloco_1	LRFDist	Distancia do LRF(Laser Range Finder) ate o ponto central da foto no solo
xmp_bloco_1:drone-dji:LRFTargetLon	LRFTargetLon	xmp_bloco_1	LRFLong	Longitude medida pelo LRF(Laser Range Finder)
xmp_bloco_1:drone-dji:LRFTargetLat	LRFTargetLat	xmp_bloco_1	LRFLati	Latitude medida pelo LRF(Laser Range Finder)
xmp_bloco_1:drone-dji:LRFTargetAlt	LRFTargetAlt	xmp_bloco_1	LRFY	Altitude Relativa do ponto de decolagem LRF(Laser Range Finder)
xmp_bloco_1:drone-dji:LRFTargetAbsAlt	LRFTargetAbsAlt	xmp_bloco_1	LrfAbsAlt	Altitude Absoluta do ponto de decolagem LRF(Laser Range Finder)
xmp_bloco_1:drone-dji:WhiteBalanceCCT	WhiteBalanceCCT	xmp_bloco_1	WhiteBlc	E um valor numerico que indica a cor da luz no ambiente onde a foto foi tirada, medida em Kelvin (K)
xmp_bloco_1:drone-dji:SensorFPS	SensorFPS	xmp_bloco_1	SensorFPS	Taxa de quadros (frames por segundo)
EXIF:RecommendedExposureIndex	RecommendedExposureIndex	xmp_bloco_1	REI	Indice de Exposicao Recomendado - REI
xmp_bloco_1:drone-dji:LensPosition	LensPosition	xmp_bloco_1	LensPosit	Posicao da Lente
xmp_bloco_1:drone-dji:LensTemperature	LensTemperature	xmp_bloco_1	LensTemp	Temperatura da Lente



"""


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

SIMPLIFIED_FIELDS = {}
# Lista 1 – Campos individuais (por imagem) como dicionário



# NAO MECHA DA QUI PARA BAIXO, EU QUERO SO DAQUI PARA CIMA, O RESTO E SÓ UM COMENTARIO QUE EU USEI PARA MONTAR A LISTA DE CAMPOS, SE VOCÊ MECHER VAI FICAR UMA BAGUNÇA E EU VOU TER QUE REFAZER TUDO DE NOVO, OBRIGADO PELA COMPREENSÃO



"""
        LISTA_CAMPOS = {
        "arquivo": {"original": "Custom:arquivo", "padronizado": "arquivo", "resumido": "arquivo", "modulo": "FILE", "atributo": "File", "descricao": "Nome do arquivo da imagem"},
        "caminho": {"original": "Custom:caminho", "padronizado": "caminho", "resumido": "caminho", "modulo": "FILE", "atributo": "Path", "descricao": "Caminho completo do arquivo"},
        "formato": {"original": "PIL:format", "padronizado": "formato", "resumido": "formato", "modulo": "PIL", "atributo": "FormatMod", "descricao": "Formato identificado pelo Pillow"},
        "modo": {"original": "PIL:mode", "padronizado": "modo", "resumido": "modo", "modulo": "PIL", "atributo": "Mode", "descricao": "Modo de cor da imagem"},
        "tamanho_mb": {"original": "Custom:tamanho_mb", "padronizado": "tamanho_mb", "resumido": "tamanho_mb", "modulo": "FILE", "atributo": "SizeMB", "descricao": "Tamanho do arquivo em megabytes"},
        "EXIF:GPSInfo:GPSMapDatum": {"original": "EXIF:GPSInfo:GPSMapDatum", "padronizado": "EXIF:GPSInfo:GPSMapDatum", "resumido": "GPSMapDatum", "modulo": "EXIF", "atributo": "GPSDatum", "descricao": "Datum da foto"},
        "EXIF:Model": {"original": "EXIF:Model", "padronizado": "EXIF:Model", "resumido": "Model", "modulo": "EXIF", "atributo": "Model", "descricao": "Modelo da Camera"},
        "EXIF:Software": {"original": "EXIF:Software", "padronizado": "EXIF:Software", "resumido": "Software", "modulo": "EXIF", "atributo": "Firmware", "descricao": "Versao do Firmware"},
        "EXIF:XResolution": {"original": "EXIF:XResolution", "padronizado": "EXIF:XResolution", "resumido": "XResolution", "modulo": "EXIF", "atributo": "DPIWidth", "descricao": "Largura em DPI"},
        "EXIF:YResolution": {"original": "EXIF:YResolution", "padronizado": "EXIF:YResolution", "resumido": "YResolution", "modulo": "EXIF", "atributo": "DPIHeigh", "descricao": "Altura em DPI"},
        "EXIF:ShutterSpeedValue": {"original": "EXIF:ShutterSpeedValue", "padronizado": "EXIF:ShutterSpeedValue", "resumido": "ShutterSpeedValue", "modulo": "EXIF", "atributo": "ShutterSp", "descricao": "Velocidade do Obturador"},
        "EXIF:DateTimeOriginal": {"original": "EXIF:DateTimeOriginal", "padronizado": "EXIF:DateTimeOriginal", "resumido": "DateTimeOriginal", "modulo": "EXIF", "atributo": "DateTime", "descricao": "Data exata da foto no fuso horario"},
        "EXIF:ApertureValue": {"original": "EXIF:ApertureValue", "padronizado": "EXIF:ApertureValue", "resumido": "ApertureValue", "modulo": "EXIF", "atributo": "ApertureV", "descricao": "Abertura da lente"},
        "EXIF:MaxApertureValue": {"original": "EXIF:MaxApertureValue", "padronizado": "EXIF:MaxApertureValue", "resumido": "MaxApertureValue", "modulo": "EXIF", "atributo": "MaxApertV", "descricao": "Abertura maxima da lente"},
        "EXIF:LightSource": {"original": "EXIF:LightSource", "padronizado": "EXIF:LightSource", "resumido": "LightSource", "modulo": "EXIF", "atributo": "LightSour", "descricao": "Luminosidade do dia"},
        "EXIF:FocalLength": {"original": "EXIF:FocalLength", "padronizado": "EXIF:FocalLength", "resumido": "FocalLength", "modulo": "EXIF", "atributo": "FocalLeng", "descricao": "Distancia focal real da lente em milimetros"},
        "EXIF:ExifImageWidth": {"original": "EXIF:ExifImageWidth", "padronizado": "EXIF:ExifImageWidth", "resumido": "ExifImageWidth", "modulo": "EXIF", "atributo": "WidthPX", "descricao": "Largura em pixels"},
        "EXIF:ExifImageHeight": {"original": "EXIF:ExifImageHeight", "padronizado": "EXIF:ExifImageHeight", "resumido": "ExifImageHeight", "modulo": "EXIF", "atributo": "HeightPX", "descricao": "Altura em pixels"},
        "EXIF:ExposureTime": {"original": "EXIF:ExposureTime", "padronizado": "EXIF:ExposureTime", "resumido": "ExposureTime", "modulo": "EXIF", "atributo": "ExpTime", "descricao": "Tempo de Exposicao"},
        "EXIF:FNumber": {"original": "EXIF:FNumber", "padronizado": "EXIF:FNumber", "resumido": "FNumber", "modulo": "EXIF", "atributo": "FNumber", "descricao": "Numero da Abertura"},
        "EXIF:ExposureProgram": {"original": "EXIF:ExposureProgram", "padronizado": "EXIF:ExposureProgram", "resumido": "ExposureProgram", "modulo": "EXIF", "atributo": "ExpProg", "descricao": "Programa de exposicao definido pelo drone"},
        "EXIF:ISOSpeedRatings": {"original": "EXIF:ISOSpeedRatings", "padronizado": "EXIF:ISOSpeedRatings", "resumido": "ISOSpeedRatings", "modulo": "EXIF", "atributo": "ISOSpeed", "descricao": "Sensibilidade do sensor a luz"},
        "EXIF:ExposureMode": {"original": "EXIF:ExposureMode", "padronizado": "EXIF:ExposureMode", "resumido": "ExposureMode", "modulo": "EXIF", "atributo": "ExpMode", "descricao": "Modo de exposicao utilizado pela camera"},
        "EXIF:LensSpecification": {"original": "EXIF:LensSpecification", "padronizado": "EXIF:LensSpecification", "resumido": "LensSpecification", "modulo": "EXIF", "atributo": "Lens", "descricao": "(FocalLengthMin, FocalLengthMax, ApertureMin, ApertureMax)"},
        "EXIF:DigitalZoomRatio": {"original": "EXIF:DigitalZoomRatio", "padronizado": "EXIF:DigitalZoomRatio", "resumido": "DigitalZoomRatio", "modulo": "EXIF", "atributo": "ZoomRatio", "descricao": "Zoom digital tem sempre que ta 0"},
        "EXIF:GPSInfo:GPSStatus": {"original": "EXIF:GPSInfo:GPSStatus", "padronizado": "EXIF:GPSInfo:GPSStatus", "resumido": "GpsStatus", "modulo": "EXIF", "atributo": "GpsStatus", "descricao": "Se RTK ou outro formato"},
        "xmp_bloco_1:drone-dji:AltitudeType": {"original": "xmp_bloco_1:drone-dji:AltitudeType", "padronizado": "xmp_bloco_1:drone-dji:AltitudeType", "resumido": "AltitudeType", "modulo": "xmp_bloco_1", "atributo": "Ytype", "descricao": "Se RTK ou outro formato"},
        "EXIF:GPSInfo:GPSLatitude": {"original": "EXIF:GPSInfo:GPSLatitude", "padronizado": "EXIF:GPSInfo:GPSLatitude", "resumido": "GpsLatitude", "modulo": "EXIF", "atributo": "GpsLat", "descricao": "Latitude da aeronave"},
        "EXIF:GPSInfo:GPSLongitude": {"original": "EXIF:GPSInfo:GPSLongitude", "padronizado": "EXIF:GPSInfo:GPSLongitude", "resumido": "GpsLongitude", "modulo": "EXIF", "atributo": "GPSLong", "descricao": "Longitude da aeronave"},
        "xmp_bloco_1:drone-dji:AbsoluteAltitude": {"original": "xmp_bloco_1:drone-dji:AbsoluteAltitude", "padronizado": "xmp_bloco_1:drone-dji:AbsoluteAltitude", "resumido": "AbsoluteAltitude", "modulo": "xmp_bloco_1", "atributo": "AbsY", "descricao": "Altitude absoluta da aeronave"},
        "xmp_bloco_1:drone-dji:RelativeAltitude": {"original": "xmp_bloco_1:drone-dji:RelativeAltitude", "padronizado": "xmp_bloco_1:drone-dji:RelativeAltitude", "resumido": "RelativeAltitude", "modulo": "xmp_bloco_1", "atributo": "RelativeY", "descricao": "Altitude Relativa do ponto de decolagem"},
        "xmp_bloco_1:drone-dji:GimbalRollDegree": {"original": "xmp_bloco_1:drone-dji:GimbalRollDegree", "padronizado": "xmp_bloco_1:drone-dji:GimbalRollDegree", "resumido": "GimbalRollDegree", "modulo": "xmp_bloco_1", "atributo": "GimbRoll", "descricao": "Rolagem do Gimbal(180 normal)(sim com acabeca)"},
        "xmp_bloco_1:drone-dji:GimbalYawDegree": {"original": "xmp_bloco_1:drone-dji:GimbalYawDegree", "padronizado": "xmp_bloco_1:drone-dji:GimbalYawDegree", "resumido": "GimbalYawDegree", "modulo": "xmp_bloco_1", "atributo": "GimbYaw", "descricao": "Direcao do Gimbal"},
        "xmp_bloco_1:drone-dji:GimbalPitchDegree": {"original": "xmp_bloco_1:drone-dji:GimbalPitchDegree", "padronizado": "xmp_bloco_1:drone-dji:GimbalPitchDegree", "resumido": "GimbalPitchDegree", "modulo": "xmp_bloco_1", "atributo": "GimbPitch", "descricao": "Inclinacao do Gimbal verticamente"},
        "Customizado:GimbalOffset": {"original": "Customizado:GimbalOffset", "padronizado": "Customizado:GimbalOffset", "resumido": "GimbalOffset", "modulo": "xmp_bloco_1", "atributo": "GimOffset", "descricao": "Deslocamento do Gimbal em relaccao a aeronave (GimbalYawDegree - FlightYawDegree -180)"},
        "xmp_bloco_1:drone-dji:FlightRollDegree": {"original": "xmp_bloco_1:drone-dji:FlightRollDegree", "padronizado": "xmp_bloco_1:drone-dji:FlightRollDegree", "resumido": "FlightRollDegree", "modulo": "xmp_bloco_1", "atributo": "DroneRoll", "descricao": "Rolagem da aeronave"},
        "xmp_bloco_1:drone-dji:FlightYawDegree": {"original": "xmp_bloco_1:drone-dji:FlightYawDegree", "padronizado": "xmp_bloco_1:drone-dji:FlightYawDegree", "resumido": "FlightYawDegree", "modulo": "xmp_bloco_1", "atributo": "DroneYaw", "descricao": "Direcao da aeronave"},
        "xmp_bloco_1:drone-dji:FlightPitchDegree": {"original": "xmp_bloco_1:drone-dji:FlightPitchDegree", "padronizado": "xmp_bloco_1:drone-dji:FlightPitchDegree", "resumido": "FlightPitchDegree", "modulo": "xmp_bloco_1", "atributo": "DronePitc", "descricao": "Inclinacao da aeronave"},
        "xmp_bloco_1:drone-dji:FlightXSpeed": {"original": "xmp_bloco_1:drone-dji:FlightXSpeed", "padronizado": "xmp_bloco_1:drone-dji:FlightXSpeed", "resumido": "FlightXSpeed", "modulo": "xmp_bloco_1", "atributo": "XSpeed", "descricao": "Velocidade de voo X"},
        "xmp_bloco_1:drone-dji:FlightYSpeed": {"original": "xmp_bloco_1:drone-dji:FlightYSpeed", "padronizado": "xmp_bloco_1:drone-dji:FlightYSpeed", "resumido": "FlightYSpeed", "modulo": "xmp_bloco_1", "atributo": "YSpeed", "descricao": "Velocidade de voo Y"},
        "xmp_bloco_1:drone-dji:FlightZSpeed": {"original": "xmp_bloco_1:drone-dji:FlightZSpeed", "padronizado": "xmp_bloco_1:drone-dji:FlightZSpeed", "resumido": "FlightZSpeed", "modulo": "xmp_bloco_1", "atributo": "ZSpeed", "descricao": "Velocidade de voo Z"},
        "Customizado:3DSpeed": {"original": "Customizado:3DSpeed", "padronizado": "Customizado:3DSpeed", "resumido": "3DSpeed", "modulo": "xmp_bloco_1", "atributo": "3DSpeed", "descricao": "Velocidade total de deslocamento"},
        "xmp_bloco_1:drone-dji:RtkFlag": {"original": "xmp_bloco_1:drone-dji:RtkFlag", "padronizado": "xmp_bloco_1:drone-dji:RtkFlag", "resumido": "RtkFlag", "modulo": "xmp_bloco_1", "atributo": "RtkFlag", "descricao": "Qualidade do sinal do drone"},
        "xmp_bloco_1:drone-dji:RtkStdLon": {"original": "xmp_bloco_1:drone-dji:RtkStdLon", "padronizado": "xmp_bloco_1:drone-dji:RtkStdLon", "resumido": "RtkStdLon", "modulo": "xmp_bloco_1", "atributo": "RtkStdLon", "descricao": "Desvio Padrao do RTK Longitude"},
        "xmp_bloco_1:drone-dji:RtkStdLat": {"original": "xmp_bloco_1:drone-dji:RtkStdLat", "padronizado": "xmp_bloco_1:drone-dji:RtkStdLat", "resumido": "RtkStdLat", "modulo": "xmp_bloco_1", "atributo": "RtkStdLat", "descricao": "Desvio Padrao do RTK Latitude"},
        "xmp_bloco_1:drone-dji:RtkStdHgt": {"original": "xmp_bloco_1:drone-dji:RtkStdHgt", "padronizado": "xmp_bloco_1:drone-dji:RtkStdHgt", "resumido": "RtkStdHgt", "modulo": "xmp_bloco_1", "atributo": "RtkStdHgt", "descricao": "Desvio Padrao do RTK Altitude"},
        "xmp_bloco_1:drone-dji:RtkDiffAge": {"original": "xmp_bloco_1:drone-dji:RtkDiffAge", "padronizado": "xmp_bloco_1:drone-dji:RtkDiffAge", "resumido": "RtkDiffAge", "modulo": "xmp_bloco_1", "atributo": "RtkDifAge", "descricao": "Tempo da Ultima correcao RTK"},
        "xmp_bloco_1:drone-dji:DewarpFlag": {"original": "xmp_bloco_1:drone-dji:DewarpFlag", "padronizado": "xmp_bloco_1:drone-dji:DewarpFlag", "resumido": "DewarpFlag", "modulo": "xmp_bloco_1", "atributo": "Dewarp", "descricao": "Dewarp habilitado =0; desabilitado = nada"},
        "xmp_bloco_1:drone-dji:UTCAtExposure": {"original": "xmp_bloco_1:drone-dji:UTCAtExposure", "padronizado": "xmp_bloco_1:drone-dji:UTCAtExposure", "resumido": "UTCAtExposure", "modulo": "xmp_bloco_1", "atributo": "UTCTime", "descricao": "Data e hora no GPS Time"},
        "xmp_bloco_1:drone-dji:ShutterCount": {"original": "xmp_bloco_1:drone-dji:ShutterCount", "padronizado": "xmp_bloco_1:drone-dji:ShutterCount", "resumido": "ShutterCount", "modulo": "xmp_bloco_1", "atributo": "ShotCount", "descricao": "Numero Total de Fotos tiradas com a camera"},
        "xmp_bloco_1:drone-dji:FocusDistance": {"original": "xmp_bloco_1:drone-dji:FocusDistance", "padronizado": "xmp_bloco_1:drone-dji:FocusDistance", "resumido": "FocusDistance", "modulo": "xmp_bloco_1", "atributo": "FocusDist", "descricao": "Distancia de foco"},
        "xmp_bloco_1:drone-dji:CameraSerialNumber": {"original": "xmp_bloco_1:drone-dji:CameraSerialNumber", "padronizado": "xmp_bloco_1:drone-dji:CameraSerialNumber", "resumido": "CameraSerialNumber", "modulo": "xmp_bloco_1", "atributo": "CameraID", "descricao": "Numero Serial da Camera"},
        "xmp_bloco_1:drone-dji:DroneModel": {"original": "xmp_bloco_1:drone-dji:DroneModel", "padronizado": "xmp_bloco_1:drone-dji:DroneModel", "resumido": "DroneModel", "modulo": "xmp_bloco_1", "atributo": "DronModel", "descricao": "Modelo do Drone"},
        "xmp_bloco_1:drone-dji:DroneSerialNumber": {"original": "xmp_bloco_1:drone-dji:DroneSerialNumber", "padronizado": "xmp_bloco_1:drone-dji:DroneSerialNumber", "resumido": "DroneSerialNumber", "modulo": "xmp_bloco_1", "atributo": "DroneID", "descricao": "Numero Serial do Drone"},
        "xmp_bloco_1:drone-dji:CaptureUUID": {"original": "xmp_bloco_1:drone-dji:CaptureUUID", "padronizado": "xmp_bloco_1:drone-dji:CaptureUUID", "resumido": "CaptureUUID", "modulo": "xmp_bloco_1", "atributo": "CaptureID", "descricao": "ID da captura para unir fotos Multespectral em drones M3M"},
        "xmp_bloco_1:drone-dji:PictureQuality": {"original": "xmp_bloco_1:drone-dji:PictureQuality", "padronizado": "xmp_bloco_1:drone-dji:PictureQuality", "resumido": "PictureQuality", "modulo": "xmp_bloco_1", "atributo": "ImgQualit", "descricao": "Nivel de compressao da imagem"},
        "JPEG:segmentos_total": {"original": "JPEG:segmentos_total", "padronizado": "JPEG:segmentos_total", "resumido": "segmentos_total", "modulo": "JPEG", "atributo": "Segments", "descricao": "Numero de segmentos do JPG"},
        "xmp_bloco_1:drone-dji:SensorTemperature": {"original": "xmp_bloco_1:drone-dji:SensorTemperature", "padronizado": "xmp_bloco_1:drone-dji:SensorTemperature", "resumido": "SensorTemperature", "modulo": "xmp_bloco_1", "atributo": "SensTemp", "descricao": "Temperatura do sensor"},
        "xmp_bloco_1:drone-dji:LRFStatus": {"original": "xmp_bloco_1:drone-dji:LRFStatus", "padronizado": "xmp_bloco_1:drone-dji:LRFStatus", "resumido": "LRFStatus", "modulo": "xmp_bloco_1", "atributo": "LRFStatus", "descricao": "Status do Laser Range Finder"},
        "xmp_bloco_1:drone-dji:LRFTargetDistance": {"original": "xmp_bloco_1:drone-dji:LRFTargetDistance", "padronizado": "xmp_bloco_1:drone-dji:LRFTargetDistance", "resumido": "LRFTargetDistance", "modulo": "xmp_bloco_1", "atributo": "LRFDist", "descricao": "Distancia do LRF(Laser Range Finder) ate o ponto central da foto no solo"},
        "xmp_bloco_1:drone-dji:LRFTargetLon": {"original": "xmp_bloco_1:drone-dji:LRFTargetLon", "padronizado": "xmp_bloco_1:drone-dji:LRFTargetLon", "resumido": "LRFTargetLon", "modulo": "xmp_bloco_1", "atributo": "LRFLong", "descricao": "Longitude medida pelo LRF(Laser Range Finder)"},
        "xmp_bloco_1:drone-dji:LRFTargetLat": {"original": "xmp_bloco_1:drone-dji:LRFTargetLat", "padronizado": "xmp_bloco_1:drone-dji:LRFTargetLat", "resumido": "LRFTargetLat", "modulo": "xmp_bloco_1", "atributo": "LRFLati", "descricao": "Latitude medida pelo LRF(Laser Range Finder)"},
        "xmp_bloco_1:drone-dji:LRFTargetAlt": {"original": "xmp_bloco_1:drone-dji:LRFTargetAlt", "padronizado": "xmp_bloco_1:drone-dji:LRFTargetAlt", "resumido": "LRFTargetAlt", "modulo": "xmp_bloco_1", "atributo": "LRFY", "descricao": "Altitude Relativa do ponto de decolagem LRF(Laser Range Finder)"},
        "xmp_bloco_1:drone-dji:LRFTargetAbsAlt": {"original": "xmp_bloco_1:drone-dji:LRFTargetAbsAlt", "padronizado": "xmp_bloco_1:drone-dji:LRFTargetAbsAlt", "resumido": "LRFTargetAbsAlt", "modulo": "xmp_bloco_1", "atributo": "LrfAbsAlt", "descricao": "Altitude Absoluta do ponto de decolagem LRF(Laser Range Finder)"},
        "xmp_bloco_1:drone-dji:WhiteBalanceCCT": {"original": "xmp_bloco_1:drone-dji:WhiteBalanceCCT", "padronizado": "xmp_bloco_1:drone-dji:WhiteBalanceCCT", "resumido": "WhiteBalanceCCT", "modulo": "xmp_bloco_1", "atributo": "WhiteBlc", "descricao": "E um valor numerico que indica a cor da luz no ambiente onde a foto foi tirada, medida em Kelvin (K)"},
        "xmp_bloco_1:drone-dji:SensorFPS": {"original": "xmp_bloco_1:drone-dji:SensorFPS", "padronizado": "xmp_bloco_1:drone-dji:SensorFPS", "resumido": "SensorFPS", "modulo": "xmp_bloco_1", "atributo": "SensorFPS", "descricao": "Taxa de quadros (frames por segundo)"},
        "EXIF:RecommendedExposureIndex": {"original": "EXIF:RecommendedExposureIndex", "padronizado": "EXIF:RecommendedExposureIndex", "resumido": "RecommendedExposureIndex", "modulo": "EXIF", "atributo": "REI", "descricao": "Indice de Exposicao Recomendado"},
        "xmp_bloco_1:drone-dji:LensPosition": {"original": "xmp_bloco_1:drone-dji:LensPosition", "padronizado": "xmp_bloco_1:drone-dji:LensPosition", "resumido": "LensPosition", "modulo": "xmp_bloco_1", "atributo": "LensPosit", "descricao": "Posicao da Lente"},
        "xmp_bloco_1:drone-dji:LensTemperature": {"original": "xmp_bloco_1:drone-dji:LensTemperature", "padronizado": "xmp_bloco_1:drone-dji:LensTemperature", "resumido": "LensTemperature", "modulo": "xmp_bloco_1", "atributo": "LensTemp", "descricao": "Temperatura da Lente"}
}
    """
