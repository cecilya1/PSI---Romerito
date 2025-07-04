# 1. *Autenticação:*

#    * O usuário pode se registrar com um nome de usuário e senha.
#    * O login deve ser protegido com flask_login.
#    * Senhas devem ser criptografadas antes de salvar.

# 2. *Sistema de Sessão e Cookies:*

#    * Use session para manter dados temporários do usuário (por exemplo, se ele já votou).
#    * Use cookies para armazenar o último login (nome do usuário).

# 3. *Página de Votação:*

#    * Exibe as opções disponíveis.
#    * Só usuários logados podem votar.
#    * Após votar, o usuário é redirecionado para uma página de agradecimento.
#    * O voto deve ser registrado em um arquivo .json.

# 4. *Página de Resultados:*

#    * Exibe a contagem de votos por opção.
#    * Só acessível para usuários logados *e* que já votaram.

# 5. *Templates:*

#    * Use base.html com block.
#    * Use include para cabeçalho e rodapé.
#    * Use flash para mensagens de erro ou sucesso.

# 6. *Restrições:*

#    * Um usuário só pode votar uma vez (verifique por session ou por arquivo).


from flask import Flask
from flask import redirect, request, render_template, make_response, session, Response, url_for, flash
from flask_login import login_manager, LoginManager, login_user, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
app = Flask(__name__)


login_manager = LoginManager()

app.config['SECRET_KEY'] = 'ESCONDA-ME'

login_manager.__init__(app)

# @app.context_processor
# def inject_user():
#     return dict(current_user=current_user)

candidatos = ['carla', 'breno', 'laura', 'paulo']
class User(UserMixin):
    def __init__(self, senha, nome):
        self.senha = senha
        self.nome =nome

    @classmethod
    def get(cls, user_id):
        if user_id in session['users']:
            user = User(senha=session['users'][user_id]['senha'], nome=session['users'][user_id]['nome'])
            user.id = user_id
            return user

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    if 'users' not in session:
        session['users'] = {}
    if not os.path.exists('votos.json'):
        votos = {}
        for x in candidatos:
            votos[x] = 0
        with open('votos.json', 'w') as f:
            json.dump(votos, f, indent=4)
    return render_template('index.html')

@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        senha_crip = generate_password_hash(senha)
        user = User(senha=senha_crip, nome=nome)
        id_user = str(len(session['users'])+1)
        user.id = id_user
        login_user(user)
        usuarios = session['users']
        usuarios[id_user] = {'nome':nome, 'senha':senha, 'voto':False}
        session['users'] = usuarios
        responta = make_response(redirect(url_for('index', usuario= session['users'][current_user.id])))
        responta.set_cookie('nome', nome)
        return responta
    return render_template('cadastro.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        for k, v in session['users'].items():
            if nome in v and check_password_hash(v['senha'], senha):
                responta = make_response(redirect(url_for('index')))
                responta.set_cookie('nome', nome)
                user = User(senha=v['senha'], nome=nome)
                user.id = k
                login_user(user)
                return responta
        flash('Algum dado está incorreto!!', category='erro')
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/votacao', methods=['POST', 'GET'])
def votacao():
    if request.method == 'POST':
        voto = request.form['voto']
        if session['users'][current_user.id]['voto'] == False:
            with open('votos.json', 'r') as f:
                votos = json.load(f)
            votos[voto] += 1
            with open('votos.json', 'w') as f:
                json.dump(votos, f, indent=4)
            usuarios = session['users']
            usuarios[current_user.id]['voto'] = True
            session['users'] = usuarios
            return redirect(url_for('index'))
        flash('Você já votou não pode votar mais!!!', category='erro')
        return redirect(url_for('index'))
    return render_template('votacao.html') 

@app.route('/resultado')
def resultado():
    with open('votos.json', 'r') as f:
        resultado_votos = json.load(f)
    return render_template('resultado.html', resultado_votos = resultado_votos)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))