from flask import Flask, render_template, request, make_response, url_for, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ESCONDIDINHA'

@app.route('/')
def index():
    if 'users' not in session:
        session['users'] = []
    return render_template('index.html')
global nome
nome = ''
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        global nome
        nome = request.form['nome']
        senha = request.form['senha']
        senha_crip = generate_password_hash(senha)
        for i in session['users']:
            if nome in i:
                return redirect(url_for('login'))
        usuario = session['users']
        usuario.append({nome:senha_crip})
        session['users'] = usuario
        return redirect(url_for('index'))
    return render_template('cadastro.html')
    

# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         nome = request.form['nome']
#         senha = request.form['senha']
#         if 'users' in session:
#             for user in session['users']:
#                 if nome in user:
#                     hash_salvo = user[nome]
#                     if check_password_hash(hash_salvo, senha):
#                         response = make_response(redirect(url_for('index')))
#                         response.set_cookie('nome', nome, max_age=24*3600) 
#                         nome = request.cookies.get('nome')
#                         return response
#         return session['users']
#     return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        global nome
        nome = request.form['nome']
        senha = request.form['senha']
        if 'users' in session:
            for user in session['users']:
                if nome in user:
                    hash_salvo = user[nome]
                    if check_password_hash(hash_salvo, senha):
                        response = make_response(redirect(url_for('index')))
                        response.set_cookie('nome', nome)
                        return response
        return '''
            <h2>Nome de usuário ou senha inválidos, ou talvez você ainda não tenha se cadastrado.</h2>
            <a href="/login">Clique aqui para tentar novamente</a>
            <br>
            <a href="/register">Cadastre-se agora</a>
            '''  

    return render_template('login.html')

@app.route('/produtos', methods=['GET', 'POST'])
def produtos():
    if request.method == 'POST':
        if len(session['users']) == 0:
            return redirect(url_for('cadastro'))
        prod = request.form['produto']
        return redirect(url_for('carrinho', prod=prod))
    return render_template('produtos.html')

@app.route('/carrinho')
def carrinho():
    produtos = {
        'Moto Homem-Aranha Yamaha': 12199,
        'Fidget Spinner': 9.99, 
        'Controle PS2 Transparente Aqua Lava': 199.90,
        'Charizard 1st edition PSA 10': 1000000 ,
        'Água mineral': 2.50,
        'Água mineral com gás': 2
    }
    global nome
    if nome not in session:
        session[nome] = {}
    carrinho = session[nome]
    prod = request.args.get('prod')
    if prod and prod in produtos:
        if prod in carrinho:
            carrinho[prod][1] += 1
        else:
            carrinho[prod] = [produtos[prod], 1] 
        session[nome] = carrinho
    total = 0
    for item in carrinho:
        total += carrinho[item][1]*carrinho[item][0]
    return render_template('carrinho.html', itens=session[nome], total=total, nome=nome)
@app.route('/esvaziar', methods=['POST'])
def esvaziar():
    global nome
    session[nome] = {}
    total = 0
    return render_template('carrinho.html', itens=session[nome], total=total, nome=nome)