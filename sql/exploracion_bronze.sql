-- Consultas de exploración sobre la capa Bronze (Semana 1, hito M5).
-- Objetivo: practicar CTEs (cláusula WITH). Las completas tú.

-- Ejercicio 1: top 5 clientes por importe total facturado.
-- Pista: una CTE que agregue SUM(importe) por cliente_id, y luego
-- SELECT de esa CTE con ORDER BY ... LIMIT 5.
-- La CTE agrega TODAS las facturas por cliente_id antes de tocar nombres:
-- separar "sumar" de "poner nombre bonito" evita mezclar un GROUP BY con un
-- JOIN en la misma consulta, que complicaría saber por qué columna agrupar.
WITH total_por_cliente as (

    SELECT
    cliente_id,
    SUM(importe) as total_importe
    from `erp-data-pipeline-dario.erp_bronze.facturas`
    group by cliente_id

)

-- inner join: clientes.id es la clave real (facturas.cliente_id es solo la
-- referencia a ella) — un join por "cliente_id" en ambos lados habría fallado,
-- porque esa columna no existe en absoluto en la tabla clientes.
-- Con INNER JOIN, un cliente_id huérfano en facturas (como el "9999" que
-- data_generator.py mete a propósito) queda fuera del resultado sin más:
-- no hay fila de clientes con id=9999 con la que emparejarlo.
SELECT
    c.nombre,
    t.total_importe
    from total_por_cliente t
    inner join `erp-data-pipeline-dario.erp_bronze.clientes` as c
    on c.id = t.cliente_id
    order by t.total_importe desc
    limit 5;


-- Ejercicio 2: facturación total por mes, ignorando facturas con importe nulo.
-- Pista: CTE 1 que filtre los nulos -> CTE 2 que agrupe por mes.

-- Primera CTE: filtra ANTES de agregar. Si el WHERE fuera después del SUM,
-- ya sería tarde — una fila con importe NULL habría podido colarse en el
-- cálculo (o BigQuery la ignora silenciosamente en el SUM, pero entonces no
-- quedaría explícito en la consulta que la estás excluyendo a propósito).
WITH facturas_sin_null AS (
  SELECT
    *  -- o solo las columnas que uses: cliente_id, producto_id, fecha, cantidad, importe
  FROM `erp-data-pipeline-dario.erp_bronze.facturas`
  WHERE importe IS NOT NULL
),
-- Segunda CTE: EXTRACT saca el año y el mes como números sueltos de la fecha
-- completa — sin esto, agruparías por fecha exacta (día a día) en vez de por
-- mes, y cada día saldría en su propia fila.
acumulado_por_mes AS (
  SELECT
    EXTRACT(YEAR FROM fecha) AS anio,
    EXTRACT(MONTH FROM fecha) AS mes,
    SUM(importe) AS facturacion_mes
  FROM facturas_sin_null
  GROUP BY anio, mes
)
-- GROUP BY y ORDER BY aquí referencian "anio"/"mes" por su alias, no por la
-- expresión EXTRACT(...) completa — BigQuery lo permite (no toda base de
-- datos lo hace), y hace la query mucho más legible.
SELECT
  anio,
  mes,
  facturacion_mes
FROM acumulado_por_mes
ORDER BY
  anio,
  mes;




-- Ejercicio 3: proveedores con más de 20 facturas.
-- Pista: CTE que cuente facturas por proveedor_id, luego filtra el conteo.

-- HAVING filtra DESPUÉS de agregar (por eso no es un WHERE): "más de 20
-- facturas" es una propiedad del GRUPO (el conteo), no de una fila suelta,
-- y el conteo todavía no existe hasta que el GROUP BY termina.
-- Referenciar "numero_facturas" (su propio alias) en el HAVING también es
-- una particularidad de BigQuery, igual que el alias en GROUP BY del ejercicio 2.
WITH

    proveedores_con_facturas AS (
    SELECT
        proveedor_id,
        count(*) as numero_facturas
    FROM `erp-data-pipeline-dario.erp_bronze.facturas`
    WHERE proveedor_id IS NOT NULL
    GROUP BY proveedor_id
    HAVING numero_facturas > 20
)

-- Mismo error que en el ejercicio 1, mismo motivo: proveedores.id es la
-- clave real, no "proveedor_id" (esa columna solo existe en facturas).
SELECT p.nombre, c.numero_facturas
    from proveedores_con_facturas c
    inner join `erp-data-pipeline-dario.erp_bronze.proveedores` p
    on c.proveedor_id = p.id
    order by c.numero_facturas desc;


