from conexion.mongo_queries import MongoQueries
import pandas as pd
from pymongo import ASCENDING, DESCENDING

class Relatorio:
    def __init__(self):
        pass
    
        
    def get_relatorio_alunos(self):

        mongo = MongoQueries()
        mongo.connect()

        query_result = mongo.db["alunos"].aggregate([
            {
                '$lookup':{
                    'from': 'responsaveis',
                    'localField': 'cpf',
                    'foreignField': 'cpf',
                    'as': 'responsavel'
                }
            },{
                '$unwind':{
                    'path': '$responsavel'
                }
            },
            {
                '$lookup':{
                    'from':'escolas',
                    'localField': 'codigo_escola',
                    'foreignField':'codigo_escola',
                    'as': 'escola'

                }
            },
            {
                '$unwind':{
                    'path': '$escola'
                }
            },
            {
                '$project':{
                    'codigo_aluno':1,
                    'nome':1,
                    'horario_aula':1,
                    'turma':1,
                    'matricula':1,
                    'responsavel': '$responsavel.nome',
                    'cpf_responsavel': '$responsavel.cpf',
                    'logradouro': '$responsavel.logradouro',
                    'bairro': '$responsavel.bairro',
                    'cidade': '$responsavel.cidade',
                    'escola': '$escola.nome',
                    'codigo_escola': '$escola.codigo_escola',
                    '_id': 0        
                }
            },{
                '$sort':{
                    'nome':1,
                }
            }

        ])
        df_alunos = pd.DataFrame(list(query_result))
        
        mongo.close()
        print(df_alunos[["codigo_aluno","nome","horario_aula","turma","matricula","responsavel", "cpf_responsavel", "logradouro", "bairro", "cidade", "escola", "codigo_escola"]])
        input("Pressione Enter para sair do relatorio de Alunos")
    
    def get_relatorio_escolas(self):


        mongo = MongoQueries()
        mongo.connect()

        query_result = mongo.db["escolas"].find({}, {"codigo_escola":1,
                                                     "nome": 1, 
                                                     "cidade":1,
                                                     "bairro":1,
                                                     "logradouro":1,
                                                     "telefone":1,
                                                     '_id':0
                                                     }).sort("nome", ASCENDING)
        df_escolas = pd.DataFrame(list(query_result))

        mongo.close()
        print(df_escolas)
        input("Pressione Enter para Sair do Relatorio de Escolas")



    def get_relatorio_motoristas(self):
        mongo = MongoQueries()
        mongo.connect()
        query_result = mongo.db["motoristas"].aggregate([{
            '$lookup':{
                'from':'escolas',
                'localField':'codigo_escola',
                'foreignField': 'codigo_escola',
                'as':'escola'
            }
         },{
             '$unwind':{
                 'path':'$escola'
             }
         },{
             '$project':{
                 'cnpj': 1,
                 'nome': 1,
                 'telefone':1,
                 'email':1,
                 'conta':1,
                 'codigo_escola': '$escola.codigo_escola',
                 'nome_escola': '$escola.nome',
                 '_id':0
             }
         },{
             '$sort':{
                 'nome':1
             }
         }
        ])
        df_motoristas = pd.DataFrame(list(query_result))
        mongo.close()
        print(df_motoristas[["cnpj", "nome", "telefone", "email", "conta", "codigo_escola", "nome_escola"]])
        input("Pressione Enter para Sair do Relatorio de Motoristas")
    def get_relatorio_peruas(self):
        mongo = MongoQueries()
        mongo.connect()
        query_result = mongo.db["peruas"].aggregate([
            {
            '$lookup':{
            'from':'motoristas',
            'localField': 'cnpj',
            'foreignField': 'cnpj',
            'as': 'motorista'
                }
            },{
                '$unwind':{
                    'path':'$motorista'
                }
            },{
                '$project':{
                    'placa':1,
                    'modelo': 1,
                    'capacidade':1,
                    'cnpj_motorista' : '$motorista.cnpj',
                    'motorista': '$motorista.nome',
                    '_id':0,

                }
            },{
                '$sort':{
                    'motorista':1
                }
            }
        ])

        df_peruas = pd.DataFrame(list(query_result))
        mongo.close()
        print(df_peruas[["placa", "modelo", "capacidade", "cnpj_motorista", "motorista"]])
        input("Pressione Enter para Sair do Relatorio de Peruas")
    def get_relatorio_responsaveis(self):
        mongo = MongoQueries()
        mongo.connect()
        query_result = mongo.db["responsaveis"].find({},{'cpf' : 1,
                                                         'nome':1,
                                                         'cidade':1,
                                                         'bairro':1,
                                                         'logradouro':1,
                                                         'numero':1,
                                                         'complemento':1,
                                                         'telefone':1,
                                                         'email':1,
                                                         '_id': 0}).sort('nome', ASCENDING)
        df_responsaveis = pd.DataFrame(list(query_result))
        mongo.close()
        print(df_responsaveis)
        input("Pressione Enter Para Sair do Relatorio de Responsaveis")

