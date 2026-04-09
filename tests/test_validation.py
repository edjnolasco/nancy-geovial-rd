import pandas as pd
import pytest

from src.validation import validate_province_coverage


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def mock_catalog(monkeypatch, provincias):
    """
    Reemplaza load_catalog() para no depender de archivos reales.
    """
    import src.validation as validation_module

    df = pd.DataFrame({"provincia": provincias})

    monkeypatch.setattr(
        validation_module,
        "load_catalog",
        lambda: df
    )


# ------------------------------------------------------------
# Tests
# ------------------------------------------------------------

def test_validation_complete_coverage(monkeypatch):
    provincias = ["A", "B", "C"]

    mock_catalog(monkeypatch, provincias)

    df = pd.DataFrame({
        "provincia": ["A", "B", "C"]
    })

    result = validate_province_coverage(df)

    assert result["is_complete"] is True
    assert result["expected"] == 3
    assert result["observed"] == 3
    assert result["missing"] == []
    assert result["extra"] == []


def test_validation_missing_provinces(monkeypatch):
    catalog = ["A", "B", "C"]
    mock_catalog(monkeypatch, catalog)

    df = pd.DataFrame({
        "provincia": ["A", "B"]
    })

    result = validate_province_coverage(df)

    assert result["is_complete"] is False
    assert result["missing"] == ["C"]
    assert result["extra"] == []


def test_validation_extra_provinces(monkeypatch):
    catalog = ["A", "B"]
    mock_catalog(monkeypatch, catalog)

    df = pd.DataFrame({
        "provincia": ["A", "B", "X"]
    })

    result = validate_province_coverage(df)

    assert result["is_complete"] is True  # no faltan
    assert result["missing"] == []
    assert result["extra"] == ["X"]


def test_validation_missing_and_extra(monkeypatch):
    catalog = ["A", "B", "C"]
    mock_catalog(monkeypatch, catalog)

    df = pd.DataFrame({
        "provincia": ["A", "X"]
    })

    result = validate_province_coverage(df)

    assert result["is_complete"] is False
    assert result["missing"] == ["B", "C"]
    assert result["extra"] == ["X"]


def test_validation_requires_provincia_column(monkeypatch):
    catalog = ["A", "B"]
    mock_catalog(monkeypatch, catalog)

    df = pd.DataFrame({
        "otra_columna": ["A"]
    })

    with pytest.raises(ValueError):
        validate_province_coverage(df)


def test_validation_handles_duplicates(monkeypatch):
    catalog = ["A", "B"]
    mock_catalog(monkeypatch, catalog)

    df = pd.DataFrame({
        "provincia": ["A", "A", "B", "B"]
    })

    result = validate_province_coverage(df)

    assert result["is_complete"] is True
    assert result["observed"] == 2


def test_validation_empty_dataset(monkeypatch):
    catalog = ["A", "B"]
    mock_catalog(monkeypatch, catalog)

    df = pd.DataFrame({
        "provincia": []
    })

    result = validate_province_coverage(df)

    assert result["is_complete"] is False
    assert result["missing"] == ["A", "B"]
