from flask import Flask
from routes.administradores import administradores
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
from base import Base

from sqlalchemy.orm import sessionmaker
from models.finca import Finca
from models.propiedad import Propiedad
from models.propietarios import Propietarios
from models.recibo_seccion import Recibo_seccion
from models.recibo_subseccion import Recibo_subseccion
from models.recibo import Recibos

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:admin@localhost/administradores"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

SQLAlchemy(app)

app.register_blueprint(administradores)

# Declara una clase base para las tablas
#Base = declarative_base()

def create_database(admin_name,user):
    # Crea una conexión a un servidor de base de datos MySQL
    engine= create_engine('mysql://root:admin@localhost/')
    # Crea la base de datos "admin1_db"
    engine.execute(f"CREATE DATABASE {admin_name}")
    # Crea una conexión a la base de datos para el administrador especificado
    engine = create_engine(f'mysql://root:admin@localhost/{admin_name}')
    # Crea la tabla en la base de datos
    Base.metadata.create_all(engine)
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
    
    return f'SE CREARON LAS TABLAS DEL ADMINISTRADOR {user}'

