from flask import Blueprint, request, Response
from models.administrador import Lista
from utils.db import db
import bson
from bson import json_util
#from controller.c_admins import *

administradores = Blueprint("administradores", __name__)

@administradores.route("/administradores")
def index():

    return "Lista index"

@administradores.route("/registroadmin", methods=["POST"])
def ruta_add_admin():
    from app import create_database
    user = request.json["username"]
    password = request.json["password"]
    data_base = request.json["base_datos"]
    print('recibio los datos')
    new_administrador = Lista(user, password, data_base)

    db.session.add(new_administrador)
    db.session.commit()
    print('admin creado')

    create_database(data_base,user)

    response = {
                    "status": 200,
                    "mensaje": f'Admin {user} creado con su base de datos {data_base} y las tablas'
                } 
    response = json_util.dumps(response)
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@administradores.route("/login")
def ruta_login():

    return "update a contact"

@administradores.route("/administradores/<id>")
def delete(id):
    return "eliminado"

@administradores.route("/about")
def about():
    return "about"