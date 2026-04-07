from flask import render_template, request, redirect, url_for, flash, session
from .dao import UserDAO
from .models import User


class UserController:

    def __init__(self):
        self.__dao = UserDAO()


    # CADASTRAR
    def cadastrar_user(self):
        email = request.form.get("email")
        senha = request.form.get("senha")

        if not email or not senha:
            flash("Erro: Preencha todos os campos obrigatórios!", "danger")
            return self.preparar_cadastro()

        try:
            novo_user = User(
                email,
                senha
            )
            self.__dao.salvar_user(novo_user)
            flash(f"Sucesso: O email '{email}' foi cadastrado!", "success")
            return redirect(url_for("user.index"))

        except Exception as e:
            flash(f"Erro ao cadastrar usuário: {str(e)}", "danger")
            return redirect(url_for("user.preparar_cadastro"))

        
    def preparar_cadastro(self):
        return render_template("cadastro.html")


    def index(self):
        return render_template("index.html")
    
    def login(self):
        email = request.form.get("email")
        senha = request.form.get("senha")

        if not email or not senha:
            flash("Erro: Preencha todos os campos obrigatórios!", "danger")
            return self.preparar_login()

        users = self.__dao.carregar_user()
        for user in users:
            if user.email == email and user.senha == senha:
                session['usuário'] = email
                flash(f"Sucesso: logou no email '{email}' !", "success")
                return redirect(url_for("user.index"))
        return redirect(url_for("user.login"))
        
    def preparar_login(self):
        return render_template("login.html")
    
    def encerrar(self):
        session.pop('usuário')
        return self.index()


    # REMOVER
#    def remover_user(self, id):
#        self.__dao.remover_user(id)
#        flash("Sucesso: User removido com sucesso!", "success")
#        return redirect(url_for("games.listar_jogos"))
    
