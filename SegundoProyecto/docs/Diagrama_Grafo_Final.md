# Diagrama de Grafo Final

Este diagrama resume el modelo conceptual/fisico implementado para el sistema de recomendacion de peliculas en Neo4j.

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

## Reglas clave reflejadas
- `CALIFICO.puntuacion` en rango de 1 a 5.
- La amistad se consulta como relacion bidireccional en Cypher.
- Una pelicula puede tener varios actores y generos, y un director.

## Trazabilidad con scripts
- Esquema: `scripts/01_schema.cypher`
- Carga: `scripts/02_load_data.cypher`
- Consultas: `consultas/consultas_obligatorias.cypher`
