from utils import config

class SplashScreen:

    def __init__(self):


        # Nome(s) do(s) criador(es)
        self.created_by = "Rhuan Vitor Pratti Peixoto, Werley Oliveria Gonçalves, Werliane Oliveira Gonçalves"
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2023/2"


    def get_documents_count(self,collection_name):
        # Retorna o Total de Registros computados pela query

        df = config.query_count(collection_name=collection_name)
        return df[f"total_{collection_name}"].values[0]
    

    def get_updated_screen(self):
        return f"""
        ########################################################
        #                   SISTEMA DE TRANSPORTE ESCOLAR                     
        #                                                         
        #  TOTAL DE REGISTROS:                                    
        #      1 - ESCOLAS:        {str(self.get_documents_count(collection_name="escolas")).rjust(5)}
        #      2 - ALUNOS:         {str(self.get_documents_count(collection_name="alunos")).rjust(5)}
        #      3 - RESPONSÁVEIS:   {str(self.get_documents_count(collection_name="responsaveis")).rjust(5)}
        #      4 - MOTORISTAS:     {str(self.get_documents_count(collection_name="motoristas")).rjust(5)}
        #      5 - PERUAS:         {str(self.get_documents_count(collection_name="peruas")).rjust(5)}
        #
        #  CRIADO POR: {self.created_by}
        #
        #  PROFESSOR:  {self.professor}
        #
        #  DISCIPLINA: {self.disciplina}
        #              {self.semestre}
        ########################################################
        """