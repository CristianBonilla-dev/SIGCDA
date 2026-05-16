from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

revision_bp = Blueprint('revision', __name__)

@revision_bp.route('/api/revisiones', methods=['GET'])
@jwt_required()
def listar_revisiones():
    return jsonify({'mensaje': 'módulo en construcción'}), 200