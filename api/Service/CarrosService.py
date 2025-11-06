from api.DAO.CarrosDAO import CarroDAO
from api.Model.carros import Carro

from api.DAO.ClientesDAO import ClienteDAO
from api.Model.clientes import Cliente

from api.utils.error_response import ErrorResponse

class CarroService:
    def __init__(self, carro_dao_dependency: CarroDAO, cliente_dao_dependency: ClienteDAO):
        print("⬆️  CarroService.__init__()")
        self.__carroDAO = carro_dao_dependency
        self.__clienteDAO = cliente_dao_dependency
    
    def create(self,jsonCarro: dict) -> Carro:
        print("🟣 CarroService.create()")

        objCliente = Cliente()
        objCliente.cpf = jsonCarro["cliente"]["clientes_cpf"]

        objCarro = Carro()
        objCarro.placa = jsonCarro["placa"]
        objCarro.montadora = jsonCarro["montadora"]
        objCarro.modelo = jsonCarro["modelo"]
        objCarro.cor = jsonCarro["cor"]
        objCarro.cliente = objCliente

        clienteExiste= self.__clienteDAO.findByField("cpf",objCarro.cliente.cpf)
        if not clienteExiste:
            raise ErrorResponse(
                400,
                "O cliente informado não existe",
                {"message":f"O cliente {objCarro.cliente.cpf} não foi encontrado"}
            )
        
        placaExiste = self.__carroDAO.findByField("placa",objCarro.placa)
        if placaExiste and len(placaExiste) > 0:
            raise ErrorResponse(
                400,
                "Placa já existe",
                {"message":f"A placa {objCarro.placa} já está cadastrada"}
            )
        
        return self.__carroDAO.create(objCarro)
    
    def readALL(self) -> list[dict]:
        print("🟣 CarroService.readlALL()")
        return self.__carroDAO.readALL()
    
    def readByPlaca(self, placa: str) -> dict:
        objCarro = Carro()
        objCarro.placa = placa

        carro = self.__carroDAO.readByPlaca(objCarro.placa)
        if not carro:
            raise ErrorResponse(
                404,
                "Carro não encontrado",
                {"message":f"Não existe carro com placa {objCarro.placa}"}
            )
        return carro
    
    def update(self, placa: str, requestBody: dict) -> bool:
        print("🟣 CarroService.update()")
        jsonCarro = requestBody["carro"]

        objCliente = Cliente()
        objCliente.cpf = jsonCarro["cliente"]["clientes_cpf"]

        objCarro = Carro()
        objCarro.placa = placa
        objCarro.montadora = jsonCarro["montadora"]
        objCarro.modelo = jsonCarro["modelo"]
        objCarro.cor = jsonCarro["cor"]
        objCarro.cliente = objCliente

        return self.__carroDAO.update(objCarro)
    
    def delete(self, placa: str) -> bool:
        print("🟣 CarroService.delete()")
        objCarro = Carro()
        objCarro.placa = placa
        return self.__carroDAO.delete(objCarro.placa)
