from api.DAO.ClientesDAO import ClienteDAO
from api.Model.clientes import Cliente
from api.utils.error_response import ErrorResponse

class ClienteService:
    def __init__(self,cliente_dao_dependency: ClienteDAO):

        print("⬆️  ClienteService.__init__()")
        self.__clienteDAO = cliente_dao_dependency

    def create(self, cargoBodyRequest: dict) -> str:

        print("🟣 ClienteService.create()")

        cliente = Cliente()
        cliente.cpf = cargoBodyRequest.get("cpf")
        cliente.nome = cargoBodyRequest.get("nome")
        cliente.telefone = cargoBodyRequest.get("telefone")

        resultado = self.__clienteDAO.findByField("cpf",cliente.cpf)
        if resultado and len(resultado) > 0:
            raise ErrorResponse(
                400,
                "Cpf já cadastrado",
                {"message":f"O cpf {cliente.cpf} já existe"}
            )
        
        return self.__clienteDAO.create(cliente)
    
    def readALL(self) -> list[dict]:
        print("🟣 ClienteService.readAll()")
        return self.__clienteDAO.readALL()

    def readByCPF(self, cpf: str) -> dict | None:
        print("🟣 ClienteService.readByCPF()")
        cliente = Cliente()
        cliente.cpf = cpf
        return self.__clienteDAO.readByCPF(cliente.cpf)
    
    def update(self, cpf: str, jsonCliente: dict) -> bool:
        print(jsonCliente)
        print("🟣 ClienteService.update()")

        cliente = Cliente()
        cliente.cpf = cpf
        cliente.nome = jsonCliente.get("nome")
        cliente.telefone = jsonCliente.get("telefone")

        return self.__clienteDAO.update(cliente)
    
    def delete(self, cpf: str) -> bool:
        print("🟣 ClienteService.delete()")

        cliente = Cliente()
        cliente.cpf = cpf
        return self.__clienteDAO.delete(cliente)