MENU_PRINCIPAL = """Menu Principal
1 - Relatórios
2 - Inserir Registros
3 - Atualizar Registros
4 - Remover Registros
5 - Sair
"""

MENU_RELATORIOS= """Relatórios
1 - Relatório de Escolas
2 - Relatório de Alunos
3 - Relatório de Responsáveis
4 - Relatório de Motoristas
5 - Relatório de Peruas
0 - Sair
"""

MENU_ENTIDADES = """ENTIDADES
1 - ESCOLA
2 - ALUNOS
3 - RESPONSÁVEIS
4 - MOTORISTAS
5 - PERUAS
"""

QUERY_COUNT = 'select count(1) as total_{tabela} from {tabela}'


def query_count(collection_name):
    from conexion.mongo_queries import MongoQueries
    import pandas as pd
    mongo = MongoQueries()
    mongo.connect()
    
    my_collection = mongo.db[collection_name]
    total_documentos = my_collection.count_documents({})
    mongo.close()
    df = pd.DataFrame({f"total_{collection_name}": [total_documentos]})
    return df
def clear_console(wait_time:int=3):
    import os
    from time import sleep
    sleep(wait_time)
    os.system("clear")