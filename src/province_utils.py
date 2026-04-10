from __future__ import annotations

import re
import unicodedata


PROVINCE_ALIASES = {
    "azua": "Azua",
    "bahoruco": "Bahoruco",
    "barahona": "Barahona",
    "dajabon": "Dajabón",
    "distrito nacional": "Distrito Nacional",
    "distritonacional": "Distrito Nacional",
    "duarte": "Duarte",
    "espaillat": "Espaillat",
    "hato mayor": "Hato Mayor",
    "hatomayor": "Hato Mayor",
    "independencia": "Independencia",
    "la altagracia": "La Altagracia",
    "laaltagracia": "La Altagracia",
    "la romana": "La Romana",
    "laromana": "La Romana",
    "la vega": "La Vega",
    "lavega": "La Vega",
    "maria trinidad sanchez": "María Trinidad Sánchez",
    "mariatrinidadsanchez": "María Trinidad Sánchez",
    "monsenor nouel": "Monseñor Nouel",
    "monsenornouel": "Monseñor Nouel",
    "monte cristi": "Monte Cristi",
    "montecristi": "Monte Cristi",
    "monte plata": "Monte Plata",
    "monteplata": "Monte Plata",
    "pedernales": "Pedernales",
    "peravia": "Peravia",
    "puerto plata": "Puerto Plata",
    "puertoplata": "Puerto Plata",
    "samana": "Samaná",
    "san cristobal": "San Cristóbal",
    "sancristobal": "San Cristóbal",
    "san jose de ocoa": "San José de Ocoa",
    "sanjosedeocoa": "San José de Ocoa",
    "san juan": "San Juan",
    "sanjuan": "San Juan",
    "san pedro de macoris": "San Pedro de Macorís",
    "sanpedrodemacoris": "San Pedro de Macorís",
    "sanchez ramirez": "Sánchez Ramírez",
    "sanchezramirez": "Sánchez Ramírez",
    "santiago": "Santiago",
    "santiago rodriguez": "Santiago Rodríguez",
    "santiagorodriguez": "Santiago Rodríguez",
    "santo domingo": "Santo Domingo",
    "santodomingo": "Santo Domingo",
    "valverde": "Valverde",
    # =========================
    # Casos especiales GADM / históricos
    # =========================
    # El Seibo
    "el seibo": "El Seibo",
    "elseibo": "El Seibo",
    "el seybo": "El Seibo",
    "elseybo": "El Seibo",
    # Elías Piña
    "elias pina": "Elías Piña",
    "eliaspina": "Elías Piña",
    "laestrelleta": "Elías Piña",
    "la estrelleta": "Elías Piña",
    # Hermanas Mirabal (Salcedo histórico)
    "hermanas mirabal": "Hermanas Mirabal",
    "hermanasmirabal": "Hermanas Mirabal",
    "salcedo": "Hermanas Mirabal",
}


def _strip_accents(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def normalize_text(s: str) -> str:
    text = str(s).strip()

    # Normalización Unicode real
    text = unicodedata.normalize("NFKC", text)

    # Quitar acentos/diacríticos
    text = _strip_accents(text)

    # Minúsculas
    text = text.lower()

    # Convertir cualquier bloque de espacios/tabs/non-breaking spaces a un solo espacio
    text = re.sub(r"\s+", " ", text, flags=re.UNICODE).strip()

    return text


def canonical_province(name: str) -> str:
    norm = normalize_text(name)
    compact = norm.replace(" ", "")

    if norm in PROVINCE_ALIASES:
        return PROVINCE_ALIASES[norm]

    if compact in PROVINCE_ALIASES:
        return PROVINCE_ALIASES[compact]

    return str(name).strip()


def province_key(name: str) -> str:
    canon = canonical_province(name)
    norm = normalize_text(canon)
    return norm.replace(" ", "_")
