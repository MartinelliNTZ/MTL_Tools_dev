# -*- coding: utf-8 -*-
"""
Módulo para extração e processamento de metadados XMP em imagens.

Este módulo fornece a classe XmpUtil que encapsula todas as operações
relacionadas à extração, parsing e normalização de dados XMP contidos
em arquivos de imagem.
"""
import os
from datetime import datetime
from xml.etree import ElementTree as ET


class XmpUtil:
    """Utilitário para extrair e processar metadados XMP de arquivos de imagem.
    
    Fornece métodos estáticos para:
    - Extrair dados XMP brutos de arquivos de imagem
    - Fazer parsing do XML e extrair campos
    - Normalizar nomes de atributos com namespaces
    - Ordenar campos por prioridade
    - Consolidar metadados de arquivo e XMP
    """

    # Mapeamento de namespaces para prefixos amigáveis
    _NAMESPACE_PREFIXES = {
        "http://www.dji.com/drone-dji/1.0/": "drone-dji",
        "http://ns.adobe.com/xap/1.0/": "xmp",
        "http://purl.org/dc/elements/1.1/": "dc",
        "http://ns.adobe.com/camera-raw-settings/1.0/": "crs",
        "http://pix4d.com/camera/1.0": "Camera",
        "http://ns.adobe.com/exif/1.0/aux/": "aux",
        "http://ns.adobe.com/photoshop/1.0/": "photoshop",
        "http://ns.adobe.com/tiff/1.0/": "tiff",
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
    }

    # Ordem de prioridade para exibição de campos XMP
    _FIELD_PRIORITY = [
        "drone-dji:Version",
        "drone-dji:ImageSource",
        "drone-dji:GpsStatus",
        "drone-dji:AltitudeType",
        "drone-dji:AbsoluteAltitude",
        "drone-dji:RelativeAltitude",
        "drone-dji:GimbalRollDegree",
        "drone-dji:GimbalYawDegree",
        "drone-dji:GimbalPitchDegree",
        "drone-dji:FlightRollDegree",
        "drone-dji:FlightYawDegree",
        "drone-dji:FlightPitchDegree",
        "drone-dji:SurveyingMode",
        "drone-dji:DewarpFlag",
        "drone-dji:DewarpData",
        "drone-dji:CalibratedFocalLength",
        "drone-dji:CalibratedOpticalCenterX",
        "drone-dji:CalibratedOpticalCenterY",
        "drone-dji:UTCAtExposure",
        "drone-dji:ShutterType",
        "drone-dji:ShutterCount",
        "drone-dji:FocusDistance",
        "drone-dji:CameraSerialNumber",
        "drone-dji:DroneModel",
        "drone-dji:DroneSerialNumber",
        "drone-dji:CaptureUUID",
        "drone-dji:PictureQuality",
        "xmp:ModifyDate",
        "xmp:CreateDate",
        "xmp:CreatorTool",
        "dc:format",
    ]

    @staticmethod
    def _extract_xmp_text_raw(image_path):
        """Extrai o bloco XMP bruto do arquivo de imagem.
        
        Realiza uma busca por padrão de texto para localizar a seção <x:xmpmeta>
        dentro do arquivo de imagem.
        
        Args:
            image_path (str): Caminho do arquivo de imagem.
        
        Returns:
            str: Texto XML contendo os metadados XMP, ou None se não encontrado.
        """
        with open(image_path, "rb") as f:
            raw = f.read().decode("latin1", errors="ignore")
        
        start = raw.find("<x:xmpmeta")
        if start == -1:
            return None

        end_marker = "</x:xmpmeta>"
        end = raw.find(end_marker, start)
        if end == -1:
            return None

        end += len(end_marker)
        return raw[start:end]

    @staticmethod
    def _normalize_attribute_name(attr_name):
        """Converte nomes de atributos com namespace em formato legível.
        
        Transforma um atributo no formato {http://...}localname em prefix:localname
        usando o mapeamento de namespaces definido na classe.
        
        Args:
            attr_name (str): Nome do atributo com namespace (ex: {http://...}value)
        
        Returns:
            str: Nome normalizado no formato "prefix:localname" ou o nome original
                 se não for possível normalizar.
        """
        if not attr_name.startswith("{"):
            return attr_name

        namespace, local_name = attr_name[1:].split("}", 1)
        prefix = XmpUtil._NAMESPACE_PREFIXES.get(namespace, namespace)
        return f"{prefix}:{local_name}"

    @staticmethod
    def _parse_xmp_xml(xmp_text):
        """Faz o parsing do texto XML e extrai atributos do bloco Description.
        
        Converte o texto XMP em estrutura de dados Python, extraindo todos
        os atributos do elemento rdf:Description.
        
        Args:
            xmp_text (str): Texto XML contendo os metadados XMP.
        
        Returns:
            dict: Dicionário com campos XMP extraídos. Se houver erro,
                  retorna dicionário com chave 'xmp_erro' descrevendo o problema.
        """
        data = {}

        try:
            root = ET.fromstring(xmp_text)
        except ET.ParseError as e:
            data["xmp_erro"] = str(e)
            return data

        description = root.find(".//{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description")
        if description is None:
            data["xmp_erro"] = "Bloco rdf:Description nao encontrado"
            return data

        for attr_name, attr_value in description.attrib.items():
            data[XmpUtil._normalize_attribute_name(attr_name)] = attr_value

        return data

    @staticmethod
    def _order_fields_by_priority(xmp_data):
        """Ordena os campos XMP por prioridade predefinida.
        
        Cria um novo dicionário colocando primeiro os campos da lista de
        prioridade, seguidos pelos demais campos em ordem alfabética.
        
        Args:
            xmp_data (dict): Dicionário com dados XMP extraídos.
        
        Returns:
            dict: Dicionário ordenado com campos prioritários primeiro.
        """
        ordered = {}
        
        for key in XmpUtil._FIELD_PRIORITY:
            if key in xmp_data:
                ordered[key] = xmp_data[key]

        for key in sorted(xmp_data):
            if key not in ordered:
                ordered[key] = xmp_data[key]

        return ordered

    @staticmethod
    def _extract_file_metadata(image_path):
        """Extrai metadados do arquivo de imagem do sistema operacional.
        
        Obtém informações como tamanho, data de criação e caminho do arquivo
        usando atributos do sistema operacional.
        
        Args:
            image_path (str): Caminho do arquivo de imagem.
        
        Returns:
            dict: Dicionário contendo:
                - arquivo: Nome do arquivo
                - caminho: Caminho completo do arquivo
                - tamanho_mb: Tamanho em MB (arredondado para 2 casas)
                - data_criacao: Data de criação em formato "YYYY-MM-DD HH:MM:SS"
        """
        stat = os.stat(image_path)
        return {
            "arquivo": os.path.basename(image_path),
            "caminho": image_path,
            "tamanho_mb": round(stat.st_size / (1024 * 1024), 2),
            "data_criacao": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
        }

    @staticmethod
    def extract_metadata(image_path):
        """Extrai todos os metadados XMP de uma imagem.
        
        Funciona como o método de orquestração principal. Realiza:
        1. Extração de metadados do arquivo (SO)
        2. Extração do bloco XMP bruto
        3. Parsing e normalização dos dados XMP
        4. Ordenação por prioridade
        
        Args:
            image_path (str): Caminho do arquivo de imagem.
        
        Returns:
            dict: Dicionário consolidado com:
                - Metadados básicos do arquivo (arquivo, caminho, tamanho_mb, data_criacao)
                - xmp_encontrado: "sim" ou "nao"
                - Campos XMP extraídos (se encontrados)
                - xmp_erro: Mensagem de erro (se houver problema no parsing)
        
        Exemplo:
            >>> metadata = XmpUtil.extract_metadata('/path/to/photo.jpg')
            >>> print(metadata['xmp_encontrado'])
            sim
        """
        data = XmpUtil._extract_file_metadata(image_path)

        xmp_text = XmpUtil._extract_xmp_text_raw(image_path)
        if not xmp_text:
            data["xmp_encontrado"] = "nao"
            return data

        data["xmp_encontrado"] = "sim"

        xmp_data = XmpUtil._parse_xmp_xml(xmp_text)
        if "xmp_erro" in xmp_data:
            data.update(xmp_data)
            return data

        data.update(XmpUtil._order_fields_by_priority(xmp_data))
        return data

    @staticmethod
    def process_directory(base_folder, output_file="relatorio_xmp.txt"):
        """Processa todos os arquivos JPG em um diretório e gera relatório.
        
        Percorre recursivamente o diretório, extrai metadados XMP de todos
        os arquivos JPEG encontrados e gera um arquivo de relatório consolidado.
        
        Args:
            base_folder (str): Caminho da pasta a ser processada.
            output_file (str): Nome do arquivo de saída (padrão: "relatorio_xmp.txt")
        
        Returns:
            str: Caminho completo do arquivo de relatório gerado.
        
        Exemplo:
            >>> report_path = XmpUtil.process_directory('/path/to/images')
            >>> print(report_path)
            /path/to/images/relatorio_xmp.txt
        """
        output_path = os.path.join(base_folder, output_file)
        all_data = []

        for root, _, files in os.walk(base_folder):
            for name in sorted(files):
                if name.lower().endswith((".jpg", ".jpeg")):
                    full_path = os.path.join(root, name)
                    try:
                        all_data.append(XmpUtil.extract_metadata(full_path))
                    except Exception as e:
                        all_data.append({
                            "arquivo": name,
                            "caminho": full_path,
                            "erro": str(e),
                        })

        with open(output_path, "w", encoding="utf-8") as f:
            for i, item in enumerate(all_data, 1):
                f.write(f"{'=' * 60}\n")
                f.write(f"FOTO {i}\n")
                f.write(f"{'=' * 60}\n")
                for key, value in item.items():
                    f.write(f"{key}: {value}\n")
                f.write("\n")

        return output_path
