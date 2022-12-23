from sqlalchemy import create_engine, MetaData, Table,select
from re_excel import *
def conexion(admin_name):
    engine = create_engine(f'mysql://root:admin@localhost/{admin_name}')
    # Obtiene información sobre la estructura de la base de datos
    
    
    return engine

def consulta_login(usuario,password):
    engine = conexion('administradores')
    metadata = MetaData()

    # Obtiene una tabla de la base de datos
    table = Table('lista', metadata, autoload=True, autoload_with=engine)
    
    # Crea una consulta usando el objeto table
    #query = (select([table]).where(table.columns.user == usuario) and (table.columns.password == password_encriptado))
    query = (select([table]).where(table.columns.user == usuario))
    # Ejecuta la consulta y obtiene el resultado
    result = engine.execute(query).fetchall()
    print(result)
    if result != '':
        for row in result:
            usuario_valor = row.user
            print('usuario_valor → ',usuario_valor)
            contra_valor = row.password
            print('contra_valor → ',contra_valor)
            print('contra valor type → ',contra_valor)

        print('Contra ingresada → ',password)
        print('Contra ingresada tipo → ',type(password))
        password_encriptado = string_a_byte(contra_valor)
        print('password_encriptado → ',password_encriptado)
        #password_encriptado = byte_a_string(contra_valor)
        print('password_encriptado → ',password.encode('utf-8'))
        if bcrypt.checkpw(password.encode('utf-8'), password_encriptado):
            print('las contraseñas coinciden!!')
            print('password ingresado → ',password)
            print('password leido de la BD→ ',password_encriptado)
            return True
        else:
            return False
        
        #password_encriptado = string_a_byte(password)
        #password_encriptado = encriptar(password_encriptado)
        #password = set_password(password)
        #print('password_encriptado → ',password_encriptado)
    else : return False

def set_password(pw):
    pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
    password_hash = pwhash.decode('utf8') # decode the hash to prevent is encoded twice
    return password_hash