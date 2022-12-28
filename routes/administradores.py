from flask import Blueprint, request, Response
from models.administrador import Lista
from utils.db import db
import bson
from bson import json_util
#from controller.c_admins import *
import bcrypt
from recursos.re_encriptacion import *
from controller.c_admins import *

administradores = Blueprint("administradores", __name__)

@administradores.route("/administradores")
def index():

    return "Lista index"

@administradores.route("/registroadmin", methods=["POST"])
def ruta_add_admin():
    response = registrar()
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@administradores.route("/login", methods=["POST"])
def ruta_login():
    response = login()
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@administradores.route("/administradores/<id>")
def delete(id):
    return "eliminado"

@administradores.route("/about")
def about():
    return "about"