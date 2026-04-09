# Methodology – NANCY GeoVial RD

## 1. Objective

Build a decision support system capable of identifying and prioritizing provinces with higher relative risk of road-traffic mortality in the Dominican Republic.

---

## 2. General approach

The project follows a hybrid DSS approach that combines:

- official statistical data
- predictive modeling
- explicit decision rules
- geospatial visualization

This means the system is not limited to descriptive reporting. It produces an interpretable prioritization output for decision-making.

---

## 3. Data source

Primary source:

- DIGESETT road mortality dataset by province

Supporting resources:

- territorial province catalog
- RD province GeoJSON for map visualization

---

## 4. Data preparation

The methodological process begins with a controlled data pipeline:

1. ingestion of the raw official file
2. delimiter and encoding detection
3. column normalization
4. province name reconciliation
5. territorial coverage validation
6. creation of a clean dataset for model input

Output dataset structure:

- `provincia`
- `year`
- `fallecidos`

---

## 5. Territorial normalization

Because official and geospatial sources may use different naming conventions, the system applies canonical normalization and alias resolution.

This includes:

- spacing differences
- accent differences
- compact names from GeoJSON sources
- historical province names

This step ensures consistency between statistical data and territorial boundaries.

---

## 6. Feature engineering

From the clean dataset, the system generates derived variables used for prediction.

Examples include:

- lag values
- absolute change
- percentage change
- rolling averages
- rolling standard deviation
- cumulative mean
- time index
- cyclical month encoding

The target variable is the next-period value of fatalities.

---

## 7. Predictive modeling

The current predictive layer uses a supervised regression approach.

The workflow includes:

- preparation of trainable observations
- temporal split
- model training
- prediction over the transformed dataset
- normalization of prediction outputs into a DSS risk score

The model output is not used alone. It is transformed into a decision-oriented signal.

---

## 8. DSS rules

The system applies explicit rules over model outputs in order to generate interpretable categories.

These rules combine:

- risk score
- recent change behavior

The result is a prioritization label such as:

- high priority
- preventive monitoring
- routine follow-up
- no data

This converts the model output into an actionable DSS layer.

---

## 9. Evaluation

The system is evaluated using both predictive and ranking-oriented metrics.

Predictive metrics:

- MAE
- R²

Ranking metrics:

- HitRate@K
- nDCG@K

This is important because the system is intended not only to predict values, but also to prioritize territories.

---

## 10. Explainability

The methodology includes a global explainability layer.

Preferred approach:

- SHAP, when available

Fallback approach:

- feature importances from the trained model

This allows the system to communicate which variables are more influential in the general model behavior.

---

## 11. Narrative generation

The system also produces an automated textual summary based on:

- ranking position
- category
- score
- evaluation metrics

This improves usability for non-technical stakeholders.

---

## 12. User interaction

The application is built in Streamlit and allows the user to:

- load a local or uploaded dataset
- validate territorial coverage
- execute the DSS
- view rankings, metrics, explainability, and maps
- export results

---

## 13. Reproducibility

Reproducibility is supported through:

- explicit project structure
- CLI-based data preparation
- Git version control
- CI workflows
- documented data flow

---

## 14. Current scope

The current implementation is focused on:

- province-level analysis
- annual data
- local execution environment

This scope is sufficient for a working DSS prototype and a strong basis for future expansion.

---

## 15. Future methodological extensions

Possible next steps include:

- monthly data modeling
- model benchmarking
- walk-forward validation
- incorporation of exogenous variables
- local explainability by province
- automatic report generation

---

## 16. Summary

The methodology of NANCY GeoVial RD combines data preparation, predictive modeling, rule-based interpretation, and geospatial visualization into a coherent hybrid DSS workflow.
