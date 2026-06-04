from flask import Blueprint, request, jsonify
from services.consulta_service import ConsultaService

consulta_bp = Blueprint('consulta', __name__)

@consulta_bp.route('/api/consulta', methods=['GET'])
def consulta_publica():
    placa     = request.args.get('placa')
    documento = request.args.get('documento')
    resultado = ConsultaService.consultar_vehiculo(placa, documento)
    if resultado['error']:
        return jsonify(resultado), 404
    return jsonify(resultado), 200