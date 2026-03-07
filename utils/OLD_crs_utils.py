# -*- coding: utf-8 -*-
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject
)
import math

# Letras UTM (C–X, sem I e O)
UTM_LETTERS = "CDEFGHJKLMNPQRSTUVWX"


def decimal_to_dms(value):
    sign = "-" if value < 0 else ""
    value = abs(value)
    deg = int(value)
    minutes_full = (value - deg) * 60
    minutes = int(minutes_full)
    seconds = (minutes_full - minutes) * 60
    return f"{sign}{deg}°{minutes}'{seconds:.3f}\""


def utm_zone_from_lon(lon):
    return int((lon + 180) / 6) + 1


def utm_letter_from_lat(lat):
    if lat < -80 or lat > 84:
        return ""
    index = int((lat + 80) / 8)
    return UTM_LETTERS[index]


def transform_point(point, source_crs, target_crs):
    transform = QgsCoordinateTransform(
        source_crs,
        target_crs,
        QgsProject.instance()
    )
    return transform.transform(point)


def get_coord_info(point, canvas_crs):
    # WGS84
    crs_wgs = QgsCoordinateReferenceSystem("EPSG:4326")
    p_wgs = transform_point(point, canvas_crs, crs_wgs)

    lon = p_wgs.x()
    lat = p_wgs.y()

    zona = utm_zone_from_lon(lon)
    letra = utm_letter_from_lat(lat)

    # SIRGAS 2000 UTM
    epsg_utm_sirgas = 31960 + zona
    crs_utm_sirgas = QgsCoordinateReferenceSystem(f"EPSG:{epsg_utm_sirgas}")
    p_utm_sirgas = transform_point(point, canvas_crs, crs_utm_sirgas)

    hemisferio = "Sul" if lat < 0 else "Norte"

    return {
        "lat": lat,
        "lon": lon,
        "lat_dms": decimal_to_dms(lat),
        "lon_dms": decimal_to_dms(lon),
        "utm_x": p_utm_sirgas.x(),
        "utm_y": p_utm_sirgas.y(),
        "zona_num": zona,
        "zona_letra": letra,
        "hemisferio": hemisferio,
        "epsg": epsg_utm_sirgas
    }
