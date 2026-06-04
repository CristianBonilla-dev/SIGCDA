from database.db_connection import DatabaseConnection
from services.revision_service import serializar_revision

class ConsultaService:

    @staticmethod
    def consultar_vehiculo(placa, documento):
        if not placa or not documento:
            return {'error': True, 'mensaje': 'Placa y documento son requeridos'}

        db = DatabaseConnection()
        cursor = db.get_cursor()

        # Verificar que el vehículo existe y el documento coincide
        cursor.execute("""
            SELECT id_vehiculo, placa, tipo_vehiculo, marca, modelo, anio,
                   nombre_propietario, documento_propietario
            FROM VEHICULO
            WHERE placa = %s AND documento_propietario = %s
        """, (placa.upper(), documento))

        vehiculo = cursor.fetchone()

        if not vehiculo:
            return {'error': True, 'mensaje': 'No se encontró ningún vehículo con esa placa y documento'}

        # Obtener la última revisión completada
        cursor.execute("""
            SELECT r.id_revision, r.fecha_revision, r.hora_revision,
                   r.tipo_revision, r.estado, r.resultado, r.observaciones,
                   u.nombre AS tecnico_nombre, u.apellido AS tecnico_apellido
            FROM REVISION r
            JOIN USUARIO u ON r.id_tecnico = u.id_usuario
            WHERE r.id_vehiculo = %s AND r.resultado IS NOT NULL
            ORDER BY r.fecha_revision DESC
            LIMIT 1
        """, (vehiculo['id_vehiculo'],))

        revision = cursor.fetchone()

        if not revision:
            return {'error': True, 'mensaje': 'Este vehículo no tiene revisiones completadas aún'}

        revision = serializar_revision(revision)

        # Obtener ítems de la revisión
        cursor.execute("""
            SELECT nombre_item, resultado, observacion
            FROM ITEM_INSPECCION
            WHERE id_revision = %s
        """, (revision['id_revision'],))

        items = cursor.fetchall()

        return {
            'error': False,
            'placa': vehiculo['placa'],
            'tipo_vehiculo': vehiculo['tipo_vehiculo'],
            'marca': vehiculo['marca'],
            'modelo': vehiculo['modelo'],
            'anio': vehiculo['anio'],
            'nombre_propietario': vehiculo['nombre_propietario'],
            'fecha_revision': revision['fecha_revision'],
            'hora_revision': revision['hora_revision'],
            'tipo_revision': revision['tipo_revision'],
            'resultado': revision['resultado'],
            'observaciones': revision['observaciones'],
            'tecnico': f"{revision['tecnico_nombre']} {revision['tecnico_apellido']}",
            'items': items
        }