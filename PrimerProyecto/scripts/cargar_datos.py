from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, ConsistencyLevel
from faker import Faker
import uuid
import random
from datetime import date, timedelta, time

# Conexion al cluster
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('reservadb')
fake = Faker('es_MX')

print("Conectado al cluster ReservaDB...")

# =====================================================
# GENERAR USUARIOS (500)
# =====================================================
print("Insertando usuarios...")
usuarios = []
for i in range(500):
    uid = uuid.uuid4()
    usuarios.append(uid)
    session.execute("""
        INSERT INTO usuarios (usuario_id, nombre, email, dpi, telefono, nit)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (uid, fake.name(), fake.email(), 
          str(random.randint(1000000000000, 9999999999999)),
          fake.phone_number()[:15], 
          str(random.randint(1000000, 9999999))))

print(f"  -> {len(usuarios)} usuarios insertados")

# =====================================================
# GENERAR ESPACIOS (50)
# =====================================================
print("Insertando espacios...")
espacios = []
tipos = ['Sala de conferencia', 'Escritorio', 'Auditorio', 'Sala privada']
ubicaciones = ['Edificio A', 'Edificio B', 'Edificio C', 'Planta baja', 'Piso 2']

for i in range(50):
    eid = uuid.uuid4()
    espacios.append(eid)
    session.execute("""
        INSERT INTO espacios (espacio_id, nombre, tipo, capacidad, ubicacion)
        VALUES (%s, %s, %s, %s, %s)
    """, (eid, f"Espacio {i+1}", 
          random.choice(tipos),
          random.randint(2, 100),
          random.choice(ubicaciones)))

print(f"  -> {len(espacios)} espacios insertados")

# =====================================================
# GENERAR 100,000 RESERVAS CON BATCH WRITES
# =====================================================
print("Insertando 100,000 reservas con Batch Writes...")

insert_por_espacio = session.prepare("""
    INSERT INTO reservas_por_espacio_fecha 
    (espacio_id, fecha, hora_inicio, reserva_id, usuario_id, hora_fin, estado, nombre_reserva)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""")

insert_por_usuario = session.prepare("""
    INSERT INTO reservas_por_usuario 
    (usuario_id, fecha, hora_inicio, reserva_id, espacio_id, hora_fin, estado, nombre_reserva)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""")

insert_por_fecha = session.prepare("""
    INSERT INTO reservas_por_fecha 
    (fecha, hora_inicio, espacio_id, reserva_id, usuario_id, hora_fin, estado, nombre_reserva)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""")

estados = ['confirmada', 'cancelada', 'pendiente']
fecha_inicio = date(2025, 1, 1)
total = 100000
batch_size = 50
contador = 0

while contador < total:
    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    
    for _ in range(min(batch_size, total - contador)):
        rid = uuid.uuid4()
        uid = random.choice(usuarios)
        eid = random.choice(espacios)
        fecha = fecha_inicio + timedelta(days=random.randint(0, 365))
        hora_inicio_h = random.randint(7, 18)
        hora_inicio_t = time(hora_inicio_h, 0, 0)
        hora_fin_t = time(min(hora_inicio_h + random.randint(1, 3), 22), 0, 0)
        estado = random.choice(estados)
        nombre = f"Reserva {fake.word().capitalize()}"

        batch.add(insert_por_espacio, (eid, fecha, hora_inicio_t, rid, uid, hora_fin_t, estado, nombre))
        batch.add(insert_por_usuario, (uid, fecha, hora_inicio_t, rid, eid, hora_fin_t, estado, nombre))
        batch.add(insert_por_fecha, (fecha, hora_inicio_t, eid, rid, uid, hora_fin_t, estado, nombre))

    session.execute(batch)
    contador += batch_size

    if contador % 5000 == 0:
        print(f"  -> {contador:,} reservas insertadas...")

print(f"\n✅ {total:,} reservas insertadas exitosamente!")
cluster.shutdown()