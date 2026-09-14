import calendar
import functools
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session

from db import obtener_conexion, init_db

load_dotenv()  # lee las variables del archivo .env (no se sube a GitHub)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "cambia-esta-clave-por-una-secreta")

init_db()

# La semana del calendario empieza en Domingo
calendar.setfirstweekday(calendar.SUNDAY)

# --- Acceso al panel de administración de Mensajes ---
# El usuario y la contraseña reales viven en el archivo ".env" (que NO se
# sube a GitHub). Si no existe ese archivo, se usan estos valores de
# respaldo — cámbialos cuanto antes si los llegas a usar.
ADMIN_USUARIO = os.environ.get("ADMIN_USUARIO", "admin")
ADMIN_CONTRASENA = os.environ.get("ADMIN_CONTRASENA", "cambia-esta-contrasena")

nombres_meses = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]


def requiere_admin(vista):
    @functools.wraps(vista)
    def envoltura(*args, **kwargs):
        if not session.get("admin_logueado"):
            flash("Debes iniciar sesión para acceder a esa sección.", "error")
            return redirect(url_for("mensajes_login"))
        return vista(*args, **kwargs)

    return envoltura


def generar_calendario_anual():
    conn = obtener_conexion()
    eventos = conn.execute(
        "SELECT * FROM eventos_calendario WHERE anio = 2026 ORDER BY mes, dia"
    ).fetchall()
    conn.close()

    eventos_por_mes = {}
    for e in eventos:
        eventos_por_mes.setdefault(e["mes"], []).append(e)

    calendario_anual = []
    for i, nombre in enumerate(nombres_meses, start=1):
        matriz_mes = calendar.monthcalendar(2026, i)
        mapa_eventos = {e["dia"]: e["titulo"] for e in eventos_por_mes.get(i, [])}
        calendario_anual.append({
            "numero": i,
            "nombre": nombre,
            "matriz": matriz_mes,
            "eventos": mapa_eventos,
            "eventos_lista": eventos_por_mes.get(i, []),
        })
    return calendario_anual


@app.route("/")
def inicio():
    try:
        conn = obtener_conexion()
        noticias = conn.execute(
            "SELECT * FROM noticias ORDER BY fecha DESC LIMIT 3"
        ).fetchall()
        conn.close()
    except Exception as e:
        noticias = []
        print(f"Error consultando noticias: {e}")

    return render_template("inicio.html", noticias=noticias)


@app.route("/acerca")
def acerca():
    return render_template("acerca.html")


@app.route("/servicios")
def servicios():
    return render_template("servicios.html")


@app.route("/quienes")
def quienes():
    return render_template("quienes.html")


@app.route("/admision/enviar", methods=["POST"])
def enviar_admision():
    nombre_estudiante = request.form.get("nombre_estudiante", "").strip()
    grado = request.form.get("grado", "").strip()
    nombre_tutor = request.form.get("nombre_tutor", "").strip()
    telefono = request.form.get("telefono", "").strip()
    email = request.form.get("email", "").strip()
    mensaje = request.form.get("mensaje", "").strip()

    if not nombre_estudiante or not grado or not nombre_tutor or not telefono:
        flash("Por favor completa todos los campos obligatorios de admisión.", "error")
        return redirect(url_for("contacto"))

    conn = obtener_conexion()
    conn.execute(
        """INSERT INTO admisiones
           (nombre_estudiante, grado, nombre_tutor, telefono, email, mensaje)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (nombre_estudiante, grado, nombre_tutor, telefono, email, mensaje),
    )
    conn.commit()
    conn.close()

    flash("¡Solicitud de admisión enviada con éxito! Nos pondremos en contacto pronto.", "success")
    return redirect(url_for("contacto"))


@app.route("/mensajes")
def mensajes():
    conn = obtener_conexion()
    avisos = conn.execute("SELECT * FROM avisos ORDER BY id DESC").fetchall()

    admin_logueado = bool(session.get("admin_logueado"))
    admisiones_recibidas = []
    contactos_recibidos = []
    if admin_logueado:
        admisiones_recibidas = conn.execute(
            "SELECT * FROM admisiones ORDER BY id DESC"
        ).fetchall()
        contactos_recibidos = conn.execute(
            "SELECT * FROM contactos ORDER BY id DESC"
        ).fetchall()

    conn.close()

    return render_template(
        "mensajes_calendario.html",
        avisos=avisos,
        calendario=generar_calendario_anual(),
        admin_logueado=admin_logueado,
        admisiones_recibidas=admisiones_recibidas,
        contactos_recibidos=contactos_recibidos,
        meses=list(enumerate(nombres_meses, start=1)),
    )


@app.route("/mensajes/login", methods=["GET", "POST"])
def mensajes_login():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        contrasena = request.form.get("contrasena", "")

        if usuario == ADMIN_USUARIO and contrasena == ADMIN_CONTRASENA:
            session["admin_logueado"] = True
            flash("Sesión iniciada correctamente.", "success")
            return redirect(url_for("mensajes"))

        flash("Usuario o contraseña incorrectos.", "error")

    return render_template("mensajes_login.html")


@app.route("/mensajes/logout")
def mensajes_logout():
    session.pop("admin_logueado", None)
    flash("Sesión cerrada.", "success")
    return redirect(url_for("mensajes"))


@app.route("/mensajes/avisos/nuevo", methods=["POST"])
@requiere_admin
def nuevo_aviso():
    titulo = request.form.get("titulo", "").strip()
    fecha = request.form.get("fecha", "").strip()
    categoria = request.form.get("categoria", "General").strip() or "General"
    contenido = request.form.get("contenido", "").strip()

    if not titulo or not fecha or not contenido:
        flash("Completa título, fecha y contenido del aviso.", "error")
        return redirect(url_for("mensajes"))

    conn = obtener_conexion()
    conn.execute(
        "INSERT INTO avisos (titulo, fecha, categoria, contenido) VALUES (?, ?, ?, ?)",
        (titulo, fecha, categoria, contenido),
    )
    conn.commit()
    conn.close()

    flash("¡Aviso publicado con éxito!", "success")
    return redirect(url_for("mensajes"))


@app.route("/mensajes/avisos/eliminar/<int:aviso_id>", methods=["POST"])
@requiere_admin
def eliminar_aviso(aviso_id):
    conn = obtener_conexion()
    conn.execute("DELETE FROM avisos WHERE id = ?", (aviso_id,))
    conn.commit()
    conn.close()

    flash("Aviso eliminado.", "success")
    return redirect(url_for("mensajes"))


@app.route("/mensajes/eventos/nuevo", methods=["POST"])
@requiere_admin
def nuevo_evento():
    try:
        mes = int(request.form.get("mes", "0"))
        dia = int(request.form.get("dia", "0"))
    except ValueError:
        mes, dia = 0, 0
    titulo = request.form.get("titulo", "").strip()

    if mes < 1 or mes > 12 or dia < 1 or dia > 31 or not titulo:
        flash("Revisa el mes, el día y el título del evento.", "error")
        return redirect(url_for("mensajes"))

    conn = obtener_conexion()
    conn.execute(
        "INSERT INTO eventos_calendario (anio, mes, dia, titulo) VALUES (2026, ?, ?, ?)",
        (mes, dia, titulo),
    )
    conn.commit()
    conn.close()

    flash("¡Evento agregado al calendario!", "success")
    return redirect(url_for("mensajes"))


@app.route("/mensajes/eventos/eliminar/<int:evento_id>", methods=["POST"])
@requiere_admin
def eliminar_evento(evento_id):
    conn = obtener_conexion()
    conn.execute("DELETE FROM eventos_calendario WHERE id = ?", (evento_id,))
    conn.commit()
    conn.close()

    flash("Evento eliminado del calendario.", "success")
    return redirect(url_for("mensajes"))


@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        mensaje = request.form.get("mensaje", "").strip()

        if not nombre or not email or not mensaje:
            flash("Por favor completa todos los campos.", "error")
            return render_template("contacto.html")

        conn = obtener_conexion()
        conn.execute(
            "INSERT INTO contactos (nombre, email, mensaje) VALUES (?, ?, ?)",
            (nombre, email, mensaje),
        )
        conn.commit()
        conn.close()

        flash("¡Mensaje enviado con éxito! Gracias por escribirnos.", "success")
        return redirect(url_for("contacto"))

    return render_template("contacto.html")


@app.route("/noticias/nueva", methods=["GET", "POST"])
def nueva_noticia():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        contenido = request.form.get("contenido", "").strip()

        if not titulo or not contenido:
            flash("Por favor completa el título y el contenido.", "error")
            return render_template("noticia_nueva.html")

        conn = obtener_conexion()
        conn.execute(
            "INSERT INTO noticias (titulo, contenido) VALUES (?, ?)",
            (titulo, contenido),
        )
        conn.commit()
        conn.close()

        flash("¡Noticia publicada con éxito!", "success")
        return redirect(url_for("inicio"))

    return render_template("noticia_nueva.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
