from base import Base
from sqlalchemy import Column,Integer,String

class Recibo_seccion(Base):
    __tablename__ = "recibo_seccion"
    idseccion = Column(Integer, primary_key=True,nullable=False)
    descripcion = Column(String(45),nullable=False,unique=False)
    def __init__(self, descripcion):
        self.descripcion = descripcion