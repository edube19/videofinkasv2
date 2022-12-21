from base import Base
from sqlalchemy import Column,Integer,String,Float

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