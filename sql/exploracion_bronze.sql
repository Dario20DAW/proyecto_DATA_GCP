-- Consultas de exploración sobre la capa Bronze (Semana 1, hito M5).
-- Objetivo: practicar CTEs (cláusula WITH). Las completas tú.

-- Ejercicio 1: top 5 clientes por importe total facturado.
-- Pista: una CTE que agregue SUM(importe) por cliente_id, y luego
-- SELECT de esa CTE con ORDER BY ... LIMIT 5.


-- Ejercicio 2: facturación total por mes, ignorando facturas con importe nulo.
-- Pista: CTE 1 que filtre los nulos -> CTE 2 que agrupe por mes.


-- Ejercicio 3: proveedores con más de 20 facturas.
-- Pista: CTE que cuente facturas por proveedor_id, luego filtra el conteo.
