from model.motoristas import Motorista
class Perua:
    def __init__(self,
                placa:str = None,
                modelo:str = None,
                capacidade:int = None,
                motorista:Motorista = None,

                ):
        self.set_placa(placa)
        self.set_modelo(modelo)
        self.set_capacidade(capacidade)
        self.set_motorista(motorista)
        

    def set_placa(self, placa:str):
        self.placa = placa

    def set_modelo(self, modelo:str):
        self.modelo = modelo

    def set_capacidade(self, capacidade:int):
        self.capacidade = capacidade

    def set_motorista(self, motorista:Motorista):
        self.motorista = motorista


    def get_placa(self) -> str:
        return self.placa
    
    def get_modelo(self) -> str:
        return self.modelo
    
    def get_capacidade(self) -> int:
        return self.capacidade
    
    def get_motorista(self) -> Motorista:
        return self.motorista
    

    def to_string(self):
        return f"Placa: {self.get_placa()} | Modelo: {self.get_modelo()} | Capacidade: {self.get_capacidade()} | Motorista: {self.get_motorista().get_CNPJ()}"
