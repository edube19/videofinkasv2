from flask import jsonify, request
#from re_excel import *
from bson import json_util
from bson.objectid import ObjectId
from libs.database import conexion,conexionv2
import bcrypt
from models.administrador import Lista
from utils.db import db

def login():
    try:
        user = request.json["user"]
        password = request.json["password"]
        #en caso no se llene algun campo
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
        #valida si el usuario existe (true existe, false no existe)
        validacion_usuario,json = validar_usuario(user)
        if validacion_usuario:#el usuario existe
            contra = json[0]['password']
            contra_byte = string_a_byte(contra)
            if bcrypt.checkpw(password.encode('utf-8'), contra_byte):
                response = {
                    "status": 200,
                    "mensaje": "Bienvenido "+user
                }
            else:
                response = {
                    "status": 200,
                    "mensaje": "La contraseña no es la correcta " 
                }
        else:
            response = {
                    "status": 200,
                    "mensaje": "El administrador "+user+" no existe" 
                }
            return response
        return response
    except Exception as e:
        # the rollback func reverts the changes made to the db ( so if an error happens after we commited changes they will be reverted )
        print('SUCEDIO UN ERROR AL LOGEAR >>> ',e)
        response = {"status":400,'mensaje': 'Hubo un error en el login >>> '+str(e)}
        return response

def registrar():

    try:
        user = request.json["user"]
        password = request.json["password"]
        #en caso no se llene algun campo
        if not user:
            response = {
                "status": 201,
                "mensaje":"Ingrese un usuario"}
            return response
        if not password:
            response = {
                "status": 201,
                "mensaje":"Ingrese una contraseña"}
            return response
        validacion_usuario,json = validar_usuario(user,'registrar')
        if validacion_usuario:
            base_datos = request.json["bd"]
            db = conexion('administradores')
            fecha = datetime.now()
            db.insert_one(
                { "user":user,"password":password,"bd":base_datos,"Fecha_creacion":fecha})
    except Exception as e:
        print('SUCEDIO UN ERROR AL REGISTRAR >>> ',e)
        response = {"status":400,'mensaje': 'Hubo un error en el registro de administradores >>> '+str(e)}
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