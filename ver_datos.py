"""
Script para ver rápidamente el contenido de la base de datos.
Uso: py -3.13 ver_datos.py
"""
from db import obtener_conexion

conn = obtener_conexion()

for tabla in ["admisiones", "contactos", "noticias"]:
    filas = conn.execute(f"SELECT * FROM {tabla} ORDER BY id DESC").fetchall()
    print(f"\n=== {tabla.upper()} ({len(filas)} registros) ===")
    if not filas:
        print("  (sin datos todavía)")
        continue
    for fila in filas:
        print(dict(fila))

conn.close()
