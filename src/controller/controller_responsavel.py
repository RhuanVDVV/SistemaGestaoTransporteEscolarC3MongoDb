import pandas as pd
from bson import ObjectId
from conexion.mongo_queries import MongoQueries


from model.responsaveis import Responsavel


class Controller_Responsavel:
    
    def __init__(self):
        self.mongo = MongoQueries()
    
    
    def inserir_responsavel(self) -> Responsavel:    
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()
   
        cpf = str(input("Entre com o CPF do Responsável: "))
        if self.verifica_existencia_responsavel(cpf):
            # Solicita ao usuario o nome do responsável
            nome = str(input("Entre com o Nome do Responsável: "))            
            #Solicita ao usuario o Telefone do responsável
            telefone = str(input("Entre com o Telefone do Responsável:"))            
            #Solicita ao usuario o email do responsável            
            email = str(input("Entre com o email do Responsável: "))            
            #Solicita ao usuario a cidade do responsável
            cidade = str(input("Entre com a Cidade do Responsável: "))    
            #Solicita ao usuario o bairro do responsável            
            bairro = str(input("Entre com o Bairro do Responsável: "))            
            #Solicita ao usuario o logradouro do responsável            
            logradouro = str(input("Entre com o Logradouro do Responsável: "))            
            #Solicita ao usuario o Numero da Residencia do Responsável            
            numero = str(input("Entre com o Número da residência do Responsável: "))            
            #Solicita ao usuario o complemento do endereço do responsavel           
            complemento = str(input("Entre com o Complemento da  residência do responsável: "))
            #Insere e persiste o novo responsavel    
            self.mongo.db["responsaveis"].insert_one({"cpf": cpf, "nome" : nome, "telefone" : telefone, "email": telefone, "cidade": cidade, "bairro": bairro, "logradouro": logradouro, "numero" : numero, "complemento" : complemento})
              
            #Recupera os dados do novo responsavel criado transformando em um DataFrame  
            df_responsavel = self.recupera_responsavel(cpf) 
                              
            #Cria um novo ojbeto do fornecedor  
    
            novo_responsavel = Responsavel(df_responsavel.cpf.values[0] , df_responsavel.nome.values[0], df_responsavel.cidade.values[0], df_responsavel.bairro.values[0], df_responsavel.logradouro.values[0], df_responsavel.telefone.values[0], df_responsavel.email.values[0], df_responsavel.numero.values[0], df_responsavel.complemento.values[0])            
            # Exibe os atributos do novo fornecedor           
            print(novo_responsavel.to_string())
            print("Responsável cadastrado com sucesso!")
            self.mongo.close()
            
            #Retorna o objeto novo_responsavel para utilização posterior, caso necessário  
            return novo_responsavel
        else:
            self.mongo.close()
            print(f"O CPF {cpf} já esta cadastrado")
            return None
    
    def atualizar_responsavel(self) -> Responsavel:
        
        self.mongo.connect()
        
        cpf = input("CPF do responsável que deseja atualizar: ")
        
        if not self.verifica_existencia_responsavel(cpf):
            
            # Solicita ao usuario o nome do responsável
            nome = str(input("Entre com o novo Nome do Responsável: "))
            
            #Solicita ao usuario o Telefone do responsável
            telefone = str(input("Entre com o novo Telefone do Responsável: "))
            
            #Solicita ao usuario o email do responsável
            
            email = str(input("Entre com o novo email do Responsável: "))
            
            #Solicita ao usuario a cidade do responsável
            cidade = str(input("Entre com a nova Cidade do Responsável: "))
    
            #Solicita ao usuario o bairro do responsável
            
            bairro = str(input("Entre com o novo Bairro do Responsável: "))
            
            #Solicita ao usuario o logradouro do responsável
            
            logradouro = str(input("Entre com o novo Logradouro do Responsável: "))
            
            #Solicita ao usuario o Numero da Residencia do Responsável
            
            numero = str(input("Entre com o novo Número da residência do Responsável: "))
            
            #Solicita ao usuario o completo do endereço do responsavel
            
            complemento = str(input("Entre com o novo Complemento da  residência do responsável: "))
            
            #Atualiza os dados do responsavel existente
            
            self.mongo.db["responsaveis"].update_one({"cpf":cpf}, 
                                                     {"$set" : {"cpf": cpf, 
                                                                "nome": nome, 
                                                                "telefone": telefone, 
                                                                "email":email, 
                                                                "cidade":cidade, 
                                                                "bairro" : bairro, 
                                                                "logradouro": logradouro, 
                                                                "numero": numero, 
                                                                "complemento": complemento
                                                                }                                                                                      
                                                    })
            
            #Recupera os novos dados do responsavel transformando em um DataFrame
            
            df_responsavel = self.recupera_responsavel(cpf) 
            
            # Cria um novo objeto fornecedor
            
            responsavel_atualizado = Responsavel(df_responsavel.cpf.values[0] , df_responsavel.nome[0], df_responsavel.cidade[0], df_responsavel.bairro[0], df_responsavel.logradouro[0], df_responsavel.telefone[0], df_responsavel.email[0], df_responsavel.numero[0], df_responsavel.complemento[0])
        
            print(responsavel_atualizado.to_string())
            print("Responsável atualizado com sucesso!")
            self.mongo.close()
            return responsavel_atualizado
            
        else:
            self.mongo.close()
            print(f"O CPF {cpf} não existe")
            return None
            
    def excluir_responsavel(self):
        self.mongo.connect()
        
        cpf = input("CPF do responsável que irá excluir: ")
        
        if not self.verifica_existencia_responsavel(cpf):
            df_responsavel = self.recupera_responsavel(cpf)

            opcao_excluir = str(input(f"Tem certeza que deseja excluir o Responsável de CPF {cpf}? [S ou N]: ")).lower()

            if opcao_excluir == "s":
                print("Caso o Responsável possua alunos estes também serão excluídos!")
                opcao_excluir = str(input(f"Tem certeza que deseja excluir o Responsável de CPF {cpf}? [S ou N]: ")).lower()
                if opcao_excluir.lower() == "s":

                    self.mongo.db["alunos"].delete_many({"cpf":f"{cpf}"})
                    print("Alunos do Responsável foram removidos com sucesso!")
                    self.mongo.db["responsaveis"].delete_one({"cpf":f"{cpf}"})
                    responsavel_excluido = Responsavel(df_responsavel.cpf.values[0] , df_responsavel.nome[0], df_responsavel.cidade[0], df_responsavel.bairro[0], df_responsavel.logradouro[0], df_responsavel.telefone[0], df_responsavel.email[0], df_responsavel.numero[0], df_responsavel.complemento[0])
                    print("Responsável removido com sucesso!")
                    print(responsavel_excluido.to_string())
                    self.mongo.close()
           
        else:
            self.mongo.close()
            print(f"O CPF {cpf} não existe")
    
    
    def get_quant_responsaveis(self, external:bool = False) -> int:
        if external:
            self.mongo.connect()
        quant_responsaveis = len(list(self.mongo.db["responsaveis"].find()))
        if external:
            self.mongo.close()
        return quant_responsaveis

    def verifica_existencia_responsavel(self, cpf:str=None, external:bool = False) -> bool:
        if external:
            self.mongo.connect()
        
        df_responsavel = pd.DataFrame(self.mongo.db["responsaveis"].find({"cpf":f"{cpf}"}, {"cpf": 1, "nome" : 1, "cidade": 1, "bairro" : 1, "logradouro" : 1, "numero":1,"complemento": 1, "telefone":1, "email" : 1, "_id":0}))

        if external:
            self.mongo.close()

        return df_responsavel.empty
    
    def recupera_responsavel(self, cpf:str = None, external:bool = False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        df_responsavel = pd.DataFrame(list(self.mongo.db["responsaveis"].find({"cpf":f"{cpf}"}, {"cpf": 1, "nome" : 1, "cidade": 1, "bairro" : 1, "logradouro" : 1, "numero":1,"complemento": 1, "telefone":1, "email" : 1, "_id":0})))

        if external:
            self.mongo.close()
        
        return df_responsavel