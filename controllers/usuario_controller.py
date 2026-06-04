from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from services.usuario_service import UsuarioService
from database.db_connection import DatabaseConnection

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/api/usuarios', methods=['POST'])
@jwt_required()
def registrar_usuario():
    claims = get_jwt()
    if claims.get('rol') != 'admin':
        return jsonify({'error': True, 'mensaje': 'Acceso no autorizado'}), 403
    datos = request.get_json()
    resultado = UsuarioService.registrar(datos)
    if resultado['error']:
        return jsonify(resultado), 400
    return jsonify(resultado), 201

@usuario_bp.route('/api/dashboard', methods=['GET'])
@jwt_required()
def dashboard_metricas():
    claims = get_jwt()
    if claims.get('rol') != 'admin':
        return jsonify({'error': True, 'mensaje': 'Acceso no autorizado'}), 403

    db = DatabaseConnection()
    cursor = db.get_cursor()

    cursor.execute("SELECT COUNT(*) as total FROM USUARIO")
    total_usuarios = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as total FROM VEHICULO")
    total_vehiculos = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as total FROM REVISION WHERE estado = 'pendiente'")
    total_pendientes = cursor.fetchone()['total']

    cursor.execute("""
        SELECT
            SUM(CASE WHEN resultado = 'aprobado' THEN 1 ELSE 0 END) as aprobadas,
            SUM(CASE WHEN resultado = 'rechazado' THEN 1 ELSE 0 END) as rechazadas
        FROM REVISION
        WHERE MONTH(fecha_revision) = MONTH(NOW())
        AND YEAR(fecha_revision) = YEAR(NOW())
    """)
    mes = cursor.fetchone()

    cursor.execute("""
        SELECT r.id_revision, r.fecha_revision, r.tipo_revision,
               r.estado, r.resultado,
               v.placa, v.marca, v.modelo,
               v.nombre_propietario,
               u.nombre AS tecnico_nombre, u.apellido AS tecnico_apellido
        FROM REVISION r
        JOIN VEHICULO v ON r.id_vehiculo = v.id_vehiculo
        JOIN USUARIO u ON r.id_tecnico = u.id_usuario
        ORDER BY r.fecha_revision DESC
        LIMIT 5
    """)
    recientes = cursor.fetchall()

    for r in recientes:
        if r.get('fecha_revision'):
            r['fecha_revision'] = r['fecha_revision'].strftime('%d/%m/%Y')

    return jsonify({
        'error': False,
        'total_usuarios': total_usuarios,
        'total_vehiculos': total_vehiculos,
        'total_pendientes': total_pendientes,
        'aprobadas_mes': mes['aprobadas'] or 0,
        'rechazadas_mes': mes['rechazadas'] or 0,
        'revisiones_recientes': recientes
    }), 200