from flask import Blueprint, request, jsonify
from services.usuario_service import UsuarioService
from flask_jwt_extended import jwt_required

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/api/usuarios', methods=['POST'])
@jwt_required()
def registrar_usuario():
    datos = request.get_json()
    resultado = UsuarioService.registrar(datos)
    if resultado['error']:
        return jsonify(resultado), 400
    return jsonify(resultado), 201