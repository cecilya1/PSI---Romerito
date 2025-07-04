from flask import Flask
from flask import session, redirect, render_template, url_for, request
from flask_login import login_manager, LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

login_manager = LoginManager()

app.config['SECRET_KEY'] = 'ESCONDE-ME'

login_manager.__init__(app)

class User(UserMixin):
    def __init__(self, senha):
        self.senha = senha
    @classmethod
    def get(cls, user_id):
        if user_id in session['users']:
            user = User(senha=session['users'][user_id]['senha'])
            user.id = user_id
            # login_user(user)
            return user

@login_manager.user_loader
def load(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    if 'users' not in session:
        session['users'] = {}
    if 'tarefas' not in session:
        session['tarefas'] = {}

    #if current_user.is_authenticated
    return render_template('index.html')

@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        senha_crip = generate_password_hash(senha)
        user = User(senha=senha_crip)
        user.id = email
        usuarios= session['users']
        usuarios[email] = {'senha':senha_crip}
        session['users'] = usuarios
        login_user(user)
        return render_template('login.html')
    return render_template('cadastro.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        for k, dados in session['users'].items():
            if k == email and check_password_hash(dados['senha'], senha):
                user = User(senha=dados['senha'])
                user.id = email
                login_user(user)
                return render_template('tasks.html')
            else:
                return render_template('login.html')
    return render_template('login.html')

@app.route('/adicionar', methods=['POST', 'GET'])
def adicionar():
    if request.method == 'POST':
        texto = request.form['texto']
        tarefas = session['tarefas']
        if current_user.id not in tarefas:
            tarefas[current_user.id] = []
        tarefas[current_user.id].append({'texto':texto, 'status': 'pendente'})
        session['tarefas'] = tarefas 
        return render_template('tasks.html', dados = session['tarefas'][current_user.id])
    return render_template('adicionar.html')

@app.route('/remover', methods=['POST'])
def remover():
    texto = request.form['texto']
    tarefas = session['tarefas']
    for dados in tarefas[current_user.id]:
        if dados['texto'] == texto:
            tarefas[current_user.id].remove(dados)
    session['tarefas']=tarefas
    return render_template('tasks.html', dados = session['tarefas'][current_user.id])
    
@app.route('/tasks')
def tasks():
    return render_template('tasks.html', dados = session['tarefas'][current_user.id])



@app.route('/concluir', methods=['POST', 'GET'])
def concluir():
    
    texto = request.form['conclui']
    tarefas = session['tarefas']
    for dados in tarefas[current_user.id]:
        if dados['texto'] == texto:
            dados['status'] = 'concluida'
    session['tarefas']=tarefas
    return render_template('tasks.html', dados = session['tarefas'][current_user.id])
    # return render_template('tasks.html', dados = session['tarefas'][current_user.id])

@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html')

