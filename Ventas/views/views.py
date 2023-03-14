from flask import Blueprint, request, jsonify, Response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
import time
import json
import os
from models.models import \
    db, \
    Venta, VentaSchema, \
    LogVenta, LogVentaSchema


ventaSchema = VentaSchema()
logVentaSchema = LogVentaSchema()


class VistaVentas(Resource):
    def get(self, vendedor, rol):
        if(rol==1):
            resultado_ventas = Venta.query.filter(
                Venta.idVendedor == vendedor).all()
            return [ventaSchema.dump(item) for item in resultado_ventas]
        else:
            return  'Esta arrecho mano, usted no puede entrar', 403


class VistaCreaVentas(Resource):
    def post(self):
        venta = Venta(
            idCliente=request.json["idCliente"],
            precioTotal=request.json["precioTotal"],
            cantidad=request.json["cantidad"],
            idVendedor=request.json["idVendedor"],
            producto=request.json["producto"]
        )
        db.session.add(venta)
        db.session.commit()
        return ventaSchema.dump(venta)


class VistaLogVenta(Resource):
    def get(self, id):
        return logVentaSchema.dump(LogVenta.query.filter(LogVenta.id == id).all())

