import os
import requests

from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect
from flask_session import Session

try:
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__, template_folder="../frontend/templates")

app.static_folder = '../frontend/src'
app.static_url_path = '/static'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'libs', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev-secret")
app.config['SESSION_TYPE'] = 'filesystem'

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=True
)

Session(app)

# Flask Site
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/saber_mais')
def saber_mais():
    return render_template('sobre.html')

@app.route('/entrar')
def entrar():
    return render_template('entrar.html')

@app.route('/dashboard')
def dashboard():
    matricula = session.get('matricula')
    
    if not matricula:
        return redirect('/entrar')
    
    return render_template('dashboard.html')

@app.route('/atividades')
def atividades():
    matricula = session.get('matricula')
    
    if not matricula:
        return redirect('/entrar')
    
    return render_template('atividades.html')

@app.route('/autoboca')
def autoboca():
    matricula = session.get('matricula')
    
    if not matricula:
        return redirect('/entrar')
    
    return render_template('autoboca.html')

@app.route('/fluxograma')
def fluxograma():
    matricula = session.get('matricula')
    
    if not matricula:
        return redirect('/entrar')
    
    return render_template('fluxograma.html')

@app.route('/materias')
def materias():
    matricula = session.get('matricula')
    
    if not matricula:
        return redirect('/entrar')
    
    return render_template('materias.html')

@app.route('/logout')
def logout():
    session.clear()
    
    return redirect('/')

# Flask API
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    response = requests.post(
        "https://academic-flow-api.onrender.com/auth/login",
        json=data,
        timeout=5
    )

    if response.status_code == 200:
        user = response.json()

        session['matricula'] = user['matricula']

        return {'status': True}, 200

    return {'status': False, 'message': 'Credenciais inválidas'}, 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    response = requests.post(
        "https://academic-flow-api.onrender.com/auth/registro",
        json=data,
        timeout=5
    )

    if response.status_code in (200, 201):
        user = response.json()

        session['matricula'] = user['matricula']
        session['nome'] = user.get('nome')
        session['email'] = user.get('email')

        return {'status': True}, 201

    print(response)

    return {
        'status': False,
        'message': response.json().get(
            'message', 'Erro ao registrar usuário'
        )
    }, 409

# Run
if __name__ == '__main__':
    app.run(debug=True)