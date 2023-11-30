from model.escolas import Escola
from model.responsaveis import Responsavel

class Aluno:
    def __init__(self, 
                 codigo_aluno:int = None,
                 horario_aula:str = None,
                 nome:str = None,
                 turma:str = None,
                 matricula:str = None,
                 escola:Escola = None,
                 responsavel:Responsavel = None
                 ):
        self.set_codigo_aluno(codigo_aluno)
        self.set_horario_aula(horario_aula)
        self.set_nome(nome)
        self.set_turma(turma)
        self.set_matricula(matricula)
        self.set_escola(escola)
        self.set_responsavel(responsavel)

    

    def set_codigo_aluno(self, codigo_aluno:int):
        self.codigo_aluno = codigo_aluno

    def set_horario_aula(self, horario_aula:str):
        self.horario_aula = horario_aula

    def set_nome(self, nome:str):
        self.nome = nome

    def set_turma(self , turma:str):
        self.turma = turma
    
    def set_matricula(self, matricula:str):
        self.matricula = matricula

    def set_escola(self, escola:Escola):
        self.escola = escola

    def set_responsavel(self, responsavel:Responsavel):
        self.responsavel = responsavel



    def get_codigo_aluno(self) -> int :
        return self.codigo_aluno

    def get_horario_aula(self) -> str:
        return self.horario_aula
    def get_nome(self) -> str:
        return self.nome

    def get_turma(self) -> str:
        return self.turma
    
    def get_matricula(self) -> str :
        return self.matricula

    def get_escola(self ) -> Escola:
        return self.escola 

    def get_responsavel(self) -> Responsavel:
        return self.responsavel
    
    def to_string(self):
        print(f"Aluno: {self.get_codigo_aluno()} | Nome: {self.get_nome()} | Matricula: {self.get_matricula()} | Horario de Aula: {self.get_horario_aula()} | Turma: {self.get_turma()} | Escola: {self.get_escola().get_codigo_escola()} | Responsavel: {self.get_responsavel().get_CPF()}")
