import bcrypt

def hashear_password(contrasena):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(contrasena.encode('utf-8'), salt).decode('utf-8')

def verificar_password(contrasena, hash_guardado):
    return bcrypt.checkpw(
        contrasena.encode('utf-8'),
        hash_guardado.encode('utf-8')
    )