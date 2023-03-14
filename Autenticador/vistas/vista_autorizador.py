from flask import jsonify, request
import hashlib
# from app import app
from flask_restful import Resource
from flask_jwt_extended import  get_jwt_identity, jwt_required
from modelos import *

class vistaAutorizador(Resource):    
    @jwt_required()  
    def get(self):  
        current_user_id = get_jwt_identity()
        # Aquí se hace la consulta a la tabla de usuarios
        if current_user_id is not None:
            usuario=Usuario.query.get_or_404(current_user_id)            
            return jsonify({'id':usuario.id,'usuario': usuario.usuario, 'rol':usuario.rol})
        return jsonify({'message': 'No se encontro el usuario'}), 404