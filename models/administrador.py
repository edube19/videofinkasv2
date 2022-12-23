from utils.db import db

class Lista(db.Model):
    _tablename__ = "lista"
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50),nullable=False,unique=True)
    password = db.Column(db.String(100),nullable=False)
    data_base = db.Column(db.String(45),nullable=False,unique=True)

    def __init__(self, user, password, data_base):
        self.user = user
        self.password = password
        self.data_base = data_base
