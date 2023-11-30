from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_aluno import Controller_Aluno
from controller.controller_escola import Controller_Escola
from controller.controller_motorista import Controller_Motorista
from controller.controller_perua import Controller_Perua
from controller.controller_responsavel import Controller_Responsavel

tela_inicial = SplashScreen()
relatorio = Relatorio()
ctrl_aluno = Controller_Aluno()
ctrl_escola = Controller_Escola()
ctrl_motorista = Controller_Motorista()
ctrl_perua = Controller_Perua()
ctrl_responsavel = Controller_Responsavel()

def reports(opcao_relatorio:int=0):

    if opcao_relatorio == 1:
        relatorio.get_relatorio_escolas()            
    elif opcao_relatorio == 2:
        relatorio.get_relatorio_alunos()
    elif opcao_relatorio == 3:
        relatorio.get_relatorio_responsaveis()
    elif opcao_relatorio == 4:
        relatorio.get_relatorio_motoristas()
    elif opcao_relatorio == 5:
        relatorio.get_relatorio_peruas()

        

def inserir(opcao_inserir:int=0):

    if opcao_inserir == 1:                               
        nova_escola = ctrl_escola.inserir_escola()
    elif opcao_inserir == 2:
        novo_aluno = ctrl_aluno.inserir_aluno()
    elif opcao_inserir == 3:
        novo_responsavel = ctrl_responsavel.inserir_responsavel()
    elif opcao_inserir == 4:
        novo_motorista = ctrl_motorista.inserir_motorista()
    elif opcao_inserir == 5:
        nova_perua = ctrl_perua.inserir_perua()

def atualizar(opcao_atualizar:int=0):

    if opcao_atualizar == 1:
        relatorio.get_relatorio_escolas()
        escola_atualizada = ctrl_escola.atualizar_escola()
    elif opcao_atualizar == 2:
        relatorio.get_relatorio_alunos()
        aluno_atualizado = ctrl_aluno.atualizar_aluno()
    elif opcao_atualizar == 3:
        relatorio.get_relatorio_responsaveis()
        responsavel_atualizado = ctrl_responsavel.atualizar_responsavel()
    elif opcao_atualizar == 4:
        relatorio.get_relatorio_motoristas()
        motorista_atualizado = ctrl_motorista.atualizar_motorista()
    elif opcao_atualizar == 5:
        relatorio.get_relatorio_peruas()
        perua_atualizada = ctrl_perua.atualizar_perua()

def excluir(opcao_excluir:int=0):

    if opcao_excluir == 1:
        relatorio.get_relatorio_escolas()
        ctrl_escola.excluir_escola()
    elif opcao_excluir == 2:                
        relatorio.get_relatorio_alunos()
        ctrl_aluno.excluir_aluno()
    elif opcao_excluir == 3:                
        relatorio.get_relatorio_responsaveis()
        ctrl_responsavel.excluir_responsavel()
    elif opcao_excluir == 4:                
        relatorio.get_relatorio_motoristas()
        ctrl_motorista.excluir_motorista()
    elif opcao_excluir == 5:
        relatorio.get_relatorio_peruas()
        ctrl_perua.excluir_perua()

def run():
    print(tela_inicial.get_updated_screen())
    config.clear_console()

    while True:
        print(config.MENU_PRINCIPAL)
        opcao = int(input("Escolha uma opção [1-5]: "))
        config.clear_console(1)
        
        if opcao == 1: # Relatórios
            
            print(config.MENU_RELATORIOS)
            opcao_relatorio = int(input("Escolha uma opção [0-6]: "))
            config.clear_console(1)

            reports(opcao_relatorio)

            config.clear_console(1)

        elif opcao == 2: # Inserir Novos Registros
            
            while True:
                print(config.MENU_ENTIDADES)
                opcao_inserir = int(input("Escolha uma opção [1-5]: "))
                config.clear_console(1)
                inserir(opcao_inserir=opcao_inserir)
                config.clear_console()
                resposta = str(input("Deseja inserir mais algum registro? [S ou N]: ")).lower()
                if resposta == "s":
                    continue
                else:
                    break       

            print(tela_inicial.get_updated_screen())    

        elif opcao == 3: # Atualizar Registros
            while True:

                print(config.MENU_ENTIDADES)
                opcao_atualizar = int(input("Escolha uma opção [1-5]: "))
                config.clear_console(1)

                atualizar(opcao_atualizar=opcao_atualizar)

                config.clear_console()

                resposta = str(input("Deseja alterar mais algum registro? [S ou N]: ")).lower()
                if resposta == "s":
                    continue
                else:
                    break           

        elif opcao == 4:

            while True:
                print(config.MENU_ENTIDADES)
                opcao_excluir = int(input("Escolha uma opção [1-5]: "))
                config.clear_console(1)
                excluir(opcao_excluir=opcao_excluir)
                config.clear_console()
                resposta = str(input("Deseja excluir mais algum registro? [S ou N]: ")).lower()
                if resposta == "s":
                    continue
                else:
                    break 
                

            print(tela_inicial.get_updated_screen())
            config.clear_console()
        elif opcao == 5:

            print(tela_inicial.get_updated_screen())
            config.clear_console()
            print("Obrigado por utilizar o nosso sistema.")
            exit(0)

        else:
            print("Opção incorreta.")
            exit(1)

if __name__ == "__main__":
    run()