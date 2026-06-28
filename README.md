# ERP Data Pipeline (GCP)

Pipeline de datos end-to-end en Google Cloud que replica datos de un ERP
(clientes, proveedores, facturas, productos): generación de datos crudos →
capas **Bronze → Silver → Gold** (star schema) en BigQuery → KPIs.

Proyecto de aprendizaje orientado a portfolio. Datos **simulados** (Faker),
nunca datos reales.

## Stack
Python · BigQuery · dbt · Pub/Sub · Cloud Functions · Airflow · Terraform

## Estructura
```
src/erp_pipeline/   código del pipeline (Python)
sql/                consultas SQL
data/               CSVs generados (ignorados por git)
tests/              tests (pytest)
```

## Capas
- **Bronze** — datos crudos tal cual entran.
- **Silver** — datos limpios y validados.
- **Gold** — modelo dimensional (star schema): `fact_facturas` + dimensiones.

## Entorno
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
