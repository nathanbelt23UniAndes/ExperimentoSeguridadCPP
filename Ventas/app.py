from flask import Flask
from faker import Faker
from faker.generator import random
from flask_cors import CORS
from flask_restful import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from views import VistaVentas, VistaCreaVentas
from models import db, LogVenta, Venta
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)
engine = create_engine('sqlite:///dbapp.db')
Session = sessionmaker(bind=engine)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbapp.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True
app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()
cors = CORS(app)
api = Api(app)
api.add_resource(VistaVentas, '/ventas/<int:vendedor>/<int:rol>')
api.add_resource(VistaCreaVentas, '/crea-venta')



def crearVentaTest(idVendedor, idCliente):
    data_factory = Faker()
    v = Venta(producto=data_factory.word(),
              cantidad=data_factory.random_number(),
              precioTotal=data_factory.random_number(),
              idVendedor=idVendedor,
              idCliente=idCliente)
    db.session.add(v)
    db.session.commit()


# Borra el log
with app.app_context():
    db.session.query(LogVenta).delete()
    db.session.commit()

    if (len(db.session.query(Venta).all())==0):
        i=0
        while i< 50:
            crearVentaTest(1,8)
            crearVentaTest(1, 9)
            crearVentaTest(1, 10)
            crearVentaTest(2, 8)
            crearVentaTest(2, 9)
            crearVentaTest(2, 10)
            i=i+1





if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv("PORT")))





