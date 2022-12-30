from flask import Flask, jsonify, request, Response, Blueprint
from recursos.re_excel import *
from bson import json_util
from controller.c_propietarios import *
from conexion.conexion import obtener_bd

propietarios = Blueprint("propietarios", __name__)
#ACTUALZIAR ESTO!!!1

@propietarios.route("/listar_propietarios", methods=["POST"])#P1 listo
def ruta_listar_propietario():
    response = listar_propietario()
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@propietarios.route("/propietario", methods=["POST"])#P2 listo
def ruta_registrar_propietario():
    usuario = request.json["user"]
    base_datos = get_sesion(usuario)
    datos =  request.json# esto lo jala del postamn o del front
    print('LECTURA DE DATOS → ',datos)
    """lista_json =  {
        "nombres_y_apellidos": request.json["nombres_y_apellidos"],"tipodocumento": request.json["tipodocumento"],
        "nro_documento": request.json["nro_documento"],"correo": request.json["correo"],"telefono": request.json["telefono"],
        "estado": 'A',"numero_deposito":request.json["numero_deposito"],"numero_departamento":request.json["numero_departamento"],
        "numero_estacionamiento": request.json["numero_estacionamiento"]
    }"""

    [
    {
        "idpropiedad": 1,
        "tipo_propietario": 1,
        "porcentaje_participacion":'5',
        "numero_deposito":'',
        "numero_departamento":'7',
        "numero_estacionamiento":'3',
        "propietario_id": 1,
        "finca_id": 1,
        "idpropietarios": 1,
        "Nombre y Apellidos":'eduardo berrios',
        "tipodocumento":'D',
        "nro_documento":'75771492',
        "correo":'edujor2@gmail.com',
        "telefono": 3547599,
        "fecha_creacion":'19/12/2022',
        "fecha_modificacion":'',
        "estado":'A'}]
    print('entrando a REGISTRAR PROPIETARIOS')
    response = registrar_propietario(base_datos,datos)
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

@propietarios.route("/buscar_propietario", methods=["POST"])#P6 falta
def ruta_buscar_propietario_tipo_documento():
    response = buscar_propietario_tipo_documento()
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    return response