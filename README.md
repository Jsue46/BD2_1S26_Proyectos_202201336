# ReservaDB — Sistema Distribuido de Gestión de Espacios Compartidos

**Curso:** Sistemas de Bases de Datos 2  
**Universidad:** San Carlos de Guatemala — Facultad de Ingeniería  
**Carnet:** 202201336  

---

## Descripción

Sistema de gestión de reservas de espacios compartidos (coworking) implementado en Apache Cassandra. Diseñado con el principio de Query-Driven Modeling para garantizar baja latencia, alta disponibilidad y escalabilidad horizontal.

---

## Tecnologías utilizadas

- Apache Cassandra 4.1 (3 nodos en Docker)
- Python 3.11
- cassandra-driver, faker
- Docker Desktop

---

## Estructura del repositorio
```
BD2_1S26_Proyectos_202201336/
└── Primer Proyecto/
    ├── scripts/
    │   ├── ddl.cql              # Definicion de keyspace y tablas
    │   ├── consultas.cql        # Consultas CQL del negocio
    │   ├── cargar_datos.py      # Script carga masiva 100,000 reservas
    │   └── pruebas_fallos.py    # Script pruebas tolerancia a fallos
    ├── docs/
    │   ├── Documentacion_Tecnica.pdf
    │   └── Manual_Usuario.pdf
    └── README.md
```

---

## Configuración del clúster

| Parámetro | Valor |
|---|---|
| Nodos | 3 |
| Replication Factor | 3 |
| Estrategia | SimpleStrategy |
| Consistency Level | QUORUM |

---

## Tablas y queries soportadas

| Tabla | Query soportada |
|---|---|
| `usuarios` | Datos maestros de usuarios |
| `espacios` | Datos maestros de espacios |
| `reservas_por_espacio_fecha` | Q1: Disponibilidad por espacio y fecha |
| `reservas_por_usuario` | Q2: Historial de reservas por usuario |
| `reservas_por_fecha` | Q3: Ocupación por rango de fechas |

---

## Instrucciones de instalación

Ver `docs/Manual_Usuario.pdf` para guía completa paso a paso.

### Inicio rápido
```bash
# 1. Crear red Docker
docker network create cassandra-net

# 2. Levantar nodos
docker run -d --name cassandra-node1 --network cassandra-net -e CASSANDRA_CLUSTER_NAME=ReservaDB -e CASSANDRA_ENDPOINT_SNITCH=SimpleSnitch -p 9042:9042 cassandra:4.1
docker run -d --name cassandra-node2 --network cassandra-net -e CASSANDRA_CLUSTER_NAME=ReservaDB -e CASSANDRA_SEEDS=cassandra-node1 -e CASSANDRA_ENDPOINT_SNITCH=SimpleSnitch cassandra:4.1
docker run -d --name cassandra-node3 --network cassandra-net -e CASSANDRA_CLUSTER_NAME=ReservaDB -e CASSANDRA_SEEDS=cassandra-node1 -e CASSANDRA_ENDPOINT_SNITCH=SimpleSnitch cassandra:4.1

# 3. Verificar cluster
docker exec -it cassandra-node1 nodetool status

# 4. Cargar datos
py -3.11 cargar_datos.py
```

---

## Pruebas de tolerancia a fallos

| Consistency Level | 3 nodos activos | 1 nodo caído |
|---|---|---|
| ONE | 191.08 ms ✅ | 19.15 ms ✅ |
| QUORUM | 380.53 ms ✅ | 29.32 ms ✅ |
| ALL | 67.25 ms ✅ | ❌ Error |