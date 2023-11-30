class Responsavel:
    def __init__(self, 
                 CPF:str = None, 
                 nome:str = None, 
                 cidade:str = None, 
                 bairro:str = None, 
                 logradouro:str = None, 
                 numero:str = None,
                 complemento:str = None,
                 telefone:str = None, 
                 email:str = None):
        self.set_CPF(CPF)
        self.set_nome(nome)
        self.set_cidade(cidade)
        self.set_bairro(bairro)
        self.set_logradouro(logradouro)
        self.set_telefone(telefone)
        self.set_email(email)
        self.set_numero(numero)
        self.set_complemento(complemento)

   


    def set_CPF(self,CPF:str):
        self.CPF = CPF

    def set_nome(self, nome:str):
        self.nome = nome
    
    def set_cidade(self,cidade:str):
        self.cidade = cidade

    def set_bairro(self,bairro:str):
        self.bairro = bairro

    def set_logradouro(self,logradouro:str):
        self.logradouro = logradouro
    def set_telefone(self,telefone:str):
        self.telefone = telefone
    def set_email(self, email:str):
        self.email = email

    def set_numero(self, numero:str):
        self.numero = numero

    def set_complemento(self, complemento:str):
        self.complemento = complemento

    def get_CPF(self) -> str:
        return self.CPF

    def get_nome(self) -> str:
        return self.nome
    
    def get_cidade(self) -> str:
        return self.cidade

    def get_bairro(self) -> str:
        return self.bairro

    def get_logradouro(self) -> str:
        return self.logradouro
    def get_telefone(self) -> str:
        return self.telefone
    def get_email(self) -> str:
        return self.email
    
    def get_numero(self) -> str:
        return self.numero

    def get_complemento(self) -> str:
        return self.complemento

    def to_string(self) -> str:
        return f"CPF {self.get_CPF()} | Nome: {self.get_nome()} | Endereço : {self.get_logradouro() + self.get_numero() + self.get_bairro() +  self.get_cidade()}  | Complemento: {self.get_complemento()} | Telefone: {self.get_telefone()} | Email: {self.get_email()}"

    