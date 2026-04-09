# Architecture – NANCY GeoVial RD

## 1. Overview

NANCY GeoVial RD is a decision support system (DSS) for identifying, ranking, and visualizing territorial hotspots of road-traffic mortality in the Dominican Republic.

The system combines:

- official data ingestion
- predictive modeling
- DSS decision rules
- geospatial visualization
- report/export features

---

## 2. Architectural style

The project follows a modular architecture with clear separation of responsibilities:

- data layer
- feature engineering layer
- modeling layer
- DSS rules layer
- visualization layer
- export/reporting layer

This makes the system easier to maintain, test, and extend.

---

## 3. Main components

## 3.1 Data ingestion

Responsible for:

- reading raw CSV and Excel files
- handling delimiter and encoding differences
- loading local and uploaded datasets
- normalizing official DIGESETT inputs

Main modules:

- `src/data_sources.py`
- `scripts/convert_digesett_csv.py`

---

## 3.2 Data validation

Responsible for:

- validating territorial coverage
- detecting missing provinces
- detecting extra or inconsistent province names
- ensuring the dataset is usable before model execution

Main module:

- `src/validation.py`

---

## 3.3 Province normalization

Responsible for:

- canonical province naming
- historical alias resolution
- GeoJSON matching keys
- compatibility with official and geospatial data sources

Main module:

- `src/province_utils.py`

---

## 3.4 Feature engineering

Responsible for:

- temporal lags
- rolling statistics
- trend-related variables
- target construction for next-period prediction

Main module:

- `src/features.py`

---

## 3.5 Modeling

Responsible for:

- training the predictive model
- scoring the dataset
- computing prediction-based risk values
- producing normalized risk scores

Main module:

- `src/modeling.py`

---

## 3.6 DSS logic

Responsible for:

- converting model outputs into interpretable decision categories
- applying explicit rules
- generating operational prioritization labels

Main module:

- `src/rules.py`

---

## 3.7 Metrics and explainability

Responsible for:

- ranking evaluation
- Top-K metrics
- model explainability
- global feature importance

Main modules:

- `src/metrics.py`
- `src/explain.py`

---

## 3.8 Narrative generation

Responsible for:

- producing an executive textual summary
- translating technical outputs into decision-oriented interpretation

Main module:

- `src/narrative.py`

---

## 3.9 Orchestration pipeline

Responsible for:

- executing the full DSS workflow
- integrating all internal components
- returning a single structured result to the app

Main module:

- `src/pipeline.py`

---

## 3.10 User interface

Responsible for:

- source selection
- data upload
- KPI display
- ranking view
- metrics view
- explainability view
- geospatial map
- export actions

Main module:

- `app/app.py`

---

## 4. High-level flow

```text
Raw data
   ↓
Data ingestion
   ↓
Province normalization
   ↓
Territorial validation
   ↓
Feature engineering
   ↓
Predictive model
   ↓
DSS rules
   ↓
Ranking + metrics + explainability + narrative
   ↓
Map + tables + exports
```

---

## 5. Data assets

```text
data/
├── raw/
├── clean/
├── catalog/
├── geo/
└── outputs/
```

Purpose:

- `raw/`: original files
- `clean/`: normalized datasets
- `catalog/`: reference province catalog
- `geo/`: geospatial boundaries
- `outputs/`: generated results

---

## 6. Execution model

The system currently runs as a local Streamlit application.

Execution entry point:

```bash
streamlit run app/app.py
```

Data preparation entry point:

```bash
python scripts/convert_digesett_csv.py --validate
```

---

## 7. CI/CD integration

The repository includes GitHub Actions for:

- syntax validation
- dataset validation
- pipeline execution checks
- release packaging

This helps ensure reproducibility and early failure detection.

---

## 8. Extensibility

The architecture is designed to support future extensions such as:

- monthly data instead of annual data
- additional explanatory variables
- model benchmarking
- local explainability
- report generation
- deployment to a hosted environment

---

## 9. Current limitations

- annual granularity limits temporal depth
- dependence on official source quality
- geospatial naming inconsistencies must be normalized
- current rules are heuristic and can be further calibrated

---

## 10. Summary

The architecture of NANCY GeoVial RD is modular, reproducible, and ready for extension into a larger research or thesis-oriented platform.
