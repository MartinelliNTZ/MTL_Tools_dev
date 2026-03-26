    
"""
Módulo para extração de metadados de imagens.

Este módulo fornece utilitários para extrair informações de metadados de arquivos de imagem
através de três abordagens: metadados do sistema operacional, propriedades da imagem e dados EXIF.
"""
from datetime import datetime
import os
from PIL import ExifTags, Image


class ExifUtil:
    """Utilitário para extrair metadados de arquivos de imagem.
    
    Fornece métodos estáticos para extrair informações de metadados de imagens
    de múltiplas fontes: sistema operacional, propriedades PIL e dados EXIF.
    """
    @staticmethod
    def extract_metadata_os(image_path):
        """Extrai metadados do sistema operacional do arquivo de imagem.
        
        Extrai informações como nome do arquivo, caminho, tamanho e data de criação
        utilizando os atributos do sistema operacional.
        
        Args:
            image_path (str): Caminho completo ou relativo do arquivo de imagem.
        
        Returns:
            dict: Dicionário contendo os seguintes campos:
                - file (str): Nome do arquivo
                - path (str): Caminho completo do arquivo
                - size_mb (float): Tamanho do arquivo em MB (arredondado para 2 casas decimais)
                - os_date (str): Data de criação/modificação no formato "YYYY-MM-DD HH:MM:SS"
        
        Exemplo:
            >>> metadata = ExifUtil.extract_metadata_os('/path/to/image.jpg')
            >>> print(metadata['size_mb'])
            2.45
        """
        data = {}
        try:            
            stat = os.stat(image_path)            
            data["file"] = os.path.basename(image_path)
            data["path"] = image_path
            data["size_mb"] = round(stat.st_size / (1024 * 1024), 2)
            data["os_date"] = datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
           #print(f"Processando: {stat}")
        except Exception as exc:
            print(f"Erro ao extrair metadados do sistema para {image_path}: {exc}")            
        return data 
    @staticmethod
    def extract_metadata_image(image_path):
        """Extrai propriedades técnicas da imagem usando PIL.
        
        Utiliza a biblioteca PIL/Pillow para extrair informações sobre dimensões,
        formato e resolução da imagem.
        
        Args:
            image_path (str): Caminho completo ou relativo do arquivo de imagem.
        
        Returns:
            dict: Dicionário contendo os seguintes campos:
                - width_px (int): Largura da imagem em pixels
                - height_px (int): Altura da imagem em pixels
                - format (str): Formato da imagem com modo de cor (ex: "JPEG_RGB" ou "PNG_RGBA")
                - dpi (str): Resolução em DPI no formato "dpi_x x dpi_y" (se disponível)
        
        Nota:
            Se a imagem não contiver informações de DPI, este campo será omitido do dicionário.
        
        Exemplo:
            >>> metadata = ExifUtil.extract_metadata_image('/path/to/image.jpg')
            >>> print(metadata['width_px'], metadata['height_px'])
            1920 1080
        """
        data = {}   
        try:
            with Image.open(image_path) as img:
                data["width_px"], data["height_px"] = img.size                
                data["format"] = f"{img.format}_{img.mode}"
                dpi = img.info.get("dpi")
                if dpi:
                    d1, d2 = dpi
                    data["dpi"]= f"{d1}x{d2}"                
                #print(f"Processando: {img.info}")               
                
        except Exception as exc:      
            print(f"Erro ao extrair metadados PIL para {image_path}: {exc}") 
              
        return data 
    @staticmethod       
    def extract_metadata_exif(image_path):
        """Extrai dados EXIF da imagem.
        
        Extrai todos os metadados EXIF embutidos no arquivo de imagem, incluindo
        informações de câmera, data de captura, GPS (se disponível) e outros dados técnicos.
        
        Args:
            image_path (str): Caminho completo ou relativo do arquivo de imagem.
        
        Returns:
            dict: Dicionário contendo pares chave-valor dos dados EXIF encontrados.
                A chave é o nome do campo EXIF (ex: "DateTime", "Model", "GPSInfo")
                e o valor contém o dado correspondente.
                
                Em caso de erro de leitura, retorna um dicionário com chave 'erro'
                contendo a mensagem de erro.
        
        Nota:
            - Imagens sem dados EXIF retornarão um dicionário vazio ou apenas com erro.
            - Campos EXIF podem conter valores complexos (tuplas, dicionários).
        
        Exemplo:
            >>> metadata = ExifUtil.extract_metadata_exif('/path/to/photo.jpg')
            >>> print(metadata.get('DateTime'))
            2024:03:15 14:30:45
        """
        data = {}
        try:    
            with Image.open(image_path) as img:
                exif_raw = img._getexif() or {}
                exif = {ExifTags.TAGS.get(k, k): v for k, v in exif_raw.items()}        
                for key, value in exif.items():
                    data[key] = value
                    
                #print(f"Processando: {data}")
        except Exception as exc:
            data["erro"] = str(exc)
        return data
