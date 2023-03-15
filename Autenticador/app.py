from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
import hashlib
from modelos import db,  Usuario, Roles
from vistas.vistaautenticacion import *
from vistas.vista_autorizador import *

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
api.add_resource(vistaAutorizador, '/autorizador')



jwt = JWTManager(app)
with app.app_context():
    usuarios = Usuario.query.all()
    if len(usuarios)==0:

        for i in range(25):
            nombre_usuario = f"vendedor{i}"
            rol_usuario = Roles.VENDEDOR
            contrasena_usuario=nombre_usuario
            contrasena_encriptada = hashlib.md5(contrasena_usuario.encode('utf-8')).hexdigest()
            usuario = Usuario(
                usuario=nombre_usuario,
                contrasena= contrasena_encriptada,
                rol=rol_usuario)
            db.session.add(usuario)
        db.session.commit()
        

        for i in range(25,51):
            nombre_comprador = f"comprador{i}"
            rol_comprador = Roles.COMPRADOR
            contrasena_usuario=nombre_usuario
            contrasena_encriptada = hashlib.md5(contrasena_usuario.encode('utf-8')).hexdigest()
            usuario = Usuario(
                usuario=nombre_comprador,
                contrasena= contrasena_encriptada,
                rol=rol_comprador)
            db.session.add(usuario)
        db.session.commit()


        for i in range(51,76):
            nombre_admin = f"admin{i}"
            rol_admin = Roles.ADMINISTRADOR
            contrasena_usuario=nombre_usuario
            contrasena_encriptada = hashlib.md5(contrasena_usuario.encode('utf-8')).hexdigest()
            usuario = Usuario(
                usuario=nombre_admin,
                contrasena= contrasena_encriptada,
                rol=rol_admin)
            db.session.add(usuario)
        db.session.commit()


        for i in range(76,101):
            nombre_conductor = f"conductor{i}"
            rol_conductor = Roles.CONDUCTOR
            contrasena_usuario=nombre_usuario
            contrasena_encriptada = hashlib.md5(contrasena_usuario.encode('utf-8')).hexdigest()
            usuario = Usuario(
                usuario=nombre_conductor,
                contrasena= contrasena_encriptada,
                rol=rol_conductor)
            db.session.add(usuario)
        db.session.commit()
    #     admin = Usuario.query.filter(Usuario.usuario == "vendedor").all()
    #     if len(admin) == 0:
    #         contrasena = 'vendedor'
    #         contrasena_encriptada = hashlib.md5(
    #             contrasena.encode('utf-8')).hexdigest()
    #         u = Usuario(usuario="vendedor", contrasena=contrasena_encriptada,
    #                     rol=Roles.VENDEDOR)
    #         u2= Usuario(usuario="vendedor2", contrasena=contrasena_encriptada,
    #                     rol=Roles.VENDEDOR)
    #         db.session.add(u)
    #         db.session.add(u2)

    #         db.session.commit()
        # comprador = Usuario.query.filter(Usuario.usuario == "comprador").all()
        # if len(admin) == 0:
        #     contrasena = 'comprador'
        #     contrasena_encriptada = hashlib.md5(
        #         contrasena.encode('utf-8')).hexdigest()
        #     e = Usuario(usuario="comprador",
        #                 contrasena=contrasena_encriptada, rol=Roles.COMPRADOR)
        #     db.session.add(e)
        #     db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, port=8000)