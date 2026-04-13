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
        usuarios = self.__dao.carregar_user()

        if not email or not senha:
            flash("Erro: Preencha todos os campos obrigatórios!", "danger")
            return self.preparar_cadastro()
        
        for user in usuarios:
            if user.email == email:
                flash("Erro: Email já existente!", "danger")
                return redirect(url_for("user.cadastrar_user"))

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
        if email == "admin@gmail.com" and senha == "root":
            user_id = self.__dao.create_admin()
            session['usuario'] = email
            session['user_id'] = user_id
            session['admin'] = True
            return redirect(url_for("user.index"))
        if not email or not senha:
            flash("Erro: Preencha todos os campos obrigatórios!", "danger")
            return redirect(url_for("user.login"))

        users = self.__dao.carregar_user()
        for user in users:
            if user.email == email and user.senha == senha:
                session['usuario'] = email
                session['user_id'] = user.id
                session['admin'] = False
                flash(f"Sucesso: logou no email '{email}' !", "success")
                return redirect(url_for("user.index"))
        flash("Erro: Usúario não existente ou senha errada", "danger")
        return redirect(url_for("user.login"))
        
    def preparar_login(self):
        return render_template("login.html")
    
    def encerrar(self):
        session.pop('usuario', None)
        session.pop('admin', None)
        return self.index()


    def erro(self):
        return render_template("erro.html")

    #REMOVER
    def remover_user(self, id):
       self.__dao.remover_user(id)
       flash("Sucesso: User removido com sucesso!", "success")
       return redirect(url_for("user.admin"))
    
    def admin(self):
        if not session.get("admin"):
            flash("Acesso negado", "danger")
            return redirect(url_for("user.index"))
        users = self.__dao.carregar_user()
        no_admin = []
        for user in users:
            if user.email != 'admin@gmail.com':
                no_admin.append(user)
        return render_template("admin.html", users=no_admin)
    
    def creditos(self):
        return render_template("creditos.html")