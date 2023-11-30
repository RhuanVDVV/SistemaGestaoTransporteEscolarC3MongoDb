import pandas as pd
from bson import ObjectId
from conexion.mongo_queries import MongoQueries

from reports.relatorios import Relatorio



from model.alunos import Aluno
from model.escolas import Escola
from model.responsaveis import Responsavel
from controller.controller_escola import Controller_Escola
from controller.controller_responsavel import Controller_Responsavel



class Controller_Aluno:
    def __init__(self):
        self.ctrl_escola = Controller_Escola()
        self.ctrl_responsavel = Controller_Responsavel()
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()

    
    def inserir_aluno(self) -> Aluno:
        
        #Cria uma nova conexao com o banco
        self.mongo.connect()


        # Caso nao tenha nenhuma escola salva no sistema pede para salvar uma

        if self.ctrl_escola.get_quant_escolas(external=True) <= 0:
            print("Insira uma escola na base de dados antes de cadastrar aluno")
            return None
        # Lista as Escolas existentes para inserir no aluno
        self.relatorio.get_relatorio_escolas()
        codigo_escola= int(input("Entre com o Codigo da Escola do Aluno: "))
        escola = self.valida_escola(codigo_escola)
        if escola == None:
            return None
        

        # Caso nao tenha nenhum responsavel salvo no ssitema, pede para salvar um

        if self.ctrl_responsavel.get_quant_responsaveis(True) <= 0:
            print("Insira um Responsavel na base de dados antes de cadastrar aluno")
            return None

        #Lista os responsaveis existentes para inserir no aluno
        self.relatorio.get_relatorio_responsaveis()       
        cpf = str(input("Entre com o CPF do Responsavel do Aluno: "))
        responsavel = self.valida_responsavel(cpf)
        if responsavel == None:
            return None
        

        # Procura pelo proximo codigo do aluno
        proximo_aluno = self.mongo.db["alunos"].aggregate([
                                                            {
                                                                '$group':{
                                                                    '_id': '$alunos',
                                                                    'proximo_aluno':{
                                                                        '$max':'$codigo_aluno'
                                                                    }
                                                                }
                                                            }, {
                                                                '$project':{
                                                                    'proximo_aluno':{
                                                                        '$sum':[
                                                                            '$proximo_aluno',1
                                                                        ]
                                                                    },
                                                                    '_id':0
                                                                }
                                                            }


                                                         ])

        
        if list(proximo_aluno) == []:
            proximo_aluno = 1
        else:
            proximo_aluno = int(list(proximo_aluno)[0]['proximo_aluno'])
        
        #Solicita o nome do Aluno

        nome = str(input("Entre com o nome do aluno: "))
        # Solicita a matricula do ALuno
        matricula = str(input("Entre com a matricula do aluno: "))
        #Solicita a turma do aluno
        turma = str(input("Entre com a turma do Aluno: "))

        #Solicita o Horario das AUlas do ALuno:
        horario_aula = str(input("Entre com o horario de aula do aluno: "))
        
        # Cria um dicionario para mapear as varaiveis de entrada e saida
        data = dict(codigo_aluno=int(proximo_aluno), cpf = str(responsavel.get_CPF()), codigo_escola = int(escola.get_codigo_escola()), horario_aula = horario_aula, nome= nome, turma = turma, matricula = matricula)

        # Insere e recuper ao codigo do novo aluno
        id_aluno = self.mongo.db["alunos"].insert_one(data)
        #Recupera os dados do novo aluno criado transformando em um DataFrame
        df_aluno = self.recupera_aluno(id_aluno.inserted_id)
        #Cria um novo objeto Aluno
        novo_aluno=Aluno(df_aluno.codigo_aluno.values[0], df_aluno.horario_aula.values[0],df_aluno.nome.values[0], df_aluno.turma.values[0], df_aluno.matricula.values[0],escola,responsavel)

        print(novo_aluno.to_string())
        print("Aluno adicionado com sucesso")
        self.mongo.close()
        return novo_aluno
    

    def atualizar_aluno(self) -> Aluno:
        # Cria uma nova conexao com o banco que permite alteraçãop

        self.mongo.connect()
        
        codigo_aluno = int(input("Entre com o Código do Aluno que irá alterar: "))

        if not self.verifica_existencia_aluno(codigo_aluno):
           # Lista as Escolas existentes para inserir no aluno
            self.relatorio.get_relatorio_escolas()
            codigo_escola= int(input("Entre com o Codigo da Escola do Aluno: "))
            escola = self.valida_escola(codigo_escola)
            if escola == None:
                return None
        

            #Lista os responsaveis existentes para inserir no aluno
            self.relatorio.get_relatorio_responsaveis()
            
            cpf = str(input("Entre com o CPF do Responsavel do Aluno: "))
            responsavel = self.valida_responsavel(cpf)
            if responsavel == None:
                return None
            

            #Solicita o nome do Aluno

            nome = str(input("Entre com o nome do aluno: "))
            # Solicita a matricula do ALuno
            matricula = str(input("Entre com a matricula do aluno: "))
            #Solicita a turma do aluno
            turma = str(input("Entre com a turma do Aluno: "))

            #Solicita o Horario das AUlas do ALuno:
            horario_aula = str(input("Entre com o horario de aula do aluno: "))
            
            self.mongo.db["alunos"].update_one({"codigo_aluno":codigo_aluno},
                                               {"$set": {"codigo_escola": int(escola.get_codigo_escola()),
                                                         "cpf": str(responsavel.get_CPF()),
                                                         "horario_aula": horario_aula,
                                                         "nome": nome,
                                                         "turma": turma,
                                                         "matricula": matricula
                                                   
                                                        }

                                               })

            
            df_aluno_atualizado = self.recupera_aluno_codigo(codigo_aluno)

            #cria um novo objeto de ALuno
            aluno_atualizado = Aluno(df_aluno_atualizado.codigo_aluno.values[0],df_aluno_atualizado.horario_aula.values[0], df_aluno_atualizado.nome.values[0], df_aluno_atualizado.turma.values[0], df_aluno_atualizado.matricula.values[0], escola, responsavel)
            
            print(aluno_atualizado.to_string())
            print("Aluno atualizado com sucesso!")
            self.mongo.close()
            return aluno_atualizado

        else:
            print(f"O Codigo do Aluno {codigo_aluno} não existe")
            self.mongo.close()
            return None

    def excluir_aluno(self):
        self.mongo.connect()

        codigo_aluno = int(input("Entre com o Código do Aluno que irá excluir: "))

        if not self.verifica_existencia_aluno(codigo_aluno):
            df_aluno = self.recupera_aluno_codigo(codigo_aluno)
            responsavel = self.valida_responsavel(str(df_aluno.cpf.values[0]))
            escola = self.valida_escola(int(df_aluno.codigo_escola.values[0]))


            self.mongo.db["alunos"].delete_one({"codigo_aluno": codigo_aluno})

            aluno_excluido = Aluno(df_aluno.codigo_aluno.values[0],df_aluno.horario_aula.values[0], df_aluno.nome.values[0], df_aluno.turma.values[0], df_aluno.matricula.values[0], escola, responsavel)

            print("Aluno removido com sucesso!")

            print(aluno_excluido.to_string())
            self.mongo.close()


        else:
            print(f"O Codigo do Aluno {codigo_aluno} não existe")
            self.mongo.close()


    def verifica_existencia_aluno(self, codigo:int =None, external: bool = False) -> bool:
        if external:
            self.mongo.connect()
        
        df_aluno = self.recupera_aluno_codigo(codigo, external)
        if external:
            self.mongo.close()
        return df_aluno.empty
    

    def recupera_aluno(self, _id:ObjectId = None) -> pd.DataFrame:
        df_aluno = pd.DataFrame(list(self.mongo.db["alunos"].find({"_id" : _id}, {"codigo_aluno": 1,"codigo_escola":1,"cpf":1, "horario_aula" : 1, "nome":1, "turma":1, "matricula":1,"_id":1})))
        return df_aluno
    def recupera_aluno_codigo(self, codigo_aluno:int = None, external: bool = False) -> pd.DataFrame:
        if external:
            self.mongo.connect()
        df_aluno = pd.DataFrame(list(self.mongo.db["alunos"].find({"codigo_aluno" : codigo_aluno}, {"codigo_aluno": 1,"codigo_escola":1,"cpf":1, "horario_aula" : 1, "nome":1, "turma":1, "matricula":1,"_id":1})))
        if external:
            self.mongo.close()
        return df_aluno
    

    
     


    def valida_escola(self, codigo_escola:int = None) -> Escola:
        if self.ctrl_escola.verifica_existencia_escola(codigo_escola, external= True):
            print(f"A escola com codigo {codigo_escola} não existe na base")
            return None
        else:
            df_escola = self.ctrl_escola.recupera_escola_codigo(codigo_escola, external=True)
            escola = Escola(df_escola.codigo_escola.values[0], df_escola.nome.values[0], df_escola.cidade.values[0], df_escola.bairro.values[0], df_escola.logradouro.values[0], df_escola.telefone.values[0])
            return escola
    
    def valida_responsavel(self, cpf:str = None ) -> Responsavel:
        if self.ctrl_responsavel.verifica_existencia_responsavel(cpf, external= True):
            print(f"O responsável com cpf {cpf} informado não existe na base")
            return None
        else:
            # Recupera os dados do novo fornecedor criado transformando em um DataFrame
            df_responsavel = self.ctrl_responsavel.recupera_responsavel(cpf,external= True)

            #Cria um novo objeto do Responsavel
            
            responsavel = Responsavel(df_responsavel.cpf.values[0] , df_responsavel.nome[0], df_responsavel.cidade[0], df_responsavel.bairro[0], df_responsavel.logradouro[0], df_responsavel.telefone[0], df_responsavel.email[0], df_responsavel.numero[0], df_responsavel.complemento[0])
            return responsavel