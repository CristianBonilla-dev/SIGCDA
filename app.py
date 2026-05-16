from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from config import Config

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET

jwt = JWTManager(app)

# ── Rutas HTML ──────────────────────────────────────
@app.route('/')
def login():
    return render_template('publico/login.html')

@app.route('/consulta')
def consulta():
    return render_template('publico/consulta.html')

@app.route('/admin/usuarios')
def admin_usuarios():
    return render_template('admin/usuarios.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')

@app.route('/tecnico/revisiones')
def tecnico_revisiones():
    return render_template('tecnico/revisiones.html')

# ── Rutas API ───────────────────────────────────────
from controllers.auth_controller import auth_bp
from controllers.usuario_controller import usuario_bp
from controllers.vehiculo_controller import vehiculo_bp
from controllers.revision_controller import revision_bp
from controllers.consulta_controller import consulta_bp

app.register_blueprint(auth_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(vehiculo_bp)
app.register_blueprint(revision_bp)
app.register_blueprint(consulta_bp)

if __name__ == "__main__":
    app.run(debug=True)