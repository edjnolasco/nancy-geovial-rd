# 🚧 Nancy GeoVial RD

[![CI](https://github.com/edjnolasco/nancy-geovial-rd/actions/workflows/ci.yml/badge.svg)](https://github.com/edjnolasco/nancy-geovial-rd/actions)
[![codecov](https://codecov.io/gh/edjnolasco/nancy-geovial-rd/branch/main/graph/badge.svg)](https://codecov.io/gh/edjnolasco/nancy-geovial-rd)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Status](https://img.shields.io/badge/status-active%20development-orange)
![License](https://img.shields.io/badge/license-MIT-green)

Sistema de análisis y predicción de accidentes viales en República Dominicana basado en técnicas de Machine Learning y análisis geoespacial.

---

## 📌 Descripción

**Nancy GeoVial RD** es una plataforma analítica orientada a la detección de patrones espaciales y temporales en accidentes de tránsito, con capacidad de predicción y priorización de zonas de riesgo.

El sistema integra:

- Procesamiento de datos estructurados
- Modelado predictivo (ML/DL)
- Análisis geoespacial
- Evaluación basada en ranking

---

## 🎯 Objetivos

### Objetivo general
Desarrollar un sistema inteligente que permita analizar y predecir accidentes viales en República Dominicana.

### Objetivos específicos
- Diseñar un pipeline reproducible de datos
- Integrar fuentes abiertas oficiales
- Implementar modelos de aprendizaje supervisado
- Incorporar análisis geoespacial
- Evaluar mediante métricas Top-K

---

## 🧠 Arquitectura del Proyecto

```
nancy-geovial-rd/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   ├── evaluation/
│   └── utils/
│
├── tests/
├── docs/
├── configs/
├── requirements.txt
└── README.md
```

---

## ⚙️ Stack Tecnológico

- Python 3.11
- Pandas / NumPy
- Scikit-learn
- TensorFlow / PyTorch
- GeoPandas
- Plotly / Matplotlib

---

## 📊 Dataset

Fuente esperada:
- Datos abiertos de accidentes de tránsito (RD)

Variables clave:
- Provincia
- Fecha
- Tipo de evento
- Número de fallecidos
- Coordenadas geográficas

---

## 🔁 Pipeline de Datos

1. Ingesta
2. Limpieza
3. Normalización
4. Agregación provincia-mes
5. Feature engineering temporal
6. Integración geoespacial
7. Dataset final

---

## Pipeline

1. Ingesta
2. Limpieza
3. Normalizacion
4. Agregacion provincia-mes
5. Feature engineering
6. Integracion geoespacial
7. Dataset final

---

## 🤖 Modelos

### Clásicos
- Random Forest
- Gradient Boosting
- Support Vector Machine (SVM)

### Avanzados
- LSTM
- Redes neuronales profundas

---

## 📈 Evaluación

- HitRate@K
- nDCG@K

Enfoque: evaluación por ranking de provincias con mayor riesgo.

---

## 🧪 Testing

```bash
pytest tests/
```

CI ejecuta pruebas automaticamente en cada push y PR.

---

## Coverage

Se utiliza **pytest-cov** para medir cobertura.

### Ejecutar localmente

```bash
pytest --cov=src --cov-report=term
```

### CI + Codecov

El pipeline:

- Ejecuta tests
- Genera `coverage.xml`
- Envia resultados a Codecov

---

## 🚀 Instalación

```bash
git clone https://github.com/edjnolasco/nancy-geovial-rd.git
cd nancy-geovial-rd

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

---

## ▶️ Ejecución

```bash
python src/main.py
```

---

## 🗺️ Roadmap

- [ ] Pipeline completo
- [ ] Dataset validado
- [ ] Modelo baseline
- [ ] Visualización geoespacial
- [ ] Modelo DL
- [ ] Evaluación Top-K
- [ ] Publicación

---

## 🔐 Licencia

MIT License

---

## 👤 Autor

Edwin José Nolasco

---

## 📄 Transparencia IA

Uso de IA limitado a:
- Asistencia en estructura
- Apoyo en documentación

Decisiones metodológicas: 100% autor.

---

## ⚠️ Estado

Proyecto en desarrollo activo.
