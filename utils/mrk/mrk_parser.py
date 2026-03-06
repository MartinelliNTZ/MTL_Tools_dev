# -*- coding: utf-8 -*-
import os
import re


class MrkParser:

    LINE_RE = re.compile(
        r"(?P<foto>\d+).*?"
        r"(?P<lat>-?\d+\.\d+),Lat.*?"
        r"(?P<lon>-?\d+\.\d+),Lon.*?"
        r"(?P<alt>-?\d+(\.\d+)?),Ellh",
        re.IGNORECASE
    )

    @staticmethod
    def _extract_file_metadata(file_name: str) -> dict:
        """Extrai numdovoo e nomedovoo do nome do arquivo MRK."""
        match = re.search(
            r"DJI_\d+_(?P<numdovoo>\d+?)_(?P<nomedovoo>[^_]+?)_Timestamp",
            file_name,
            re.IGNORECASE,
        )
        if not match:
            return {"numdovoo": None, "nomedovoo": None}
        return {
            "numdovoo": match.group("numdovoo"),
            "nomedovoo": match.group("nomedovoo"),
        }

    @staticmethod
    def parse_folder(folder, recursive=True, extra_fields=None):
        """Lê todos os MRKs de uma pasta e retorna lista de pontos."""
        points = []

        for root, _, files in os.walk(folder):
            for f in files:
                if not f.lower().endswith(".mrk"):
                    continue

                # Relativo à pasta base para extrair pastas de nível 1/2
                rel_dir = os.path.relpath(root, folder)
                if rel_dir == ".":
                    rel_dir = ""
                parts = [p for p in rel_dir.split(os.sep) if p] if rel_dir else []
                pasta1 = parts[0] if len(parts) > 0 else None
                pasta2 = parts[1] if len(parts) > 1 else None

                # Extrai metadados do nome do arquivo MRK (numdovoo e nomedovoo)
                file_meta = MrkParser._extract_file_metadata(f)

                with open(os.path.join(root, f), "r", encoding="utf-8", errors="ignore") as fh:
                    for line in fh:
                        m = MrkParser.LINE_RE.search(line)
                        if not m:
                            continue

                        data_mrk = None
                        # extrai data do nome do MRK: DJI_YYYYMMDDHHMM_...
                        m_date = re.search(r"DJI_(\d{8})", f)
                        if m_date:
                            data_mrk = m_date.group(1)

                        points.append({
                            "foto": int(m.group("foto")),
                            "lat": float(m.group("lat")),
                            "lon": float(m.group("lon")),
                            "alt": float(m.group("alt")),
                            "data_name": data_mrk,
                            "folder": root,
                            "mrk_file": f,
                            "mrk_path": os.path.join(root, f),
                            "numdovoo": file_meta.get("numdovoo"),
                            "nomedovoo": file_meta.get("nomedovoo"),
                            "pasta1": pasta1,
                            "pasta2": pasta2,
                        })

            if not recursive:
                break

        return points

    @staticmethod
    def to_point_layer(points, name="MRK_Pontos", extra_fields=None):
        """[Deprecated] Cria uma camada de pontos a partir da lista de pontos.

        Use VectorLayerGeometry.create_point_layer_from_dicts() para comportamentos mais flexíveis.
        """
        from ..vector.VectorLayerGeometry import VectorLayerGeometry

        return VectorLayerGeometry.create_point_layer_from_dicts(
            points=points,
            name=name,
            extra_fields=extra_fields,
        )
