from flask_jwt_extended import  jwt_required,create_access_token
from flask import request
import hashlib
from flask_restful import Resource
from modelos import *
usuario_schema = UsuarioSchema()


class VistaSignIn(Resource):

    def post(self):
        usuario = Usuario.query.filter(
            Usuario.usuario == request.json["usuario"]).first()
        if usuario is None:
            contrasena_encriptada = hashlib.md5(
                request.json["contrasena"].encode('utf-8')).hexdigest()
            nuevo_usuario = Usuario(
                usuario=request.json["usuario"], contrasena=contrasena_encriptada, rol=Roles.VENDEDOR)
            db.session.add(nuevo_usuario)
            db.session.commit()
            return {"mensaje": "usuario creado exitosamente", "id": nuevo_usuario.id}
        else:
            return "El usuario ya existe", 404

    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena", usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204

class VistaLogIn(Resource):
    @jwt_required()
    def post(self):
        contrasena_encriptada = hashlib.md5(
            request.json["contrasena"].encode('utf-8')).hexdigest()
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                       Usuario.contrasena == contrasena_encriptada).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "id": usuario.id, "rol": usuario.rol}
