import json
import os
from .models import User
import mysql.connector


class UserDAO:

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


    def carregar_user(self):
        sql = "SELECT id, Email, Senha FROM Usuario"
        lista_user = []

        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql)
            for linha in cursor.fetchall():
                user = User(
                    linha["Email"],
                    linha["Senha"],
                    linha["id"]
                )
                lista_user.append(user)
        finally:
            cursor.close()
            conexao.close()

        return lista_user

    def salvar_user(self, novo_user):
        sql = """
        INSERT INTO Usuario (Email, Senha)
        VALUES (%s, %s)
        """
        valores = (
            novo_user.email,
            novo_user.senha
        )

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
            conexao.commit()
            novo_user.id = cursor.lastrowid
        finally:
            cursor.close()
            conexao.close()

        return novo_user.id

    def buscar_user_por_id(self, user_id):
        user = self.carregar_user()
        for usuario in user:
            if usuario.id == user_id:
                return usuario
        return None


    def atualizar_user(self, useratt):
        sql = """
        UPDATE Usuarios
        SET Titulo = %s,
            Email = %s,
            Senha = %s,
        WHERE id = %s
        """

        val = (
            useratt.email,
            useratt.senha,
            useratt.id
        )

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, val)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def remover_user(self, id_jogo):
        sql = "DELETE FROM Jogos WHERE id = %s"

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, (id_jogo,))
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

