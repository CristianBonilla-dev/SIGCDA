from flask import Blueprint, request, jsonify

consulta_bp = Blueprint('consulta', __name__)

@consulta_bp.route('/api/consulta', methods=['GET'])
def consulta_publica():
    return jsonify({'mensaje': 'módulo en construcción'}), 200