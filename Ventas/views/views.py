from flask import Blueprint, request, jsonify, Response
from flask_restful import Resource
from datetime import datetime
from models.models import \
    db, \
    Venta, VentaSchema, \
    LogVenta, LogVentaSchema


ventaSchema = VentaSchema()
logVentaSchema = LogVentaSchema()


class VistaVentas(Resource):
    def get(self, vendedor, rol):
        if(rol==1):
            lv= LogVenta (idVenta=0,fechaTransaccion=datetime.now(),idVendedor=vendedor, error=0 )
            db.session.add(lv)
            db.session.commit()
            resultado_ventas = Venta.query.filter(
                Venta.idVendedor == vendedor).all()
            return [ventaSchema.dump(item) for item in resultado_ventas]
        else:
            lvError = LogVenta(idVenta=0, fechaTransaccion=datetime.now(),
                          idVendedor=vendedor, error=1)
            db.session.add(lvError)
            db.session.commit()
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

