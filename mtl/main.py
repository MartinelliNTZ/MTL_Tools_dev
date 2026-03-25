
from ExifUtil import ExifUtil
from XmpUtil import XmpUtil
from Manager import Manager




def main():
    manager = Manager()

    img_path = r"G:\np\IMAGENS\1_CERRADO (1).JPG"
    folder_path = r"G:\np\IMAGENS"

    #field_lookup = _build_field_lookup_table()
    #print(f"Field lookup entries: {len(field_lookup)}\n")

    # Caminho único (arquivo)
    dicionario = manager.collect_metadata(img_path)
    print("== Metadados da imagem ==")
    #print(dicionario)

    # Caminho de pasta
    result_folder = manager.collect_metadata(folder_path)
    #print("== Metadados do diretório ==")
    print(result_folder)
    print(f"{len(result_folder)} imagens processadas")


if __name__ == "__main__":
    main()
