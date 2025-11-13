from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from database import init_db
from routes import tasks_bp
import os

# Obtener la ruta absoluta de la carpeta frontend
FRONTEND_PATH = os.path.join(os.path.dirname(__file__), '..', 'frontend')
FRONTEND_PATH = os.path.abspath(FRONTEND_PATH)

app = Flask(__name__, static_folder=FRONTEND_PATH, static_url_path='/')

CORS(app)

# Inicializar base de datos
init_db()

# Registrar blueprints
app.register_blueprint(tasks_bp)

@app.route('/')
def index():
    return send_from_directory(FRONTEND_PATH, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(FRONTEND_PATH, filename)

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)