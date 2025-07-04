from flask import Flask
from flask import redirect, render_template, make_response, url_for, session, request, flash
from flask_login import login_manager, LoginManager, login_user, UserMixin, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

login_manager = LoginManager()

app.config['SECRET_KEY'] = 'ESCONDA-ME'

login_manager.__init__(app)

global tema_cor
tema_cor = 'white'

livros_al = [
    {
        "titulo": "O Poder do Habito",
        "autor": "Charles Duhigg",
        "descricao": "Como habitos funcionam e como transforma-los em aliados no dia a dia."
    },
    {
        "titulo": "Dom Casmurro",
        "autor": "Machado de Assis",
        "descricao": "Classico da literatura brasileira sobre duvidas, ciumes e memoria."
    },
    {
        "titulo": "1984",
        "autor": "George Orwell",
        "descricao": "Uma distopia sobre vigilancia, censura e totalitarismo."
    },
    {
        "titulo": "A Revolucao dos Bichos",
        "autor": "George Orwell",
        "descricao": "Uma fabula politica que critica regimes autoritarios."
    },
    {
        "titulo": "A Culpa e das Estrelas",
        "autor": "John Green",
        "descricao": "Um romance jovem-adulto sobre amor, doenca e superacao."
    },
]
# 1. Página Inicial

#     Deve exibir uma mensagem de boas-vindas.

#     Se o usuário estiver logado, mostrar seu nome e um link para deslogar.

#     Se não estiver logado, mostrar links para login e cadastro.

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
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    if 'users' not in session:
        session['users'] = {}
    if 'historico' not in session:
        session['historico'] = {}
    # tema = request.cookies.get('tema')
    # if tema is not None:
    #     resposta = Response(redirect(url_for('index')))
    #     resposta.set_cookie('tema', 'white')
    #     return resposta
    return render_template('index.html')

@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        if nome in session['users']:
            flash('Você já possui cadastro', category='error')
            return redirect(url_for('cadastro'))
        senha_crip = generate_password_hash(senha)
        usuarios = session['users']
        usuarios[nome] = senha_crip
        session['users'] = usuarios
        user = User(senha=senha_crip)
        user.id = nome
        login_user(user)
        if current_user.id not in session['historico']:
            historico_pessoal  = session['historico']
            historico_pessoal[current_user.id] = []
            session['historico'] = historico_pessoal 
        return redirect(url_for('index'))
    return render_template('cadastro.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        if nome in session['users'] and check_password_hash(session['users'][nome], senha):
            user = User(senha=session['users'][nome])
            user.id = nome
            login_user(user)
            return redirect(url_for('index'))
        flash('Dados incorretos', category='error')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/livros', methods=['POST', 'GET'])
def livros():
    if request.method == 'POST':
        livro = request.form['livro']
        historico_pessoal = session['historico']
        historico_pessoal [current_user.id].append(livro)
        session['historico'] = historico_pessoal 
        flash('Livro alugado com sucesso!!!', category='alugado')
        return redirect(url_for('livros'))
    return render_template('livros.html', livros_al = livros_al)

# Permitir ao usuário escolher uma “cor de tema” (claro ou escuro, por exemplo).

# Armazenar essa preferência em um cookie.

# Usar make_response para definir esse cookie.

@app.route('/configuracao', methods=['POST', 'GET'])
def configuracao():
    if request.method == 'POST':
        tema = request.form['tema']
        resposta = make_response(redirect(url_for('index')))
        resposta.set_cookie(current_user.id, tema)
        return resposta
    return render_template('configuracao.html')

@app.route('/historico')
def historico():
    historico_pessoal = session['historico'][current_user.id]
    return render_template('historico.html', historico_pessoal = historico_pessoal)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

