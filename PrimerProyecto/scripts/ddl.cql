-- =====================================================
-- ReservaDB: DDL - Definicion de Estructura
-- Sistema Distribuido de Gestion de Espacios Compartidos
-- Universidad San Carlos de Guatemala
-- Curso: Sistemas de Bases de Datos 2
-- =====================================================

-- -----------------------------------------------------
-- PASO 1: Crear el Keyspace
-- Estrategia: SimpleStrategy (entorno local/single DC)
-- Replication Factor: 3 (un dato en cada nodo)
-- Justificacion: con RF=3 el sistema tolera la caida
-- de 1 nodo sin perder disponibilidad usando QUORUM
-- -----------------------------------------------------
CREATE KEYSPACE IF NOT EXISTS reservadb
WITH replication = {
  'class': 'SimpleStrategy',
  'replication_factor': 3
}
AND durable_writes = true;

-- Seleccionar el keyspace
USE reservadb;

-- -----------------------------------------------------
-- PASO 2: Tablas maestras (datos de referencia)
-- -----------------------------------------------------

-- Tabla: usuarios
-- Proposito: almacenar datos maestros de usuarios
-- Patron de acceso: busqueda directa por usuario_id
CREATE TABLE IF NOT EXISTS usuarios (
    usuario_id UUID PRIMARY KEY,
    nombre     TEXT,
    email      TEXT,
    dpi        TEXT,
    telefono   TEXT,
    nit        TEXT
);

-- Tabla: espacios
-- Proposito: almacenar datos maestros de espacios
-- Patron de acceso: busqueda directa por espacio_id
CREATE TABLE IF NOT EXISTS espacios (
    espacio_id UUID PRIMARY KEY,
    nombre     TEXT,
    tipo       TEXT,
    capacidad  INT,
    ubicacion  TEXT
);

-- -----------------------------------------------------
-- PASO 3: Tablas especializadas por query
-- Principio: Query-Driven Modeling
-- Una tabla por patron de acceso identificado
-- Sin JOINs, sin ALLOW FILTERING
-- -----------------------------------------------------

-- Tabla: reservas_por_espacio_fecha
-- Query soportada (Q1): consultar disponibilidad de
-- un espacio en una fecha especifica
-- SELECT ... WHERE espacio_id = ? AND fecha = ?
-- Partition Key: (espacio_id, fecha) compuesta
--   -> garantiza que todas las reservas de un espacio
--      en una fecha esten en la misma particion
-- Clustering Key: hora_inicio
--   -> ordena las reservas cronologicamente
CREATE TABLE IF NOT EXISTS reservas_por_espacio_fecha (
    espacio_id     UUID,
    fecha          DATE,
    hora_inicio    TIME,
    reserva_id     UUID,
    usuario_id     UUID,
    hora_fin       TIME,
    estado         TEXT,
    nombre_reserva TEXT,
    PRIMARY KEY ((espacio_id, fecha), hora_inicio)
);

-- Tabla: reservas_por_usuario
-- Query soportada (Q2): ver historial de reservas
-- de un usuario especifico
-- SELECT ... WHERE usuario_id = ?
-- Partition Key: usuario_id
--   -> agrupa todas las reservas del usuario en una
--      sola particion para acceso rapido
-- Clustering Keys: fecha, hora_inicio
--   -> ordena el historial cronologicamente
CREATE TABLE IF NOT EXISTS reservas_por_usuario (
    usuario_id     UUID,
    fecha          DATE,
    hora_inicio    TIME,
    reserva_id     UUID,
    espacio_id     UUID,
    hora_fin       TIME,
    estado         TEXT,
    nombre_reserva TEXT,
    PRIMARY KEY (usuario_id, fecha, hora_inicio)
);

-- Tabla: reservas_por_fecha
-- Query soportada (Q3): obtener ocupacion de espacios
-- en un rango de fechas
-- SELECT ... WHERE fecha >= ? AND fecha <= ?
-- Partition Key: fecha
--   -> cada dia es una particion independiente
--      permite range scan eficiente por fecha
-- Clustering Keys: hora_inicio, espacio_id
--   -> ordena resultados por hora y espacio
CREATE TABLE IF NOT EXISTS reservas_por_fecha (
    fecha          DATE,
    hora_inicio    TIME,
    espacio_id     UUID,
    reserva_id     UUID,
    usuario_id     UUID,
    hora_fin       TIME,
    estado         TEXT,
    nombre_reserva TEXT,
    PRIMARY KEY (fecha, hora_inicio, espacio_id)
);