from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement, ConsistencyLevel
from datetime import date
import time

cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('reservadb')

print("=" * 60)
print("PLAN DE EJECUCION Y MEDICION DE LATENCIAS")
print("ReservaDB - Sistema de Reservas en Cassandra")
print("=" * 60)

# Obtener datos reales para las consultas
espacio = session.execute("SELECT espacio_id FROM espacios LIMIT 1").one()
usuario = session.execute("SELECT usuario_id FROM usuarios LIMIT 1").one()
fecha = session.execute("SELECT fecha FROM reservas_por_fecha LIMIT 1").one()

espacio_id = espacio.espacio_id
usuario_id = usuario.usuario_id
fecha_consulta = fecha.fecha

print(f"\nDatos usados en las consultas:")
print(f"  espacio_id : {espacio_id}")
print(f"  usuario_id : {usuario_id}")
print(f"  fecha      : {fecha_consulta}")

# -------------------------------------------------------
# Funcion para medir latencia promedio
# -------------------------------------------------------
def medir_latencia(nombre_query, query, params, repeticiones=5):
    print(f"\n{'─' * 60}")
    print(f"Query: {nombre_query}")
    print(f"Repeticiones: {repeticiones}")
    
    latencias = []
    filas_total = 0
    
    stmt = SimpleStatement(query, consistency_level=ConsistencyLevel.QUORUM)
    
    for i in range(repeticiones):
        inicio = time.time()
        resultado = session.execute(stmt, params)
        filas = len(resultado.all())
        fin = time.time()
        latencia = round((fin - inicio) * 1000, 2)
        latencias.append(latencia)
        filas_total = filas
        print(f"  Ejecucion {i+1}: {latencia} ms | {filas} filas")
    
    promedio = round(sum(latencias) / len(latencias), 2)
    minima = min(latencias)
    maxima = max(latencias)
    
    print(f"\n  Filas devueltas : {filas_total}")
    print(f"  Latencia minima : {minima} ms")
    print(f"  Latencia maxima : {maxima} ms")
    print(f"  Latencia promedio: {promedio} ms")
    print(f"  Uso de ALLOW FILTERING: NO")
    print(f"  Uso de JOINs: NO")
    return promedio

# -------------------------------------------------------
# Q1: Disponibilidad de espacio por fecha
# -------------------------------------------------------
q1 = """
    SELECT hora_inicio, hora_fin, nombre_reserva, usuario_id, estado
    FROM reservas_por_espacio_fecha
    WHERE espacio_id = %s AND fecha = %s
"""
lat_q1 = medir_latencia(
    "Q1 - Disponibilidad de espacio por fecha",
    q1, (espacio_id, fecha_consulta)
)

# -------------------------------------------------------
# Q2: Historial de reservas por usuario
# -------------------------------------------------------
q2 = """
    SELECT fecha, hora_inicio, hora_fin, espacio_id, nombre_reserva, estado
    FROM reservas_por_usuario
    WHERE usuario_id = %s
"""
lat_q2 = medir_latencia(
    "Q2 - Historial de reservas por usuario",
    q2, (usuario_id,)
)

# -------------------------------------------------------
# Q3: Ocupacion por fecha exacta (1 particion)
# -------------------------------------------------------
q3 = """
    SELECT fecha, hora_inicio, espacio_id, nombre_reserva, usuario_id, estado
    FROM reservas_por_fecha
    WHERE fecha = %s
"""
lat_q3 = medir_latencia(
    "Q3 - Ocupacion de espacios por fecha",
    q3, (fecha_consulta,)
)

# -------------------------------------------------------
# Q3b: Ocupacion por rango de fechas (via Python)
# -------------------------------------------------------
print(f"\n{'─' * 60}")
print("Query: Q3b - Ocupacion por rango de fechas (via Python)")
print("Rango: 2025-07-01 al 2025-07-07 (7 dias)")

from datetime import timedelta
fecha_inicio = date(2025, 7, 1)
fecha_fin = date(2025, 7, 7)
fecha_actual = fecha_inicio
total_filas = 0
latencias_rango = []

stmt_rango = SimpleStatement(
    "SELECT fecha, hora_inicio, espacio_id, estado FROM reservas_por_fecha WHERE fecha = %s",
    consistency_level=ConsistencyLevel.QUORUM
)

while fecha_actual <= fecha_fin:
    inicio = time.time()
    rows = session.execute(stmt_rango, (fecha_actual,))
    filas = len(rows.all())
    fin = time.time()
    latencia = round((fin - inicio) * 1000, 2)
    latencias_rango.append(latencia)
    total_filas += filas
    print(f"  {fecha_actual}: {latencia} ms | {filas} filas")
    fecha_actual += timedelta(days=1)

promedio_rango = round(sum(latencias_rango) / len(latencias_rango), 2)
print(f"\n  Total filas: {total_filas}")
print(f"  Latencia promedio por dia: {promedio_rango} ms")
print(f"  Nota: rango manejado a nivel de aplicacion (Python)")
print(f"        para evitar ALLOW FILTERING en Cassandra")

# -------------------------------------------------------
# Resumen final
# -------------------------------------------------------
print(f"\n{'=' * 60}")
print("RESUMEN DE LATENCIAS")
print(f"{'=' * 60}")
print(f"  Q1 - Disponibilidad por espacio y fecha : {lat_q1} ms")
print(f"  Q2 - Historial por usuario              : {lat_q2} ms")
print(f"  Q3 - Ocupacion por fecha exacta         : {lat_q3} ms")
print(f"  Q3b - Rango de fechas (por dia)         : {promedio_rango} ms promedio")
print(f"\n  Consistency Level usado: QUORUM")
print(f"  Todas las consultas sin ALLOW FILTERING: SI")
print(f"  Todas las consultas sin JOINs: SI")
print("=" * 60)

cluster.shutdown()