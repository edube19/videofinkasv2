from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
#from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from conexion.conexion import get_sesion
from sqlalchemy import select
from sqlalchemy.ext.declarative import declarative_base
import json
Base = declarative_base()

class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String(30))

    addresses = relationship(
         "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
         return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
         return f"Address(id={self.id!r}, email_address={self.email_address!r})"

admin_name = 'test'
session,engine = get_sesion(admin_name)
#Base.metadata.create_all(engine) descomentar esto para q se cree desde cero
stmt = session.query(Address,User).join(User).all()
# Convert the result to a list of dictionaries
result = [
     {
          "id": x.id, 
          "email_address": x.email_address, 
          "user_id": x.user_id, 
          "user_name": y.name, 
          "user_fullname": y.fullname
     } 
     for x,y in stmt]

# Convert the list to JSON format
json_result = json.dumps(result)
print(type(json.loads(json_result)))

print(json.loads(json_result))


"""stmt = (select(Address,User).join(Address.user))
print('STMT → ',stmt)
session.query(stmt).all()
sandy_address = session.scalar(stmt)
print('*** → ',sandy_address)"""