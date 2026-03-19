from cassandra.cluster import Cluster
from cassandra.policies import ConsistencyLevel
from cassandra.query import SimpleStatement
import time
import uuid

cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('reservadb')

print("=" * 55)
print("PRUEBAS DE CONSISTENCY LEVELS")
print("=" * 55)

# Tomamos un usuario_id real para la prueba
row = session.execute("SELECT usuario_id FROM reservas_por_usuario LIMIT 1").one()
uid = row.usuario_id

def medir_consulta(nivel, nombre):
    query = SimpleStatement(
        f"SELECT * FROM reservas_por_usuario WHERE usuario_id = {uid} LIMIT 10",
        consistency_level=nivel
    )
    inicio = time.time()
    resultado = session.execute(query)
    filas = len(resultado.all())
    fin = time.time()
    latencia = round((fin - inicio) * 1000, 2)
    print(f"  {nombre:10} -> {filas} filas | Latencia: {latencia} ms")
    return latencia

print("\n[SIN FALLOS - 3 nodos activos]")
l1 = medir_consulta(ConsistencyLevel.ONE,    "ONE")
l2 = medir_consulta(ConsistencyLevel.QUORUM, "QUORUM")
l3 = medir_consulta(ConsistencyLevel.ALL,    "ALL")

print(f"\n  Resumen: ONE={l1}ms | QUORUM={l2}ms | ALL={l3}ms")
print("\n✅ Guardar estos resultados para la documentacion")

cluster.shutdown()