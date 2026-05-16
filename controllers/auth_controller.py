from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    datos = request.get_json()
    resultado = AuthService.login(datos)
    if resultado['error']:
        return jsonify(resultado), 401
    return jsonify(resultado), 200