from base import Base
from sqlalchemy import Column,Integer,String

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