from flask import jsonify, request
#from recursos.re_excel import *
from bson import json_util
from bson.objectid import ObjectId
#from libs.database import conexion
from conexion.conexion import conexion,get_sesion
from models.finca import Finca
from sqlalchemy import create_engine, MetaData, Table,select
from sqlalchemy.orm import sessionmaker
import json
from recursos.re_otros import *
#LISTAR
def listar_finca(base_datos):#F1
    #base_datos = 'jorgebd'
    try:
        #finca = conexion('finca').find()
        session,engine = get_sesion(base_datos)
        respuesta = session.query(Finca).all()
        #res = json.dumps(respuesta)
        people_dicts = [person.to_dict() for person in respuesta]
        print(people_dicts)  # Muestra una lista de diccionarios con los datos de cada persona
        r = json.dumps(people_dicts) #esto es un string
        q = json.loads(r)#esto ya es una lista
        return json.dumps(q)
    except Exception as e:
        print(e)
        response =  json_util.dumps({"status":500, 'message':'Sucedio un error al conseguir datos de la finca → '+str(e)})
        return response

#ELIMINAR
def eliminar_finca_ID(base_datos,id,nombre):#F3 
    try:
        #finca = conexion('finca').find()
        session,engine = get_sesion(base_datos)
        metadata = MetaData()
        finca = Table("finca", metadata, autoload=True, autoload_with=engine)

        # Crea una consulta de eliminación
        query = finca.delete().where(finca.columns.id == id)

        # Ejecuta la consulta
        result = engine.execute(query)

        # Obtiene el número de filas afectadas por la consulta
        filas_afectadas = result.rowcount

        # Si se ha eliminado una fila, muestra un mensaje de confirmación
        if filas_afectadas == 1:
            response = {'status':200,'mensaje':'Se ha eliminado la finca'+str(nombre)+' correctamente'}
        else:
            response = {'status':200,'mensaje':'No se ha eliminado ningún registro'}
        return json_util.dumps(response)
    except Exception as e:
        print(e)
        response =  json_util.dumps({"status":500, 'message':'Sucedio un error al conseguir datos de la finca → '+str(e)})
        return response

def listar_finca_ID(id):#F4
    plantilla = conexion('finca').find({'Finca': id, })
    response = json_util.dumps(plantilla)
    return response

def crear_finca(base_datos,Direccion,Nombre):
    
    try:
        print('entro a crear finca')
        session,engine = get_sesion(base_datos)
        if Direccion or Nombre:
            modificacion = ''
            now = agregar_fecha()
            #db = conexion('finca')
            porc_participacion = 1
            #db.insert_one({ "_id":_id,"Admin_Id":Admin_Id,"Direccion":Direccion, "Nombre":Nombre, "Fecha_creacion":now,"Fecha_modificacion":modificacion,"Total_porc_participacion":total_porc_participacion})
            #print('RESPUESTA',respuesta)
            new_finca = Finca( 
            direccion=Direccion,
            nombre=Nombre,
            fecha_creacion=now,
            fecha_modificacion=modificacion,
            total_porc_participacion=porc_participacion)
            session.add(new_finca)
            session.commit()
            response = {
                "status": 201,
                "mensaje" : 'Se registro satisfactoriamente la finca '+Nombre
            }
            return response
    except Exception as e:
        response = {
                "status": 500,
                "mensaje":"Hubo error al registrar → "+str(e)}
        return  json_util.dumps(response)

def actualizar_finca_ID(base_datos,id,datos_actualizar):
    session,engine = get_sesion(base_datos)
    metadata = MetaData()
    finca = Table("finca", metadata, autoload=True, autoload_with=engine)
    query = (
    finca.update()
    .values(nombre = datos_actualizar[0],direccion = datos_actualizar[1])
    .where(finca.columns.id ==id)
    )
    result = engine.execute(query)
    filas_afectadas = result.rowcount
    # Si se ha eliminado una fila, muestra un mensaje de confirmación
    if filas_afectadas == 1:
        response = {'status':200,'mensaje':'Se ha actualizado la finca'+str(datos_actualizar[0])+' correctamente'}
    else:
        response = {'status':200,'mensaje':'No se ha actualizado ningún registro'}
    return json_util.dumps(response)

def not_found(mensaje):
    message = {
        'mensaje': mensaje,
        'status': 404
    }
    response = jsonify(message)