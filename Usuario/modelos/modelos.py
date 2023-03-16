from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime

db = SQLAlchemy()

class LogUsuario(db.Model):
    __tablename__ = 'log_Usuario'
    id= db.Column(db.Integer, primary_key=True)
    rol = db.Column(db.Integer)
    fechaTransaccion = db.Column(db.DateTime(), default=datetime.now())
    usuario = db.Column(db.String)
    error = db.Column(db.Integer)
    mensaje = db.Column(db.String)
    statusCode = db.Column(db.String)
