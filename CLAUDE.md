# Proyecto Darío — ERP Data Pipeline (GCP)

Proyecto de aprendizaje de Darío: pipeline de datos ERP simulado (Faker) → Bronze → Silver → Gold en BigQuery, con Python "en serio", como vehículo para preparar la certificación **Associate Cloud Engineer (ACE)**. Repo GitHub: `Dario20DAW/proyecto_DATA_GCP`.

## Segundo cerebro

Darío usa una bóveda de Obsidian como segundo cerebro personal — este proyecto vivía dentro de ella y desde el 11-oct-2026 está fuera, en `~/Desktop/proyectos/proyecto_DATA_GCP/` (el `.venv` se recrea con el README). El estado del curso tiene su propia nota: `~/Desktop/DaríoVault/03 Darío Personal/Projects/estudio-gcp-ace/erp-data-pipeline-gcp.md`. **Cuando se complete una semana o milestone, o se tome una decisión de fondo, actualiza esa nota** (no hace falta por cada commit).

## Reglas de trabajo de este proyecto (no se aplican en ningún otro)

- **⚠️ Cuenta GCP:** este proyecto usa `adminwpdgc@gmail.com` (perfil `curso-gcp` de `gcloud config configurations`), **nunca** la cuenta de trabajo `dario@adgco.es`. Verificar con `gcloud config configurations list` antes de tocar nada en BigQuery/GCS. Ver `02 Darío ADG/Areas/perfil-dario-adg.md` en el vault para el porqué de esta separación — es una regla general de Darío, no solo de este proyecto.
- **Modo de trabajo en los ejercicios (fijado 23-sep-2026):** Claude **NO escribe código directamente** en `src/`, `sql/`, etc. Para cada ejercicio: (1) dicta el código en el chat, explicando el concepto antes de mostrarlo, (2) Darío lo escribe él mismo en su editor, (3) una vez escrito, Claude añade los comentarios explicando el porqué (ahí sí puede tocar el archivo, solo para comentar). Ejecutar/verificar (`python -m ...`, `bq`, etc.) sigue siendo tarea de Claude.
- **Certificación objetivo confirmada: ACE**, no Associate Data Practitioner (recomendación del jefe de Darío en ADG) — no revertir sin que lo confirme él de nuevo.
