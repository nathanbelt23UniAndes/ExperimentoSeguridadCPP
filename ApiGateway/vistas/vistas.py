from flask import request, jsonify
import requests
import json
from app import app
import os


@app.route('/login', methods=['POST'])
def login():
    # Obtener credenciales del usuario desde el cuerpo de la solicitud
    username = request.json.get('username')
    password = request.json.get('password')
    # Enviar solicitud al servicio de autenticación
    auth_response = requests.post(os.getenv("AUTH_SERVICE_URL"), json={'usuario': username, 'contrasena': password})
    # Si la autenticación es exitosa, devolver el token
    if auth_response.status_code == 200:
        token = auth_response.json()['token']
        id = auth_response.json()['id']
        return jsonify({'token': token,'id': id}), 200
    else:
        return jsonify({'mensaje': 'Credenciales inválidas'}), 401


@app.route('/solicitud', methods=['GET'])
def solicitud():
    # Obtener token de la cabecera de la solicitud
    token = request.headers.get('Authorization')
    # Si no se envió token, devolver error de autenticación
    if not token:
        return jsonify({'mensaje': 'No se proporcionó un token de acceso'}), 401
    # Enviar solicitud al servicio de autorización para validar el token
    headers = {'Content-Type': 'application/json', "Authorization": f"{token}"}
    auth_response = requests.get(os.getenv("AUTHZ_SERVICE_URL"), headers = headers)
    # Si el token es válido, continuar con la solicitud
    if auth_response.status_code == 200:
            id_usuario = auth_response.json()['id']
            usuario = auth_response.json()['usuario']
            rol = auth_response.json()['rol']
            # Devolver información del usuario y sus permisos
            return jsonify({'id': id_usuario,'usuario': usuario, 'rol': rol}), 200
    else:
        return jsonify({'mensaje': 'Token inválido'}), 401
