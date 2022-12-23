from flask import Blueprint, request, Response
from models.administrador import Lista
from utils.db import db
import bson
from bson import json_util
#from controller.c_admins import *
import bcrypt
from re_excel import *

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

    password_encriptado = string_a_byte(password)
    password_encriptado = encriptar(password_encriptado)
    print(type(password_encriptado))
    new_administrador = Lista(user, password_encriptado, data_base)

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

@administradores.route("/login", methods=["POST"])
def ruta_login():
    try:
        from app import validar_usuario
        user = request.json["username"]
        password = request.json["password"]
        if not user:
                response = {
                    "status": 201,
                    "mensaje":"Ingrese un usuario"}
                return response
        if not password:
            response = {
                "status": 201,
                "mensaje":"Ingrese la contraseña"}
            return response
        print('entro a validar')
        validacion_usuario= validar_usuario(user,password)
        print('validacion →',validacion_usuario)
        print('acabo la validacion')
        if validacion_usuario:#el usuario existe
            """print('Entro a validar la contraseña')
            password_encryptado = encriptar(password)
            print('password_encryptado → ',password_encryptado)
            contra_byte = byte_a_string(password_encryptado)
            print('Contra a byte → ',contra_byte)
            response = {
                    "status": 200,
                    "mensaje": contra_byte
                }
            if bcrypt.checkpw(password.encode('utf-8'), contra_byte):
                response = {
                    "status": 200,
                    "mensaje": "Bienvenido "+user
                }
            else:
                response = {
                    "status": 200,
                    "mensaje": "La contraseña no es la correcta " 
            }"""
            response = {
                    "status": 200,
                    "mensaje": "Bienvenido "+user}   
        else:
            response = {
                    "status": 200,
                    "mensaje": "El administrador "+user+" no existe" 
                }
        return response
    except Exception as e:
        # the rollback func reverts the changes made to the db ( so if an error happens after we commited changes they will be reverted )
        print('SUCEDIO UN ERROR AL LOGEAR >>> ',e)
        response = {"status":400,'mensaje': 'Hubo un error en el login >>> '+str(e)}
        return response

@administradores.route("/administradores/<id>")
def delete(id):
    return "eliminado"

@administradores.route("/about")
def about():
    return "about"