-- =====================================================
-- ReservaDB: Consultas CQL eficientes
-- Sistema Distribuido de Gestion de Espacios Compartidos
-- Universidad San Carlos de Guatemala
-- Curso: Sistemas de Bases de Datos 2
-- =====================================================

-- -----------------------------------------------------
-- Q1: Consultar disponibilidad de un espacio en una fecha
-- Tabla usada: reservas_por_espacio_fecha
-- Partition Key: (espacio_id, fecha) -> acceso directo
-- sin ALLOW FILTERING
-- -----------------------------------------------------
SELECT hora_inicio, hora_fin, nombre_reserva, usuario_id, estado
FROM reservas_por_espacio_fecha
WHERE espacio_id = 535b89d4-4adb-4c91-81ef-3457be5d72cb
AND fecha = '2025-07-24';

-- -----------------------------------------------------
-- Q2: Ver historial de reservas de un usuario
-- Tabla usada: reservas_por_usuario
-- Partition Key: usuario_id -> todas las reservas del
-- usuario en una particion, orden cronologico
-- -----------------------------------------------------
SELECT fecha, hora_inicio, hora_fin, espacio_id, nombre_reserva, estado
FROM reservas_por_usuario
WHERE usuario_id = 18439029-3649-4749-afe0-fd2f540ce555;

-- -----------------------------------------------------
-- Q3: Obtener ocupacion de espacios en un rango de fechas
-- Tabla usada: reservas_por_fecha
-- NOTA: En Cassandra cada fecha es una particion separada.
-- La consulta por fecha exacta es eficiente (1 particion).
-- Para rangos de fechas se usa el script consulta_rango.py
-- que itera fecha por fecha desde la aplicacion Python.
-- -----------------------------------------------------

-- Q3a: Consulta por fecha exacta (eficiente en CQL)
SELECT fecha, hora_inicio, espacio_id, nombre_reserva, usuario_id, estado
FROM reservas_por_fecha
WHERE fecha = '2025-07-24';

