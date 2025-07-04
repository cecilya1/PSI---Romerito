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
from flask import redirect, request, render_template, make_response, session
from flask_login import login_manager, LoginManager, login_user, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

login_manager = LoginManager()

app.config['SECRET_KEY'] = 'ESCONDA-ME'

LoginManager.__init__(app)

class User(UserMixin):
    def __init__(self, senha, nome):
        self.senha = senha
        self.nome =nome

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
        usuarios = session['users']
        usuarios[id_user] = {'nome':nome, 'senha':senha}
        session['users'] = usuarios

    pass

@app.route('/login', methods=['POST', 'GET'])
def login():
    pass