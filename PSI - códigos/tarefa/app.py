from flask import Flask, request, redirect, url_for, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, LoginManager, login_user, login_required, logout_user
app = Flask(__name__)

app.config['SECRET_KEY'] = 'SECRETY_PASSWORD'

login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    if 'usuarios' not in session:
        session['usuarios'] = {}
    return render_template('index.html')

@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        senha = generate_password_hash(senha)

        usuarios = session['usuarios']
        for dados in usuarios.values():
            if email == dados['email']:
                return redirect(url_for('login'))
        
        id = len(usuarios) + 1
        id = str(id)
        usuarios[id] = {'email': email, 'senha': senha}
        session['usuarios'] = usuarios
        user = User(email = email, senha = senha)
        user.id = id
        login_user(user)
        session['logout'] = True
        return redirect(url_for('tarefas'))
    return render_template('cadastro.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuarios = session['usuarios']
        for dados in usuarios.values():
            if email == dados['email'] and check_password_hash(dados['senha'], senha):
                user = User(email = email, senha = senha)
                user.id = id
                login_user(user)
                return redirect(url_for('tarefas'))
        
        return redirect(url_for('login'))
    return render_template('login.html')

@login_required
@app.route('/tarefas')
def tarefas():
    pass

@login_required
@app.route('/logout')
def logout():
    logout_user()
    pass