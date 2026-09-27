from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import date
import os

app = Flask(__name__)

app.secret_key = "gran_circo_fantacia_clave_secreta"


# ==============================
# DATOS DEL ADMINISTRADOR
# ==============================

USUARIO_ADMIN = "ADMISTRADOR/DUEÑO"

CONTRASENA_ADMIN = "luis192009"


# ==============================
# BASE DE DATOS
# ==============================

RUTA_BD = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "gran_circo_fantacia.db"
)


def conectar_bd():

    conexion = sqlite3.connect(RUTA_BD)

    conexion.execute("PRAGMA foreign_keys = ON")

    return conexion


def inicializar_bd():

    conexion = conectar_bd()
    cursor = conexion.cursor()


    # ==========================
    # TABLA CLIENTES
    # ==========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE
        )
    """)


    # ==========================
    # TABLA ESPECTÁCULOS
    # ==========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS espectaculos (
            id_espectaculo INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            duracion INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    """)


    # ==========================
    # TABLA FUNCIONES
    # ==========================

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


    # ==========================
    # TABLA RESERVACIONES
    # ==========================

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


    # ==========================
    # ESPECTÁCULOS INICIALES
    # ==========================

    cursor.execute("""
        INSERT OR IGNORE INTO espectaculos
        (
            id_espectaculo,
            nombre,
            descripcion,
            duracion,
            precio
        )
        VALUES
        (
            1,
            'Gran Espectáculo',
            'Un espectáculo lleno de magia y diversión.',
            90,
            150
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO espectaculos
        (
            id_espectaculo,
            nombre,
            descripcion,
            duracion,
            precio
        )
        VALUES
        (
            2,
            'Exhibición de Animales',
            'Conoce a los animales del Gran Circo Fantacia.',
            60,
            100
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO espectaculos
        (
            id_espectaculo,
            nombre,
            descripcion,
            duracion,
            precio
        )
        VALUES
        (
            3,
            'Los Payasos',
            'Un show lleno de risas y diversión.',
            45,
            80
        )
    """)


    # ==========================
    # FUNCIONES INICIALES
    # ==========================

    cursor.execute("""
        INSERT OR IGNORE INTO funciones
        (
            id_funcion,
            id_espectaculo,
            fecha,
            hora
        )
        VALUES
        (
            1,
            1,
            '2026-10-03',
            '18:00'
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO funciones
        (
            id_funcion,
            id_espectaculo,
            fecha,
            hora
        )
        VALUES
        (
            2,
            1,
            '2026-10-03',
            '21:00'
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO funciones
        (
            id_funcion,
            id_espectaculo,
            fecha,
            hora
        )
        VALUES
        (
            3,
            2,
            '2026-10-04',
            '17:00'
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO funciones
        (
            id_funcion,
            id_espectaculo,
            fecha,
            hora
        )
        VALUES
        (
            4,
            3,
            '2026-10-04',
            '19:00'
        )
    """)


    conexion.commit()

    conexion.close()


# Crear la base de datos automáticamente
# cuando inicia la aplicación
inicializar_bd()


# ==============================
# INICIO
# ==============================

@app.route("/")
def inicio():

    return render_template("index.html")


# ==============================
# ANIMALES
# ==============================

@app.route("/animales")
def animales():

    return render_template("animales.html")


# ==============================
# PAYASOS
# ==============================

@app.route("/payasos")
def payasos():

    return render_template("payasos.html")


# ==============================
# CONTACTO
# ==============================

@app.route("/contacto")
def contacto():

    return render_template("contacto.html")


# ==============================
# ESPECTÁCULOS
# ==============================

@app.route("/espectaculos")
def espectaculos():

    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_espectaculo,
            nombre,
            descripcion,
            duracion,
            precio
        FROM espectaculos
        ORDER BY id_espectaculo
    """)

    espectaculos = cursor.fetchall()

    conexion.close()

    return render_template(
        "espectaculos.html",
        espectaculos=espectaculos
    )


# ==============================
# RESERVACIONES
# ==============================

@app.route("/reservaciones", methods=["GET", "POST"])
def reservaciones():

    conexion = conectar_bd()
    cursor = conexion.cursor()


    # ==========================
    # GUARDAR RESERVACIÓN
    # ==========================

    if request.method == "POST":

        nombre = request.form["nombre"].strip()
        apellido = request.form["apellido"].strip()
        telefono = request.form["telefono"].strip()
        correo = request.form["correo"].strip().lower()
        id_funcion = request.form["id_funcion"]

        try:

            cantidad_boletos = int(
                request.form["cantidad_boletos"]
            )

        except ValueError:

            conexion.close()

            return redirect(
                url_for("reservaciones")
            )


        if cantidad_boletos < 1 or cantidad_boletos > 10:

            conexion.close()

            return redirect(
                url_for("reservaciones")
            )


        # ==========================
        # VERIFICAR FUNCIÓN
        # ==========================

        cursor.execute("""
            SELECT id_funcion
            FROM funciones
            WHERE id_funcion = ?
        """, (
            id_funcion,
        ))

        funcion = cursor.fetchone()


        if funcion is None:

            conexion.close()

            return redirect(
                url_for("reservaciones")
            )


        # ==========================
        # BUSCAR CLIENTE
        # ==========================

        cursor.execute("""
            SELECT id_cliente
            FROM clientes
            WHERE correo = ?
        """, (
            correo,
        ))

        cliente = cursor.fetchone()


        # ==========================
        # CREAR CLIENTE
        # ==========================

        if cliente is None:

            cursor.execute("""
                INSERT INTO clientes
                (
                    nombre,
                    apellido,
                    telefono,
                    correo
                )
                VALUES (?, ?, ?, ?)
            """, (
                nombre,
                apellido,
                telefono,
                correo
            ))

            id_cliente = cursor.lastrowid


        # ==========================
        # CLIENTE EXISTENTE
        # ==========================

        else:

            id_cliente = cliente[0]

            cursor.execute("""
                UPDATE clientes

                SET
                    nombre = ?,
                    apellido = ?,
                    telefono = ?

                WHERE id_cliente = ?
            """, (
                nombre,
                apellido,
                telefono,
                id_cliente
            ))


        # ==========================
        # GUARDAR RESERVACIÓN
        # ==========================

        cursor.execute("""
            INSERT INTO reservaciones
            (
                id_cliente,
                id_funcion,
                cantidad_boletos,
                fecha_reservacion
            )

            VALUES (?, ?, ?, ?)
        """, (
            id_cliente,
            id_funcion,
            cantidad_boletos,
            date.today().isoformat()
        ))


        conexion.commit()

        conexion.close()


        return redirect(
            url_for("reservacion_exitosa")
        )


    # ==========================
    # MOSTRAR FUNCIONES
    # ==========================

    cursor.execute("""
        SELECT
            funciones.id_funcion,
            espectaculos.nombre,
            funciones.fecha,
            funciones.hora,
            CAST(
                REPLACE(
                    REPLACE(
                        REPLACE(
                            TRIM(
                                CAST(
                                    COALESCE(
                                        espectaculos.precio,
                                        0
                                    ) AS TEXT
                                )
                            ),
                            '$',
                            ''
                        ),
                        ',',
                        ''
                    ),
                    'MXN',
                    ''
                ) AS REAL
            ) AS precio

        FROM funciones

        INNER JOIN espectaculos

        ON funciones.id_espectaculo =
           espectaculos.id_espectaculo

        ORDER BY
            funciones.fecha,
            funciones.hora
    """)

    funciones = cursor.fetchall()

    conexion.close()


    return render_template(
        "reservaciones.html",
        funciones=funciones
    )


# ==============================
# LOGIN
# ==============================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        password = request.form["password"]


        if (
            usuario == USUARIO_ADMIN
            and password == CONTRASENA_ADMIN
        ):

            session["admin"] = True

            return redirect(
                url_for("admin")
            )


        return render_template(
            "login.html",
            error="Usuario o contraseña incorrectos."
        )


    return render_template(
        "login.html"
    )


# ==============================
# PANEL ADMINISTRADOR
# ==============================

@app.route("/admin")
def admin():

    if not session.get("admin"):

        return redirect(
            url_for("login")
        )


    conexion = conectar_bd()
    cursor = conexion.cursor()


    # ==========================
    # RESERVACIONES
    # ==========================

    cursor.execute("""
        SELECT
            reservaciones.id_reservacion,
            clientes.nombre,
            clientes.apellido,
            clientes.telefono,
            clientes.correo,
            espectaculos.nombre,
            funciones.fecha,
            funciones.hora,
            reservaciones.cantidad_boletos,
            espectaculos.precio

        FROM reservaciones

        INNER JOIN clientes

        ON reservaciones.id_cliente =
           clientes.id_cliente

        INNER JOIN funciones

        ON reservaciones.id_funcion =
           funciones.id_funcion

        INNER JOIN espectaculos

        ON funciones.id_espectaculo =
           espectaculos.id_espectaculo

        ORDER BY
            reservaciones.id_reservacion DESC
    """)

    reservaciones = cursor.fetchall()


    # ==========================
    # ESPECTÁCULOS
    # ==========================

    cursor.execute("""
        SELECT
            id_espectaculo,
            nombre,
            descripcion,
            duracion,
            precio

        FROM espectaculos

        ORDER BY id_espectaculo
    """)

    espectaculos = cursor.fetchall()


    # ==========================
    # FUNCIONES
    # ==========================

    cursor.execute("""
        SELECT
            funciones.id_funcion,
            espectaculos.nombre,
            funciones.fecha,
            funciones.hora

        FROM funciones

        INNER JOIN espectaculos

        ON funciones.id_espectaculo =
           espectaculos.id_espectaculo

        ORDER BY
            funciones.fecha,
            funciones.hora
    """)

    funciones = cursor.fetchall()


    conexion.close()


    mensaje = session.pop(
        "mensaje",
        None
    )


    return render_template(
        "admin.html",
        reservaciones=reservaciones,
        espectaculos=espectaculos,
        funciones=funciones,
        mensaje=mensaje
    )


# ==============================
# ELIMINAR RESERVACIÓN
# ==============================

@app.route(
    "/eliminar-reservacion/<int:id_reservacion>"
)
def eliminar_reservacion(id_reservacion):

    if not session.get("admin"):

        return redirect(
            url_for("login")
        )


    conexion = conectar_bd()
    cursor = conexion.cursor()


    cursor.execute("""
        DELETE FROM reservaciones
        WHERE id_reservacion = ?
    """, (
        id_reservacion,
    ))


    conexion.commit()

    conexion.close()


    session["mensaje"] = (
        "🗑️ Reservación eliminada correctamente."
    )


    return redirect(
        url_for("admin")
    )


# ==============================
# AGREGAR ESPECTÁCULO
# ==============================

@app.route(
    "/agregar-espectaculo",
    methods=["POST"]
)
def agregar_espectaculo():

    if not session.get("admin"):

        return redirect(
            url_for("login")
        )


    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    duracion = request.form["duracion"]
    precio = request.form["precio"]


    conexion = conectar_bd()
    cursor = conexion.cursor()


    cursor.execute("""
        INSERT INTO espectaculos
        (
            nombre,
            descripcion,
            duracion,
            precio
        )

        VALUES (?, ?, ?, ?)
    """, (
        nombre,
        descripcion,
        duracion,
        precio
    ))


    conexion.commit()

    conexion.close()


    session["mensaje"] = (
        "🎭 Espectáculo agregado correctamente."
    )


    return redirect(
        url_for("admin")
    )


# ==============================
# EDITAR ESPECTÁCULO
# ==============================

@app.route(
    "/editar-espectaculo/<int:id_espectaculo>",
    methods=["POST"]
)
def editar_espectaculo(id_espectaculo):

    if not session.get("admin"):

        return redirect(
            url_for("login")
        )


    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    duracion = request.form["duracion"]
    precio = request.form["precio"]


    conexion = conectar_bd()
    cursor = conexion.cursor()


    cursor.execute("""
        UPDATE espectaculos

        SET
            nombre = ?,
            descripcion = ?,
            duracion = ?,
            precio = ?

        WHERE id_espectaculo = ?
    """, (
        nombre,
        descripcion,
        duracion,
        precio,
        id_espectaculo
    ))


    conexion.commit()

    conexion.close()


    session["mensaje"] = (
        "✏️ Espectáculo actualizado correctamente."
    )


    return redirect(
        url_for("admin")
    )


# ==============================
# ELIMINAR ESPECTÁCULO
# ==============================

@app.route(
    "/eliminar-espectaculo/<int:id_espectaculo>"
)
def eliminar_espectaculo(id_espectaculo):

    if not session.get("admin"):

        return redirect(
            url_for("login")
        )


    conexion = conectar_bd()
    cursor = conexion.cursor()


    cursor.execute("""
        SELECT COUNT(*)
        FROM funciones
        WHERE id_espectaculo = ?
    """, (
        id_espectaculo,
    ))


    cantidad_funciones = cursor.fetchone()[0]


    if cantidad_funciones > 0:

        conexion.close()


        session["mensaje"] = (
            "⚠️ No se puede eliminar este espectáculo "
            "porque tiene funciones programadas."
        )


        return redirect(
            url_for("admin")
        )


    cursor.execute("""
        DELETE FROM espectaculos
        WHERE id_espectaculo = ?
    """, (
        id_espectaculo,
    ))


    conexion.commit()

    conexion.close()


    session["mensaje"] = (
        "🗑️ Espectáculo eliminado correctamente."
    )


    return redirect(
        url_for("admin")
    )


# ==============================
# AGREGAR FUNCIÓN
# ==============================

@app.route(
    "/agregar-funcion",
    methods=["POST"]
)
def agregar_funcion():

    if not session.get("admin"):

        return redirect(
            url_for("login")
        )


    id_espectaculo = request.form[
        "id_espectaculo"
    ]

    fecha = request.form["fecha"]

    hora = request.form["hora"]


    conexion = conectar_bd()
    cursor = conexion.cursor()


    cursor.execute("""
        INSERT INTO funciones
        (
            id_espectaculo,
            fecha,
            hora
        )

        VALUES (?, ?, ?)
    """, (
        id_espectaculo,
        fecha,
        hora
    ))


    conexion.commit()

    conexion.close()


    session["mensaje"] = (
        "📅 Función agregada correctamente."
    )


    return redirect(
        url_for("admin")
    )


# ==============================
# EDITAR FUNCIÓN
# ==============================

@app.route(
    "/editar-funcion/<int:id_funcion>",
    methods=["POST"]
)
def editar_funcion(id_funcion):

    if not session.get("admin"):

        return redirect(
            url_for("login")
        )


    id_espectaculo = request.form[
        "id_espectaculo"
    ]

    fecha = request.form["fecha"]

    hora = request.form["hora"]


    conexion = conectar_bd()
    cursor = conexion.cursor()


    cursor.execute("""
        UPDATE funciones

        SET
            id_espectaculo = ?,
            fecha = ?,
            hora = ?

        WHERE id_funcion = ?
    """, (
        id_espectaculo,
        fecha,
        hora,
        id_funcion
    ))


    conexion.commit()

    conexion.close()


    session["mensaje"] = (
        "✏️ Función actualizada correctamente."
    )


    return redirect(
        url_for("admin")
    )


# ==============================
# ELIMINAR FUNCIÓN
# ==============================

@app.route(
    "/eliminar-funcion/<int:id_funcion>"
)
def eliminar_funcion(id_funcion):

    if not session.get("admin"):

        return redirect(
            url_for("login")
        )


    conexion = conectar_bd()
    cursor = conexion.cursor()


    cursor.execute("""
        SELECT COUNT(*)
        FROM reservaciones
        WHERE id_funcion = ?
    """, (
        id_funcion,
    ))


    cantidad_reservaciones = cursor.fetchone()[0]


    if cantidad_reservaciones > 0:

        conexion.close()


        session["mensaje"] = (
            "⚠️ No se puede eliminar esta función "
            "porque tiene reservaciones."
        )


        return redirect(
            url_for("admin")
        )


    cursor.execute("""
        DELETE FROM funciones
        WHERE id_funcion = ?
    """, (
        id_funcion,
    ))


    conexion.commit()

    conexion.close()


    session["mensaje"] = (
        "🗑️ Función eliminada correctamente."
    )


    return redirect(
        url_for("admin")
    )


# ==============================
# CERRAR SESIÓN
# ==============================

@app.route("/logout")
def logout():

    session.pop(
        "admin",
        None
    )

    return redirect(
        url_for("inicio")
    )


# ==============================
# RESERVACIÓN EXITOSA
# ==============================

@app.route("/reservacion-exitosa")
def reservacion_exitosa():

    return """
    <!DOCTYPE html>

    <html lang="es">

    <head>

        <meta charset="UTF-8">

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0"
        >

        <title>
            Reservación exitosa
        </title>

        <style>

            * {
                box-sizing: border-box;
            }

            body {

                font-family: Arial, sans-serif;

                background-color: #fff7e6;

                text-align: center;

                padding: 70px 20px;

                color: #222;
            }

            .mensaje {

                background-color: white;

                max-width: 600px;

                margin: auto;

                padding: 45px 30px;

                border-radius: 18px;

                box-shadow:
                    0 4px 15px
                    rgba(0,0,0,0.2);
            }

            .icono {

                font-size: 65px;

                margin-bottom: 15px;
            }

            h1 {

                color: #8b0000;

                margin-bottom: 20px;
            }

            p {

                font-size: 18px;

                line-height: 1.6;
            }

            .confirmado {

                margin-top: 20px;

                padding: 15px;

                background-color: #fff3cd;

                border-radius: 10px;

                font-weight: bold;
            }

            a {

                display: inline-block;

                margin-top: 25px;

                padding: 13px 25px;

                background-color: #8b0000;

                color: white;

                text-decoration: none;

                border-radius: 8px;

                font-weight: bold;
            }

            a:hover {

                background-color: #600000;
            }

        </style>

    </head>


    <body>


        <div class="mensaje">

            <div class="icono">
                🎉🎪🎟️
            </div>


            <h1>
                ¡Reservación realizada!
            </h1>


            <p>

                Tu reservación en
                <strong>
                    GRAN CIRCO FANTACIA
                </strong>

                se realizó correctamente.

            </p>


            <div class="confirmado">

                ✅ Tu lugar ha sido registrado correctamente.

            </div>


            <a href="/">

                🏠 Volver al inicio

            </a>


            <a
                href="/reservaciones"
                style="background-color:#222;"
            >

                🎟️ Hacer otra reservación

            </a>

        </div>


    </body>

    </html>
    """


# ==============================
# INICIAR SERVIDOR
# ==============================

if __name__ == "__main__":

    app.run(
        debug=True
    )