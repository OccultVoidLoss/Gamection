class User:

    def __init__(self, email, senha, id=None):
        self.__email = email
        self.__senha = senha
        self.__id = id
    
    def to_dict(self):
        return {
            "email": self.email,
            "senha": self.senha,
            "id":self.id
        }
    

    @property
    def email(self):
        return (self.__email)
    
    
    @email.setter
    def email(self, valor):
        self.__email = valor


    @property 
    def senha(self):
        return self.__senha
    
    @senha.setter
    def dev(self, valor):
        self.__senha = (valor)

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, v):
        self.__id = (v)
    
    

