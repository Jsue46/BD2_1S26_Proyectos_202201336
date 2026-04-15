# Guia de Explicacion del Proyecto (Defensa Oral)

## 0. Mapa de entregables (que decir si te preguntan "donde esta cada cosa")
- Prototipo funcional: Neo4j + scripts en `scripts/` + consultas en `consultas/`.
- Documentacion tecnica: `docs/Documentacion_Tecnica.md`.
- Codigo fuente organizado: `scripts/`, `consultas/`, `data/csv/`.
- Mockups/disenos: `docs/Diagrama_Grafo_Final.md` y `docs/Mockups_Disenos.md`.
- Manual de usuario: `docs/Manual_Usuario.md`.
- Evidencias: `docs/evidencias/capturas/` y `docs/Plantilla_Evidencias.md`.

## 1. Que problema resuelve este proyecto
Este proyecto implementa un sistema de recomendacion de peliculas en Neo4j, usando un modelo de grafo para representar relaciones complejas entre usuarios, peliculas y su red social.

La idea central es recomendar mejor contenido combinando:
- gustos del usuario,
- lo que ven y califican sus amigos,
- patrones de conectividad del grafo.

## 2. Que construiste (resumen rapido)
Se construyo una base de datos de grafos con:
- 5 tipos de nodos: Usuario, Pelicula, Genero, Actor, Director.
- 7 tipos de relaciones: CALIFICO, VIO, ES_AMIGO_DE, PERTENECE_A, ACTUO_EN, DIRIGIO, LE_GUSTA.
- carga masiva con `LOAD CSV`.
- consultas obligatorias del enunciado.
- analisis de redes y recomendacion.

Frase corta para defensa:
- "Implemente un recomendador de peliculas basado en relaciones sociales y preferencias, con carga masiva en Neo4j y consultas Cypher orientadas al negocio."

## 3. Arquitectura de carpetas (SegundoProyecto)
- `scripts/01_schema.cypher`: constraints e indices.
- `scripts/02_load_data.cypher`: carga de nodos y relaciones desde CSV.
- `scripts/generar_csv.py`: generacion automatica de datos de prueba.
- `data/csv/`: archivos CSV generados.
- `consultas/consultas_obligatorias.cypher`: consultas obligatorias, analisis y validaciones.
- `docs/`: manual, documentacion tecnica, mockups y evidencias.

## 4. Modelo de datos (como explicarlo)
### Nodos
- `Usuario`: user_id, nombre, email, edad, pais.
- `Pelicula`: pelicula_id, titulo, anio_lanzamiento, duracion, sinopsis.
- `Genero`: genero_id, nombre, descripcion.
- `Actor`: actor_id, nombre, fecha_nacimiento, nacionalidad.
- `Director`: director_id, nombre, fecha_nacimiento, nacionalidad.

### Relaciones
- `CALIFICO` (Usuario -> Pelicula): puntuacion, fecha, comentario.
- `VIO` (Usuario -> Pelicula): fecha_visualizacion, completo.
- `ES_AMIGO_DE` (Usuario -> Usuario): fecha_amistad.
- `PERTENECE_A` (Pelicula -> Genero).
- `ACTUO_EN` (Actor -> Pelicula): personaje.
- `DIRIGIO` (Director -> Pelicula).
- `LE_GUSTA` (Usuario -> Genero): nivel_interes.

## 5. Reglas de negocio y como se validan
### Regla 1: puntuacion de 1 a 5
Se cumple en la generacion de datos (`random.randint(1, 5)`) y se valida con:
```cypher
MATCH ()-[r:CALIFICO]->()
WHERE r.puntuacion < 1 OR r.puntuacion > 5
RETURN count(r) AS calificaciones_fuera_de_rango;
```
Esperado: `0`.

### Regla 2: amistad tratada como bidireccional
Las consultas usan patron sin direccion: `-[:ES_AMIGO_DE]-`.

### Regla 3: actor no repetido con mismo personaje en la misma pelicula
Se controla en la generacion con un set de claves `(actor, pelicula, personaje)`.
Validacion:
```cypher
MATCH (a:Actor)-[r:ACTUO_EN]->(p:Pelicula)
WITH a.actor_id AS actor_id, p.pelicula_id AS pelicula_id, r.personaje AS personaje, count(*) AS repeticiones
WHERE repeticiones > 1
RETURN actor_id, pelicula_id, personaje, repeticiones;
```
Esperado: 0 filas.

## 6. Carga de datos (pipeline)
1. Generar CSV con `python scripts/generar_csv.py`.
2. Copiar CSV a carpeta `import` de Neo4j.
3. Ejecutar `scripts/01_schema.cypher`.
4. Ejecutar `scripts/02_load_data.cypher`.
5. Verificar conteos minimos.

Resultado esperado al final del pipeline:
- Base funcional con nodos, relaciones y volumen minimo requerido para ejecutar consultas de negocio y analisis.

## 7. Volumen minimo requerido (y como lo cumples)
Objetivo del enunciado:
- usuarios >= 500
- peliculas >= 200
- actores >= 100
- directores >= 50
- generos >= 15

En el script se define explicitamente:
```python
COUNTS = {
    "usuarios": 500,
    "peliculas": 200,
    "actores": 100,
    "directores": 50,
    "generos": 15,
}
```

## 8. Consultas obligatorias (explicacion funcional)
### Q1
Peliculas calificadas por un usuario con puntuacion > 4.
Uso: detectar gustos fuertes.

### Q2
Peliculas vistas por amigos y no vistas por el usuario.
Uso: recomendacion social.

### Q3
Promedio de calificaciones de una pelicula.
Uso: medir aceptacion global.

### Q4
Generos favoritos segun calificaciones del usuario.
Uso: perfil de preferencias.

### Q5
Ruta mas corta de amistad entre dos usuarios (`shortestPath`).
Uso: grados de separacion.

### Q6
Peliculas mas populares por genero.
Uso: ranking por consumo.

## 9. Consultas complementarias
- Q7: actores por director.
- Q8: score de recomendacion (70% amigos + 30% gusto por genero).

Formula usada en Cypher:
- `score_recomendacion = 0.7 * score_amigos + 0.3 * score_genero`

Como explicarlo facil:
- `score_amigos` captura evidencia social.
- `score_genero` captura afinidad personal.
- la combinacion prioriza recomendaciones utiles y no vistas por el usuario.

## 10. Analisis de red
### Analisis 1: distribucion de grados de separacion
Mide que tan conectada esta la red de usuarios.

### Analisis 2: peliculas altamente conectadas
Construye un indice con:
- actores,
- directores,
- calificaciones,
- visualizaciones.

Indice:
- `indice = total_actores*2 + total_directores*3 + total_calificaciones + total_vistas`

Mensaje clave para exponer:
- "No solo consulto datos; tambien extraigo estructura de la red para entender conectividad y relevancia de contenido."

## 11. Decisiones tecnicas importantes (para justificar)
- Se usa Neo4j por su ventaja en traversal y relaciones multi-salto.
- Se usa `MERGE` para evitar duplicados en carga.
- Se definieron constraints unicos por ID para integridad.
- Se agregaron indices para campos de consulta frecuente.
- Se uso semilla fija (`RANDOM_SEED`) para reproducibilidad de datos.

## 12. Que mostrar en demo en 3-5 minutos
1. Diagrama del modelo (Mermaid).
2. Conteos minimos (usuarios/peliculas/etc.).
3. Q2 (recomendacion social simple).
4. Q5 (ruta corta entre usuarios).
5. Q8 (recomendacion con score).
6. Analisis 1 o 2 para cerrar con valor analitico.

Orden recomendado para hablar (guion de 1 minuto):
1. Contexto del problema.
2. Modelo de grafo y por que Neo4j.
3. Carga masiva y validacion de volumen.
4. Consultas obligatorias.
5. Recomendacion + analisis de red.
6. Cierre con ventajas y mejoras futuras.

## 13. Preguntas tipicas y respuestas cortas
### Por que Neo4j y no relacional?
Porque el problema es altamente relacional y requiere recorridos de varios saltos. En grafo, estas consultas son mas naturales y legibles.

### Como garantizaste integridad de datos?
Con constraints unicos en nodos principales, `MERGE` en carga y validaciones de reglas de negocio.

### Como evitaste duplicados en relaciones criticas?
Con `MERGE` y, para ACTUO_EN, control previo en generacion para no repetir actor-personaje-pelicula.

### Como funciona tu recomendador?
Combina evidencia social (calificaciones de amigos) y afinidad de genero del usuario, con ponderacion 70/30.

### Que limitaciones tiene tu prototipo?
Datos sinteticos y pesos fijos en el score; como mejora se puede calibrar con datos reales y evaluar precision.

### Como demuestras que cumples el enunciado?
Con evidencia de esquema, carga masiva, conteos minimos, ejecucion de consultas obligatorias, analisis de red y documentacion tecnica/manual de usuario en la carpeta `docs/`.

### Donde esta el diagrama y los mockups?
En `docs/Diagrama_Grafo_Final.md` y `docs/Mockups_Disenos.md`, con representacion de nodos, relaciones, direcciones y propiedades clave.

## 14. Guion sugerido para exponer
"Modele el dominio de streaming como grafo con 5 nodos y 7 relaciones. Cargue datos masivos con LOAD CSV cumpliendo los minimos del enunciado. Implemente las 6 consultas obligatorias, mas una recomendacion hibrida social-preferencias y dos analisis de red. Valide reglas de negocio (rango de calificacion y no duplicidad actor-personaje) y documente evidencias de ejecucion."

## 15. Checklist personal antes de presentar
- [ ] Explico el modelo sin leer.
- [ ] Entiendo cada consulta y su salida.
- [ ] Puedo justificar por que shortestPath es clave.
- [ ] Puedo explicar el score de recomendacion.
- [ ] Tengo claro que es obligatorio y que es valor agregado.
- [ ] Se donde esta cada entregable dentro de `SegundoProyecto`.
