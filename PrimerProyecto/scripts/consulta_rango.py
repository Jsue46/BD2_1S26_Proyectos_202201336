from cassandra.cluster import Cluster
from datetime import date, timedelta

cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('reservadb')

fecha_inicio = date(2025, 7, 1)
fecha_fin = date(2025, 7, 5)  # Solo 5 dias para no imprimir demasiado

fecha_actual = fecha_inicio
total = 0

print("Ocupacion de espacios del 2025-07-01 al 2025-07-05:")
print("=" * 60)

while fecha_actual <= fecha_fin:
    rows = session.execute("""
        SELECT fecha, hora_inicio, espacio_id, nombre_reserva, estado
        FROM reservas_por_fecha
        WHERE fecha = %s
    """, (fecha_actual,))
    
    for row in rows:
        print(f"{row.fecha} | {str(row.hora_inicio)[:8]} | {row.estado} | {row.nombre_reserva}")
        total += 1
    
    fecha_actual += timedelta(days=1)

print(f"\nTotal de reservas encontradas: {total}")
cluster.shutdown()