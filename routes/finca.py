from flask import jsonify, request, Response,Blueprint
from bson import json_util
from controller.c_finca import *
from conexion.conexion import obtener_bd

finca = Blueprint("finca", __name__)

@finca.route("/finca", methods=["POST"])#F1 FUNCIONA EN POSTMAN
def ruta_listar_finca():
    usuario = request.json["user"]
    base_datos= obtener_bd(usuario)
    response =listar_finca(base_datos)
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@finca.route("/finca", methods=["DELETE"])#F3 IMPLEMENTADO
def ruta_eliminar_finca_ID():
    usuario = request.json["user"]
    id= request.json["id"]
    nombre = request.json["nombre"]
    base_datos= obtener_bd(usuario)
    response = eliminar_finca_ID(base_datos,id,nombre)
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@finca.route("/finca/<id>", methods=["GET"])#F4 NO ES NECESARIO
def ruta_listar_finca_ID(id):
    response = listar_finca_ID(id)
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@finca.route("/crear_finca", methods=["POST"])#YA FUNCIONA EN EL POSTMAN
def ruta_crear_finca():
    usuario = request.json["user"]
    base_datos= obtener_bd(usuario)
    Direccion = request.json["Direccion"]
    Nombre = request.json["Nombre"]
    response = crear_finca(base_datos,Direccion,Nombre)
    response = json_util.dumps(response)
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@finca.route("/finca", methods=["PUT"])#P6
def ruta_actualizar_finca_ID():#funciona
    usuario = request.json["user"]
    base_datos= obtener_bd(usuario)
    id= request.json["id"]
    nombre = request.json["nombre"]
    direccion= request.json["direccion"]
    datos_actualizar = [nombre,direccion]
    print('datos a actualizar → ',datos_actualizar)
    response = actualizar_finca_ID(base_datos,id,datos_actualizar)
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)