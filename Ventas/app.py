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
data_factory = Faker()


def crearVentaTest(idVendedor, idCliente):
  
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
        i=1
        while i< 26:
            crearVentaTest(i,data_factory.random_number())
            crearVentaTest(i, data_factory.random_number())
            crearVentaTest(i, data_factory.random_number())
            crearVentaTest(i, data_factory.random_number())
            crearVentaTest(i, data_factory.random_number())
            i=i+1





if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv("PORT")))





