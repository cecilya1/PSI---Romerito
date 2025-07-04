from flask import Flask, render_template, request,\
    url_for, session, redirect, url_for

app = Flask(__name__)

app.config['SECRET_KEY'] = 'MEAGADIFICIL_ME_ESCONDE'

users = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        if nome in users:
            return redirect(url_for('login'))
        else:
            users.append(nome)
            session['user'] = nome
            return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        if nome in users:
            session['user'] = nome
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dash')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))
    
@app.route('/logout', methods = ['POST'])
def logout():
    session.pop('user')
    return redirect(url_for('index'))