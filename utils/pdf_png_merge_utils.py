import os

HAS_PYPDF2 = False
HAS_PIL = False

try:
    from PyPDF2 import PdfMerger
    HAS_PYPDF2 = True
except ImportError:
    PdfMerger = None

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    Image = None


def merge_pdfs(pdf_list, output_pdf):
    """
    Retorna (success: bool, message: str)
    """
    if not HAS_PYPDF2:
        return False, "PyPDF2 não está instalada."

    if not pdf_list:
        return False, "Nenhum PDF foi informado para união."

    merger = PdfMerger()

    for pdf in pdf_list:
        if os.path.exists(pdf):
            merger.append(pdf)

    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    merger.write(output_pdf)
    merger.close()

    return True, f"PDF final criado em: {output_pdf}"


def merge_pngs_to_pdf(png_list, output_pdf, max_width=3500):
    """
    Retorna (success: bool, message: str)
    """
    if not HAS_PIL:
        return False, "Pillow não está instalada."

    if not png_list:
        return False, "Nenhum PNG foi informado para união."

    pil_images = []

    for path in png_list:
        if not os.path.exists(path):
            continue

        img = Image.open(path).convert("RGB")
        w, h = img.size

        if w > max_width:
            ratio = max_width / float(w)
            new_h = int(h * ratio)
            img = img.resize((max_width, new_h), Image.LANCZOS)

        pil_images.append(img)

    if not pil_images:
        return False, "Nenhuma imagem válida para unir."

    first, rest = pil_images[0], pil_images[1:]
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    first.save(output_pdf, save_all=True, append_images=rest)

    return True, f"PDF unido a partir de PNG criado em: {output_pdf}"
