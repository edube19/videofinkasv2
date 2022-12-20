from flask import Blueprint, request
from models.administrador import Lista
from utils.db import db

administradores = Blueprint("administradores", __name__)

@administradores.route("/administradores")
def index():

    return "Lista index"

@administradores.route("/registroadmin", methods=["POST"])
def add_admin():
    from app import create_database
    user = request.form["user"]
    password = request.form["password"]
    data_base = request.form["data_base"]

    new_administrador = Lista(user, password, data_base)

    db.session.add(new_administrador)
    db.session.commit()
    print('admin creado')

    create_database(data_base,user)

    return f'Admin {user} creado con su base de datos {data_base} y las tablas'

@administradores.route("/administradores")
def update():
    return "update a contact"

@administradores.route("/administradores/<id>")
def delete(id):
    return "eliminado"

@administradores.route("/about")
def about():
    return "about"