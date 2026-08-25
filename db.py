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
"""


def obtener_conexion():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = obtener_conexion()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
