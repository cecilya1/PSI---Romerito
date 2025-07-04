from flask import Flask, render_template, request, make_response, redirect, url_for

app = Flask(__name__)
genero = ' '
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/votacao', methods=['POST', 'GET'])
def votar():
    if request.method == 'POST':
        nome = request.form['nome']
        genero = request.form['genero']
        response = make_response(redirect(url_for('resultado', genero=genero)))
        response.set_cookie('nome',nome, max_age=5*60)
        return response
    return render_template('votacao.html')
@app.route('/resultado')
def resultado():
    nome = request.cookies.get('nome')
    if nome == None:
        nome = 'Vitante'
    genero = request.args.get('genero')
    return render_template('resultado.html', genero=genero, nome=nome)