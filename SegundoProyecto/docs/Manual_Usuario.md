# Manual de Usuario - Segundo Proyecto BD2

## 1. Objetivo
Este manual describe el flujo completo para ejecutar el proyecto en Neo4j, validar resultados y documentar evidencias para entrega.

## 2. Requisitos previos
- Neo4j Desktop o Neo4j Community 5.x.
- Python 3.10 o superior.
- Carpeta de trabajo: `SegundoProyecto`.

Archivos base del proyecto:
- `scripts/01_schema.cypher`
- `scripts/02_load_data.cypher`
- `scripts/generar_csv.py`
- `consultas/consultas_obligatorias.cypher`
- `docs/Plantilla_Evidencias.md`

## 3. Flujo operativo recomendado
### Paso 1. Generar datos CSV
Ejecutar en terminal dentro de `SegundoProyecto`:

```bash
pip install -r requirements.txt
python scripts/generar_csv.py
```

Salida esperada: mensaje `CSV generation completed` y archivos en `data/csv`.

Nota: esta ejecucion puede documentarse en la captura de carga de datos de la plantilla de evidencias.



### Paso 2. Cargar archivos al DBMS
1. Abrir Neo4j Desktop y verificar instancia en estado RUNNING.
2. Abrir la carpeta del DBMS desde el icono de carpeta junto a `Path`.
3. Entrar a la carpeta `import`.
4. Copiar todos los CSV desde `data/csv` a `import`.

Capturas sugeridas:
![E01 Instancia RUNNING](evidencias/capturas/01_instancia_running.png)
Descripcion: estado RUNNING de la instancia local en Neo4j Desktop.

![E02 Import con CSV](evidencias/capturas/02_import_csv.png)
Descripcion: carpeta import con los CSV listos para ser leidos por LOAD CSV.

![E03 Query conectado](evidencias/capturas/03_query_conectado.png)
Descripcion: sesion de Query conectada a la base neo4j.

### Paso 3. Ejecutar esquema y carga
En Neo4j Query ejecutar en orden:
1. Todo `scripts/01_schema.cypher`.
2. Todo `scripts/02_load_data.cypher`.

Capturas sugeridas:
![E05 Schema OK](evidencias/capturas/05_schema_ok.png)
Descripcion: ejecucion correcta del script de esquema (constraints e indices).

![E06 Load CSV OK](evidencias/capturas/06_load_csv_ok.png)
Descripcion: ejecucion correcta de la carga masiva de nodos y relaciones.

### Paso 4. Validar conteos minimos
Ejecutar:

```cypher
MATCH (u:Usuario) RETURN count(u) AS usuarios;
MATCH (p:Pelicula) RETURN count(p) AS peliculas;
MATCH (a:Actor) RETURN count(a) AS actores;
MATCH (d:Director) RETURN count(d) AS directores;
MATCH (g:Genero) RETURN count(g) AS generos;
```

Minimos esperados:
- usuarios >= 500
- peliculas >= 200
- actores >= 100
- directores >= 50
- generos >= 15

Captura sugerida:
![E07 Conteos finales](evidencias/capturas/07_conteos_finales.png)
Descripcion: verificacion de cantidades minimas requeridas por el enunciado.

### Paso 5. Ejecutar consultas funcionales
Abrir `consultas/consultas_obligatorias.cypher` y ejecutar bloques en este orden:
1. Q1
2. Q2
3. Q3
4. Q4
5. Q5
6. Q6
7. Q7
8. Q8
9. Analysis 1
10. Analysis 2

Capturas sugeridas por bloque:
![E08 Q1](evidencias/capturas/08_q1.png)
Descripcion: peliculas calificadas por el usuario con puntuacion mayor a 4.

![E09 Q2](evidencias/capturas/09_q2.png)
Descripcion: peliculas vistas por amigos que el usuario aun no ha visto.

![E10 Q3](evidencias/capturas/10_q3.png)
Descripcion: promedio y cantidad de calificaciones de una pelicula.

![E11 Q4](evidencias/capturas/11_q4.png)
Descripcion: generos favoritos del usuario segun historial de calificaciones.

![E12 Q5](evidencias/capturas/12_q5.png)
Descripcion: ruta mas corta de amistad entre dos usuarios.

![E13 Q6](evidencias/capturas/13_q6.png)
Descripcion: ranking de peliculas mas populares dentro de un genero.

![E14 Q7](evidencias/capturas/14_q7.png)
Descripcion: actores asociados a peliculas dirigidas por un director especifico.

![E15 Q8 Recomendacion](evidencias/capturas/15_q8_recomendacion.png)
Descripcion: recomendaciones calculadas por calificaciones de amigos y gustos del usuario.

![E16 Analisis de grados](evidencias/capturas/16_analisis_grados.png)
Descripcion: distribucion de grados de separacion en la red de amistades.

### Interpretacion de resultados de recomendacion (Q8)
- `score_amigos`: promedio de calificaciones altas dadas por amigos a una pelicula no vista por el usuario.
- `score_genero`: afinidad del usuario con los generos de esa pelicula, segun relaciones `LE_GUSTA`.
- `score_recomendacion`: combinacion ponderada (70% social y 30% preferencias) para priorizar sugerencias.
- Lectura practica: entre mayor sea `score_recomendacion`, mayor prioridad tiene la pelicula para recomendarse al usuario.



## 4. Guia profesional de capturas
### 4.1 Herramienta de captura
- Usar `Win + Shift + S`.
- Tipo recomendado: recorte rectangular.
- Incluir siempre consulta y resultado en la misma imagen cuando sea posible.

### 4.2 Ubicacion para guardar capturas
Guardar todas las evidencias en:
- `docs/evidencias/capturas/`

### 4.3 Capturas obligatorias y significado
1. `01_instancia_running.png`
Descripcion: instancia Neo4j en RUNNING.
Significado: confirma entorno activo.

2. `02_import_csv.png`
Descripcion: carpeta `import` con CSV visibles.
Significado: confirma disponibilidad de insumos para `LOAD CSV`.

3. `03_query_conectado.png`
Descripcion: Neo4j Query conectado a la base `neo4j`.
Significado: confirma sesion lista para ejecutar Cypher.

4. `05_schema_ok.png`
Descripcion: ejecucion de `01_schema.cypher` con salida sin error.
Significado: confirma constraints e indices creados.

5. `06_load_csv_ok.png`
Descripcion: ejecucion de `02_load_data.cypher` finalizada.
Significado: confirma carga de nodos y relaciones.

6. `07_conteos_finales.png`
Descripcion: resultados de conteos de Usuario/Pelicula/Actor/Director/Genero.
Significado: confirma cumplimiento de volumen minimo.

7. `08_q1.png`
Descripcion: consulta Q1 y resultado.
Significado: valida peliculas con puntuacion > 4 para usuario fijo.

8. `09_q2.png`
Descripcion: consulta Q2 y resultado.
Significado: valida peliculas vistas por amigos no vistas por el usuario.

9. `10_q3.png`
Descripcion: consulta Q3 y resultado.
Significado: valida promedio de calificaciones de una pelicula.

10. `10_q4.png`
Descripcion: consulta Q4 y resultado.
Significado: valida generos favoritos por historial de calificacion.

11. `11_q5.png`
Descripcion: consulta Q5 con ruta (grafo y/o tabla).
Significado: valida ruta mas corta de amistad.

12. `12_q6.png`
Descripcion: consulta Q6 y ranking.
Significado: valida peliculas mas populares por genero.

13. `13_q7.png`
Descripcion: consulta Q7 y resultado.
Significado: valida actores por director y pelicula.

14. `14_q8_recomendacion.png`
Descripcion: consulta Q8 y top resultados.
Significado: valida recomendacion por amigos y gustos.

15. `16_analisis_grados.png`
Descripcion: Analysis 1 y distribucion de grados.
Significado: evidencia analisis de red de separacion social.

## 5. Buenas practicas de evidencia
- Mantener visible el comentario `// Qx` de cada consulta en la captura.
- Si resultado es largo, tomar una segunda captura solo de resultados.
- No recortar columnas clave (IDs, metricas, promedios).
- Usar nombres de archivo exactos para trazabilidad.

## 6. Seccion de galeria final en el informe
Al exportar a PDF, mantener esta secuencia visual:
1. Configuracion y preparacion (E01-E03).
2. Implementacion fisica y validacion (E05-E07).
3. Consultas de negocio (E08-E13).
4. Consultas complementarias y recomendacion (E14-E15).
5. Analisis de red (E16).

## 7. Solucion de problemas frecuente
- Error `Couldn't load the external resource`:
  - Verificar que el CSV exista en `import` y con el mismo nombre.
  - Verificar permisos de lectura de la carpeta.
- Error de datos no encontrados:
  - Ejecutar primero `01_schema.cypher` y luego `02_load_data.cypher`.
- Lotes lentos:
  - Ejecutar bloques por separado y esperar confirmacion antes del siguiente.



