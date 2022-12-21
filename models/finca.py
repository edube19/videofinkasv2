from base import Base
from sqlalchemy import Column,Integer,String,Float

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