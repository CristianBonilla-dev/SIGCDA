import mysql.connector
from config import Config

class DatabaseConnection:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.conexion = mysql.connector.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
                port=Config.DB_PORT
            )
        return cls._instancia

    def get_cursor(self):
        if not self.conexion.is_connected():
            self.conexion.reconnect()
        return self.conexion.cursor(dictionary=True)