from database.db_connection import DatabaseConnection
from utils.hash_helper import hashear_password

class UsuarioService:

    @staticmethod
    def registrar(datos):
        nombre    = datos.get('nombre')
        apellido  = datos.get('apellido')
        telefono  = datos.get('telefono')
        correo    = datos.get('correo')
        contrasena = datos.get('contrasena')
        rol       = datos.get('rol')

        if not all([nombre, apellido, correo, contrasena, rol]):
            return {'error': True, 'mensaje': 'Faltan campos obligatorios'}

        if rol not in ['admin', 'tecnico']:
            return {'error': True, 'mensaje': 'Rol no válido'}

        db = DatabaseConnection()
        cursor = db.get_cursor()

        cursor.execute("SELECT id_usuario FROM USUARIO WHERE correo = %s", (correo,))
        if cursor.fetchone():
            return {'error': True, 'mensaje': 'El correo ya está registrado'}

        hash_pw = hashear_password(contrasena)

        cursor.execute("""
            INSERT INTO USUARIO (nombre, apellido, telefono, correo, contrasena_hash, rol)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre, apellido, telefono, correo, hash_pw, rol))

        db.conexion.commit()

        return {'error': False, 'mensaje': 'Usuario registrado correctamente'}