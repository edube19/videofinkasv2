from base import Base
from sqlalchemy import Column,Integer,String

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