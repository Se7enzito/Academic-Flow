import os

from backend.libs.db.dbAPI import Conexao

from flask import Flask, render_template, request, session, redirect
from flask_session import Session

app = Flask(__name__, template_folder="../frontend/templates")

conn = Conexao()

app.static_folder = '../frontend/src'
app.static_url_path = '/static'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'libs', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SESSION_TYPE'] = 'securecookie'
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
    matricula = data.get('matricula')
    senha = data.get('senha')
    
    sucesso = conn.loginUser(matricula, senha)
    
    if sucesso:
        session['matricula'] = matricula
        return {'status': True}, 200
    else:
        return {'status': False, 'message': 'Invalid credentials.'}, 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    matricula = data.get('matricula')
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    
    sucesso = conn.registrarUser(matricula, nome, email, senha)
    
    if sucesso:
        session['matricula'] = matricula
        return {'status': True}, 201
    else:
        return {'status': False, 'message': 'Email already registered.'}, 409

# Run
if __name__ == '__main__':
    conn.criarTabelas()
    
    app.run(debug=True)