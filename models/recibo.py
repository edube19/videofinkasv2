from base import Base
from sqlalchemy import Column,Integer,String

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