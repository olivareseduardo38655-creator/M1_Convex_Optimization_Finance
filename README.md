# Optimización Convexa de Portafolios Financieros (M1)

![Python](https://img.shields.io/badge/Python-3.10%2B-000000?style=flat&logo=python&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-Optimization-000000?style=flat&logo=scipy&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-000000?style=flat&logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-000000?style=flat)

## Descripción Ejecutiva

Este sistema implementa un motor de asignación de activos de grado institucional basado en la Teoría Moderna de Portafolios (Markowitz). El software resuelve un problema de optimización convexa cuadrática para determinar la frontera eficiente de inversión, minimizando la volatilidad de la cartera sujeto a restricciones de retorno esperado y asignación de capital.

El proyecto está diseñado para servir como herramienta de soporte a la decisión (DSS) para gestores de activos, permitiendo la construcción de portafolios matemáticamente robustos, descorrelacionados y ajustados al perfil de riesgo del inversor mediante un dashboard interactivo.

## Objetivos Técnicos

1.  **Formulación Matemática Rigurosa:** Implementación de la función objetivo de varianza mínima utilizando álgebra lineal matricial y solvers numéricos (SLSQP).
2.  **Ingesta de Datos Resiliente:** Pipeline ETL automatizado capaz de extraer, limpiar y normalizar series temporales financieras de múltiples fuentes.
3.  **Arquitectura Modular:** Separación estricta de responsabilidades entre la capa de datos, la lógica de negocio (motor de optimización) y la capa de presentación.
4.  **Visualización Prescriptiva:** Generación de dashboards interactivos que traducen resultados estadísticos complejos en métricas de negocio accionables.

## Arquitectura del Sistema

```mermaid
graph LR
    A[Yahoo Finance API] -->|Raw Data| B(Data Loader Module)
    B -->|Cleaning & ETL| C[(CSV Storage)]
    C -->|Time Series| D{Optimizer Engine}
    C -->|Metadata| E[Jupyter Analysis]
    D -->|Minimize Risk| F[Scipy Solver]
    F -->|Optimal Weights| G[Streamlit Dashboard]
    E -->|Validation| G
