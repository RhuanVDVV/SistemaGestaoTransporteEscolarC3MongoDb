from model.escolas import Escola
class Motorista:
    def __init__(self,
                 CNPJ:str = None,
                 nome:str = None,
                 telefone:str = None,
                 email:str = None,
                 conta:str = None,
                 escola:Escola = None):
            self.set_CNPJ(CNPJ)
            self.set_nome(nome)
            self.set_telefone(telefone)
            self.set_email(email)
            self.set_conta(conta)
            self.set_escola(escola)
            

    def set_CNPJ(self, CNPJ:str):
          self.CNPJ = CNPJ
    
    def set_nome(self, nome:str):
          self.nome = nome

    def set_telefone(self, telefone:str):
          self.telefone = telefone

    def set_email(self, email:str):
          self.email = email

    def set_conta(self, conta:str):
          self.conta = conta

    def set_escola(self, escola:Escola):
          self.escola = escola

   

    def get_CNPJ(self) -> str:
          return self.CNPJ
    
    def get_nome(self) -> str:
          return self.nome
    
    def get_telefone(self) -> str:
          return self.telefone
    
    def get_email(self) -> str:
          return self.email
    

    def get_conta(self) -> str:
          return self.conta
    
    def get_escola(self) -> Escola:
          return self.escola
    
    def to_string(self):
          return f"CNPJ: {self.get_CNPJ()} | Nome: {self.get_nome()} | Telefone: {self.get_telefone()} | Email: {self.get_telefone()} | Conta: {self.get_conta()} | Escola: {self.get_escola().get_codigo_escola()}"