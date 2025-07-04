from flask import Flask, render_template, request, make_response, redirect, url_for, session

app = Flask(__name__)

app.config['SECRET_KEY'] = 'segredodificil'

@app.route('/')
def index():
    return render_template('index.html')
@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')
    else:
        nome = request.form['nome']
        genero = request.form['genero']
        # guardar o usuário na sessão
        session['user'] = nome 
        response = make_response(redirect(url_for('preferencia')))
        # response.set_cookie('nome', nome, max_age=7*24*3600)
        response.set_cookie(nome, genero, max_age=7*24*3600)
        return response
@app.route('/preferencia')
def preferencia():
    # nome = request.cookies['nome']
    # genero = request.cookies['genero']

    if 'user' in session:
        user = session['user']
        if user in request.cookies:
            genero = request.cookies.get(user)
            return user + '-' + genero
    return 'deu ruim'
@app.route('/recomendar')
def recomendar():
    filmes_por_genero = {
    'acao': ['Missão Impossível', 'John Wick', 'Velozes e Furiosos'],
    'comedia': ['As Branquelas', 'Todo Mundo em Pânico', 'Click'],
    'drama': ['À Espera de um Milagre', 'Forrest Gump', 'Clube da Luta'],
    'ficcao': ['Interestelar', 'Matrix', 'Blade Runner']
    }
    genero = request.args.get('genero')
    if genero in filmes_por_genero.keys():
        filmes = filmes_por_genero[genero]
    return render_template('filmes.html', filmes=filmes)
