// Segundo Proyecto BD2 - Bulk data load with LOAD CSV
// IMPORTANT:
// 1) Copy CSV files into Neo4j import directory.
// 2) If needed, set dbms.security.allow_csv_import_from_file_urls=true.
// 3) Execute in this order.

// -------------------------
// Nodes
// -------------------------
LOAD CSV WITH HEADERS FROM 'file:///usuarios.csv' AS row
MERGE (u:Usuario {user_id: toInteger(row.user_id)})
SET u.nombre = row.nombre,
    u.email = row.email,
    u.edad = toInteger(row.edad),
    u.pais = row.pais;

LOAD CSV WITH HEADERS FROM 'file:///peliculas.csv' AS row
MERGE (p:Pelicula {pelicula_id: toInteger(row.pelicula_id)})
SET p.titulo = row.titulo,
    p.anio_lanzamiento = toInteger(row.anio_lanzamiento),
    p.duracion = toInteger(row.duracion),
    p.sinopsis = row.sinopsis;

LOAD CSV WITH HEADERS FROM 'file:///generos.csv' AS row
MERGE (g:Genero {genero_id: toInteger(row.genero_id)})
SET g.nombre = row.nombre,
    g.descripcion = row.descripcion;

LOAD CSV WITH HEADERS FROM 'file:///actores.csv' AS row
MERGE (a:Actor {actor_id: toInteger(row.actor_id)})
SET a.nombre = row.nombre,
    a.fecha_nacimiento = date(row.fecha_nacimiento),
    a.nacionalidad = row.nacionalidad;

LOAD CSV WITH HEADERS FROM 'file:///directores.csv' AS row
MERGE (d:Director {director_id: toInteger(row.director_id)})
SET d.nombre = row.nombre,
    d.fecha_nacimiento = date(row.fecha_nacimiento),
    d.nacionalidad = row.nacionalidad;

// -------------------------
// Relationships
// -------------------------
LOAD CSV WITH HEADERS FROM 'file:///pertenece_a.csv' AS row
MATCH (p:Pelicula {pelicula_id: toInteger(row.pelicula_id)})
MATCH (g:Genero {genero_id: toInteger(row.genero_id)})
MERGE (p)-[:PERTENECE_A]->(g);

LOAD CSV WITH HEADERS FROM 'file:///dirigio.csv' AS row
MATCH (d:Director {director_id: toInteger(row.director_id)})
MATCH (p:Pelicula {pelicula_id: toInteger(row.pelicula_id)})
MERGE (d)-[:DIRIGIO]->(p);

LOAD CSV WITH HEADERS FROM 'file:///actuo_en.csv' AS row
MATCH (a:Actor {actor_id: toInteger(row.actor_id)})
MATCH (p:Pelicula {pelicula_id: toInteger(row.pelicula_id)})
MERGE (a)-[r:ACTUO_EN {personaje: row.personaje}]->(p);

LOAD CSV WITH HEADERS FROM 'file:///es_amigo_de.csv' AS row
MATCH (u1:Usuario {user_id: toInteger(row.user_id)})
MATCH (u2:Usuario {user_id: toInteger(row.friend_id)})
MERGE (u1)-[r:ES_AMIGO_DE]->(u2)
SET r.fecha_amistad = date(row.fecha_amistad);

LOAD CSV WITH HEADERS FROM 'file:///le_gusta.csv' AS row
MATCH (u:Usuario {user_id: toInteger(row.user_id)})
MATCH (g:Genero {genero_id: toInteger(row.genero_id)})
MERGE (u)-[r:LE_GUSTA]->(g)
SET r.nivel_interes = toInteger(row.nivel_interes);

LOAD CSV WITH HEADERS FROM 'file:///vio.csv' AS row
MATCH (u:Usuario {user_id: toInteger(row.user_id)})
MATCH (p:Pelicula {pelicula_id: toInteger(row.pelicula_id)})
MERGE (u)-[r:VIO]->(p)
SET r.fecha_visualizacion = date(row.fecha_visualizacion),
    r.completo = (toLower(row.completo) = 'true');

LOAD CSV WITH HEADERS FROM 'file:///califico.csv' AS row
MATCH (u:Usuario {user_id: toInteger(row.user_id)})
MATCH (p:Pelicula {pelicula_id: toInteger(row.pelicula_id)})
MERGE (u)-[r:CALIFICO]->(p)
SET r.puntuacion = toInteger(row.puntuacion),
    r.fecha = date(row.fecha),
    r.comentario = row.comentario;

// -------------------------
// Validation checks
// -------------------------
MATCH (u:Usuario) RETURN count(u) AS usuarios;
MATCH (p:Pelicula) RETURN count(p) AS peliculas;
MATCH (a:Actor) RETURN count(a) AS actores;
MATCH (d:Director) RETURN count(d) AS directores;
MATCH (g:Genero) RETURN count(g) AS generos;
