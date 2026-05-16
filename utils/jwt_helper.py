from flask_jwt_extended import create_access_token

def generar_token(id_usuario, rol):
    return create_access_token(
        identity=str(id_usuario),
        additional_claims={'rol': rol}
    )