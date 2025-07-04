from flask import Flask, render_template, request, \
    url_for, session, redirect

app = Flask(__name__)

app.config['SECRET_KEY'] = 'MEGADIFICIL_ME_ESCONDE'

users = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        if nome in users:
            session['user'] = nome
            return redirect(url_for('dashboard'))

@app.route('/dash')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html')
    return redirect(url_for('login'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user')
    return redirect(url_for('index'))