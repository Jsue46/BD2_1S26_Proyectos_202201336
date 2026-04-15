# Documentacion Tecnica - Segundo Proyecto BD2

## 1. Descripcion general
Este proyecto implementa un sistema de recomendacion de peliculas con Neo4j, modelando entidades y relaciones sociales para explotar consultas de grafos.

## 2. Modelo conceptual de grafo
### Nodos
- Usuario: `user_id`, `nombre`, `email`, `edad`, `pais`
- Pelicula: `pelicula_id`, `titulo`, `anio_lanzamiento`, `duracion`, `sinopsis`
- Genero: `genero_id`, `nombre`, `descripcion`
- Actor: `actor_id`, `nombre`, `fecha_nacimiento`, `nacionalidad`
- Director: `director_id`, `nombre`, `fecha_nacimiento`, `nacionalidad`

### Relaciones
- `(:Usuario)-[:CALIFICO {puntuacion, fecha, comentario}]->(:Pelicula)`
- `(:Usuario)-[:VIO {fecha_visualizacion, completo}]->(:Pelicula)`
- `(:Usuario)-[:ES_AMIGO_DE {fecha_amistad}]-(:Usuario)`
- `(:Pelicula)-[:PERTENECE_A]->(:Genero)`
- `(:Actor)-[:ACTUO_EN {personaje}]->(:Pelicula)`
- `(:Director)-[:DIRIGIO]->(:Pelicula)`
- `(:Usuario)-[:LE_GUSTA {nivel_interes}]->(:Genero)`

## 3. Reglas de negocio reflejadas
- Rango de calificacion de 1 a 5 (controlado en la generacion de datos).
- Amistad tratada como bidireccional en consultas usando patron sin direccion.
- Evita duplicados por IDs unicos y uso de `MERGE`.

## 4. Scripts implementados
- `scripts/01_schema.cypher`: constraints e indices.
- `scripts/02_load_data.cypher`: carga de nodos y relaciones con `LOAD CSV`.
- `scripts/generar_csv.py`: genera data minima requerida.

### 4.1 Script Cypher completo de creacion del esquema
```cypher
CREATE CONSTRAINT usuario_id_unique IF NOT EXISTS
FOR (u:Usuario)
REQUIRE u.user_id IS UNIQUE;

CREATE CONSTRAINT pelicula_id_unique IF NOT EXISTS
FOR (p:Pelicula)
REQUIRE p.pelicula_id IS UNIQUE;

CREATE CONSTRAINT genero_id_unique IF NOT EXISTS
FOR (g:Genero)
REQUIRE g.genero_id IS UNIQUE;

CREATE CONSTRAINT actor_id_unique IF NOT EXISTS
FOR (a:Actor)
REQUIRE a.actor_id IS UNIQUE;

CREATE CONSTRAINT director_id_unique IF NOT EXISTS
FOR (d:Director)
REQUIRE d.director_id IS UNIQUE;

CREATE INDEX pelicula_titulo_idx IF NOT EXISTS
FOR (p:Pelicula)
ON (p.titulo);

CREATE INDEX genero_nombre_idx IF NOT EXISTS
FOR (g:Genero)
ON (g.nombre);

CREATE INDEX usuario_email_idx IF NOT EXISTS
FOR (u:Usuario)
ON (u.email);
```

## 5. Consultas y analisis
Archivo: `consultas/consultas_obligatorias.cypher`
- Consultas de negocio obligatorias.
- Consulta de recomendacion por amigos + gustos.
- Analisis de grados de separacion.
- Analisis de peliculas altamente conectadas.

## 6. Evidencia visual tecnica
### 6.0 Diagrama conceptual del modelo (mockup requerido)
Esta evidencia corresponde al entregable de mockups/disenos del enunciado.

```mermaid
graph LR
	U[Usuario\nuser_id, nombre, email, edad, pais]
	P[Pelicula\npelicula_id, titulo, anio_lanzamiento, duracion, sinopsis]
	G[Genero\ngenero_id, nombre, descripcion]
	A[Actor\nactor_id, nombre, fecha_nacimiento, nacionalidad]
	D[Director\ndirector_id, nombre, fecha_nacimiento, nacionalidad]

	U -- CALIFICO\n(puntuacion, fecha, comentario) --> P
	U -- VIO\n(fecha_visualizacion, completo) --> P
	U -- ES_AMIGO_DE\n(fecha_amistad) --- U
	U -- LE_GUSTA\n(nivel_interes) --> G

	P -- PERTENECE_A --> G
	A -- ACTUO_EN\n(personaje) --> P
	D -- DIRIGIO --> P
```
Descripcion: diagrama visual del modelo con todos los tipos de nodos, relaciones con direccion y propiedades clave.

### 6.1 Preparacion de entorno
Instancia en ejecucion y carpeta import con archivos CSV cargados.

![Instancia RUNNING](evidencias/capturas/01_instancia_running.png)
Descripcion: confirma que el DBMS local se encuentra activo y listo para pruebas.

![Import con CSV](evidencias/capturas/02_import_csv.png)
Descripcion: evidencia que los archivos fuente estan disponibles para carga masiva.

![Sesion Query conectada](evidencias/capturas/03_query_conectado.png)
Descripcion: confirma conexion operativa a la base neo4j para ejecutar Cypher.

### 6.2 Implementacion fisica
Ejecucion del esquema y carga masiva con validacion por conteos.

![Schema aplicado](evidencias/capturas/05_schema_ok.png)
Descripcion: evidencia de creacion de restricciones e indices del modelo.

![Carga masiva aplicada](evidencias/capturas/06_load_csv_ok.png)
Descripcion: evidencia de insercion de nodos y relaciones via LOAD CSV.

![Conteos finales](evidencias/capturas/07_conteos_finales.png)
Descripcion: validacion de cantidades minimas exigidas por el proyecto.

### 6.3 Evidencia de consultas de negocio
Resultados representativos de consultas obligatorias.

![Q1](evidencias/capturas/08_q1.png)
Descripcion: peliculas con puntuacion mayor a 4 para el usuario de referencia.

![Q2](evidencias/capturas/09_q2.png)
Descripcion: peliculas vistas por amigos que aun no figuran en el historial del usuario.

![Q3](evidencias/capturas/10_q3.png)
Descripcion: promedio de calificacion y numero de votos de una pelicula.

![Q4](evidencias/capturas/11_q4.png)
Descripcion: identificacion de generos favoritos por comportamiento de calificacion.

![Q5](evidencias/capturas/12_q5.png)
Descripcion: resultado del camino minimo de amistad entre dos usuarios.

![Q6](evidencias/capturas/13_q6.png)
Descripcion: ranking de peliculas mas vistas para el genero consultado.

### 6.4 Evidencia de recomendacion y analisis de red
Consultas de recomendacion y analitica del grafo.

![Q7](evidencias/capturas/14_q7.png)
Descripcion: relacion director-pelicula-actor como evidencia de traversal multihop.

![Q8 Recomendacion](evidencias/capturas/15_q8_recomendacion.png)
Descripcion: top de recomendaciones calculadas con score social y de preferencia.

![Analisis grados](evidencias/capturas/16_analisis_grados.png)
Descripcion: distribucion de grados de separacion de la red de usuarios.

## 7. Analisis de ventajas de usar Neo4j
- Neo4j modela de forma natural relaciones complejas entre usuarios, peliculas y red social sin necesidad de joins costosos.
- El lenguaje Cypher facilita expresar recorridos multihop (amistades, gustos y visualizaciones) de manera legible.
- Consultas de recomendacion y analisis de conectividad se implementan con menor complejidad que en modelos relacionales tradicionales.
- `shortestPath` permite resolver de forma directa grados de separacion entre usuarios.
- El enfoque de grafo favorece evolucion del modelo para agregar nuevas relaciones sin redisenar un esquema tabular rigido.

