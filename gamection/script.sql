USE games_db;
CREATE TABLE IF NOT EXISTS Jogos(
	id INT auto_increment PRIMARY KEY,
    Titulo VARCHAR(50),
    Desenvolvedora VARCHAR (50),
    Data_lanc DATE,
    Genero VARCHAR(50),
    Sinopse VARCHAR (1000),
    Plataformas VARCHAR (50),
    Imagem LONGBLOB ,
    Categoria VARCHAR (50)
);