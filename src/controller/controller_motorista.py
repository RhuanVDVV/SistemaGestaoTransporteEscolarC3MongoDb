import pandas as pd
from bson import ObjectId
from conexion.mongo_queries import MongoQueries

from reports.relatorios import Relatorio

from model.motoristas import Motorista
from controller.controller_escola import Controller_Escola

from model.escolas import Escola




class Controller_Motorista:
    def __init__(self):
        self.ctrl_escola = Controller_Escola()
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()


    def inserir_motorista(self) -> Motorista:
        self.mongo.connect()


        # Caso nao tenha escola salva na base de dados pede para salvar uma 
        if self.ctrl_escola.get_quant_escolas(True) <= 0:
            print("Insira uma escola na base de dados para cadastrar motorista")
            return None


        # Listar as escolas existentes para inserir nos motoristas

        self.relatorio.get_relatorio_escolas()

        codigo_escola = int(input("Entre com o Codigo da Escola: "))
        escola = self.valida_escola(codigo_escola)
        if escola == None:
            return None

        # Solicita  ao usuario o cnpj do Motorista
        cnpj = str(input("Entre com o CNPJ do Motorista: "))

        if self.verifica_existencia_motorista(cnpj):
            # solicita ao usuario o nome do Motorista
            nome = str(input("Entre com o nome do Motorista: "))
            #Solicita ao usuario o Telefone do Motorista
            telefone = str(input("Entre com o telefone do Motorista: "))
            #Solicita ao usuario o email do motorista
            email = str(input("Entre com o email do Motorista: "))
            #Solicita ao usuario a conta do motorista
            conta = str(input("Entre com a conta do Motorista: "))
            #Insere e persite o novo motorista
            data = dict(cnpj= cnpj, nome =nome, telefone = telefone, email = email,conta = conta, codigo_escola = int(escola.get_codigo_escola()))
            
            
            self.mongo.db["motoristas"].insert_one(data)

            # Recupera os dados do Novo Motorista criado transformando em um data Frame

            df_motorista = self.recupera_motorista(cnpj)

            #Cria um novo objeto de motorista
            novo_motorista = Motorista(df_motorista.cnpj.values[0], df_motorista.nome.values[0], df_motorista.telefone.values[0], df_motorista.email.values[0], df_motorista.conta.values[0], escola)
            print(novo_motorista.to_string())
            print("Motorista adicionado com sucesso!")
            self.mongo.close()
            return novo_motorista
        


        else:
            self.mongo.close()
            print(f"O CNPJ {cnpj} já está cadastrado")
            return None


    def atualizar_motorista(self) -> Motorista:
        self.mongo.connect()
            
        cnpj = str(input("Entre com o CNPJ do motorista que irá alterar: "))

        if not self.verifica_existencia_motorista(cnpj):
            self.relatorio.get_relatorio_escolas()
            codigo_escola = int(input("Entre com o Codigo da Escola: "))
            escola = self.valida_escola(codigo_escola)
            if escola == None:
                return None
            
            # solicita ao usuario o nome do Motorista
            nome = str(input("Entre com o nome do Motorista: "))

            #Solicita ao usuario o Telefone do Motorista
            telefone = str(input("Entre com o telefone do Motorista: "))

            #Solicita ao usuario o email do motorista
            email = str(input("Entre com o email do Motorista: "))

            #Solicita ao usuario a conta do motorista
            conta = str(input("Entre com a conta do Motorista: "))

            # Atualiza os dados do motorista existente
            self.mongo.db["motoritas"].update_one({"cnpj": f"{cnpj}"}, 
                                                    {"$set": 
                                                        {"cnpj" : cnpj, 
                                                         "nome" : nome,
                                                         "telefone": telefone,
                                                         "email": email,
                                                         "conta": conta,
                                                         "codigo_escola": int(escola.get_codigo_escola())
                                                        }
                                                 })
            
            
            # Recupera os novos dados do motorista transformand oem um dataframe
            df_motorista = self.recupera_motorista(cnpj)


            #cria um novo objeto de motorista

            motorista_atualizado = Motorista(df_motorista.cnpj.values[0], df_motorista.nome.values[0], df_motorista.telefone.values[0], df_motorista.email.values[0], df_motorista.conta.values[0], escola)
            
            print(motorista_atualizado.to_string())
            print("Motorista atualizado com sucesso!")
            self.mongo.close()
            return motorista_atualizado
        else:
            self.mongo.close()
            print(f"O CNPJ {cnpj} não existe")


    def excluir_motorista(self):
        self.mongo.connect()
        cnpj = input("CNPJ do motorista que irá excluir: ")

        if not self.verifica_existencia_motorista(cnpj):
            opcao_excluir = str(input(f"Tem certeza que deseja excluir o Motorista de CNPJ {cnpj}? [S ou N]: ")).lower()

            if opcao_excluir == "s":
                print("Caso o Motorista possua peruas estas também serão excluídas!")
                opcao_excluir = str(input(f"Tem certeza que deseja excluir o motorista de CNPJ {cnpj}? [S ou N]: ")).lower()
                if opcao_excluir.lower() == "s":


                    df_motorista = self.recupera_motorista(cnpj)
                    escola = self.valida_escola(int(df_motorista.codigo_escola.values[0]))
                    self.mongo.db["peruas"].delete_many({"cnpj":f"{cnpj}"})
                    print("Peruas do motorista excluidas com sucesso")

                    self.mongo.db["motoristas"].delete_one({"cnpj": f"{cnpj}"})


                    motorista_removido = Motorista(df_motorista.cnpj.values[0], df_motorista.nome.values[0], df_motorista.telefone.values[0], df_motorista.email.values[0], df_motorista.conta.values[0], escola)
                    self.mongo.close()
                    print("Motorista removido com sucesso! Caso o motorista possua Peruas, estas também foram excluídas! ")
                    print(motorista_removido.to_string())

        
        else:
            self.mongo.close()
            print(f"O CNPJ {cnpj} não existe")

    

    def get_quant_motoristas(self, external:bool = False) -> int:
        if external:
            self.mongo.connect()
        quant_motoristas = len(list(self.mongo.db["motoristas"].find()))
        if external:
            self.mongo.close()

        return quant_motoristas


    def recupera_motorista(self, cnpj:str = None, external:bool = False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        df_motorista = pd.DataFrame(list(self.mongo.db["motoristas"].find({"cnpj": f"{cnpj}"}, {"cnpj":1, "nome": 1, "telefone": 1, "email":1, "conta" :1, "codigo_escola":1, "_id":0})))
        if external:
            self.mongo.connect()
        return df_motorista

    

    def verifica_existencia_motorista(self, cnpj:str = None, external: bool = False) -> bool:
        if external:
            self.mongo.connect()
        df_motorista = pd.DataFrame(self.mongo.db["motoristas"].find({"cnpj": f"{cnpj}"}, {"cnpj":1, "nome":1, "telefone":1,"email":1, "conta":1, "codigo_escola":1,"_id":1}))
        return df_motorista.empty
    


    def valida_escola(self, codigo_escola:int = None) -> Escola:

        if self.ctrl_escola.verifica_existencia_escola(int(codigo_escola), external = True):
            print(f"O Codigo da Escola {codigo_escola} informado não existe na base de dados")
            return None
        else:
            
            df_escola = self.ctrl_escola.recupera_escola_codigo(int(codigo_escola), external= True)
            escola = Escola(int(df_escola.codigo_escola.values[0]), df_escola.nome.values[0],df_escola.cidade.values[0], df_escola.bairro.values[0], df_escola.logradouro.values[0], df_escola.telefone.values[0])
            return escola
        


