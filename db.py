import sqlite3

DATABASE = "mibasededatos.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS admisiones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_estudiante TEXT NOT NULL,
    grado TEXT NOT NULL,
    nombre_tutor TEXT NOT NULL,
    telefono TEXT NOT NULL,
    email TEXT,
    mensaje TEXT,
    fecha TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS contactos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL,
    mensaje TEXT NOT NULL,
    fecha TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS noticias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    contenido TEXT NOT NULL,
    fecha TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS avisos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    fecha TEXT NOT NULL,
    categoria TEXT NOT NULL DEFAULT 'General',
    contenido TEXT NOT NULL,
    creado TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS eventos_calendario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    anio INTEGER NOT NULL DEFAULT 2026,
    mes INTEGER NOT NULL,
    dia INTEGER NOT NULL,
    titulo TEXT NOT NULL
);
"""

# Datos de partida: se insertan una sola vez si las tablas están vacías,
# para no perder los avisos/eventos que ya existían en el diseño original.
AVISOS_INICIALES = [
    ("Aviso Importante: Suspensión de Clases", "10 de Septiembre, 2026", "Urgente",
     "Estimada comunidad educativa, se les informa que el día jueves 10 de"
     " septiembre no habrá clases por motivo de asueto institucional."
     " Reanudamos actividades normales el viernes 11."),
    ("Reunión de Padres de Familia", "15 de Septiembre, 2026", "General",
     "Convocatoria a todos los padres de familia para la entrega del"
     " reporte de avance académico correspondiente al parcial."),
]

EVENTOS_INICIALES = [
    (1, 1, "Matrícula"),
    (2, 1, "Inicio de Matrículas"),
    (3, 1, "Inicio de Clases"),
    (4, 2, "Semana Santa"),
    (5, 1, "Día del Trabajo"),
    (6, 15, "Exámenes"),
    (7, 20, "Vacaciones"),
    (8, 1, "Reanudación"),
    (9, 2, "Examen Parcial"),
    (9, 10, "Suspensión"),
    (9, 15, "Reunión"),
    (10, 3, "Feriado"),
    (11, 25, "Clausura"),
    (12, 25, "Navidad"),
]


def obtener_conexion():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def _sembrar_datos_iniciales(conn):
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM avisos")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO avisos (titulo, fecha, categoria, contenido) VALUES (?, ?, ?, ?)",
            AVISOS_INICIALES,
        )

    cur.execute("SELECT COUNT(*) FROM eventos_calendario")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO eventos_calendario (mes, dia, titulo) VALUES (?, ?, ?)",
            EVENTOS_INICIALES,
        )

    conn.commit()


def init_db():
    conn = obtener_conexion()
    conn.executescript(SCHEMA)
    conn.commit()
    _sembrar_datos_iniciales(conn)
    conn.close()
