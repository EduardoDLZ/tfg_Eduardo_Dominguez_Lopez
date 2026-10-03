# Intelligent Network Threat Detection with Machine Learning


## Project Information

| | |
|---|---|
| **Author** | Eduardo Domínguez López |
| **Supervisors** | Ignacio Javier Pérez Gálvez · José Ramón Trillo Vílchez |
| **Institution** | University of Granada |
| **Degree** | BSc in Computer Engineering |
| **School** | School of Informatics and Telecommunications Engineering |
---

## Overview

This project implements an experimental pipeline for detecting malicious network traffic using supervised Machine Learning.

The system is based on labelled network-flow data and evaluates different feature representations and classification algorithms. The experiments investigate how data preprocessing, categorical encoding, feature reduction, logarithmic transformations, and feature scaling affect model performance.

### Main objectives

- Classify network traffic as **DDoS** or **BENIGN**.
- Evaluate different ML classification algorithms.
- Analyse the effect of feature engineering and feature selection.
- Reduce redundant and highly correlated features.
- Evaluate model performance using IDS-oriented metrics.

---


## Dataset
The project uses a reduced version of the original CIC-DDoS2019 dataset, obtained through Kaggle. This dataset was subsequently processed to generate two datasets used across the different experimental stages.

### Dataset configurations

| Stage | Dataset | Preparation | Features |
|---|---|---|---:|
| Stage I | `encoded` | Data cleaning and categorical encoding | 78 |
| Stage I | `numeric` | Universal data cleaning | 67 |
| Stage I | `correlation_09` | `encoded` with correlation filtering `(R > 0.9)` | 41 |
| Stage I | `correlation_08` | `encoded` with correlation filtering `(R > 0.8)` | 35 |
| Stage II | `filtered` | Universal cleaning and structural filtering | 59 |
| Stage II | `log_filtered` | Structural filtering and logarithmic transformation | 59 |
| Stage II | `correlation_098_filtered` | `filtered` with correlation filtering `(R > 0.98)` | 43 |
| Stage II | `correlation_098_scaled` | `correlation_098` with `StandardScaler` | 43 |

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
