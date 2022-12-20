from flask import Flask
from routes.administradores import administradores
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#from models.finca import Finca

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:admin@localhost/administradores"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

SQLAlchemy(app)

app.register_blueprint(administradores)

# Declara una clase base para las tablas
Base = declarative_base()

# Declara una clase de tabla
"""class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    age = Column(Integer)"""
class Finca(Base):
    #__bind_key__ = 'two'
    __tablename__ = "finca"
    #__table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True,nullable=False)
    admin_id= Column(Integer,nullable=False,unique=True)
    direccion= Column(String(45),nullable=False,unique=True)
    nombre= Column(String(45),nullable=False,unique=True)
    fecha_creacion= Column(String(45))
    fecha_modificacion= Column(String(45))
    total_porc_participacion= Column(Float(20),nullable=False)

    def __init__(self, admin_id, direccion,nombre,fecha_creacion,fecha_modificacion,total_porc_participacion):
        #self.id = id
        self.admin_id = admin_id
        self.direccion = direccion
        self.nombre = nombre
        self.fecha_creacion = fecha_creacion
        self.fecha_modificacion = fecha_modificacion
        self.total_porc_participacion = total_porc_participacion

class Propiedad(Base):
    #__bind_key__ = 'two'
    __tablename__ = "propiedad"
    idpropiedad = Column(Integer, primary_key=True,nullable=False)
    tipo_propietario = Column(Integer,nullable=False,unique=False)
    porcentaje_participacion = Column(String(45),nullable=False,unique=False)
    numero_deposito = Column(String(45),nullable=True,unique=True)
    numero_departamento = Column(String(45),nullable=True,unique=True)
    numero_estacionamiento = Column(String(45),nullable=True,unique=True)

    def __init__(self,tipo_propietario, porcentaje_participacion,numero_deposito,numero_departamento,numero_estacionamiento):
        self.tipo_propietario = tipo_propietario
        self.porcentaje_participacion = porcentaje_participacion
        self.numero_deposito = numero_deposito
        self.numero_departamento = numero_departamento
        self.numero_estacionamiento = numero_estacionamiento

class Propietarios(Base):
    __tablename__ = "propietarios"
    idpropietarios = Column(Integer, primary_key=True,nullable=False)
    nombres_y_apellidos = Column(String(45),nullable=False,unique=True)
    tipodocumento = Column(String(45),nullable=False,unique=False)
    nro_documento = Column(String(45),nullable=False,unique=True)
    correo = Column(String(45),nullable=False,unique=True)
    telefono = Column(Integer,nullable=True,unique=False)
    fecha_creacion = Column(String(45))
    fecha_modificacion = Column(String(45))
    estado = Column(String(45),nullable=False,unique=False)
    def __init__(self, nombres_y_apellidos, tipodocumento,nro_documento,correo,telefono,fecha_creacion,fecha_modificacion,estado):
        self.nombres_y_apellidos = nombres_y_apellidos
        self.tipodocumento = tipodocumento
        self.nro_documento = nro_documento
        self.correo = correo
        self.telefono = telefono
        self.fecha_creacion = fecha_creacion
        self.fecha_modificacion = fecha_modificacion
        self.estado = estado

class Recibo_seccion(Base):
    __tablename__ = "recibo_seccion"
    idseccion = Column(Integer, primary_key=True,nullable=False)
    descripcion = Column(String(45),nullable=False,unique=False)
    def __init__(self, descripcion):
        self.descripcion = descripcion

class Recibo_subseccion(Base):
    __tablename__ = "recibo_subseccion"
    id_subseccion = Column(Integer, primary_key=True,nullable=False)
    nombre = Column(String(45),nullable=False,unique=True)
    monto = Column(Float(45),nullable=False,unique = False)
    descripcion = Column(String(45),nullable=False,unique = False)

    def __init__(self, nombre, monto,descripcion):
        self.nombre = nombre
        self.monto = monto
        self.descripcion = descripcion

class Recibos(Base):
    __tablename__ = "recibos"
    idrecibos = Column(Integer, primary_key=True,nullable=False)
    year = Column(Integer,nullable=False,unique=False)
    mes = Column(Integer,nullable=False,unique=False)
    nombre = Column(String(45),nullable=False,unique=True)
    fecha_modificacion = Column(String(45))

    def __init__(self,year,mes,nombre,fecha_modificacion):
        self.year = year
        self.mes = mes
        self.nombre = nombre
        self.fecha_modificacion = fecha_modificacion

def create_database(admin_name,user):
    print('entro a crear la otra base de datos')
    
    # Crea una conexión a un servidor de base de datos MySQL
    engine= create_engine('mysql://root:admin@localhost/')
    # Crea una sesión de base de datos
    
    # Crea la base de datos "admin1_db"
    engine.execute(f"CREATE DATABASE {admin_name}")
    # Crea una conexión a la base de datos para el administrador especificado
    engine = create_engine(f'mysql://root:admin@localhost/{admin_name}')
    # Crea la tabla en la base de datos
    Base.metadata.create_all(engine)
    print(f'creo la base de datos {admin_name}')
    Session = sessionmaker(bind=engine)
    session = Session()
    new_finca = Finca(admin_id=1, direccion="los girasoles",nombre="edificio1",fecha_creacion='19/12/2022',fecha_modificacion="",total_porc_participacion=5.8)
    new_propiedad = Propiedad(tipo_propietario=1,porcentaje_participacion="5",numero_deposito="",numero_departamento="7",numero_estacionamiento="3")
    new_propietarios = Propietarios(nombres_y_apellidos="eduardo berrios",tipodocumento="D",nro_documento="75771492",correo="edujor2@gmail.com",telefono=3547599,fecha_creacion='19/12/2022',fecha_modificacion="",estado="A")
    new_recibo_seccion = Recibo_seccion(descripcion="seccion1")
    new_recibo_subseccion = Recibo_subseccion(nombre="subseccion1",monto=32.22,descripcion="servicios de luz")
    new_recibos = Recibos(year=2022,mes=10,nombre="servicio de agua",fecha_modificacion="")
    session.add(new_finca)
    session.add(new_propiedad)
    session.add(new_propietarios)
    session.add(new_recibo_seccion)
    session.add(new_recibo_subseccion)
    session.add(new_recibos)
    session.commit()
    
    # Agrega un nuevo registro a la tabla
    #new_user = User(name='John', age=30)
    #session.add(new_user)
    #session.commit()

    # Consulta los registros de la tabla
    #users = session.query(User).all()
    #for user in users:
    #    print(user.name, user.age)
    return f'SE CREARON LAS TABLAS DEL ADMINISTRADOR {user}'

# Crea una base de datos y tablas para el administrador "admin1"
#create_database("admin1")

# Crea una base de datos y tablas para el administrador "admin2"
#create_database("admin2")

