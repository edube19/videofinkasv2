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
    set_password(password)
    password_byte = encriptar(password)
    
    # Crea una consulta usando el objeto table
    query = (select([table]).where(table.columns.user == usuario) and (table.columns.password == password_byte))

    # Ejecuta la consulta y obtiene el resultado
    result = engine.execute(query).fetchall()
    # Recorre el resultado de la consulta
    if result != '':
        return True
    else : return False

def set_password(self, pw):
    pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
    self.password_hash = pwhash.decode('utf8') # decode the hash to prevent is encoded twice