// Segundo Proyecto BD2 - Neo4j schema
// Run this script in Neo4j Browser before loading CSV data.

// Constraints for unique identifiers
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

// Optional indexes for frequent filters
CREATE INDEX pelicula_titulo_idx IF NOT EXISTS
FOR (p:Pelicula)
ON (p.titulo);

CREATE INDEX genero_nombre_idx IF NOT EXISTS
FOR (g:Genero)
ON (g.nombre);

CREATE INDEX usuario_email_idx IF NOT EXISTS
FOR (u:Usuario)
ON (u.email);
