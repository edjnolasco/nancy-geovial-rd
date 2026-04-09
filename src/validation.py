from __future__ import annotations

from typing import Any

import pandas as pd


def load_catalog() -> pd.DataFrame:
    raise NotImplementedError("Catalog loading not implemented.")


def validate_province_coverage(df: pd.DataFrame) -> dict[str, Any]:
    if "provincia" not in df.columns:
        raise ValueError("Column 'provincia' is required")

    catalog_df = load_catalog()
    catalog = set(catalog_df["provincia"].astype(str))
    expected = len(catalog)

    # ⚠️ IMPORTANTE: NO lanzar error si está vacío
    if df.empty:
        return {
            "missing": sorted(list(catalog)),
            "extra": [],
            "is_complete": False,
            "expected": expected,
            "observed": 0,
        }

    observed_values = set(df["provincia"].astype(str))
    observed = len(observed_values)

    missing = sorted(list(catalog - observed_values))
    extra = sorted(list(observed_values - catalog))
    is_complete = len(missing) == 0

    return {
        "missing": missing,
        "extra": extra,
        "is_complete": is_complete,
        "expected": expected,
        "observed": observed,
    }
