# Data Pipeline – NANCY GeoVial RD

## 1. Propósito

Definir cómo se transforman los datos oficiales de DIGESETT en un dataset limpio, consistente y listo para el motor DSS.

---

## 2. Estructura de datos

```
data/
├── raw/
│   └── digesett_provincias_raw.csv
├── clean/
│   └── fallecimientos_provincias.csv
├── catalog/
│   └── provincias_rd_catalog.csv
├── geo/
│   └── rd_provinces.geojson
└── outputs/
```

---

## 3. Flujo del pipeline

```
RAW → NORMALIZE → VALIDATE → CLEAN → MODEL INPUT
```

---

## 4. Ingesta de datos

Se realiza mediante el CLI:

```bash
python scripts/convert_digesett_csv.py --validate
```

El sistema soporta:

- CSV con delimitador `,` o `;`
- Excel (`.xlsx`)
- múltiples encodings

---

## 5. Normalización

Se ejecuta en:

```
src/province_utils.py
```

Incluye:

- eliminación de acentos
- normalización de espacios
- conversión a formato consistente
- mapeo a nombres canónicos

---

## 6. Manejo de inconsistencias

El sistema corrige automáticamente:

### Variantes de formato

- `SanCristóbal` → `San Cristóbal`
- `SantoDomingo` → `Santo Domingo`

### Variantes históricas (GeoJSON)

- `Salcedo` → `Hermanas Mirabal`
- `LaEstrelleta` → `Elías Piña`
- `ElSeybo` → `El Seibo`

---

## 7. Validación territorial

Se ejecuta en:

```
src/validation.py
```

Verifica:

- cobertura de 32 provincias
- provincias faltantes
- provincias adicionales

Ejemplo de salida:

```
Esperadas: 32
Observadas: 32
Cobertura completa
```

---

## 8. Limpieza final

El dataset resultante:

- elimina valores nulos
- convierte tipos numéricos
- agrupa duplicados por provincia y año
- ordena los registros

---

## 9. Salida

El resultado final es:

```
data/clean/fallecimientos_provincias.csv
```

Este archivo:

- es la entrada oficial del modelo DSS
- es independiente del formato original
- está validado y normalizado

---

## 10. Resultado del pipeline

El pipeline garantiza:

- datos consistentes
- cobertura territorial completa
- formato estándar para modelado
- ejecución reproducible
