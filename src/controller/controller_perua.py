import pandas as pd
from bson import ObjectId
from conexion.mongo_queries import MongoQueries
from controller.controller_motorista import Controller_Motorista
from model.peruas import Perua
from model.motoristas import Motorista

from reports.relatorios import Relatorio

class Controller_Perua:
    def __init__(self) -> None:
        self.ctrl_motorista = Controller_Motorista()
        self.relatorio = Relatorio()
        self.mongo = MongoQueries()


    def inserir_perua(self) -> Perua:

        self.mongo.connect()

        # Caso nao tenha nenhum motorista salvo na base de dados pede para salvar

        if self.ctrl_motorista.get_quant_motoristas(True) <= 0:
            print("Insira um motorista na base de dados para cadastrar uma perua")
            return None

        # Lista os motoristas existentes para inserir nas peruas
        self.relatorio.get_relatorio_motoristas()   

        cnpj = str(input("Entre com o CNPJ do Motorista: "))
        motorista = self.valida_motorista(cnpj)
        if motorista == None:
            return None
        
        # SOlicita ao usuario a placa da Perua
        placa = str(input("Entre com a placa da Perua: "))

        if self.verifica_existencia_perua(placa):

             # SOlicita ao usuario o modelo da Perua
            modelo = str(input("Entre com o modelo da Perua: "))

            # SOlicita ao usuario a capacidade de pessoa na Perua
            capacidade = str(input("Entre com a capacidade de pessoas na Perua: "))

            # Insere e persiste a nova Perua    
            self.mongo.db["peruas"].insert_one({"placa": placa, "cnpj": motorista.get_CNPJ(), "modelo": modelo, "capacidade":int(capacidade)})

            #Recupera os dados da nova Perua criada transformando em um Data Frame
            df_perua = self.recupera_perua(placa)

            #Cria um novo objeto de perua

            nova_perua = Perua(df_perua.placa.values[0], df_perua.modelo.values[0], df_perua.capacidade.values[0], motorista)


            # Exibe os atributos da nova Perua

            print(nova_perua.to_string())
            print("Perua adicionada com sucesso")
            self.mongo.close()
            return nova_perua

        else:          
            print(f"A Placa {placa} já está cadastrada")
            self.mongo.close()
            return None
        

    def atualizar_perua(self) -> Perua:

        self.mongo.connect()

        placa = input("Placa da Perua que deseja atualizar: ")

        if not self.verifica_existencia_perua(placa):
            # Lista os motoristas existentes para inserir nas peruas
            self.relatorio.get_relatorio_motoristas()
            cnpj = str(input("Entre com o CNPJ do Motorista: "))
            motorista = self.valida_motorista(cnpj)
            if motorista == None:
                return None
            
            # Solicita ao usuario o novo modelo da Perua
            modelo = str(input("Entre com o modelo da Perua: "))

            # Solicita ao usuario a nova capacidade de pessoa na Perua
            capacidade = str(input("Entre com a capacidade de pessoas na Perua: "))
            #Atualiza os dados da perua existente
            self.mongo.db["peruas"].update_one({"placa": f"{placa}"},
                                                {"$set": { "cnpj": f'{motorista.get_CNPJ()}',
                                                            "modelo": modelo,
                                                            "capacidade": int(capacidade)

                                                         }

                                                })

            #Recupera os novos dados da perua transformando em um DataFrame

            df_perua = self.recupera_perua(placa)

            # cria um novo objeto perua 
            perua_atualizada = Perua(df_perua.placa.values[0], df_perua.modelo.values[0], df_perua.capacidade.values[0], motorista)

            print(perua_atualizada.to_string())
            print("Perua atualizada com sucesso")
            self.mongo.close()
            return perua_atualizada
        
        else:
            print(f"A placa {placa} não existe")
            self.mongo.close()
            return None
        

    def excluir_perua(self):
        
        # Cria uma nova conexão com banco que permite alteração
        self.mongo.connect()


        # SOlicita ao usuário a placa da perua que deseja ser excluida
        
        placa = input("Placa da Perua que irá excluir: ")
        # verifica se existe a placa na base de dados
        if not self.verifica_existencia_perua(placa):
            opcao_excluir = input(f"Tem certeza que deseja excluir a perua {placa} [S ou N]: ").lower()
            if opcao_excluir == "s":
                
                
                # Recupera os dados da placa transformada em um dataFrame
                df_perua = self.recupera_perua(placa)
                
                motorista = self.valida_motorista(df_perua.cnpj.values[0])

                self.mongo.db["peruas"].delete_one({"placa": f"{placa}"})
                perua_excluida = Perua(df_perua.placa.values[0], df_perua.modelo.values[0], df_perua.capacidade.values[0], motorista)
                print("Perua excluida com sucesso!")
                print(perua_excluida.to_string())
                self.mongo.close()

        else:
            
            print(f"A Perua de placa {placa} não existe")
            self.mongo.close()



    def verifica_existencia_perua(self, placa:str = None, external:bool = False) -> bool:
        if external:
            self.mongo.connect()
        
        df_perua = pd.DataFrame(self.mongo.db["peruas"].find({"placa":f"{placa}"}, {"cnpj": 1, "modelo" : 1, "capacidade": 1,"_id":0}))

        if external:
            self.mongo.close()

        return df_perua.empty

   
    def recupera_perua(self,placa:str =None, external:bool = False) -> pd.DataFrame:
        if external:
            self.mongo.connect()
        df_perua = pd.DataFrame(list(self.mongo.db["peruas"].find({"placa": f"{placa}"}, { "placa":1, "cnpj": 1, "modelo" : 1, "capacidade": 1,"_id":0})))
        if external:
            self.mongo.close()
        return df_perua
        
    def valida_motorista(self, cnpj:str = None) -> Motorista:
        if self.ctrl_motorista.verifica_existencia_motorista(cnpj, True):
            print(f"O CNPJ {cnpj} informado não existe na base de dados")
            return None
        else:
            df_motorista = self.ctrl_motorista.recupera_motorista(cnpj, True)
            #Recupera os dados do motorista transfomando em data frame
            escola = self.ctrl_motorista.valida_escola(int(df_motorista.codigo_escola.values[0]))

            #Cria um novo objeto de motorista
            motorista = Motorista(df_motorista.cnpj.values[0], df_motorista.nome.values[0], df_motorista.telefone.values[0], df_motorista.email.values[0], df_motorista.conta.values[0], escola)

            return motorista