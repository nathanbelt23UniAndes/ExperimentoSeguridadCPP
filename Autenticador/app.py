from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
import hashlib
from modelos import db,  Usuario, Roles
from vistas.vistaautenticacion import *

app = Flask(__name__)
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
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/login')


jwt = JWTManager(app)

with app.app_context():
    admin = Usuario.query.filter(Usuario.usuario == "vendedor").all()
    if len(admin) == 0:
        contrasena = 'vendedor'
        contrasena_encriptada = hashlib.md5(
            contrasena.encode('utf-8')).hexdigest()
        u = Usuario(usuario="vendedor", contrasena=contrasena_encriptada,
                    rol=Roles.VENDEDOR)
        db.session.add(u)
        db.session.commit()
    comprador = Usuario.query.filter(Usuario.usuario == "comprador").all()
    if len(admin) == 0:
        contrasena = 'comprador'
        contrasena_encriptada = hashlib.md5(
            contrasena.encode('utf-8')).hexdigest()
        e = Usuario(usuario="comprador",
                    contrasena=contrasena_encriptada, rol=Roles.COMPRADOR)
        db.session.add(e)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, port=8000)