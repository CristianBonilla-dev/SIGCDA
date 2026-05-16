from database.db_connection import DatabaseConnection
from utils.hash_helper import verificar_password
from utils.jwt_helper import generar_token

class AuthService:

    @staticmethod
    def login(datos):
        correo = datos.get('correo')
        contrasena = datos.get('contrasena')

        if not correo or not contrasena:
            return {'error': True, 'mensaje': 'Correo y contraseña son requeridos'}

        db = DatabaseConnection()
        cursor = db.get_cursor()
        cursor.execute(
            "SELECT * FROM USUARIO WHERE correo = %s", (correo,)
        )
        usuario = cursor.fetchone()

        if not usuario:
            return {'error': True, 'mensaje': 'Credenciales incorrectas'}

        if not verificar_password(contrasena, usuario['contrasena_hash']):
            return {'error': True, 'mensaje': 'Credenciales incorrectas'}

        token = generar_token(usuario['id_usuario'], usuario['rol'])

        return {
            'error': False,
            'token': token,
            'rol': usuario['rol'],
            'nombre': usuario['nombre']
        }