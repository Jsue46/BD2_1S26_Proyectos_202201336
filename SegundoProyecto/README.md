# Segundo Proyecto - Sistema de Recomendacion de Peliculas con Neo4j

Implementacion del Segundo Proyecto de BD2 orientada a modelado de grafos, carga masiva de datos y consultas de recomendacion en Neo4j.

## Objetivo
Construir un sistema de recomendacion de peliculas basado en:
- preferencias del usuario,
- relaciones de amistad,
- patrones de visualizacion y calificacion.

## Tecnologias
- Neo4j Desktop / Neo4j Community 5.x
- Cypher
- Python 3.10+
- Faker

## Estructura del proyecto
- `scripts/01_schema.cypher`: constraints e indices del modelo.
- `scripts/02_load_data.cypher`: carga masiva de nodos y relaciones con `LOAD CSV`.
- `scripts/generar_csv.py`: generacion automatica de CSV.
- `consultas/consultas_obligatorias.cypher`: consultas obligatorias, analisis y validaciones.
- `data/csv/`: datos generados para carga.
- `docs/Documentacion_Tecnica.md`: documento tecnico principal.
- `docs/Manual_Usuario.md`: guia de instalacion, carga y ejecucion.
- `docs/Mockups_Disenos.md`: mockups/diagrama e instancia de grafo.
- `docs/Plantilla_Evidencias.md`: evidencia de resultados y analisis.
- `docs/Guia_Explicacion_Proyecto.md`: guia de defensa oral.

## Flujo de ejecucion rapido
1. Instalar dependencias Python:
   - `pip install -r requirements.txt`
2. Generar CSV:
   - `python scripts/generar_csv.py`
3. Copiar CSV de `data/csv/` a la carpeta `import` de Neo4j.
4. En Neo4j Query, ejecutar en orden:
   - `scripts/01_schema.cypher`
   - `scripts/02_load_data.cypher`
5. Ejecutar consultas en:
   - `consultas/consultas_obligatorias.cypher`

## Validacion minima
Conteos esperados:
- usuarios >= 500
- peliculas >= 200
- actores >= 100
- directores >= 50
- generos >= 15

## Cobertura del enunciado
- Nodos: `Usuario`, `Pelicula`, `Genero`, `Actor`, `Director`.
- Relaciones: `CALIFICO`, `VIO`, `ES_AMIGO_DE`, `PERTENECE_A`, `ACTUO_EN`, `DIRIGIO`, `LE_GUSTA`.
- Consultas obligatorias de rubrica implementadas: Q1, Q2, Q4, Q5, Q7 y Q8.
- Consultas adicionales implementadas: Q3 (promedio de calificaciones), Q6 (populares por genero), analisis de red y validaciones de integridad.

## Entregables en `docs/`
- Documentacion tecnica
- Manual de usuario
- Mockups/Disenos
- Plantilla de evidencias
- Guia de explicacion del proyecto
