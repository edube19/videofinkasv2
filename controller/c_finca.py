from flask import jsonify, request
from re_excel import *
from bson import json_util
from bson.objectid import ObjectId
#from libs.database import conexion
from conexion.conexion import conexion
from models.finca import Finca
from sqlalchemy import create_engine, MetaData, Table,select
from sqlalchemy.orm import sessionmaker

#LISTAR
def listar_finca():#F1
    base_datos = 'isabelbd'
    try:
        engine = conexion(base_datos)
        Session = sessionmaker(bind= engine)
        #finca = conexion('finca').find()
        session = Session()
        respuesta = session.query(Finca).all()
        print(respuesta)
        
        response = ""
        return response
    except Exception as e:
        print(e)
        response =  json_util.dumps({"status":500, 'message':'Sucedio un error al conseguir datos de la finca → '+str(e)})
        return response

#ELIMINAR
def eliminar_finca_ID():#F3 
    try:
        id = request.json["_id"]
        Nombre = request.json["Nombre"]
        conexion('finca').delete_one({'_id': id})
        response = json_util.dumps({"status": 201,'message': 'La finca ' + Nombre + ' se elimino satisfactoriamente'})
        return response
    except Exception as e:
        print(e)
        response =  json_util.dumps({"status":500, 'message':'Sucedio un error al tratar de eliminar la finca → '+str(e)})
        return response


def listar_finca_ID(id):#F4
    plantilla = conexion('finca').find({'Finca': id, })
    response = json_util.dumps(plantilla)
    return response

def crear_finca(base_datos,Admin_Id,Direccion,Nombre):
    
    try:
        print('entro a crear finca')
        engine = conexion(base_datos)#conectarme a la BD del usuario
        metadata = MetaData()
        table = Table('finca', metadata, autoload=True, autoload_with=engine)
        print('conecto con la BD del usuario → ',base_datos)
        if Admin_Id or Direccion or Nombre:
            modificacion = ''
            _id = generar_id()
            now = agregar_fecha()
            #db = conexion('finca')
            porc_participacion = 0
            #db.insert_one({ "_id":_id,"Admin_Id":Admin_Id,"Direccion":Direccion, "Nombre":Nombre, "Fecha_creacion":now,"Fecha_modificacion":modificacion,"Total_porc_participacion":total_porc_participacion})
            #print('RESPUESTA',respuesta)
            new_finca = Finca(admin_id=Admin_Id, 
            direccion=Direccion,
            nombre=Nombre,
            fecha_creacion=now,
            fecha_modificacion=modificacion,
            total_porc_participacion=porc_participacion)
            Session = sessionmaker(bind=engine)
            session = Session()
            session.add(new_finca)
            r = session.commit()
            print('RESPUESTA DEL SESSION COMMIT',r)
            response = {
                "status": 201,
                "_id":     _id,
                "Admin_Id":Admin_Id,
                "Direccion":Direccion,
                "Nombre":Nombre,
                "Fecha_creacion": now,
                "Total_porc_participacion":porc_participacion,
                "mensaje" : 'Se registro satisfactoriamente la finca '+Nombre
            }
            #busqeuda = (select([table]))
            #busqeuda = session.query(Finca).all()
            #print('BUSQUEDA',busqeuda)
            #result = engine.execute(busqeuda).fetchall()
            #print(type(result)) #es una lista
    
            #for row in result:
                #print(row)
            #else:
                #return not_found('No se registro')
    except Exception as e:
        response = {
                "status": 500,
                "mensaje":"Hubo error al registrar → "+str(e)}
        return  json_util.dumps(response)

def actualizar_finca_ID():
    try:
        id = request.json["_id"]
        Admin_Id = request.json["Admin_Id"]
        Direccion = request.json["Direccion"]
        Nombre = request.json["Nombre"]
        if Admin_Id or Direccion or Nombre:
            fecha_modificacion = agregar_fecha()
            Total_porc_participacion = contar_porc_participacion(id,'A')
            conexion('finca').update_one(
                #{'_id': ObjectId(id['$oid']) if '$oid' in id else ObjectId(id)}, {'$set': {  
                {'_id': id}, {'$set': {  
                    #"_id": id,
                    "Admin_Id":Admin_Id,
                    "Direccion":Direccion,
                    "Nombre":Nombre,
                    "Total_porc_participacion":Total_porc_participacion,
                    "Fecha_modificacion": fecha_modificacion}}
            )
        response = json_util.dumps({"status": 201,'message': 'La Finca ' + Nombre + ' ha sido actualizado satisfactoriamente'})
        return response
    except Exception as e:
        response = {
                "status": 500,
                "mensaje":"Hubo error al actualizar → " + str(e)}
        return json_util.dumps(response)

def not_found(mensaje):
    message = {
        'mensaje': mensaje,
        'status': 404
    }
    response = jsonify(message)
    
    return response