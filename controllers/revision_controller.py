from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from services.revision_service import RevisionService

revision_bp = Blueprint('revision', __name__)

@revision_bp.route('/api/revisiones', methods=['POST'])
@jwt_required()
def registrar_revision():
    claims = get_jwt()
    if claims.get('rol') != 'admin':
        return jsonify({'error': True, 'mensaje': 'Acceso no autorizado'}), 403
    datos = request.get_json()
    resultado = RevisionService.registrar(datos)
    if resultado['error']:
        return jsonify(resultado), 400
    return jsonify(resultado), 201

@revision_bp.route('/api/revisiones', methods=['GET'])
@jwt_required()
def listar_revisiones():
    claims = get_jwt()
    rol = claims.get('rol')
    id_usuario = get_jwt_identity()
    if rol == 'admin':
        resultado = RevisionService.listar_todas()
    else:
        resultado = RevisionService.listar_por_tecnico(id_usuario)
    return jsonify(resultado), 200

@revision_bp.route('/api/revisiones/<int:id_revision>/resultado', methods=['POST'])
@jwt_required()
def registrar_resultado(id_revision):
    claims = get_jwt()
    if claims.get('rol') != 'tecnico':
        return jsonify({'error': True, 'mensaje': 'Solo los técnicos pueden registrar resultados'}), 403
    datos = request.get_json()
    resultado = RevisionService.registrar_resultado(id_revision, datos)
    if resultado['error']:
        return jsonify(resultado), 400
    return jsonify(resultado), 200

@revision_bp.route('/api/revisiones/<int:id_revision>/items', methods=['GET'])
@jwt_required()
def obtener_items(id_revision):
    resultado = RevisionService.obtener_items(id_revision)
    return jsonify(resultado), 200

@revision_bp.route('/api/historial/<string:placa>', methods=['GET'])
@jwt_required()
def historial_vehiculo(placa):
    resultado = RevisionService.obtener_historial(placa)
    if resultado['error']:
        return jsonify(resultado), 404
    return jsonify(resultado), 200

@revision_bp.route('/api/tecnicos', methods=['GET'])
@jwt_required()
def listar_tecnicos():
    resultado = RevisionService.listar_tecnicos()
    return jsonify(resultado), 200