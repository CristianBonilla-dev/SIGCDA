import mysql.connector
import os

conn = mysql.connector.connect(
    host=os.environ.get('DB_HOST'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    database=os.environ.get('DB_NAME'),
    port=int(os.environ.get('DB_PORT', 3306))
)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS USUARIO (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(15),
    correo VARCHAR(150) NOT NULL UNIQUE,
    contrasena_hash VARCHAR(255) NOT NULL,
    rol ENUM('admin','tecnico') NOT NULL,
    fecha_creacion DATETIME DEFAULT NOW()
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS VEHICULO (
    id_vehiculo INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(10) NOT NULL UNIQUE,
    tipo_vehiculo ENUM('carro','moto','camion','otro') NOT NULL,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    anio YEAR,
    nombre_propietario VARCHAR(100) NOT NULL,
    documento_propietario VARCHAR(20) NOT NULL,
    telefono_propietario VARCHAR(15),
    email_propietario VARCHAR(150),
    fecha_registro DATETIME DEFAULT NOW(),
    registrado_por INT,
    FOREIGN KEY (registrado_por) REFERENCES USUARIO(id_usuario)
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS REVISION (
    id_revision INT AUTO_INCREMENT PRIMARY KEY,
    id_vehiculo INT NOT NULL,
    id_tecnico INT NOT NULL,
    fecha_revision DATE NOT NULL,
    hora_revision TIME,
    tipo_revision ENUM('tecnico_mecanica','gases','preventiva','reinspeccion') NOT NULL,
    estado ENUM('pendiente','aprobado','rechazado') DEFAULT 'pendiente',
    resultado ENUM('aprobado','rechazado'),
    observaciones TEXT,
    fecha_resultado DATETIME,
    FOREIGN KEY (id_vehiculo) REFERENCES VEHICULO(id_vehiculo),
    FOREIGN KEY (id_tecnico) REFERENCES USUARIO(id_usuario)
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS ITEM_INSPECCION (
    id_item INT AUTO_INCREMENT PRIMARY KEY,
    id_revision INT NOT NULL,
    nombre_item ENUM('frenos','luces','suspension','neumaticos','emision_gases','direccion','motor','carroceria') NOT NULL,
    resultado ENUM('aprobado','rechazado'),
    observacion TEXT,
    FOREIGN KEY (id_revision) REFERENCES REVISION(id_revision)
)""")

conn.commit()
print("Tablas creadas correctamente")
conn.close()