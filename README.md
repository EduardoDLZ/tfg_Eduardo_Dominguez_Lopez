# Sistemas Inteligentes de Detección de Amenazas en Redes mediante Machine Learning

## Autoría
| Campo | Datos |
|---|---|
| **Autor** | Eduardo Domínguez López |
| **Directores** | Ignacio Javier Pérez Gálvez<br>José Ramón Trillo Vílchez |
| **Titulación** | Grado de Ingeniería Informática |
| **Centro** | E.T.S. de Ingenierías Informática y de Telecomunicación, Universidad de Granada |

---

## Objetivo general

Desarrollar un modelo de inteligencia artificial capaz de detectar intrusiones maliciosas en redes informáticas y generar alertas automáticas ante posibles amenazas.

---

## Conjuntos de datos utilizados

| Fase | Conjunto | Preparación | Nº de atributos |
|---|---|---|---:|
| Fase I | `encoded` | Limpieza y codificación categórica | 78 |
| Fase I | `numeric` | Limpieza universal | 67 |
| Fase I | `correlation_09` | Conjunto `encoded` con correlación `(R > 0.9)` | 41 |
| Fase I | `correlation_08` | Conjunto `encoded` con correlación `(R > 0.8)` | 35 |
| Fase II | `filtered` | Limpieza universal y filtro estructural | 59 |
| Fase II | `log_filtered` | Limpieza universal, filtro estructural y transformación logarítmica | 59 |
| Fase II | `correlation_098_filtered` | Conjunto `filtered` con correlación `(R > 0.98)` | 43 |
| Fase II | `correlation_098_scaled` | Conjunto `correlation_098` con escalado mediante `StandardScaler` | 43 |

---

## Estructura del proyecto

```text
.
├── data/
│   ├── raw/
│   ├── intermediate/
│   └── processed/
│
├── models/
│   ├── stage1/
│   └── stage2/
│
├── notebooks/
│   ├── 00-data-preparation/
│   │   ├── 01-dataset-construction.ipynb
│   │   └── 02-data-cleaning.ipynb
│   │
│   ├── 01-EDA/
│   │   └── 03-exploratory-data-analysis.ipynb
│   │
│   ├── 02-stage1/
│   │   ├── 04-feature-engineering.ipynb
│   │   ├── 05-feature-selection.ipynb
│   │   ├── 06-comparative-modeling.ipynb
│   │   └── 07-analysis.ipynb
│   │
│   └── 03-stage2/
│       ├── 04-feature-engineering.ipynb
│       ├── 05-feature-selection.ipynb
│       ├── 06-experimental-feature-selection.ipynb
│       ├── 07-comparative-modeling.ipynb
│       └── 08-analysis.ipynb
│
├── results/
│
└── src/
    ├── data/
    ├── features/
    ├── models/
    ├── evaluation/
    └── utils/
