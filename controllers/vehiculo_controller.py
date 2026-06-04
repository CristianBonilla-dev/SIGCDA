from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.vehiculo_service import VehiculoService

vehiculo_bp = Blueprint('vehiculo', __name__)

@vehiculo_bp.route('/api/vehiculos', methods=['GET'])
@jwt_required()
def listar_vehiculos():
    resultado = VehiculoService.listar()
    return jsonify(resultado), 200

@vehiculo_bp.route('/api/vehiculos', methods=['POST'])
@jwt_required()
def registrar_vehiculo():
    datos = request.get_json()
    id_admin = get_jwt_identity()
    resultado = VehiculoService.registrar(datos, id_admin)
    if resultado['error']:
        return jsonify(resultado), 400
    return jsonify(resultado), 201

@vehiculo_bp.route('/api/vehiculos/<int:id_vehiculo>', methods=['PUT'])
@jwt_required()
def editar_vehiculo(id_vehiculo):
    datos = request.get_json()
    resultado = VehiculoService.editar(id_vehiculo, datos)
    if resultado['error']:
        return jsonify(resultado), 400
    return jsonify(resultado), 200