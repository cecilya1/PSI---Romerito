from flask import Flask
from flask import request, render_template, redirect, url_for, session
from flask_login import login_manager, LoginManager, UserMixin, login_user, logout_user, current_user

app = Flask(__name__)

login_manager = LoginManager()

app.config['SECRET_KEY'] = 'Esconde-me'

login_manager.__init__(app)

produtos_vender =  {
    "Camisa": 49.90,
    "Calça Jeans": 89.90,
    "Tênis Esportivo": 199.90,
    "Relógio Digital": 149.00,
    "Mochila": 79.90,
    "Fone de Ouvido": 59.90,
    "Garrafa Térmica": 39.90,
    "Jaqueta Corta-Vento": 129.90,
    "Boné": 29.90,
    "Carteira de Couro": 69.90
}


class User(UserMixin):
    def __init__(self, senha):
        self.senha = senha
    
    @classmethod
    def get(cls, user_id):
        if user_id in session['users']:
            user = User(senha=session['users'][user_id])
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
        user = User(senha=senha)
        user.id = nome
        usuarios = session['users']
        usuarios[nome] = [senha, {}]
        session['users'] = usuarios
        login_user(user)
        return redirect(url_for('produtos'))
    return render_template('cadastro.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        if nome in session['users'] and senha == session['users'][nome][0]:
            user = User(senha=senha)
            user.id = nome
            login_user(user)
            return redirect(url_for('produtos'))
        elif nome not in session['users']:
            return render_template('cadastro.html')
        return render_template('login.html')
    return render_template('login.html')

@app.route('/produtos')
def produtos():
    return render_template('produtos.html', itens = produtos_vender)

@app.route('/adicionar',  methods=['POST', 'GET'])
def adicionar():
    if request.method == 'POST':
        prod = request.form['produto']
        if prod in session['users'][current_user.id][1]:
            usuarios = session['users']
            usuarios[current_user.id][1][prod] += 1
        else:
            usuarios = session['users']
            usuarios[current_user.id][1][prod] = 1
            session['users'] = usuarios
        return session['users']



