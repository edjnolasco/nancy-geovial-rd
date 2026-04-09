from __future__ import annotations

from typing import Dict, List

import pandas as pd


def load_catalog() -> pd.DataFrame:
    """
    Load province catalog.
    En producción se implementará.
    En tests será mockeado.
    """
    raise NotImplementedError("Catalog loading not implemented.")


def validate_province_coverage(df: pd.DataFrame) -> Dict[str, List[str] | bool]:
    """
    Compare dataset provinces against catalog.
    """
    if "provincia" not in df.columns:
        raise ValueError("Column 'provincia' is required")

    catalog_df = load_catalog()

    catalog = set(catalog_df["provincia"].astype(str))

    # ⚠️ IMPORTANTE: no lanzar error si está vacío
    if df.empty:
        return {
            "missing": sorted(list(catalog)),
            "extra": [],
            "is_complete": False,
        }

    data = set(df["provincia"].astype(str))

    missing = sorted(list(catalog - data))
    extra = sorted(list(data - catalog))

    is_complete = len(missing) == 0

    return {
        "missing": missing,
        "extra": extra,
        "is_complete": is_complete,
    }
