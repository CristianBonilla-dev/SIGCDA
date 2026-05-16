from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

vehiculo_bp = Blueprint('vehiculo', __name__)

@vehiculo_bp.route('/api/vehiculos', methods=['GET'])
@jwt_required()
def listar_vehiculos():
    return jsonify({'mensaje': 'módulo en construcción'}), 200