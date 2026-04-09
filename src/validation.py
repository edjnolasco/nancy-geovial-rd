from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import pandas as pd


def load_catalog() -> pd.DataFrame:
    """
    Load province catalog.
    En producción esto leerá un archivo.
    En tests será mockeado.
    """
    raise NotImplementedError("Catalog loading not implemented.")


def validate_province_coverage(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Compare dataset provinces against catalog.

    Returns:
        {
            "missing": [...],
            "extra": [...]
        }
    """
    if "provincia" not in df.columns:
        raise ValueError("Column 'provincia' is required")

    if df.empty:
        raise ValueError("Input dataset is empty")

    catalog_df = load_catalog()

    catalog = set(catalog_df["provincia"].astype(str))
    data = set(df["provincia"].astype(str))

    missing = sorted(list(catalog - data))
    extra = sorted(list(data - catalog))

    return {
        "missing": missing,
        "extra": extra,
    }
