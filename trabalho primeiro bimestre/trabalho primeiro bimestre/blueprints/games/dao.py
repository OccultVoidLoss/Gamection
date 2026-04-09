import json
import os
from .models import Jogo
import mysql.connector


class JogoDAO:

    def __init__(self):
        self.__db_config = {
            'host': os.getenv("MYSQL_HOST"),
            'user': os.getenv("MYSQL_USER"),
            'password': os.getenv("MYSQL_PASSWORD"),
            'database': os.getenv("MYSQL_DATABASE"),
            'port': os.getenv("MYSQL_PORT")
        }

    def __get_connection(self):
        return mysql.connector.connect(**self.__db_config)

    @property
    def arquivo_caminho(self):
        return self.__arquivo_caminho

    @arquivo_caminho.setter
    def arquivo_caminho(self, v):
        self.__arquivo_caminho = v


    def carregar_jogos(self):
        sql = "SELECT id, Titulo, Desenvolvedora, Data_lanc, Genero, Sinopse, Plataformas, Imagem,  Categoria FROM Jogos"
        lista_jogos = []

        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql)
            for linha in cursor.fetchall():
                jogo = Jogo(
                    linha["Titulo"],
                    linha["Desenvolvedora"],
                    linha["Data_lanc"],
                    linha["Genero"],
                    linha["Sinopse"],
                    linha["Plataformas"],
                    linha["Imagem"],
                    linha["Categoria"],
                    linha["id"]
                )
                lista_jogos.append(jogo)
        finally:
            cursor.close()
            conexao.close()

        return lista_jogos

    def salvar_jogo(self, novo_jogo):
        sql = """
        INSERT INTO Jogos (Titulo, Desenvolvedora, Data_lanc, Genero, Sinopse, Plataformas ,Imagem, Categoria)
        VALUES (%s, %s, %s, %s, %s, %s,%s,%s)
        """
        valores = (
            novo_jogo.nome,
            novo_jogo.dev,
            novo_jogo.data,
            novo_jogo.genero,
            novo_jogo.sinopse,
            novo_jogo.plat,
            novo_jogo.img,
            novo_jogo.categoria
        )

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
            conexao.commit()
            novo_jogo.id = cursor.lastrowid
        finally:
            cursor.close()
            conexao.close()

        return novo_jogo.id

    def buscar_jogo_por_id(self, id_jogo):
        jogos = self.carregar_jogos()
        for jogo in jogos:
            if jogo.id == id_jogo:
                return jogo
        return None


    def atualizar_jogo(self, jogoatt):
        sql = """
        UPDATE Jogos
        SET Titulo = %s,
            Desenvolvedora = %s,
            Data_lanc = %s,
            Genero = %s,
            Sinopse = %s,
            Categoria = %s
        WHERE id = %s
        """

        val = (
            jogoatt.nome,
            jogoatt.dev,
            jogoatt.data,
            jogoatt.genero,
            jogoatt.sinopse,
            jogoatt.categoria,
            jogoatt.id
        )

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, val)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def remover_jogo(self, id_jogo):
        sql = "DELETE FROM Jogos WHERE id = %s"

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, (id_jogo,))
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

