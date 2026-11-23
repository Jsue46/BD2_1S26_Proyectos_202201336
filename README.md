# Advanced Database Systems — Apache Cassandra and Neo4j Benchmarking

Academic projects developed for the **Database Systems 2** course at the Universidad de San Carlos de Guatemala (First Semester 2026).

This repository contains two comprehensive database engineering projects focusing on distributed NoSQL systems: column-family architecture with **Apache Cassandra** and graph database modeling with **Neo4j**.

---

## Overview

The repository covers practical design, data modeling, automated ETL pipelines, latency benchmarking, and fault-tolerance evaluation across distinct NoSQL paradigms:

1. **Project 1 — Apache Cassandra (Distributed Column Family):** High-throughput data ingestion, DDL partition key design, consistency tuning, replication factor testing, and node failure survival analysis.
2. **Project 2 — Neo4j (Graph Database):** Graph data modeling, Cypher queries, relationship traversals, entity mapping, and complex graph analytics.

---

## Project 1: Apache Cassandra

- **Schema Design (`ddl.cql`):** Denormalized tables optimized for query-driven read patterns and uniform hash ring distribution.
- **Automated Data Loading:** Python ingestion scripts handling bulk inserts and data transformations.
- **Latency Benchmarks (`medir_latencias.py`):** Quantitative metrics comparing read/write latencies across various consistency levels (ONE, QUORUM, ALL).
- **Fault Tolerance Testing (`pruebas_fallos.py`):** Evaluating cluster health and response behaviors under simulated node failure and network partitioning.

---

## Project 2: Neo4j Graph Database

- **Graph Model (`01_schema.cypher`):** Node labels, indexed properties, and directional relationships designed for connected domain analysis.
- **Batch Import Pipeline (`02_load_data.cypher`):** High-speed CSV ingestion using `LOAD CSV WITH HEADERS`.
- **Analytical Queries:** Advanced Cypher pattern matching, degree of separation lookups, and graph pattern mining.

---

## Technologies

- **Database Engines:** Apache Cassandra, Neo4j
- **Query Languages:** CQL (Cassandra Query Language), Cypher (Neo4j)
- **Programming & Scripting:** Python 3, `cassandra-driver`, `neo4j`
- **Documentation:** Markdown technical reports and schema design diagrams

---

## Repository Structure

```
BD2_1S26_Proyectos_202201336/
├── PrimerProyecto/           # Apache Cassandra distributed database
│   ├── scripts/              # Ingestion, latency benchmarks, failover tests
│   ├── Consultas/            # CQL query suites
│   ├── diagramas/            # Ring topology and schema diagrams
│   └── docs/                 # Technical documentation
├── SegundoProyecto/          # Neo4j graph database
│   ├── scripts/              # Cypher schema, load scripts, CSV generators
│   ├── consultas/            # Analytical graph queries
│   ├── data/                 # Raw and processed datasets
│   └── docs/                 # User and technical manuals
└── README.md
```

---

## Academic Context

| Field       | Detail                                         |
|-------------|------------------------------------------------|
| Course      | Database Systems 2 (BD2)                       |
| Institution | Universidad de San Carlos de Guatemala         |
| Semester    | First Semester 2026                            |
| Author      | Estuardo Josue Vaquiax Reyes (202201336)       |
