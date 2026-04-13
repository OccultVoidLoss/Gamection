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
        sql = "SELECT id, Titulo, Desenvolvedora, Data_lanc, Genero, Sinopse, Plataformas, Imagem FROM Jogos"
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
                    None,
                    linha["id"]
                )
                lista_jogos.append(jogo)
        finally:
            cursor.close()
            conexao.close()

        return lista_jogos

    def salvar_jogo(self, novo_jogo, categorias):
        sql = """
        INSERT INTO Jogos (Titulo, Desenvolvedora, Data_lanc, Genero, Sinopse, Plataformas ,Imagem)
        VALUES (%s, %s, %s, %s, %s, %s,%s)
        """
        valores = (
            novo_jogo.nome,
            novo_jogo.dev,
            novo_jogo.data,
            novo_jogo.genero,
            novo_jogo.sinopse,
            novo_jogo.plat,
            novo_jogo.img
        )

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
            
            novo_jogo.id = cursor.lastrowid

            for id_categoria in categorias:
                cursor.execute(
                    "INSERT INTO Jogo_categoria (id_jogo, id_categoria) VALUES (%s, %s)",
                    (novo_jogo.id, id_categoria)
                )
            conexao.commit()
                                                            

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
            Plataformas = %s,
            Imagem = %s
        WHERE id = %s
        """

        val = (
            jogoatt.nome,
            jogoatt.dev,
            jogoatt.data,
            jogoatt.genero,
            jogoatt.sinopse,
            jogoatt.plat,
            jogoatt.img,
            jogoatt.id
        )

        conexao = self.__get_connection()
        cursor = conexao.cursor()
        categorias = jogoatt.cat
        if type(categorias) != list:
            categorias = [categorias]

        try:
            cursor.execute(sql, val)
            cursor.execute("DELETE FROM Jogo_categoria where id_jogo = %s", (jogoatt.id,))
            for id_categoria in categorias:
                cursor.execute("INSERT INTO Jogo_categoria (id_jogo, id_categoria) VALUES (%s, %s)", (jogoatt.id, id_categoria))
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def remover_jogo(self, id_jogo):
        sql = "DELETE FROM Jogos WHERE id = %s"
        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)


        try:
            cursor.execute("SELECT Imagem FROM Jogos WHERE id = %s", (id_jogo,))
            resultado = cursor.fetchone()
            imagem = resultado["Imagem"]
            cursor.execute("DELETE FROM Comentarios WHERE Id_jogo = %s", (id_jogo,))
            cursor.execute("DELETE FROM Jogo_Categoria WHERE id_jogo = %s", (id_jogo,))
            cursor.execute(sql, (id_jogo,))
            if imagem:
                caminho = os.path.join("static/uploads",imagem)
                os.remove(caminho)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def enviar_comentario(self, autor, comentario, id_autor, Id_jogo):
        sql = """
                INSERT INTO Comentarios (Autor, Comentario, Id_autor, Id_jogo)
                VALUES (%s, %s, %s, %s)
                """
        val = (autor, comentario, id_autor, Id_jogo)


        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, val)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def selecionar_comentario(self, Id_jogo ):
        sql = """
            SELECT c.Id, c.Comentario, u.Email, c.Id_autor
            FROM Comentarios c
            JOIN Usuario u ON c.id_autor = u.id
            WHERE c.Id_jogo = %s                 
            """
        conexao = self.__get_connection()
        cursor = conexao.cursor()
        try: 
            cursor.execute(sql, (Id_jogo,))
            resultado = cursor.fetchall()  
        finally: 
            cursor.close()
            conexao.close()
        return resultado 
    
    def excluir_comentario(self, id_comentario):
        sql = """
            DELETE FROM Comentarios
            WHERE Id = %s
            """
        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, (id_comentario,))
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()


    def bc(self, id_jogo):
            sql = """
                SELECT c.nome
                FROM Categorias c
                JOIN Jogo_Categoria jc ON c.id = jc.id_categoria
                WHERE jc.id_jogo = %s
            """

            conexao = self.__get_connection()
            cursor = conexao.cursor()

            try:
                cursor.execute(sql, (id_jogo,))
                resultado = cursor.fetchall()
                return resultado
            finally:
                cursor.close()
                conexao.close()

    def recentes(self):
        sql = "SELECT * FROM Jogos WHERE YEAR(Data_lanc) >= 2020 ORDER BY Data_lanc DESC"
        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)
        lista =[]
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
                    None,
                    linha["id"]
                )
                lista.append(jogo)
            return lista
        finally:
            cursor.close()
            conexao.close()
    
    def buscar_jogo_por_categoria(self, categoria):
        sql = " SELECT j.* FROM Jogos j JOIN Jogo_categoria jc ON j.id = jc.id_jogo JOIN Categorias c ON c.id = jc.id_categoria WHERE c.nome = %s"
        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)
        lista = []
        try:
            cursor.execute(sql, (categoria,))
            for linha in cursor.fetchall():
                jogo = Jogo(
                    linha["Titulo"],
                    linha["Desenvolvedora"],
                    linha["Data_lanc"],
                    linha["Genero"],
                    linha["Sinopse"],
                    linha["Plataformas"],
                    linha["Imagem"],
                    None,
                    linha["id"]
                )
                lista.append(jogo)
            return lista
            
        finally:
            cursor.close()
            conexao.close()