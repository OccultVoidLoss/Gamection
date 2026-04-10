from flask import render_template, request, redirect, url_for, flash, session
import os
from .dao import JogoDAO
from .models import Jogo
from werkzeug.utils import secure_filename


class JogoController:

    def __init__(self):
        self.__dao = JogoDAO()

    # LISTAR
    def listar_jogos(self):
        if 'usuário' not in session:
            flash("Erro: deve estar logado para essa função", "danger")
            return redirect(url_for("user.erro"))
        else:
            lista = self.__dao.carregar_jogos()
            return render_template("jogos.html", jogos=lista)

    # CADASTRAR
    def cadastrar_jogo(self):
            dir = "static/uploads"
            nome = request.form.get("nome")
            dev = request.form.get("dev")
            data = request.form.get("data")
            genero = request.form.get("genero")
            sinopse = request.form.get("sinopse")
            categoria = request.form.get("categoria")
            img = request.files.get("img")
            plat = request.form.get("plataforma")

            if not nome or not dev or not data or not genero or not categoria or not img or not plat or img.filename == "":
                flash("Erro: Preencha todos os campos obrigatórios!", "danger")
                return self.preparar_cadastro()

            try:
                filename = secure_filename(img.filename)
                caminho = os.path.join(dir, filename)
                novo_jogo = Jogo(
                    nome,
                    dev,
                    data,
                    genero,
                    sinopse,
                    plat,
                    filename,
                    categoria
                )

                self.__dao.salvar_jogo(novo_jogo)
                img.save(caminho)

                flash(f"Sucesso: O jogo '{nome}' foi cadastrado!", "success")
                return redirect(url_for("games.listar_jogos"))
            

            except Exception as e:
                flash(f"Erro ao cadastrar jogo: {str(e)}", "danger")
                return self.preparar_cadastro()

    def preparar_cadastro(self):
        if 'usuário' not in session:
            flash("Erro: deve estar logado para essa função", "danger")
            return redirect(url_for("user.erro"))
        else:
            return render_template("cadastrar.html")

    # PREPARAR EDIÇÃO
    def preparar_edicao(self, id):
        if 'usuário' not in session:
            flash("Erro: deve estar logado para essa função", "danger")
            return redirect(url_for("user.erro"))
        else:
            jogo = self.__dao.buscar_jogo_por_id(id)

            if not jogo:
                flash("Erro: Jogo não encontrado!", "danger")
                return redirect(url_for("games.listar_jogos"))

            return render_template("editar.html", jogo=jogo)

    # EDITAR
    def editar_jogo(self, id):
        nome = request.form.get("nome")
        dev = request.form.get("dev")
        data = request.form.get("data")
        genero = request.form.get("genero")
        sinopse = request.form.get("sinopse")
        img = request.form.get("img")
        plat = request.form.get("plataforma")
        categoria = request.form.get("categoria")

        if not nome or not dev or not data or not genero or not categoria or not plat or not img:
            flash("Erro: Preencha todos os campos obrigatórios!", "danger")
            return redirect(url_for("games.editar_jogo", id=id))

        try:
            jogo_atualizado = Jogo(
                nome,
                dev,
                data,
                genero,
                sinopse,
                plat,
                img,
                categoria,
                id
            )

            self.__dao.atualizar_jogo(jogo_atualizado)

            flash(f"Sucesso: O jogo '{nome}' foi atualizado!", "success")
            return redirect(url_for("games.listar_jogos"))

        except Exception as e:
            flash(f"Erro ao atualizar jogo: {str(e)}", "danger")
            return redirect(url_for("games.editar_jogo", id=id))

    # REMOVER
    def remover_jogo(self, id):
        self.__dao.remover_jogo(id)
        flash("Sucesso: Jogo removido com sucesso!", "success")
        return redirect(url_for("games.listar_jogos"))
    

    def index(self):
        return render_template("index.html")