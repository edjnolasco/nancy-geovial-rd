from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

# ============================================================
# CONFIGURACIÓN BASE
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

DEFAULT_INPUT = ROOT / "data" / "digesett_provincias_raw.csv"
DEFAULT_OUTPUT = ROOT / "data" / "fallecimientos_provincias.csv"
CATALOG_PATH = ROOT / "data" / "provincias_rd_catalog.csv"


# ============================================================
# UTILIDADES
# ============================================================

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]

    column_map = {}

    for col in df.columns:
        if "prov" in col:
            column_map[col] = "provincia"
        elif "año" in col or "ano" in col or "year" in col:
            column_map[col] = "year"
        elif "falle" in col or "cantidad" in col or "valor" in col:
            column_map[col] = "fallecidos"

    return df.rename(columns=column_map)


def read_digesett_file(input_path: Path) -> pd.DataFrame:
    if not input_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {input_path}")

    suffix = input_path.suffix.lower()

    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(input_path)

    encodings = ["utf-8", "utf-8-sig", "latin1", "cp1252"]
    separators = [";", ",", "\t"]

    last_error = None

    for encoding in encodings:
        for sep in separators:
            try:
                df = pd.read_csv(input_path, sep=sep, encoding=encoding)
                if df.shape[1] > 1:
                    return df
            except Exception as e:
                last_error = e

    raise ValueError(f"No se pudo leer el archivo: {last_error}")


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_columns(df)

    required_cols = ["provincia", "year", "fallecidos"]
    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        raise ValueError(f"Faltan columnas requeridas: {missing}")

    out = df[required_cols].copy()

    out["provincia"] = out["provincia"].astype(str).str.strip()
    out["year"] = pd.to_numeric(out["year"], errors="coerce")
    out["fallecidos"] = pd.to_numeric(out["fallecidos"], errors="coerce")

    out = out.dropna(subset=["provincia", "year", "fallecidos"]).copy()

    out["year"] = out["year"].astype(int)
    out["fallecidos"] = out["fallecidos"].astype(int)

    out = out.sort_values(["year", "provincia"]).reset_index(drop=True)

    return out


# ============================================================
# VALIDACIÓN TERRITORIAL
# ============================================================

def load_catalog() -> pd.DataFrame:
    if not CATALOG_PATH.exists():
        raise FileNotFoundError(f"No se encontró el catálogo: {CATALOG_PATH}")

    catalog = pd.read_csv(CATALOG_PATH)

    if "provincia" not in catalog.columns:
        raise ValueError("El catálogo debe tener columna 'provincia'")

    catalog["provincia"] = catalog["provincia"].astype(str).str.strip()
    return catalog.drop_duplicates()


def validate_coverage(df: pd.DataFrame) -> dict:
    catalog = load_catalog()

    expected = set(catalog["provincia"])
    observed = set(df["provincia"])

    missing = sorted(expected - observed)
    extra = sorted(observed - expected)

    return {
        "expected": len(expected),
        "observed": len(observed),
        "missing": missing,
        "extra": extra,
        "is_complete": len(missing) == 0,
    }


def print_validation_report(report: dict):
    print("\n=== VALIDACIÓN TERRITORIAL ===")

    print(f"Esperadas: {report['expected']}")
    print(f"Observadas: {report['observed']}")

    if report["is_complete"]:
        print("[OK] Cobertura completa")
    else:
        print("[WARNING] Cobertura parcial")

    if report["missing"]:
        print(f"Faltantes ({len(report['missing'])}):")
        for p in report["missing"]:
            print(" -", p)

    if report["extra"]:
        print(f"Extras ({len(report['extra'])}):")
        for p in report["extra"]:
            print(" -", p)

    print("================================\n")


# ============================================================
# CORE
# ============================================================

def convert_digesett_csv(
    input_path: Path,
    output_path: Path,
    validate: bool = False,
    fail_on_incomplete: bool = False,
) -> Path:
    print(f"[INFO] Leyendo archivo: {input_path}")

    raw_df = read_digesett_file(input_path)
    print(f"[INFO] Columnas: {list(raw_df.columns)}")
    print(f"[INFO] Shape original: {raw_df.shape}")

    clean_df = clean_dataset(raw_df)
    print(f"[INFO] Shape limpio: {clean_df.shape}")

    # VALIDACIÓN
    if validate:
        report = validate_coverage(clean_df)
        print_validation_report(report)

        if fail_on_incomplete and not report["is_complete"]:
            raise ValueError("Cobertura territorial incompleta")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    clean_df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"[OK] Archivo guardado en: {output_path}")

    return output_path


# ============================================================
# CLI
# ============================================================

def build_parser():
    parser = argparse.ArgumentParser(description="Conversor DIGESETT → CSV limpio DSS")

    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)

    parser.add_argument(
        "--validate",
        action="store_true",
        help="Valida cobertura territorial contra catálogo"
    )

    parser.add_argument(
        "--fail-on-incomplete",
        action="store_true",
        help="Falla si faltan provincias (útil para CI)"
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        convert_digesett_csv(
            args.input,
            args.output,
            validate=args.validate,
            fail_on_incomplete=args.fail_on_incomplete
        )
        return 0
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

