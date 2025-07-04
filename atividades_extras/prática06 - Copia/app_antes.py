from flask import Flask, render_template
from flask import request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ULTRAMEGADIFICIL'

login_manager = LoginManager()
login_manager.__init__(app)

produtos_carrinho = {
    'gibao' : 500,
    'bota' : 1500,
    'espora' : 200,
    'carralo' : 15000,
    'bezerro' : 3000,
    'chape' : 500,
    'oculos' : 1500,
    'capacete' : 300
}
# Revisar o projeto de produtos e compras.
# Salvar os dados de produtos em arquivo json (recuperar na sessão quando o projeto for executado novamente após ter o servidor encerrado)
# Salvar as compras de um usuário em arquivo json. 
# Ao fechar o carrinho de compras, salvar os dados no arquivo mencionado acima e limpar o carrinho.

class User(UserMixin):
    def __init__(self, nome, senha) -> None:
        self.id = nome
        self.senha = senha

    @classmethod
    def get(cls, user_id):
        lista_usuarios = session['usuarios']
        if user_id in lista_usuarios:
            senha = lista_usuarios[user_id]
            user = User(nome=user_id, senha=senha)
            return user


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
        nome = request.form['nome']
        senha= request.form['senha']
        if nome in session['usuarios']:
            return redirect(url_for('cadastro'))
        senha_crip = generate_password_hash(senha)
        user = User(nome=nome, senha=senha_crip)
        usuarios = session['usuarios']
        usuarios[nome] = {
            'senha': senha_crip,
            'carrinho': []
        }
        session['usuarios'] = usuarios
        login_user(user)
        try:
            with open('arquivo.json', 'r') as f:
                dados = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
                # Se o arquivo não existir ou estiver vazio/corrompido, cria um dict vazio e grava
            dados = {}
        dados[current_user.id]={}
        with open('arquivo.json', 'w') as f:
            json.dump(dados, f)
        #     if 'carrinho' in session['usuarios'][nome]:
        #         session[nome] = session['usuarios'][nome]['carrinho']
        #     else:
        #         session[nome] = []
        return redirect(url_for('login'))
    return render_template('cadastro.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        if nome in session['usuarios'] and check_password_hash(session['usuarios'][nome]['senha'], senha):
            user = User(nome=nome, senha=session['usuarios'][nome]['senha'])
            login_user(user)
            return redirect(url_for('produtos'))
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/produtos')
@login_required
def produtos():
    return render_template('produtos.html', produtos=produtos_carrinho)


@app.route('/adicionar', methods=['POST'])
@login_required
def adicionar():
    prod = request.form['prod']
    try:
        with open('arquivo.json', 'r') as f:
            dados = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {}
        with open('arquivo.json', 'w') as f:
            json.dump(dados, f)

    # Adiciona o novo elemento
    if isinstance(dados, dict):
        if prod in dados[current_user.id]:
            dados[current_user.id][prod] = [produtos_carrinho[prod], dados[current_user.id][prod][1]+1]
            # dados[current_user.id] = 'pii'
        else:
            dados[current_user.id][prod] = [produtos_carrinho[prod], 1]
    else:
        print("Formato de JSON inválido.")
        return

    with open('arquivo.json', 'w') as f:
        json.dump(dados, f, indent=4)
    
    
   
    return redirect(url_for('carrinho'))


@app.route('/carrinho')
@login_required
def carrinho():
    # soma=0
    # for x in session[current_user.id]:
    #     soma += produtos_carrinho[x]
    with open('arquivo.json', 'r') as f:
        dados = json.load(f)

    return render_template('carrinho.html', carrinho=dados)


@app.route('/compra', methods=['POST', 'GET'])

def compra():
    if request.method == 'POST':
        try:
            with open('compras.json', 'r') as f:
                compras = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            compras = {}
            with open('compras.json', 'w') as f:
                json.dump(compras, f)
        with open('arquivo.json', 'r') as f:
            dados = json.load(f)
        if current_user.id in compras:
            # compras[current_user.id] = str(len(compras[current_user.id])+1)
            id = str(len(compras[current_user.id])+1)
            compras[current_user.id][id] = dados[current_user.id]
            dados[current_user.id] = {}
        else:
            compras[current_user.id] = {'1': dados[current_user.id]}
            # compras[current_user.id]['1'] = dados[current_user.id]
            dados[current_user.id] = {}
        with open('arquivo.json', 'w') as f:
            json.dump(dados, f, indent=4)
        with open('compras.json', 'w') as f:
            json.dump(compras, f, indent=4)
        return render_template('compra.html')
    
    
    





@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/remover_prod', methods=['POST', 'GET'])
@login_required
def remover_prod():
    with open('arquivo.json', 'r') as f:
        dados = json.load(f)
    dados[current_user.id] = {}
    with open('arquivo.json', 'w') as f:
        json.dump(dados, f, indent=4)
    return redirect(url_for('carrinho'))

    
if __name__ == '__main__':
    app.run(debug=True)
