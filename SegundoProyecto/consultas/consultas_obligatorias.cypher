// Segundo Proyecto BD2 - Consultas Cypher listas para ejecutar
// Estas consultas usan valores fijos para ejecutarse sin parametros.
// Valores usados:
// usuarioId = 1
// usuarioA = 10
// usuarioB = 33
// generoNombre = 'Action'
// peliculaId = 5
// directorId = 7
// Consultas obligatorias segun rubrica: Q1, Q2, Q4, Q5, Q7, Q8.
// Consultas adicionales implementadas: Q3 y Q6.

// Q1: Movies rated by a user with score > 4
MATCH (u:Usuario {user_id: 1})-[r:CALIFICO]->(p:Pelicula)
WHERE r.puntuacion > 4
RETURN p.pelicula_id, p.titulo, r.puntuacion, r.fecha
ORDER BY r.puntuacion DESC, r.fecha DESC;

// Q2: Movies watched by user friends but not watched by the user
MATCH (u:Usuario {user_id: 1})-[:ES_AMIGO_DE]-(amigo:Usuario)-[:VIO]->(p:Pelicula)
WHERE NOT (u)-[:VIO]->(p)
RETURN DISTINCT p.pelicula_id, p.titulo
ORDER BY p.titulo;

// Q3: Average ratings of a movie (enunciado section 3.2)
MATCH (:Usuario)-[r:CALIFICO]->(p:Pelicula {pelicula_id: 5})
RETURN p.titulo AS pelicula, avg(r.puntuacion) AS promedio, count(r) AS total_calificaciones;

// Q4: Favorite genres of a user based on own ratings
MATCH (u:Usuario {user_id: 1})-[r:CALIFICO]->(p:Pelicula)-[:PERTENECE_A]->(g:Genero)
RETURN g.nombre AS genero, avg(r.puntuacion) AS promedio_genero, count(*) AS interacciones
ORDER BY promedio_genero DESC, interacciones DESC;

// Q5: Shortest friendship path between two users
MATCH (u1:Usuario {user_id: 10}), (u2:Usuario {user_id: 33})
MATCH p = shortestPath((u1)-[:ES_AMIGO_DE*]-(u2))
RETURN p, length(p) AS grados_separacion;

// Q6: Most popular movies inside a specific genre (most views)
MATCH (:Usuario)-[:VIO]->(p:Pelicula)-[:PERTENECE_A]->(g:Genero {nombre: 'Action'})
RETURN p.pelicula_id, p.titulo, count(*) AS total_visualizaciones
ORDER BY total_visualizaciones DESC
LIMIT 20;

// Q7: Actors by director (rubrica/metodologia mention)
MATCH (d:Director {director_id: 7})-[:DIRIGIO]->(p:Pelicula)<-[aRel:ACTUO_EN]-(a:Actor)
RETURN d.nombre AS director, p.titulo AS pelicula, a.nombre AS actor, aRel.personaje AS personaje
ORDER BY p.titulo, a.nombre;

// Q8: Recommendation score based on friends ratings and user preferences
MATCH (u:Usuario {user_id: 1})-[:ES_AMIGO_DE]-(amigo:Usuario)-[c:CALIFICO]->(p:Pelicula)
WHERE c.puntuacion >= 4 AND NOT (u)-[:VIO]->(p)
OPTIONAL MATCH (u)-[gusto:LE_GUSTA]->(:Genero)<-[:PERTENECE_A]-(p)
WITH p,
     avg(c.puntuacion) AS score_amigos,
     coalesce(avg(gusto.nivel_interes), 0) AS score_genero
RETURN p.pelicula_id,
       p.titulo,
       round((score_amigos * 0.7 + score_genero * 0.3) * 100) / 100.0 AS score_recomendacion,
       score_amigos,
       score_genero
ORDER BY score_recomendacion DESC
LIMIT 20;

// Analysis 1: Degrees of separation distribution
MATCH (u1:Usuario), (u2:Usuario)
WHERE u1.user_id < u2.user_id
MATCH p = shortestPath((u1)-[:ES_AMIGO_DE*]-(u2))
RETURN length(p) AS grados, count(*) AS pares_usuarios
ORDER BY grados;

// Analysis 2: Highly connected movies (actors + direction + ratings + views)
MATCH (p:Pelicula)
OPTIONAL MATCH (p)<-[:ACTUO_EN]-(a:Actor)
WITH p, count(DISTINCT a) AS total_actores
OPTIONAL MATCH (p)<-[:DIRIGIO]-(d:Director)
WITH p, total_actores, count(DISTINCT d) AS total_directores
OPTIONAL MATCH (p)<-[:CALIFICO]-(:Usuario)
WITH p, total_actores, total_directores, count(*) AS total_calificaciones
OPTIONAL MATCH (p)<-[:VIO]-(:Usuario)
RETURN p.pelicula_id,
       p.titulo,
       total_actores,
       total_directores,
       total_calificaciones,
       count(*) AS total_vistas,
       (total_actores * 2 + total_directores * 3 + total_calificaciones + count(*)) AS indice_conectividad
ORDER BY indice_conectividad DESC
LIMIT 20;

// Validation 1: ratings outside allowed range (must be 0 rows)
MATCH ()-[r:CALIFICO]->()
WHERE r.puntuacion < 1 OR r.puntuacion > 5
RETURN count(r) AS calificaciones_fuera_de_rango;

// Validation 2: duplicate actor+character in same movie (must be 0 rows)
MATCH (a:Actor)-[r:ACTUO_EN]->(p:Pelicula)
WITH a.actor_id AS actor_id, p.pelicula_id AS pelicula_id, r.personaje AS personaje, count(*) AS repeticiones
WHERE repeticiones > 1
RETURN actor_id, pelicula_id, personaje, repeticiones;

// Mockup helper: sample instance subgraph for screenshot evidence
MATCH p = (u:Usuario {user_id: 1})-[:ES_AMIGO_DE]-(amigo:Usuario)-[:VIO]->(pel:Pelicula)
RETURN p
LIMIT 30;
