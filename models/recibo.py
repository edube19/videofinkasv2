from base import Base
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship,backref

class Recibos(Base):
    __tablename__ = "recibos"
    idrecibos = Column(Integer, primary_key=True,nullable=False)
    year = Column(Integer,nullable=False,unique=False)
    mes = Column(Integer,nullable=False,unique=False)
    nombre = Column(String(45),nullable=False,unique=True)
    fecha_modificacion = Column(String(45))

    """#llaves foraneas
    propiedad_idpropiedad = Column(Integer,ForeignKey('propiedad.idpropiedad'))
    finca_id = Column(Integer,ForeignKey('finca.id'))

    propiedad = relationship("Propiedad", back_populates="llave_propiedad")
    finca = relationship("Finca", back_populates="llave_finca1")

    #llave foraneas asignada
    llave_recibos = relationship("Recibo_seccion", back_populates="recibos")"""
    finca_id= Column(Integer, ForeignKey('finca.id'))
    finca = relationship('Finca', backref=backref('recibos'), lazy=True)

    propiedad_idpropiedad = Column(Integer, ForeignKey('propiedad.idpropiedad'))
    propiedad = relationship('Propiedad', backref=backref('recibos'), lazy=True)

    def __init__(self,year,mes,nombre,fecha_modificacion):
        self.year = year
        self.mes = mes
        self.nombre = nombre
        self.fecha_modificacion = fecha_modificacion