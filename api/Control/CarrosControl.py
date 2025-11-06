from flask import request, jsonify
from api.Service.CarrosService import CarroService

class CarroControl:
    def __init__(self, carro_service: CarroService):
        print("⬆️  CarroControl.constructor()")
        self.__carro_service = carro_service

    def store(self):
        print ("🔵 CarroControl.store()")

        json_carro = request.json.get("carro")
        placa = self.__carro_service.create(json_carro)
        return jsonify({"success": True,
        "message": "Cadastro realizado com sucesso",
        "data": {
            "carro": {
                "placa": placa,
                "montadora": json_carro.get("montadora"),
                "modelo": json_carro.get("modelo"),
                "cor": json_carro.get("cor"),
                "cliente": {
                    "cpf": json_carro.get("cliente", {}).get("cpf"),
                }
            }
        }
    }), 201

    def showALL(self):
        print ("🔵 CarroControl.showALL()")
        lista_carros = self.__carro_service.readALL()
        return jsonify({
            "success": True,
            "message": "Executado com sucesso",
            "data": {"carros": lista_carros}
        }), 200
    
    def showOne(self, placa):
        print ("🔵 CarroControl.showOne()")
        carro = self.__carro_service.readByPlaca(placa)
        return jsonify({
            "success": True,
            "message": "Executado com sucesso",
            "data": {"carro": carro}
        }), 200
    
    def update(self, placa):
        print ("🔵 CarroControl.update()")
        sucesso = self.__carro_service.update(placa,request.json)

        if sucesso:
            return jsonify({
                "success": True,
                "message": "Atualizado com sucesso",
                "data": {
                    "carro": {
                        "placa": placa,
                        "modelo": request.json.get("carro", {}).get("modelo")
                    }
                }
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": {"message": f"Não foi possível atualizar o carro com a placa {placa}"},
            }), 404
        
    def destroy(self, placa):
        print ("🔵 CarroControl.delete()")
        excluiu = self.__carro_service.delete(placa)
        if excluiu:
            return jsonify({
            "success": True,
            "message": "Excluído com sucesso"
        }), 204
        else:
            return jsonify({
                "success": False,
                "error": {"message": f"Não existe carro com placa {placa}"}
            }), 404