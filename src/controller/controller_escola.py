import pandas as pd
from bson import ObjectId
from conexion.mongo_queries import MongoQueries


from model.escolas import Escola


class Controller_Escola:
    def __init__(self):
        self.mongo = MongoQueries()
        pass

    def inserir_escola(self) -> Escola:
        self.mongo.connect()


        #Solicita ao usuario o nome da escola
        novo_nome = str(input("Entre com o nome da escola: "))

        #Solicita ao usuario a cidade da escola
        novo_cidade = str(input("Entre com a cidade da escola: "))

        #Solicita ao usuario o bairro da escola
        novo_bairro = str(input("Entre com o bairro da escola: "))

        #Solicita ao usuario o logradouro da escola
        novo_logradouro = str(input("Entre com o logradouro da escola: "))

        #Solicita ao usuario o telefone da escola
        novo_telefone = str(input("Entre com o telefone da Escola: "))


        proxima_escola = self.mongo.db["escolas"].aggregate([
            {
                '$group':{
                    '_id': '$escolas',
                    'proxima_escola':{
                        '$max': '$codigo_escola'
                    }
                }
            },{
                '$project':{
                    'proxima_escola':{
                        '$sum':[
                            '$proxima_escola', 1
                        ]
                    },
                    '_id': 0
                }
            }

        ])
        print(list(proxima_escola))
        if list(proxima_escola) == []:
            proxima_escola = 1
        else:
            proxima_escola = int(list(proxima_escola)[0]['proxima_escola'])


        #Cria um dicionario para mapear as variaveis da entrada e saída
        data = dict(codigo_escola = proxima_escola, nome = novo_nome, cidade = novo_cidade, bairro = novo_bairro, logradouro = novo_logradouro, telefone = novo_telefone)

        #Insere e Recupera o codigo da nova escola
        id_escola = self.mongo.db["escolas"].insert_one(data)

        #Recupera os dados do novo produto criado trasnformando em um DataFrame
        df_escola = self.recupera_escola(id_escola.inserted_id)

        # Cria um novo objeto da Escola
        nova_escola = Escola(df_escola.codigo_escola.values[0],df_escola.nome.values[0], df_escola.cidade.values[0],df_escola.bairro.values[0],df_escola.logradouro.values[0],df_escola.telefone.values[0])
        #Exibe os atributos da nova escola
        print(nova_escola.to_string())
        print("Escola adicionada com sucesso!")
        self.mongo.close()
        return nova_escola
    
    def atualizar_escola(self) -> Escola:
        # Cria uma Nova conexao com o banco que permite alteração
        self.mongo.connect()

        

        codigo_escola = int(input("Código da Escola que irá alterar: "))

        if not self.verifica_existencia_escola(codigo_escola):
            #Solicita ao usuario o nome da escola
            novo_nome = str(input("Entre com o nome da escola: "))

            #Solicita ao usuario a cidade da escola
            novo_cidade = str(input("Entre com a cidade da escola: "))

            #Solicita ao usuario o bairro da escola
            novo_bairro = str(input("Entre com o bairro da escola: "))

            #Solicita ao usuario o logradouro da escola
            novo_logradouro = str(input("Entre com o logradouro da escola: "))

            #Solicita ao usuario o telefone da escola
            novo_telefone = str(input("Entre com o telefone da Escola: "))
            # Atualiza os dados de uma escola existente
            self.mongo.db["escolas"].update_one({"codigo_escola": codigo_escola}, 
                                                {"$set": {"nome": novo_nome, 
                                                          "cidade": novo_cidade,
                                                          "bairro": novo_bairro,
                                                          "logradouro": novo_logradouro,
                                                          "telefone": novo_telefone
                                                         } 
                                                })
            # Recupra os dados a escola atualizada transformando em um data frame
            df_escola = self.recupera_escola_codigo(codigo_escola)
            #Cria um objeto Escola do dataframe
            escola_atualizado = Escola(df_escola.codigo_escola.values[0], df_escola.nome.values[0], df_escola.cidade.values[0], df_escola.bairro.values[0], df_escola.logradouro.values[0], df_escola.telefone.values[0])
            #Exibe os atributos da escola atualizada
            print(escola_atualizado.to_string())
            print("Escola atualizada com sucesso!")
            self.mongo.close()
            return escola_atualizado   
            
        else:
            self.mongo.close()
            print(f"O código da escola {codigo_escola} não existe ")
            return None
        

    def excluir_escola(self):
        # Cria uma nova conexao com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuario o codgio da escola a ser excluido

        codigo_escola = int(input("Código da Escola que irá excluir: "))

        if not self.verifica_existencia_escola(codigo_escola):
            
            opcao_excluir = str(input(f"Tem certeza que deseja excluir a Escola com Código {codigo_escola}? [S ou N]: ")).lower()

            if opcao_excluir == "s":
                print("Caso a Escola possua alunos, motoristas e motorista possua peruas estes também serão excluídos!")
                opcao_excluir = str(input(f"Tem certeza que deseja excluir a Escola com Código {codigo_escola}? [S ou N]: ")).lower()
                if opcao_excluir.lower() == "s":
                    

                    self.mongo.db["alunos"].delete_many({"codigo_escola":int(codigo_escola)})

                    self.mongo.db["motoristas"].delete_many({"codigo_escola":int(codigo_escola)})
                
                    df_escola = self.recupera_escola_codigo(codigo_escola)

                    self.mongo.db["escolas"].delete_one({"codigo_escola": int(codigo_escola)})
                    
                    escola_excluida = Escola(df_escola.codigo_escola.values[0], df_escola.nome.values[0], df_escola.cidade.values[0], df_escola.bairro.values[0], df_escola.logradouro.values[0], df_escola.telefone.values[0])
                    self.mongo.close()
                    print("Escola removida com sucesso! Caso a escola possua alunos, motoristas e motorista possua peruas estes também foram excluídos")
                    print(escola_excluida.to_string())
            
        else:
            self.mongo.close()
            print(f"O Código da Escola {codigo_escola} não existe")

    
    def verifica_existencia_escola(self, codigo:int=None, external: bool = False) -> bool:
        if external:
            self.mongo.connect()
        
        df_escola = pd.DataFrame(self.mongo.db["escolas"].find({"codigo_escola": int(codigo)}, {"codigo_escola" : 1, "nome": 1, "cidade": 1, "bairro": 1, "logradouro": 1, "telefone":1, "_id": 0} ))
        if external:
            self.mongo.close()
        return df_escola.empty
    
    def get_quant_escolas(self, external:bool = False) -> int:
        if external:
            self.mongo.connect()
        quant_escolas = len(list(self.mongo.db["escolas"].find()))
        if external:
            self.mongo.close()

        return quant_escolas

    def recupera_escola(self, _id:ObjectId = None) -> pd.DataFrame:
        df_escola = pd.DataFrame(list(self.mongo.db["escolas"].find({"_id": _id}, {"codigo_escola" : 1, "nome": 1, "cidade": 1, "bairro": 1, "logradouro": 1, "telefone":1, "_id": 0})))
        return df_escola

    def recupera_escola_codigo(self, codigo:int=None, external: bool = False) -> pd.DataFrame:
        if external:
            self.mongo.connect()
        df_escola = pd.DataFrame(list(self.mongo.db["escolas"].find({"codigo_escola": codigo}, {"codigo_escola" : 1, "nome": 1, "cidade": 1, "bairro": 1, "logradouro": 1, "telefone":1, "_id": 0} )))

        if external:
            self.mongo.close()
        return df_escola