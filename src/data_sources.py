from __future__ import annotations

import csv
from io import BytesIO
from pathlib import Path

import pandas as pd
import requests

from .province_utils import canonical_province, normalize_text


# ============================================================
# URLS
# ============================================================

OFFICIAL_PROVINCES_URL = (
    "http://digesett.gob.do/transparencia/index.php/estadisticas/"
    "category/359-datos-abiertos?download=417:fallecimientos-segun-provincia&start=20"
)

PROVINCES_GEOJSON_URL = (
    "https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_DOM_1.json"
)


# ============================================================
# SINÓNIMOS DE COLUMNAS
# ============================================================

PROVINCE_SYNONYMS = ["provincia", "provincias", "province"]
YEAR_SYNONYMS = ["año", "ano", "year"]
VALUE_SYNONYMS = ["fallecidos", "fallecimiento", "cantidad", "total_fallecidos", "valor"]


# ============================================================
# DETECCIÓN AUTOMÁTICA DE CSV
# ============================================================

def detect_csv_delimiter(sample_text: str) -> str:
    """
    Detecta el delimitador del CSV usando csv.Sniffer.
    Si falla, aplica heurística simple.
    """
    try:
        dialect = csv.Sniffer().sniff(sample_text, delimiters=[",", ";", "\t", "|"])
        return dialect.delimiter
    except Exception:
        first_line = sample_text.splitlines()[0] if sample_text.splitlines() else ""
        delimiter_counts = {
            ",": first_line.count(","),
            ";": first_line.count(";"),
            "\t": first_line.count("\t"),
            "|": first_line.count("|"),
        }
        return max(delimiter_counts, key=delimiter_counts.get)


def read_csv_with_auto_detection(content: bytes) -> pd.DataFrame:
    """
    Lee un CSV detectando automáticamente delimitador y tolerando encodings comunes.
    """
    encodings_to_try = ["utf-8", "utf-8-sig", "latin1", "cp1252"]

    last_error = None

    for encoding in encodings_to_try:
        try:
            text = content.decode(encoding)
            sample = "\n".join(text.splitlines()[:10])
            delimiter = detect_csv_delimiter(sample)

            return pd.read_csv(
                BytesIO(content),
                sep=delimiter,
                encoding=encoding,
            )
        except Exception as e:
            last_error = e

    raise ValueError(f"No se pudo leer el CSV automáticamente: {last_error}")


def read_local_csv_with_auto_detection(path: str | Path) -> pd.DataFrame:
    """
    Lee un CSV local detectando delimitador y encoding automáticamente.
    """
    path = Path(path)
    content = path.read_bytes()
    return read_csv_with_auto_detection(content)


# ============================================================
# LECTURA DE ARCHIVOS
# ============================================================

def read_dataframe_from_bytes(
    content: bytes,
    filename_hint: str = "dataset.csv",
) -> pd.DataFrame:
    """
    Lee un DataFrame desde bytes.
    Soporta CSV, XLSX y XLS.
    """
    hint = filename_hint.lower()

    if hint.endswith(".xlsx") or hint.endswith(".xls"):
        return pd.read_excel(BytesIO(content))

    return read_csv_with_auto_detection(content)


def load_local_dataframe(path: str | Path) -> pd.DataFrame:
    """
    Carga un DataFrame desde una ruta local.
    Soporta CSV, XLSX y XLS.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo local: {path}")

    if path.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(path)

    return read_local_csv_with_auto_detection(path)


# ============================================================
# DESCARGA REMOTA
# ============================================================

def fetch_remote_dataframe(
    url: str,
    filename_hint: str = "dataset.csv",
    timeout: int = 30,
) -> pd.DataFrame:
    """
    Descarga un archivo tabular remoto y lo convierte en DataFrame.
    """
    response = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    response.raise_for_status()

    return read_dataframe_from_bytes(response.content, filename_hint)


def fetch_geojson_text(
    url: str = PROVINCES_GEOJSON_URL,
    timeout: int = 30,
) -> str:
    """
    Descarga un GeoJSON remoto y devuelve su contenido como texto.
    """
    response = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    response.raise_for_status()

    return response.text


# ============================================================
# UTILIDADES DE COLUMNAS
# ============================================================

def find_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """
    Busca una columna por nombre usando normalización defensiva.
    """
    normalized_map = {normalize_text(col): col for col in df.columns}

    for candidate in candidates:
        norm_candidate = normalize_text(candidate)
        if norm_candidate in normalized_map:
            return normalized_map[norm_candidate]

    return None


# ============================================================
# NORMALIZACIÓN DEL DATASET OFICIAL
# ============================================================

def normalize_official_provinces(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza el dataset oficial de provincias a la estructura esperada
    por el pipeline del DSS.

    Entrada esperada (con variantes toleradas):
    - provincia / provincias
    - año / ano / year
    - fallecidos / cantidad / valor / etc.

    Salida:
    - provincia
    - year
    - fallecidos
    - month
    - fecha
    """
    work = df.copy()

    work.columns = [normalize_text(col) for col in work.columns]

    province_col = find_column(work, PROVINCE_SYNONYMS)
    year_col = find_column(work, YEAR_SYNONYMS)
    value_col = find_column(work, VALUE_SYNONYMS)

    if not province_col or not year_col or not value_col:
        raise ValueError(
            "No fue posible identificar columnas equivalentes a "
            "'provincia', 'año/year' y 'fallecidos'."
        )

    out = work[[province_col, year_col, value_col]].copy()
    out.columns = ["provincia", "year", "fallecidos"]

    out["provincia"] = out["provincia"].astype(str).map(canonical_province)
    out["year"] = pd.to_numeric(out["year"], errors="coerce")
    out["fallecidos"] = pd.to_numeric(out["fallecidos"], errors="coerce")

    out = out.dropna(subset=["provincia", "year", "fallecidos"]).copy()

    out["year"] = out["year"].astype(int)
    out["month"] = 1
    out["fecha"] = pd.to_datetime(
        dict(year=out["year"], month=out["month"], day=1)
    )

    out = out.sort_values(["year", "provincia"]).reset_index(drop=True)

    return out

