# -*- coding: utf-8 -*-
"""
MÓDULO DEPRECATED - Usar PDFUtils e DependenciesManager ao invés

Este módulo foi substituído por:
- PDFUtils: lógica de merge com logging completo
- DependenciesManager: validação e instalação de dependências

Mantido apenas para compatibilidade com código legado.
"""

import warnings
from .DependenciesManager import DependenciesManager
from .PDFUtils import PDFUtils

warnings.warn(
    "pdf_png_merge_utils está deprecated. Use PDFUtils e DependenciesManager ao invés.",
    DeprecationWarning,
    stacklevel=2
)

# Backward compatibility
HAS_PYPDF2 = DependenciesManager.check_dependency('PyPDF2')
HAS_PIL = DependenciesManager.check_dependency('Pillow')


def merge_pdfs(pdf_list, output_pdf):
    """Deprecated: Use PDFUtils.merge_pdfs() ao invés."""
    warnings.warn(
        "merge_pdfs() está deprecated. Use PDFUtils.merge_pdfs() ao invés.",
        DeprecationWarning,
        stacklevel=2
    )
    return PDFUtils.merge_pdfs(pdf_list, output_pdf)


def merge_pngs_to_pdf(png_list, output_pdf, max_width=3500):
    """Deprecated: Use PDFUtils.merge_pngs_to_pdf() ao invés."""
    warnings.warn(
        "merge_pngs_to_pdf() está deprecated. Use PDFUtils.merge_pngs_to_pdf() ao invés.",
        DeprecationWarning,
        stacklevel=2
    )
    return PDFUtils.merge_pngs_to_pdf(png_list, output_pdf, max_width)


def install_pypdf2():
    """Deprecated: Use DependenciesManager.install_dependency() ao invés."""
    return DependenciesManager.install_dependency('PyPDF2')


def install_pillow():
    """Deprecated: Use DependenciesManager.install_dependency() ao invés."""
    return DependenciesManager.install_dependency('Pillow')
