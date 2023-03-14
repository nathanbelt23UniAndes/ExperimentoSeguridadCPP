from flask import Flask
from faker import Faker
from faker.generator import random
from flask_cors import CORS
from flask_restful import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from vistas.vista_usuario import vistaUsuario

import os

app = Flask(__name__)
engine = create_engine('sqlite:///dbapp.db')
Session = sessionmaker(bind=engine)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbapp.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True
app_context = app.app_context()
app_context.push()
#db.init_app(app)
#db.create_all()

cors = CORS(app)
api = Api(app)

api.add_resource(vistaUsuario , '/usuario' )



if __name__ == '__main__':
    app.run(debug=True, port=int(69))

