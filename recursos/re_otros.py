from datetime import datetime
import uuid 
import json
from bson import json_util
def agregar_fecha():
    now = str(datetime.now())
    now = now[:19]
    return now

def generar_id():
    id = str(uuid.uuid4())
    return id

def valores_a_actualizar(lista):
    valores_actualizar = {}
    for i in range(len(lista)):
        if lista[i] != '':
            valores_actualizar[lista[i]] = lista[i]
    return valores_actualizar

def transformar_json(stmt):
    """nuevo_diccionario = {}

    # Iteramos sobre cada clave y valor del diccionario original
    for clave, valor in nuevo_diccionario.items():
        # Si la clave es "Propiedad", añadimos cada par clave-valor del diccionario "Propiedad" al diccionario vacío, eliminando la palabra "Propiedad" de la clave
        if clave == "Propiedad":
            for k, v in valor.items():
                nueva_clave = k.replace("Propiedad", "propiedad")
                nuevo_diccionario[nueva_clave] = v
        # Si la clave es "Propietarios", añadimos cada par clave-valor del diccionario "Propietarios" al diccionario vacío, eliminando la palabra "Propietarios" de la clave
        elif clave == "Propietarios":
            for k, v in valor.items():
                nueva_clave = k.replace("Propietarios", "propietarios")
                nuevo_diccionario[nueva_clave] = v
    # Convertimos el diccionario a JSON
    json_string = json.dumps(nuevo_diccionario)"""
    """diccionarios = {}

    # Iteramos sobre cada tupla en la lista
    for tupla in stmt:
        print('TUPLA → ', tupla)
        # Convertimos la tupla a diccionario
        diccionario = dict(tupla)
        print('valor q se agrega al diccionario ', diccionario)
        print('\n')
        # Añadimos el diccionario a la lista
        diccionarios[0]=diccionario
    print('dicc → ',diccionarios)
    print('tipo → ',type(diccionarios))
    # Convertimos la lista de diccionarios a JSON
    json_string = json.dumps(diccionarios)"""
    
    """a = stmt.replace('(','{')
    b = a.replace(')','}')"""
    json_string = json.dumps(stmt)

    print('RESULTADO → ',json_string)
    print('VALOR → ', type(json_string))
    return json_string