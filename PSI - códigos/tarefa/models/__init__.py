from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin
from flask import session

class User(UserMixin):
    def __init__(self, email, senha):
        self.email = email
        self.senha = senha

    @classmethod
    def get(cls, user_id):
        usuarios = session['usuarios']
        for id, dados in usuarios.items():
            if user_id == id:
                user = User(email=dados['email'], senha=dados['senha'])
                user.id = user_id
                return user