import os
import requests

from time import time
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect
from flask_session import Session

try:
    load_dotenv()
except ImportError:
    pass

CACHE = {}
CACHE_TTL = 300

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
    acess_token = session.get('access_token')
    refresh_token = session.get('refresh_token')
    
    if not acess_token or not refresh_token:
        return redirect('/entrar')
    
    return render_template('dashboard.html')

@app.route('/atividades')
def atividades():
    acess_token = session.get('access_token')
    refresh_token = session.get('refresh_token')
    
    if not acess_token or not refresh_token:
        return redirect('/entrar')
    
    return render_template('atividades.html')

@app.route('/autoboca')
def autoboca():
    acess_token = session.get('access_token')
    refresh_token = session.get('refresh_token')
    
    if not acess_token or not refresh_token:
        return redirect('/entrar')
    
    return render_template('autoboca.html')

@app.route('/fluxograma')
def fluxograma():
    acess_token = session.get('access_token')
    refresh_token = session.get('refresh_token')
    
    if not acess_token or not refresh_token:
        return redirect('/entrar')
    
    return render_template('fluxograma.html')

@app.route('/materias')
def materias():
    acess_token = session.get('access_token')
    refresh_token = session.get('refresh_token')
    
    if not acess_token or not refresh_token:
        return redirect('/entrar')
    
    return render_template('materias.html')

@app.route('/logout')
def logout():
    refresh = session.get('refresh_token')

    if refresh:
        requests.post(
            "https://academic-flow-api.onrender.com/auth/logout",
            json={"refresh_token": refresh},
            timeout=5
        )

    session.clear()
    
    return redirect('/')

# Flask API
def cache_get(key):
    item = CACHE.get(key)

    if not item:
        return None

    data, expires = item
    if time() > expires:
        del CACHE[key]
        return None

    return data


def cache_set(key, value, ttl=CACHE_TTL):
    CACHE[key] = (value, time() + ttl)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    response = requests.post(
        "https://academic-flow-api.onrender.com/auth/login",
        json=data,
        timeout=5
    )

    if response.status_code in (200, 201):
        tokens = response.json()

        session['access_token'] = tokens['access_token']
        session['refresh_token'] = tokens['refresh_token']

        return {'status': True}, response.status_code

    return {
        'status': False,
        'message': response.json().get('detail', 'Credenciais inválidas')
    }, response.status_code

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    response = requests.post(
        "https://academic-flow-api.onrender.com/auth/register",
        json=data,
        timeout=5
    )

    if response.status_code in (200, 201):
        tokens = response.json()
    
        session['access_token'] = tokens['access_token']
        session['refresh_token'] = tokens['refresh_token']
    
        return {'status': True}, response.status_code

    return {
        'status': False,
        'message': response.json().get(
            'message', 'Erro ao registrar usuário'
        )
    }, response.status_code

def api_request(method, url, **kwargs):
    access = session.get("access_token")

    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {access}"

    response = requests.request(
        method,
        url,
        headers=headers,
        **kwargs
    )

    if response.status_code == 401:
        refresh = session.get("refresh_token")

        refresh_response = requests.post(
            "https://academic-flow-api.onrender.com/auth/refresh",
            json={"refresh_token": refresh}
        )

        if refresh_response.status_code == 200:
            new_access = refresh_response.json()["access_token"]
            session["access_token"] = new_access

            headers["Authorization"] = f"Bearer {new_access}"
            return requests.request(method, url, headers=headers, **kwargs)

    return response

@app.route('/api/fluxograma', methods=['GET'])
def get_fluxograma():
    cached = cache_get("fluxograma")

    if cached:
        return cached, 200

    response = api_request(
        "GET",
        "https://academic-flow-api.onrender.com/fluxograma/"
    )

    if response.status_code == 200:
        cache_set("fluxograma", response.json())

    return response.json(), response.status_code

@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    CACHE.clear()
    return {'status': 'cache limpo'}

# Run
if __name__ == '__main__':
    app.run(debug=True)