<<<<<<< HEAD
from base import Base
from sqlalchemy import Column,Integer,String,Float,ForeignKey
from sqlalchemy.orm import relationship
class Finca(Base):
    #__bind_key__ = 'two'
    __tablename__ = "finca"
    #__table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True,nullable=False)
    direccion= Column(String(45),nullable=False,unique=True)
    nombre= Column(String(45),nullable=False,unique=True)
    fecha_creacion= Column(String(45))
    fecha_modificacion= Column(String(45))
    total_porc_participacion= Column(Float(20),nullable=False)

    #llave foranea asignada
    #llave_finca1 = relationship("Recibos", back_populates="finca")
    #llave_finca2 = relationship("Propiedad", back_populates="finca")

    def __init__(self,direccion,nombre,fecha_creacion,fecha_modificacion,total_porc_participacion):
        self.direccion = direccion
        self.nombre = nombre
        self.fecha_creacion = fecha_creacion
        self.fecha_modificacion = fecha_modificacion
=======
from base import Base
from sqlalchemy import Column,Integer,String,Float

class Finca(Base):
    #__bind_key__ = 'two'
    __tablename__ = "finca"
    #__table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True,nullable=False)
    direccion= Column(String(45),nullable=False,unique=True)
    nombre= Column(String(45),nullable=False,unique=True)
    fecha_creacion= Column(String(45))
    fecha_modificacion= Column(String(45))
    total_porc_participacion= Column(Float(20),nullable=False)

    def __init__(self,direccion,nombre,fecha_creacion,fecha_modificacion,total_porc_participacion):
        self.direccion = direccion
        self.nombre = nombre
        self.fecha_creacion = fecha_creacion
        self.fecha_modificacion = fecha_modificacion
>>>>>>> bcd26f988ee1cca1b3d49f89666c01331cff41e7
        self.total_porc_participacion = total_porc_participacion