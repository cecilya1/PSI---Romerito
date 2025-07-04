from flask import Flask
from flask import session, render_template, redirect, url_for, request
from flask_login import login_manager, LoginManager, login_user, logout_user, UserMixin, current_user

from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

app = Flask(__name__)

login_manager = LoginManager()

app.config['SECRET_KEY'] = 'ENCONDE-ME'

login_manager.__init__(app)

livros_al = {
    "Dom Casmurro": {"alugados": 3, "total": 4},
    "O Pequeno Principe": {"alugados": 5, "total": 15},
    "1984": {"alugados": 2, "total": 8},
    "A Revolucao dos Bichos": {"alugados": 4, "total": 12},
    "Memorias Postumas": {"alugados": 1, "total": 5}
}

class User(UserMixin):
    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha
    
    @classmethod
    def get(cls, user_id):
        if user_id in session['users']:
            user = User(nome=session['users'][user_id]['nome'], senha=session['users'][user_id]['senha'])
            user.id = user_id
            return user
        
@login_manager.user_loader
def load(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    if 'users' not in session:
        session['users'] = {}
    return render_template('index.html')

@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        senha_crip = generate_password_hash(senha)
        usuario_id = str(len(session['users']) + 1)
        usuarios = session['users'] 
        usuarios[usuario_id]={'nome':nome, 'senha':senha_crip}
        session['users'] = usuarios
        user = User(nome=nome, senha=senha_crip)
        user.id = usuario_id
        login_user(user)
        return render_template('login.html')
    return render_template('cadastro.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        for k, dados in session['users'].items():
            if nome == dados['nome'] and check_password_hash(dados['senha'], senha):
                user = User(nome=nome, senha=dados['senha'])
                user.id = k
                login_user(user)
                if not os.path.exists('historico.json'):
                    with open('historico.json', 'w') as f:
                        json.dump({}, f)

                return render_template('livros.html', livros_al=livros_al)
                # return 'oiii'
        return render_template('login.html')
    return render_template('login.html')

@app.route('/livros', methods=['POST', 'GET'])
def livros():
    if request.method == 'POST':
        livro = request.form['livro']
        livros_al[livro]['alugados'] +=1 
        with open('historico.json', 'r') as f:
            historico = json.load(f)
        if current_user.nome not in historico:
            historico[current_user.nome] = {}
        if livro not in historico[current_user.nome] or historico[current_user.nome][livro]['quant'] == 0:
            historico[current_user.nome][livro] = {'status': 'alugado'}
            historico[current_user.nome][livro]['quant'] = 1
            print(historico[current_user.nome][livro])
        else:
            historico[current_user.nome][livro] = {'status': 'alugado', 'quant':historico[current_user.nome][livro]['quant']+1}
            # return historico[current_user.nome][livro]['quant']
            # print(historico[current_user.nome][livro])
        with open('historico.json', 'w') as f:
            json.dump(historico, f, indent=4)
        return render_template('livros.html', livros_al=livros_al)
    return render_template('livros.html', livros_al=livros_al)

@app.route('/devolucao', methods=['POST', 'GET'])
def devolucao():
    if request.method == 'POST':
        livro = request.form['livro']
        with open('historico.json', 'r') as f:
            historico = json.load(f)
        historico[current_user.nome][livro]['quant'] -=1
        if historico[current_user.nome][livro]['quant'] == 0:
            historico[current_user.nome][livro]['status'] = 'devolvido'
        with open('historico.json', 'w') as f:
            json.dump(historico, f, indent=4)
        return render_template('devolucao.html', historico=historico)
        # return livro
    with open('historico.json', 'r') as f:
        historico = json.load(f)
    return render_template('devolucao.html', historico=historico)









