from sqlalchemy import create_engine, MetaData, Table,select
from recursos.re_encriptacion import *
from sqlalchemy.orm import sessionmaker
from flask import request
def string_a_byte(palabra):#en string
    palabra = str.encode(palabra)
    return palabra

def conexion(admin_name):
    engine = create_engine(f'mysql://root:admin@localhost/{admin_name}')
    # Obtiene información sobre la estructura de la base de datos
    return engine

def consulta_login(usuario,password):
    try : 
        engine = conexion('administradores')
        metadata = MetaData()
        # Obtiene una tabla de la base de datos
        table = Table('lista', metadata, autoload=True, autoload_with=engine)
        
        # Crea una consulta usando el objeto table
        #query = (select([table]).where(table.columns.user == usuario) and (table.columns.password == password_encriptado))
        query = (select([table]).where(table.columns.user == usuario))
        # Ejecuta la consulta y obtiene el resultado
        result = engine.execute(query).fetchall()
        usuario_valor = ''
        if result != '':
            for row in result:
                contra_valor = row.password
                usuario_valor = row.user
            password_encriptado = string_a_byte(contra_valor)
            if bcrypt.checkpw(password.encode('utf-8'), password_encriptado):
                print('las contraseñas coinciden!!')
                return True,usuario_valor
            else: return False,usuario_valor
        else : return False,usuario_valor
    except Exception as e : 
        print('Error en la consulta de la BD → '+str(e))
        return False

def set_password(pw):
    pwhash = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
    password_hash = pwhash.decode('utf-8') # decode the hash to prevent is encoded twice
    return password_hash

def obtener_bd():
    user = request.json["user"]#esto tiene q ir afuera de la funcion
    print('usuario', user)
    engine = conexion('administradores')
    metadata = MetaData()
    nombrebd_valor = ""
    # Obtiene una tabla de la base de datos
    table = Table('lista', metadata, autoload=True, autoload_with=engine)
    
    # Crea una consulta usando el objeto table
    #query = (select([table]).where(table.columns.user == usuario) and (table.columns.password == password_encriptado))
    query = (select([table]).where(table.columns.user == user))
    # Ejecuta la consulta y obtiene el resultado
    result = engine.execute(query).fetchall()
    #print(type(result)) #es una lista
    if result != '':
        for row in result:
            nombrebd_valor = row.data_base

    print('Nombre de la BD del usuario → ',nombrebd_valor)
    return nombrebd_valor

def get_sesion(admin_name):
    engine = create_engine(f'mysql://root:admin@localhost/{admin_name}')
    Session = sessionmaker(bind= engine)
    session = Session()
    return session,engine
