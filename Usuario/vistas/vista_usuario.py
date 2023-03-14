from flask_jwt_extended import  create_access_token
from flask import request
import hashlib
from flask_restful import Resource
import requests


API_BASE_URL = 'http://localhost:5000/solicitud'

class vistaUsuario(Resource):
    def post (self):
        response = requests.post(f'{API_BASE_URL}/login', json={'username': request.json["usuario"], 'password': request.json["contrasena"]})
        if response.status_code == 200:
            token = response.json()['token']
            print(f'Token de acceso: {token}')
        else:
            return "Error de autenticacion",404