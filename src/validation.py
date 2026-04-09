from __future__ import annotations

from pathlib import Path

import pandas as pd

from .province_utils import canonical_province

def load_province_catalog() -> pd.DataFrame:
    root = Path(__file__).resolve().parents[1]
    catalog_path = root / "data" / "provincias_rd_catalog.csv"

    if not catalog_path.exists():
        raise FileNotFoundError(
            f"No se encontró el catálogo de provincias en: {catalog_path}"
        )

    catalog = pd.read_csv(catalog_path)

    if "provincia" not in catalog.columns:
        raise ValueError("El catálogo debe contener la columna 'provincia'.")

    catalog["provincia"] = catalog["provincia"].astype(str).apply(canonical_province)
    catalog = (
    catalog[["provincia"]]
    .drop_duplicates()
    .sort_values("provincia")
    .reset_index(drop=True)
)

    return catalog


def validate_province_coverage(df: pd.DataFrame) -> dict:
    """
    Valida la cobertura territorial del dataset cargado.
    Requiere una columna 'provincia'.
    """
    if "provincia" not in df.columns:
        raise ValueError("El dataframe no contiene la columna 'provincia'.")

    catalog_df = load_province_catalog()

    expected = set(catalog_df["provincia"].astype(str).tolist())
    observed = set(df["provincia"].dropna().astype(str).apply(canonical_province).tolist())

    missing = sorted(expected - observed)
    extra = sorted(observed - expected)

    return {
        "expected_count": len(expected),
        "observed_count": len(observed),
        "coverage_ratio": round(len(observed) / len(expected), 4) if expected else 0.0,
        "missing_provinces": missing,
        "extra_provinces": extra,
        "is_complete": len(missing) == 0,
    }
