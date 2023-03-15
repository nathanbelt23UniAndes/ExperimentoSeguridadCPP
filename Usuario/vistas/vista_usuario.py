from flask_jwt_extended import  create_access_token
from flask import request, jsonify
import json
import hashlib
from datetime import datetime
from flask_restful import Resource
import requests
from modelos.modelos import db, LogUsuario



API_BASE_URL = 'http://localhost:5000'

class vistaUsuario(Resource):
    def post (self):
        response = requests.post(f'{API_BASE_URL}/login', json={'username': request.json["usuario"], 'password': request.json["contrasena"]})
        if response.status_code == 200:
            data = response.json()
            return jsonify(data)

        else:
            return "Error de autenticacion",404
        
class vista_Generar_Peticiones(Resource):
    def get(self):
        usuarios = []
        for i in range(100):
            if(i <=24):
                user = f'vendedor{i}'

            elif( i > 24 and i <=50):
                user = f'comprador{i}'

            elif(i > 50 and i <=75):
                user = f'admin{i}'

            elif(i > 75 and i <=100):
                user = f'conductor{i}'

            data = {
                       'username' : user,
                       'password' : user
                  }
            usuarios.append(data)

        for usuario in usuarios:
            response = requests.post(f'{API_BASE_URL}/login', json=usuario)
            if response.status_code == 200:
                token = response.json()['token']
                # consumo solicitud
                headers = {'Content-Type': 'application/json', "Authorization": f"Bearer {token}"}
                response_solicitud = requests.get(f'{API_BASE_URL}/solicitud', headers = headers)
                # response_new = response_solicitud.json()
                logusuario= LogUsuario (fechaTransaccion=datetime.now(),usuario=str(usuario), error=0, mensaje= "mensaje")
                db.session.add(logusuario)
                db.session.commit()
            
            else:
                print(jsonify({'mensaje': 'Credenciales inválidas'}))

        return jsonify({'mensaje': 'Credenciales inválidas'}) ,200
    
    
                
                

                
     

            


            


