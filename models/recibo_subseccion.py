from base import Base
from sqlalchemy import Column,Integer,String,Float,ForeignKey
from sqlalchemy.orm import relationship,backref
class Recibo_subseccion(Base):
    __tablename__ = "recibo_subseccion"
    id_subseccion = Column(Integer, primary_key=True,nullable=False)
    nombre = Column(String(45),nullable=False,unique=True)
    monto = Column(Float(45),nullable=False,unique = False)
    descripcion = Column(String(45),nullable=False,unique = False)
    
    """#llave foranea
    idseccion = Column(Integer, ForeignKey("recibo_seccion.idseccion"))
    recibo_seccion = relationship("Recibo_seccion", back_populates="llave_recibo_seccion")"""
    recibo_seccion_idseccion= Column(Integer, ForeignKey('recibo_seccion.idseccion'))
    recibo_seccion = relationship('Recibo_seccion', backref=backref('recibos_subseccion'), lazy=True)

    def __init__(self, nombre, monto,descripcion):
        self.nombre = nombre
        self.monto = monto
        self.descripcion = descripcion