from datetime import datetime
import uuid 
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