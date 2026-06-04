from database.db_connection import DatabaseConnection

ITEMS_INSPECCION = [
    'frenos', 'luces', 'suspension', 'neumaticos',
    'emision_gases', 'direccion', 'motor', 'carroceria'
]

def serializar_revision(r):
    r = dict(r)
    if r.get('hora_revision') is not None:
        total = int(r['hora_revision'].total_seconds())
        horas = total // 3600
        minutos = (total % 3600) // 60
        r['hora_revision'] = f"{horas:02d}:{minutos:02d}"
    return r

class RevisionService:

    @staticmethod
    def registrar(datos):
        id_vehiculo   = datos.get('id_vehiculo')
        id_tecnico    = datos.get('id_tecnico')
        fecha         = datos.get('fecha_revision')
        hora          = datos.get('hora_revision')
        tipo          = datos.get('tipo_revision')
        observaciones = datos.get('observaciones')

        if not all([id_vehiculo, id_tecnico, fecha, tipo]):
            return {'error': True, 'mensaje': 'Faltan campos obligatorios'}

        db = DatabaseConnection()
        cursor = db.get_cursor()

        cursor.execute("""
            INSERT INTO REVISION (id_vehiculo, id_tecnico, fecha_revision,
                hora_revision, tipo_revision, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_vehiculo, id_tecnico, fecha, hora, tipo, observaciones))

        id_revision = cursor.lastrowid

        # Crear los 8 ítems automáticamente
        for item in ITEMS_INSPECCION:
            cursor.execute("""
                INSERT INTO ITEM_INSPECCION (id_revision, nombre_item)
                VALUES (%s, %s)
            """, (id_revision, item))

        db.conexion.commit()
        return {'error': False, 'mensaje': 'Revisión programada correctamente'}

    @staticmethod
    def listar_todas():
        db = DatabaseConnection()
        cursor = db.get_cursor()
        cursor.execute("""
            SELECT r.id_revision, r.fecha_revision, r.hora_revision,
                   r.tipo_revision, r.estado, r.resultado,
                   v.placa, v.marca, v.modelo,
                   v.nombre_propietario,
                   u.nombre AS tecnico_nombre,
                   u.apellido AS tecnico_apellido
            FROM REVISION r
            JOIN VEHICULO v ON r.id_vehiculo = v.id_vehiculo
            JOIN USUARIO u ON r.id_tecnico = u.id_usuario
            ORDER BY r.fecha_revision DESC
        """)
        revisiones = [serializar_revision(r) for r in cursor.fetchall()]
        return {'error': False, 'revisiones': revisiones}

    @staticmethod
    def listar_por_tecnico(id_tecnico):
        db = DatabaseConnection()
        cursor = db.get_cursor()
        cursor.execute("""
            SELECT r.id_revision, r.fecha_revision, r.hora_revision,
                   r.tipo_revision, r.estado, r.resultado,
                   v.placa, v.marca, v.modelo,
                   v.nombre_propietario, v.documento_propietario
            FROM REVISION r
            JOIN VEHICULO v ON r.id_vehiculo = v.id_vehiculo
            WHERE r.id_tecnico = %s
            ORDER BY r.fecha_revision DESC
        """, (id_tecnico,))
        revisiones = [serializar_revision(r) for r in cursor.fetchall()]
        return {'error': False, 'revisiones': revisiones}

    @staticmethod
    def listar_tecnicos():
        db = DatabaseConnection()
        cursor = db.get_cursor()
        cursor.execute("""
            SELECT id_usuario, nombre, apellido
            FROM USUARIO WHERE rol = 'tecnico'
        """)
        return {'error': False, 'tecnicos': cursor.fetchall()}
    
    @staticmethod
    def registrar_resultado(id_revision, datos):
        items         = datos.get('items')
        observaciones = datos.get('observaciones')

        if not items or len(items) != 8:
            return {'error': True, 'mensaje': 'Debes registrar los 8 ítems de inspección'}

        db = DatabaseConnection()
        cursor = db.get_cursor()

        # Actualizar cada ítem
        for item in items:
            cursor.execute("""
                UPDATE ITEM_INSPECCION
                SET resultado = %s, observacion = %s
                WHERE id_revision = %s AND nombre_item = %s
            """, (item['resultado'], item.get('observacion', ''), id_revision, item['nombre_item']))

        # Calcular resultado automático
        cursor.execute("""
            SELECT COUNT(*) as rechazados
            FROM ITEM_INSPECCION
            WHERE id_revision = %s AND resultado = 'rechazado'
        """, (id_revision,))

        rechazados = cursor.fetchone()['rechazados']
        resultado  = 'rechazado' if rechazados > 0 else 'aprobado'

        # Actualizar la revisión
        cursor.execute("""
            UPDATE REVISION
            SET resultado = %s, estado = %s,
                observaciones = %s, fecha_resultado = NOW()
            WHERE id_revision = %s
        """, (resultado, resultado, observaciones, id_revision))

        db.conexion.commit()
        return {'error': False, 'mensaje': f'Revisión {resultado} correctamente', 'resultado': resultado}

    @staticmethod
    def obtener_historial(placa):
        db = DatabaseConnection()
        cursor = db.get_cursor()

        cursor.execute("""
            SELECT r.id_revision, r.fecha_revision, r.hora_revision,
                   r.tipo_revision, r.estado, r.resultado, r.observaciones,
                   v.placa, v.marca, v.modelo, v.nombre_propietario,
                   u.nombre AS tecnico_nombre, u.apellido AS tecnico_apellido
            FROM REVISION r
            JOIN VEHICULO v ON r.id_vehiculo = v.id_vehiculo
            JOIN USUARIO u ON r.id_tecnico = u.id_usuario
            WHERE v.placa = %s
            ORDER BY r.fecha_revision DESC
        """, (placa,))

        revisiones = [serializar_revision(r) for r in cursor.fetchall()]

        if not revisiones:
            return {'error': True, 'mensaje': 'No se encontraron revisiones para esa placa'}

        # Obtener ítems de cada revisión
        for rev in revisiones:
            cursor.execute("""
                SELECT nombre_item, resultado, observacion
                FROM ITEM_INSPECCION
                WHERE id_revision = %s
            """, (rev['id_revision'],))
            rev['items'] = cursor.fetchall()

        return {'error': False, 'revisiones': revisiones}

    @staticmethod
    def obtener_items(id_revision):
        db = DatabaseConnection()
        cursor = db.get_cursor()
        cursor.execute("""
            SELECT nombre_item, resultado, observacion
            FROM ITEM_INSPECCION
            WHERE id_revision = %s
        """, (id_revision,))
        return {'error': False, 'items': cursor.fetchall()}