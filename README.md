# Exemplo de Sistema em Python fazendo CRUD no MongoDB

Esse sistema de exemplo é composto por um conjunto de coleções(collections) que representam uma gestão de transporte escolar, contendo tabelas como: Motoristas, Peruas, Escolas, Alunos e Responsáveis.

O sistema exige que as coleções existam, então basta executar o script Python a seguir para criação das coleções:
```shell
~$ python createCollectionsAndData.py
```

Para executar o sistema basta executar o script Python a seguir:
```shell
~$ python principal.py
```

## Organização
- [diagrams](diagrams): Nesse diretório está o [diagrama relacional](diagrams/DIAGRAMA_RELACIONAL_GESTAO_TRANSPORTE_ESCOLAR.png) (lógico) do sistema.
    * O sistema possui cinco entidades: ALUNOS, ESCOLAS, MOTORISTAS, RESPONSAVEIS e PERUAS
- [src](src): Nesse diretório estão os scripts do sistema
    * [conexion](src/conexion): Nesse repositório encontra-se o [módulo de conexão com o banco de dados Mongo](src/conexion/mongo_queries.py). Esse módulo possue algumas funcionalidades úteis para execução de instruções. O módulo do Mongo realiza a conexão, os métodos CRUD e de recuperação de dados são implementados diretamente nos objetos controladores (_Controllers_) e no objeto de Relatório (_reports_).
      
      - Caso esteja utilizando na máquina virtual antiga, você precisará alterar o método connect de:
          ```python
          self.conn = cx_Oracle.connect(user=self.user,
                                  password=self.passwd,
                                  dsn=self.connectionString()
                                  )
          ```
        Para:
          ```python
          self.conn = cx_Oracle.connect(user=self.user,
                                  password=self.passwd,
                                  dsn=self.connectionString(in_container=True)
                                  )
          ```
      - Exemplo de utilização para conexão no Mongo;
      ```python
            # Importa o módulo MongoQueries
            from conexion.mongo_queries import MongoQueries
            
            # Cria o objeto MongoQueries
            mongo = MongoQueries()

            # Realiza a conexão com o Mongo
            mongo.connect()

            """<inclua aqui suas declarações>"""

            # Fecha a conexão com o Mong
            mongo.close()
      ```
      - Exemplo de criação de um documento no Mongo:
      ```python
            from conexion.mongo_queries import MongoQueries
            import pandas as pd
            
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
      ```
    * [controller](src/controller/): Nesse diretório encontram-sem as classes controladoras, responsáveis por realizar inserção, alteração e exclusão dos registros das collections.
    * [model](src/model/): Nesse diretório encontram-ser as classes das entidades descritas no [diagrama relacional](diagrams/DIAGRAMA_RELACIONAL_GESTAO_TRANSPORTE_ESCOLAR.png)
    * [reports](src/reports/) Nesse diretório encontra-se a [classe](src/reports/relatorios.py) responsável por gerar todos os relatórios do sistema
    * [utils](src/utils/): Nesse diretório encontram-se scripts de [configuração](src/utils/config.py) e automatização da [tela de informações iniciais](src/utils/splash_screen.py)
    * [createCollectionsAndData.py](src/createCollectionsAndData.py): Script responsável por criar as collection . Esse script deve ser executado antes do script [principal.py](src/principal.py) para gerar as collection, caso não execute os scripts diretamente no Mongo Compass ou em alguma outra IDE de acesso ao Banco de Dados.
    * [principal.py](src/principal.py): Script responsável por ser a interface entre o usuário e os módulos de acesso ao Banco de Dados. Deve ser executado após a criação das tabelas.

### Bibliotecas Utilizadas
- [requirements.txt](src/requirements.txt): `pip install -r requirements.txt`

