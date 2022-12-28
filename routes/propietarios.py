from flask import Flask, jsonify, request, Response, Blueprint
from recursos.re_excel import *
from bson import json_util
from controller.c_propietarios import *
from conexion.conexion import obtener_bd

propietarios = Blueprint("propietarios", __name__)
#ACTUALZIAR ESTO!!!1

@propietarios.route("/propietarios", methods=["GET"])#P1 listo
def ruta_listar_propietario():
    response = listar_propietario()
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@propietarios.route("/propietario", methods=["POST"])#P2 listo
def ruta_registrar_propietario():
    usuario = request.json["user"]
    base_datos,Admin_Id = obtener_bd(usuario)
    datos_propietario = []
    #tabla propiedad
    Porcentaje_Participacion = request.json["porcentaje_participacion"]
    datos_propietario[0]= Porcentaje_Participacion
    Numero_deposito = request.json["numero_deposito"]
    datos_propietario[1]= Numero_deposito
    Numero_departamento = request.json["numero_departamento"]
    datos_propietario[2]= Numero_departamento
    Numero_Estacionamiento = request.json["numero_estacionamiento"]
    datos_propietario[3]= Numero_Estacionamiento

    #propietarios
    Nombres_y_Apellidos = request.json["nombres_y_apellidos"]
    datos_propietario[4]= Nombres_y_Apellidos
    Tipo_Documento = request.json["tipodocumento"]
    datos_propietario[5]= Tipo_Documento
    Nro_Documento = request.json["nro_documento"]
    datos_propietario[6]= Nro_Documento
    Correo = request.json["correo"]
    datos_propietario[7]= Correo
    Telefono = request.json["telefono"]
    datos_propietario[8]= Telefono

    response = registrar_propietario(base_datos,datos_propietario)
    response = json_util.dumps(response)
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

"""@propietarios.route("/propietario", methods=["DELETE"])#P3 
def ruta_eliminar_propietario():
    response = eliminar_propietario()
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}"""

@propietarios.route("/propietario/<id>", methods=["GET"])#P4 NO ES NECESARIO
def ruta_listar_propietario_ID(id):
    response = listar_propietario_ID(id)
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@propietarios.route("/propietario", methods=["DELETE"])#P5 IMPLEMENTADO
def ruta_eliminar_propietario_ID():
    response = eliminar_propietario_ID()
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@propietarios.route("/propietarios", methods=["PUT"])#P6 falta
def ruta_actualizar_propietario_ID():
    response = actualizar_propietario_ID()
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    return response