import os

class Config:
    DB_HOST     = os.environ.get('DB_HOST', 'localhost')
    DB_USER     = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME     = os.environ.get('DB_NAME', 'sigcda_db')
    DB_PORT     = int(os.environ.get('DB_PORT', 3306))
    JWT_SECRET  = os.environ.get('JWT_SECRET', 'sigcda_secret_key_2026')