from flask import Flask, render_template, request, make_response, url_for, redirect

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/votar", methods=['GET', 'POST'])
def votar():
    if request.method == 'POST':
        nome = request.form['nome']
        genero = request.form['generos']
        response = make_response(redirect(url_for('resultado', genero=genero)))
        response.set_cookie('nome', nome, max_age=5*60)
        return response
    return render_template('votar.html')

@app.route("/resultado")
def resultado():
    nome = request.cookies.get('nome')
    if nome == None:
        nome = 'Visitante'
    genero = request.args.get('genero')
    return render_template('resultado.html', nome=nome, genero=genero)