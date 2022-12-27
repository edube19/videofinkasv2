from base import Base
from sqlalchemy import Column,Integer,String,Float,ForeignKey
from sqlalchemy.orm import relationship,backref
class Recibo_seccion(Base):
    __tablename__ = "recibo_seccion"
    idseccion = Column(Integer, primary_key=True,nullable=False)
    descripcion = Column(String(45),nullable=False,unique=False)
    
    """#llave foranea
    idrecibos = Column(Integer, ForeignKey("recibos.idrecibos"))

    recibos = relationship("Recibos", back_populates = "llave_recibos")

    #llave foranea asignada
    llave_recibo_seccion = relationship("Recibo_subseccion", back_populates = "recibo_seccion")"""
    recibos_idrecibos= Column(Integer, ForeignKey('recibos.idrecibos'))
    recibo = relationship('Recibos', backref=backref('recibos_seccion'), lazy=True)
    
    def __init__(self, descripcion):
        self.descripcion = descripcion