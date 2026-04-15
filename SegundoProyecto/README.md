# Segundo Proyecto - Sistema de Recomendacion de Peliculas con Neo4j

Este directorio contiene el arranque del Segundo Proyecto de BD2.

## Objetivo
Construir una base de datos de grafos en Neo4j para recomendaciones de peliculas basadas en:
- preferencias del usuario,
- relaciones de amistad,
- patrones de visualizacion y calificacion.

## Estructura
- `scripts/01_schema.cypher`: constraints e indices.
- `scripts/02_load_data.cypher`: carga masiva con LOAD CSV.
- `scripts/generar_csv.py`: generacion de datos CSV.
- `consultas/consultas_obligatorias.cypher`: consultas obligatorias y analisis.
- `data/csv/`: archivos CSV generados.
- `docs/`: documentacion tecnica y manual de usuario.

## Flujo de ejecucion
1. Generar CSV:
   - `python scripts/generar_csv.py`
2. Copiar CSV a carpeta import de Neo4j.
3. Ejecutar en Neo4j Browser:
   - `scripts/01_schema.cypher`
   - `scripts/02_load_data.cypher`
4. Ejecutar consultas en:
   - `consultas/consultas_obligatorias.cypher`

## Cobertura minima del enunciado
- Nodos: Usuario, Pelicula, Genero, Actor, Director.
- Relaciones: CALIFICO, VIO, ES_AMIGO_DE, PERTENECE_A, ACTUO_EN, DIRIGIO, LE_GUSTA.
- Volumen minimo generado: 500 usuarios, 200 peliculas, 100 actores, 50 directores, 15 generos.
