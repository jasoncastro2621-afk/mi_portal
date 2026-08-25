from flask import Flask, render_template, request, redirect, url_for, flash

from db import obtener_conexion, init_db

app = Flask(__name__)
app.secret_key = "cambia-esta-clave-por-una-secreta"

init_db()


@app.route("/")
def inicio():
    conn = obtener_conexion()
    noticias = conn.execute(
        "SELECT * FROM noticias ORDER BY fecha DESC LIMIT 3"
    ).fetchall()
    conn.close()
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


@app.route("/admision", methods=["GET", "POST"])
def admision():
    if request.method == "POST":
        nombre_estudiante = request.form.get("nombre_estudiante", "").strip()
        grado = request.form.get("grado", "").strip()
        nombre_tutor = request.form.get("nombre_tutor", "").strip()
        telefono = request.form.get("telefono", "").strip()
        email = request.form.get("email", "").strip()
        mensaje = request.form.get("mensaje", "").strip()

        if not nombre_estudiante or not grado or not nombre_tutor or not telefono:
            flash("Por favor completa todos los campos obligatorios.", "error")
            return render_template("admision.html")

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
        return redirect(url_for("admision"))

    return render_template("admision.html")


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
