from flask import request, jsonify
from api.Service.ClientesService import ClienteService

class ClientesControl:
    def __init__(self, cliente_service:ClienteService):
        print("⬆️  ClienteControl.constructor()")
        self.__cliente_service = cliente_service

    def store(self):
        print("🔵 ClienteControle.store()")

        cliente_body_request = request.json.get("cliente")
        cpf_stored = self.__cliente_service.create(cliente_body_request)

        obj_resposta = {
            "success":True,
            "message": "Cadastro Realizado com sucesso",
            "data":{
                "cliente": [
                    {
                        "cpf": cpf_stored,
                        "nome":cliente_body_request.get("nome"),
                        "telefone":cliente_body_request.get("telefone")
                    }
                ]
            }
        }

        if cpf_stored:
            return jsonify(obj_resposta), 200
        
    def showALL(self):
        print("🔵 ClientesControl.showALL()")

        array_clientes = self.__cliente_service.readALL()

        return jsonify({
            "success":True,
            "message":"Busca realizada",
            "data":{"clientes":array_clientes}
        })
    
    def showOne(self):
        print("🔵 ClientesControl.showOne()")
        cpf = request.view_args.get("cpf")

        cliente = self.__cliente_service.readByCPF(cpf)
        obj_resposta = {
            "success":True,
            "message": "executado com sucesso",
            "data":{"clientes": cliente}
        }
        return jsonify(obj_resposta),200
    
    def update(self):
        print("🔵 ClientesControl.update()")

        cpf = request.view_args.get("cpf")

        json_cliente = request.json.get("cliente")
        print(json_cliente)

        resposta = self.__cliente_service.update(cpf, json_cliente)

        if resposta:
            return jsonify({
                "success": True,
                "message": "Cliente atualizado com sucesso",
                "data": {
                    "cliente": {
                        "cpf": cpf,
                        "nome": json_cliente.get("nome"),
                        "telefone": json_cliente.get("telefone"),
                    }
                }
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": f"Cliente com o cpf {cpf} não pode ser atualizado ou não pode ser encontrado",
            }), 404
    
    def destroy(self):
        print("🔵 ClientesControl.destroy()")
        
        cpf = request.view_args.get("cpf")

        excluiu = self.__cliente_service.delete(cpf)
        if not excluiu:
            return jsonify({
                "success": False,
                "message": f"Não existe Cliente com cpf {cpf}"
            }), 404
        
        return jsonify({
            "success": True,
            "message": "Excluído com sucesso"
        }), 204
