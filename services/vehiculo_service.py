from database.db_connection import DatabaseConnection

class VehiculoService:

    @staticmethod
    def registrar(datos, id_admin):
        placa                 = datos.get('placa')
        tipo_vehiculo         = datos.get('tipo_vehiculo')
        marca                 = datos.get('marca')
        modelo                = datos.get('modelo')
        anio                  = datos.get('anio')
        nombre_propietario    = datos.get('nombre_propietario')
        documento_propietario = datos.get('documento_propietario')
        telefono_propietario  = datos.get('telefono_propietario')
        email_propietario     = datos.get('email_propietario')

        if not all([placa, tipo_vehiculo, nombre_propietario, documento_propietario]):
            return {'error': True, 'mensaje': 'Faltan campos obligatorios'}

        db = DatabaseConnection()
        cursor = db.get_cursor()

        cursor.execute("SELECT id_vehiculo FROM VEHICULO WHERE placa = %s", (placa,))
        if cursor.fetchone():
            return {'error': True, 'mensaje': 'La placa ya está registrada'}

        cursor.execute("""
            INSERT INTO VEHICULO (placa, tipo_vehiculo, marca, modelo, anio,
                nombre_propietario, documento_propietario,
                telefono_propietario, email_propietario, registrado_por)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (placa, tipo_vehiculo, marca, modelo, anio,
              nombre_propietario, documento_propietario,
              telefono_propietario, email_propietario, id_admin))

        db.conexion.commit()
        return {'error': False, 'mensaje': 'Vehículo registrado correctamente'}

    @staticmethod
    def listar():
        db = DatabaseConnection()
        cursor = db.get_cursor()
        cursor.execute("""
            SELECT id_vehiculo, placa, tipo_vehiculo, marca, modelo, anio,
                   nombre_propietario, documento_propietario,
                   telefono_propietario, email_propietario
            FROM VEHICULO
            ORDER BY fecha_registro DESC
        """)
        return {'error': False, 'vehiculos': cursor.fetchall()}

    @staticmethod
    def editar(id_vehiculo, datos):
        tipo_vehiculo         = datos.get('tipo_vehiculo')
        marca                 = datos.get('marca')
        modelo                = datos.get('modelo')
        anio                  = datos.get('anio')
        nombre_propietario    = datos.get('nombre_propietario')
        documento_propietario = datos.get('documento_propietario')
        telefono_propietario  = datos.get('telefono_propietario')
        email_propietario     = datos.get('email_propietario')

        if not all([tipo_vehiculo, nombre_propietario, documento_propietario]):
            return {'error': True, 'mensaje': 'Faltan campos obligatorios'}

        db = DatabaseConnection()
        cursor = db.get_cursor()

        cursor.execute("""
            UPDATE VEHICULO SET
                tipo_vehiculo = %s, marca = %s, modelo = %s, anio = %s,
                nombre_propietario = %s, documento_propietario = %s,
                telefono_propietario = %s, email_propietario = %s
            WHERE id_vehiculo = %s
        """, (tipo_vehiculo, marca, modelo, anio,
              nombre_propietario, documento_propietario,
              telefono_propietario, email_propietario, id_vehiculo))

        db.conexion.commit()
        return {'error': False, 'mensaje': 'Vehículo actualizado correctamente'}