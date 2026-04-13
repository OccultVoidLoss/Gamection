USE games_db;
CREATE TABLE IF NOT EXISTS Jogos(
	id INT auto_increment PRIMARY KEY,
    Titulo VARCHAR(50),
    Desenvolvedora VARCHAR (50),
    Data_lanc DATE,
    Genero VARCHAR(50),
    Sinopse VARCHAR (1000),
    Plataformas VARCHAR (50),
    Imagem VARCHAR(1000) 
);

CREATE TABLE IF NOT EXISTS Usuario(
		id INT auto_increment PRIMARY KEY,
		Email VARCHAR(50),
        Senha VARCHAR(50)
);

select * from usuario;
drop table comentarios; 

CREATE TABLE IF NOT EXISTS Comentarios(
		Id INT auto_increment PRIMARY KEY,
		Autor VARCHAR(50),
        Comentario VARCHAR(1000),
        Id_autor INT,
		FOREIGN KEY (Id_autor) REFERENCES Usuario(id),
        Id_jogo INT,
        FOREIGN KEY (Id_jogo) REFERENCES Jogos (id)
        
);




CREATE TABLE IF NOT EXISTS Categorias(
		Id INT auto_increment PRIMARY KEY,
        Nome VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Jogo_categoria(
		Id_jogo INT NOT NULL,
		Id_categoria INT NOT NULL,
        PRIMARY KEY (Id_jogo, Id_categoria),
		FOREIGN KEY (Id_jogo) REFERENCES Jogos(id),
		FOREIGN KEY (Id_categoria) REFERENCES Categorias(id)
	
);
INSERT INTO Categorias (id, nome) VALUES
(1, 'Ação'),
(2, 'Aventura'),
(3, 'RPG'),
(4, 'Estratégia'),
(5, 'FPS'),
(6, 'Simulação'),
(7, 'Esportes'),
(8, 'Puzzle'),
(9, 'Promoção'),
(10, 'Destaque');

DROP TABLE Categorias;
DROP TABLE Jogo_categoria;

