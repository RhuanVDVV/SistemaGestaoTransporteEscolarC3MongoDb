class Escola:
    def __init__(self,
                codigo_escola:int = None,
                nome:str = None,
                cidade:str = None,
                bairro:str = None,
                logradouro:str = None,
                telefone:str = None
                ):
        self.set_codigo_escola(codigo_escola)
        self.set_nome(nome)
        self.set_cidade(cidade)
        self.set_bairro(bairro)
        self.set_logradouro(logradouro)
        self.set_telefone(telefone)

    def set_codigo_escola(self, codigo_escola:int):
        self.codigo_escola = codigo_escola
    
    def set_nome(self, nome:str):
        self.nome = nome

    def set_cidade(self, cidade:str):
        self.cidade = cidade

    def set_bairro(self, bairro:str):
        self.bairro = bairro

    def set_logradouro(self, logradouro:str):
        self.logradouro = logradouro

    def set_telefone(self, telefone:str):
        self.telefone = telefone

    def get_codigo_escola(self) -> int:
        return self.codigo_escola
    
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
    
    def to_string(self):
        return f"Codigo Escola: {self.get_codigo_escola()} | Nome: {self.get_nome()} | Endereço : {self.get_logradouro() + self.get_bairro() +  self.get_cidade()} | Telefone: {self.get_telefone()}" 