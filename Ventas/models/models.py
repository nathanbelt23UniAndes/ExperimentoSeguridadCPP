from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime

db = SQLAlchemy()


class Venta(db.Model):
    __tablename__ = 'ventas'

    id = db.Column(db.Integer, primary_key=True)
    producto = db.Column(db.String(50))
    cantidad = db.Column(db.Integer)
    precioTotal = db.Column(db.Integer)
    idVendedor = db.Column(db.Integer)
    idCliente = db.Column(db.Integer)


class LogVenta(db.Model):
    __tablename__ = 'log_Venta'
    id = db.Column(db.Integer, primary_key=True)
    idVenta = db.Column(db.Integer())
    fechaTransaccion = db.Column(db.DateTime(), default=datetime.now())
    idVendedor = db.Column(db.Integer)
    error = db.Column(db.Integer)


class VentaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Venta
        load_instance = True


class LogVentaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LogVenta
        load_instance = True
