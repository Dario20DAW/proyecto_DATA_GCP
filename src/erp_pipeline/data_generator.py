"""Generador de datos ERP simulados para la capa Bronze.

Crea datos crudos y *sucios* a propósito (duplicados, nulos y valores mal
formados) que más adelante limpiaremos en la capa Silver. Los datos son
reproducibles: con la misma semilla, salen exactamente los mismos.
"""
from __future__ import annotations

import pandas as pd
from faker import Faker


def generar_datos_crudos(
    n_clientes: int,
    n_proveedores: int,
    n_productos: int,
    n_facturas: int,
    semilla: int = 42,
) -> dict[str, pd.DataFrame]:
    """Genera las 4 tablas crudas del ERP.

    Args:
        n_clientes: nº de clientes a generar.
        n_proveedores: nº de proveedores a generar.
        n_productos: nº de productos a generar.
        n_facturas: nº de facturas a generar.
        semilla: fija la aleatoriedad para que el resultado sea reproducible.

    Returns:
        Un dict con 4 claves -> 'clientes', 'proveedores', 'productos',
        'facturas', cada una con su DataFrame.
    """
    faker = Faker("es_ES")
    # Sembramos el azar de Faker: con la misma semilla, los mismos datos.
    # Como las facturas usan faker.random_int (no random.randint), todo el
    # azar del módulo queda cubierto por esta única semilla.
    Faker.seed(semilla)

    # --- Clientes -------------------------------------------------------
    # Construimos una lista de diccionarios (una fila = un dict) y al final
    # la convertimos en DataFrame de una sola vez (más eficiente que ir
    # añadiendo filas al DataFrame una a una).
    lista_clientes = []
    for i in range(1, n_clientes + 1):
        lista_clientes.append({
            "id": f"CLI-{i:04}",          # id con relleno de ceros: CLI-0001
            "nombre": faker.name(),
            "email": faker.email(),
            "dni": faker.ssn(),
            "ciudad": faker.city(),
        })

    df_clientes = pd.DataFrame(lista_clientes)

    # Suciedad intencionada (se limpiará en Silver, semana 3):
    df_clientes.loc[0, "email"] = "sin-arroba.com"   # email inválido (sin @)
    df_clientes.loc[1, "dni"] = "123456Ñ8X"          # dni mal formado
    df_clientes.loc[2, "ciudad"] = None              # valor nulo

    # Duplicamos el primer cliente para tener un registro repetido.
    df_clientes = pd.concat([df_clientes, df_clientes.iloc[[0]]], ignore_index=True)

    # --- Proveedores ----------------------------------------------------
    lista_proveedores = []
    for i in range(1, n_proveedores + 1):
        lista_proveedores.append({
            "id": f"PROV-{i:04}",
            "nombre": faker.company(),
            "email": faker.email(),
            "telefono": faker.phone_number(),
        })

    df_proveedores = pd.DataFrame(lista_proveedores)

    # Suciedad intencionada (sobre columnas que SÍ existen en la tabla):
    df_proveedores.loc[0, "email"] = "sin-arrob2a.com"   # email inválido
    df_proveedores.loc[2, "telefono"] = None             # proveedor sin teléfono

    # --- Productos ------------------------------------------------------
    lista_productos = []
    for i in range(1, n_productos + 1):
        lista_productos.append({
            "id": f"PROD-{i:04}",
            "nombre": faker.word(),
            "categoria": faker.word(),
            "precio": faker.pyfloat(left_digits=2, right_digits=2, positive=True),
        })

    df_productos = pd.DataFrame(lista_productos)

    # Suciedad intencionada:
    df_productos.loc[0, "precio"] = -99.0    # precio negativo (no debería ser < 0)
    df_productos.loc[1, "categoria"] = None  # categoría nula

    # --- Facturas -------------------------------------------------------
    # Las columnas *_id son claves foráneas: apuntan a ids reales de las
    # tablas de arriba (elegimos un número al azar dentro del rango válido).
    lista_facturas = []
    for i in range(1, n_facturas + 1):
        lista_facturas.append({
            "id": f"FAC-{i:04}",
            "cliente_id": f"CLI-{faker.random_int(1, n_clientes):04}",
            "proveedor_id": f"PROV-{faker.random_int(1, n_proveedores):04}",
            "producto_id": f"PROD-{faker.random_int(1, n_productos):04}",
            "fecha": faker.date_between(start_date="-5y", end_date="today"),
            "cantidad": faker.pyint(min_value=1, max_value=100),
            "importe": faker.pyfloat(left_digits=2, right_digits=2, positive=True),
        })

    df_facturas = pd.DataFrame(lista_facturas)

    # Suciedad intencionada:
    df_facturas.loc[0, "cantidad"] = 9999    # cantidad atípica (outlier)
    df_facturas.loc[1, "cliente_id"] = "9999"  # FK huérfana (no existe ese cliente)

    # Devolvemos las 4 tablas en un dict; la clave es el nombre de la tabla.
    return {
        "clientes": df_clientes,
        "proveedores": df_proveedores,
        "productos": df_productos,
        "facturas": df_facturas,
    }


# Este bloque solo se ejecuta si lanzas el archivo directamente
# (python -m src.erp_pipeline.data_generator), no si lo importas desde otro sitio.
if __name__ == "__main__":
    datos = generar_datos_crudos(n_clientes=50, n_proveedores=15, n_productos=30, n_facturas=300)
    for nombre, df in datos.items():
        print(f"{nombre}: {len(df)} filas")
        print(df.head(), "\n")
