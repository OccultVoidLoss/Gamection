from flask import Flask, render_template, request, redirect, url_for, flash
from . import user_bp
from .controllers import UserController



controller = UserController()



@user_bp.route("/cadastro", methods=["GET", "POST"])
def cadastrar_user():
    if request.method == "POST":
        return controller.cadastrar_user()

    return controller.preparar_cadastro()

@user_bp.route("/")
def index():
    return controller.index()


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return controller.login()

    return controller.preparar_login()

@user_bp.route("/sair", methods=["POST", "GET"])
def sair():
    return controller.encerrar()


#@user_bp.route("/editar/<int:id>", methods=["GET", "POST"])
#def editar_jogo(id):
#    if request.method == "POST":
#        return controller.editar_jogo(id)
#    return controller.preparar_edicao(id)


#@user_bp.route("/excluir/<int:id>", methods=["POST"])
#def excluir_livro(id):
#    return controller.remover_jogo(id)
