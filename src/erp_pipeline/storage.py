"""Utilidades de entrada/salida para el pipeline ERP.

Persisten los DataFrames generados en disco (CSV) como paso intermedio
antes de cargarlos a BigQuery (capa Bronze).
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd


def guardar_csv(datos: dict[str, pd.DataFrame], carpeta: str = "data") -> None:
    """Guarda cada DataFrame del dict como un CSV en `carpeta`.

    Args:
        datos: dict nombre_tabla -> DataFrame (lo que devuelve
            generar_datos_crudos).
        carpeta: ruta de la carpeta destino. Se crea si no existe.
    """
    # Path(...) representa la ruta como objeto (no como string suelto):
    # permite usar "/" para unir rutas (línea 27) de forma portable entre
    # sistemas operativos, en vez de concatenar texto a mano.
    carpeta_destino = Path(carpeta)

    # parents=True: crea también carpetas intermedias si faltaran (p.ej.
    # si "carpeta" fuera "a/b/c" y ni "a" ni "a/b" existiesen todavía).
    # exist_ok=True: si la carpeta ya existe, no lanza error (sin esto,
    # la segunda vez que ejecutes el script fallaría).
    carpeta_destino.mkdir(parents=True, exist_ok=True)

    # Recorremos el dict con .items(): nombre = clave ("clientes", ...),
    # df = el DataFrame asociado. Así generalizamos a las 4 tablas con
    # un único bucle, en vez de repetir el mismo código 4 veces.
    for nombre, df in datos.items():
        ruta = carpeta_destino / f"{nombre}.csv"

        # index=False: si no, pandas añade una columna extra con el índice
        # numérico (0,1,2...) que no queremos en el CSV.
        df.to_csv(ruta, index=False)

        # Confirmación visual fila por fila guardada, para detectar a ojo
        # si alguna tabla salió con menos filas de las esperadas.
        print(f"{nombre}: {len(df)} filas -> {ruta}")

    print("✓ CSVs guardados en la carpeta 'data'")
