from flask import jsonify, request,Response
#from re_excel import *
from bson import json_util
from bson.objectid import ObjectId
#from libs.database import conexion,conexionv2
from models.administrador import Lista
from utils.db import db
from conexion.conexion import string_a_byte,conexion
from recursos.re_encriptacion import *

def login():
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
        validacion_usuario,usuario_valor= validar_usuario(user,password)
        if validacion_usuario:#el usuario existe
            response = {
                    "status": 200,
                    "usuario": user,
                    "mensaje": "Bienvenido "+user}   
        else:
            if usuario_valor == '':
                response = {
                        "status": 200,
                        "mensaje": "El administrador "+user+" no existe" 
                    }
        return json_util.dumps(response)
    except Exception as e:
        # the rollback func reverts the changes made to the db ( so if an error happens after we commited changes they will be reverted )
        print('SUCEDIO UN ERROR AL LOGEAR >>> ',e)
        response = {"status":400,'mensaje': 'Hubo un error en el login >>> '+str(e)}
        return response

def registrar():

    try:
        from app import create_database
        user = request.json["username"]
        password = request.json["password"]
        data_base = request.json["base_datos"]

        password_encriptado = string_a_byte(password)
        password_encriptado = encriptar(password_encriptado)
        new_administrador = Lista(user, password_encriptado, data_base)
        db.session.add(new_administrador)
        db.session.commit() 

        create_database(data_base,user)
        print('admin creado')
        response = {
                        "status": 200,
                        "mensaje": f'Admin {user} creado con su base de datos {data_base} y las tablas'
                    } 
        response = json_util.dumps(response)
        return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}
    except Exception as e:
        print('Error al registrar administrador → '+str(e))
        response = {
                        "status": 400,
                        "mensaje": 'Error al registrar administrador → '+str(e)
                    } 
        return response


def listar_admins():#F1
    finca = conexion('admins').find()
    response = json_util.dumps(finca)
    return response

def eliminar_admins():
    conexion('admins').drop()
    response = jsonify({"status": 201,'message':' se elimino satisfactoriamente'})
    return response

def eliminar_admins_ID(id):
    conexion('admins').delete_one({'_id': id})
    response = jsonify({"status": 201,'message': 'El admin ' + id + ' se elimino satisfactoriamente'})
    return response 

def actualizar_admins_ID(id):
    pass