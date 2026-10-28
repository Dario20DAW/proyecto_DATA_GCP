"""Carga los CSV de la capa Bronze a BigQuery.

Lee los 4 CSV generados por data_generator.py + storage.py y los sube
como tablas al dataset `erp_bronze` de BigQuery, reemplazando el
contenido en cada ejecución (para que el pipeline sea repetible).
"""
from __future__ import annotations

from pathlib import Path

from google.cloud import bigquery

PROJECT_ID = "erp-data-pipeline-dario"
DATASET_ID = "erp_bronze"
TABLAS = ["clientes", "proveedores", "productos", "facturas"]
ESQUEMAS = {
    "clientes": [
        bigquery.SchemaField("id", "STRING"),
        bigquery.SchemaField("nombre", "STRING"),
        bigquery.SchemaField("email", "STRING"),
        bigquery.SchemaField("dni", "STRING"),
        bigquery.SchemaField("ciudad", "STRING"),
    ],
    "proveedores": [
        bigquery.SchemaField("id", "STRING"),
        bigquery.SchemaField("nombre", "STRING"),
        bigquery.SchemaField("email", "STRING"),
        bigquery.SchemaField("telefono", "STRING"),
    ],
    "productos": [
        bigquery.SchemaField("id", "STRING"),
        bigquery.SchemaField("nombre", "STRING"),
        bigquery.SchemaField("categoria", "STRING"),
        bigquery.SchemaField("precio", "FLOAT"),
    ],
    "facturas": [
        bigquery.SchemaField("id", "STRING"),
        bigquery.SchemaField("cliente_id", "STRING"),
        bigquery.SchemaField("proveedor_id", "STRING"),
        bigquery.SchemaField("producto_id", "STRING"),
        bigquery.SchemaField("fecha", "DATE"),
        bigquery.SchemaField("cantidad", "INTEGER"),
        bigquery.SchemaField("importe", "FLOAT"),
    ],
}


def cargar_csv_a_bigquery(cliente: bigquery.Client, ruta_csv: Path, tabla_destino: str) -> int:
    """Carga un único CSV a una tabla de BigQuery.

    Args:
        cliente: cliente de BigQuery ya autenticado.
        ruta_csv: ruta local al fichero CSV.
        tabla_destino: nombre de la tabla (sin proyecto ni dataset).

    Returns:
        El número de filas cargadas.
    """
    # Id completo de la tabla: BigQuery necesita los 3 niveles (proyecto.dataset.tabla)
    # para saber exactamente dónde escribir. tabla_destino llega como parámetro
    # porque esta misma función se reutiliza para las 4 tablas (ver cargar_todo_bronze).
    tabla_id = f"{PROJECT_ID}.{DATASET_ID}.{tabla_destino}"

    # Config del job: le decimos a BigQuery CÓMO leer el CSV, no solo que lo lea.
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,  # la fila 1 es la cabecera (nombres de columna), no un dato
        # Esquema explícito, no autodetect: cuando todas las columnas de una
        # tabla son texto (clientes, proveedores), BigQuery no puede distinguir
        # la fila de cabecera de una fila de datos real y le pone nombres
        # genéricos (string_field_0, string_field_1...) en vez de los reales.
        schema=ESQUEMAS[tabla_destino],
        # WRITE_TRUNCATE en vez de WRITE_APPEND: si volvemos a ejecutar el pipeline,
        # reemplaza la tabla entera en vez de duplicar filas encima de las que ya había.
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    # "rb" (read binary): la API de carga de BigQuery espera bytes, no texto,
    # independientemente de que el contenido sea un CSV "de texto".
    with open(ruta_csv, "rb") as fichero:
        job = cliente.load_table_from_file(fichero, tabla_id, job_config=job_config)
        # load_table_from_file es asíncrono: lanza el job y devuelve el control
        # enseguida. job.result() BLOQUEA hasta que BigQuery confirma que terminó
        # (o lanza la excepción del job si algo falló, p.ej. un CSV mal formado).
        job.result()

    # No nos fiamos de "terminó sin error" como prueba de éxito: preguntamos a
    # BigQuery cuántas filas tiene la tabla AHORA, que es el dato real verificable.
    return cliente.get_table(tabla_id).num_rows


def cargar_todo_bronze(carpeta_datos: str = "data") -> None:
    """Carga las 4 tablas de la carpeta `carpeta_datos` a erp_bronze."""
    cliente = bigquery.Client(project=PROJECT_ID)
    carpeta = Path(carpeta_datos)

    for tabla in TABLAS:
        ruta_csv = carpeta / f"{tabla}.csv"
        filas = cargar_csv_a_bigquery(cliente, ruta_csv, tabla)
        print(f"{tabla}: {filas} filas cargadas en {DATASET_ID}.{tabla}")


if __name__ == "__main__":
    cargar_todo_bronze()
