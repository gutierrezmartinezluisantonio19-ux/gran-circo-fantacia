import sqlite3

conexion = sqlite3.connect("gran_circo_fantacia.db")

cursor = conexion.cursor()

# Activar las relaciones entre tablas
cursor.execute("PRAGMA foreign_keys = ON")

# Tabla de clientes
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    telefono TEXT NOT NULL,
    correo TEXT NOT NULL UNIQUE
)
""")

# Tabla de espectáculos
cursor.execute("""
CREATE TABLE IF NOT EXISTS espectaculos (
    id_espectaculo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    duracion INTEGER NOT NULL,
    precio REAL NOT NULL
)
""")

# Tabla de funciones
cursor.execute("""
CREATE TABLE IF NOT EXISTS funciones (
    id_funcion INTEGER PRIMARY KEY AUTOINCREMENT,
    id_espectaculo INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    hora TEXT NOT NULL,
    FOREIGN KEY (id_espectaculo)
        REFERENCES espectaculos(id_espectaculo)
)
""")

# Tabla de reservaciones
cursor.execute("""
CREATE TABLE IF NOT EXISTS reservaciones (
    id_reservacion INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    id_funcion INTEGER NOT NULL,
    cantidad_boletos INTEGER NOT NULL,
    fecha_reservacion TEXT NOT NULL,
    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_funcion)
        REFERENCES funciones(id_funcion)
)
""")

# Espectáculos iniciales
cursor.execute("""
INSERT OR IGNORE INTO espectaculos
(id_espectaculo, nombre, descripcion, duracion, precio)
VALUES
(1, 'Gran Espectáculo', 'Un espectáculo lleno de magia y diversión.', 90, 150),
(2, 'Exhibición de Animales', 'Conoce a los animales del Gran Circo Fantacia.', 60, 100),
(3, 'Los Payasos', 'Un show lleno de risas y diversión.', 45, 80)
""")

# Funciones iniciales
cursor.execute("""
INSERT OR IGNORE INTO funciones
(id_funcion, id_espectaculo, fecha, hora)
VALUES
(1, 1, '2026-10-03', '18:00'),
(2, 1, '2026-10-03', '21:00'),
(3, 2, '2026-10-04', '17:00'),
(4, 3, '2026-10-04', '19:00')
""")

conexion.commit()
conexion.close()

print("Base de datos creada y configurada correctamente.")