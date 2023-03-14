from flask import request, jsonify
import requests
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
        rol = auth_response.json()['rol']
        return jsonify({'token': token,'id': id ,'rol' : rol}), 200
    else:
        return jsonify({'mensaje': 'Credenciales inválidas'}), 401


@app.route('/solicitud', methods=['GET'])
def solicitud():
    # Obtener token de la cabecera de la solicitud
    token = request.headers.get('Authorization')
    # Si no se envió token, devolver error de autenticación
    if not token:
        return jsonify({'mensaje': 'No se proporcionó un token de acceso'}), 401
    # Enviar solicitud al servicio de autenticación para validar el token
    auth_response = requests.post(os.getenv("AUTH_SERVICE_URL"), json={'token': token})
    # Si el token es válido, continuar con la solicitud
    if auth_response.status_code == 200:
        # Enviar solicitud al servicio de autorización
        authz_response = requests.post(os.getenv("AUTHZ_SERVICE_URL"), json={'token': token})
        # Si la autorización es exitosa, continuar con la solicitud
        if authz_response.status_code == 200:
            # Obtener información del usuario y sus permisos desde la respuesta de autorización
            usuario = authz_response.json()['usuario']
            rol = authz_response.json()['rol']
            permisos = authz_response.json()['permisos']
            # Devolver información del usuario y sus permisos
            return jsonify({'usuario': usuario, 'rol': rol, 'permisos': permisos}), 200
        else:
            return jsonify({'mensaje': 'No se pudo obtener la información de autorización'}), 403
    else:
        return jsonify({'mensaje': 'Token inválido'}), 401
