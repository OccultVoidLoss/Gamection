class Jogo:

    def __init__(self, nome_jogo, dev_jogo, data_lanc, genero_jogo, sinopse_jogo, plataformas_jogo, imagens_jogo, categoria_jogo, jogo_id=None):
        self.__nome = nome_jogo
        self.__dev = dev_jogo
        self.__data = data_lanc
        self.__genero = genero_jogo
        self.__sinopse = sinopse_jogo
        self.__plat = plataformas_jogo
        self.__img = imagens_jogo
        self.__cat = categoria_jogo
        self.__id = jogo_id

    
    def to_dict(self):
        return {
            "nome": self.nome,
            "dev": self.dev,
            "data": self.data,
            "genero": self.genero,
            "sinopse": self.sinopse,
            "plat": self.plat,
            "img": self.img,
            "categoria": self.cat,
            "id":self.id
        }
    
    #nome
    @property
    def nome(self):
        return str.capitalize(self.__nome)
    
    
    @nome.setter
    def nome(self, valor):
        self.__nome = str.capitalize(valor)

    #desenvolvedora
    @property 
    def dev(self):
        return self.__dev
    
    @dev.setter
    def dev(self, valor):
        self.__dev = (valor)

    #data de lançamento
    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self,valor):
        self.__data = (valor)

    #genero
    @property
    def genero(self):
        return self.__genero
    
    @genero.setter
    def genero(self, v):
        self.__genero = (v)

    #sinopse
    @property
    def sinopse(self):
        return self.__sinopse
    
    @sinopse.setter
    def sinopse(self, v):
        self.__sinopse = (v)

    #plataforma    
    @property
    def plat(self):
        return self.__plat
    
    @plat.setter
    def plat(self, v):
        self.__plat = (v)
    
    #imagens?
    @property
    def img(self):
        return self.__img
    
    @img.setter
    def img(self, v):
        self.__img = (v)

    #categoria
    @property
    def cat(self):
        return self.__cat
    
    @cat.setter
    def cat(self, v):
        self.__cat = (v)

    #id
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, v):
        self.__id = (v)
    
    

