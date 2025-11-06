from api.Model.clientes import Cliente
from api.Model.carros import Carro

class CarroDAO:
    def __init__(self, database_dependency):
        print("⬆️  CarroDAO.__init__()")
        self.__database = database_dependency
    
    def create(self, objCarro: Carro) -> None:
        SQL = """INSERT INTO carros (placa,montadora,modelo,cor,clientes_cpf) 
                VALUES (%s,%s,%s,%s,%s)"""
        
        params = (
            objCarro.placa,
            objCarro.montadora,
            objCarro.modelo,
            objCarro.cor,
            objCarro.cliente.cpf,
        )

        with self.__database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(SQL, params)
                connection.commit()
                affected = cursor.rowcount
        if not affected:
            raise Exception("Falha ao inserir carro")
        print("✅ CarroDAO.create()")
    
    def readALL(self)-> list[dict]:
        SQL = """
        SELECT placa, montadora, modelo, cor, clientes_cpf, nome, telefone
        FROM carros
        JOIN clientes on carros.clientes_cpf = clientes.cpf
        ;"""

        with self.__database.get_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(SQL)
                rows = cursor.fetchall()
        
        carros = [
            {
                "placa": row["placa"],
                "montadora":row["montadora"],
                "modelo":row["modelo"],
                "cor":row["cor"],
                "cliente": {
                    "cpf":row["clientes_cpf"],
                    "nome":row["nome"],
                    "telefone":row["telefone"]
                }
            }
            for row in rows
        ]
        print(f"✅ CarroDAO.readALL() -> {len(carros)} registros encontrados")
        return carros
    
    def readByPlaca(self, placa) -> dict | None:
        SQL = """
        SELECT placa, montadora, modelo, cor, clientes_cpf, nome, telefone
        FROM carros
        JOIN clientes on carros.clientes_cpf = clientes.cpf
        WHERE placa = %s;"""
        params = (placa,)

        with self.__database.get_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(SQL, params)
                row = cursor.fetchone()

        if not row:
            print("✅ CarroDAO.readByPlaca() -> Não encontrado")
            return None

        carro = {
                "placa": row["placa"],
                "montadora":row["montadora"],
                "modelo":row["modelo"],
                "cor":row["cor"],
                "cliente": {
                    "cpf":row["clientes_cpf"],
                    "nome":row["nome"],
                    "telefone":row["telefone"]
                }
            }
        print("✅ CarroDAO.readByPlaca()")
        return carro
    
    def update(self, objCarro: Carro) -> bool:
        SQL = "UPDATE carros SET montadora = %s, modelo = %s, cor = %s, clientes_cpf = %s where placa = %s;"
        params = ( 
            objCarro.montadora, 
            objCarro.modelo, 
            objCarro.cor, 
            objCarro.cliente.cpf,
            objCarro.placa
        )

        with self.__database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(SQL, params)
                connection.commit()
                affected = cursor.rowcount
        
        return affected > 0
    
    def delete(self, placa) -> bool:
        SQL = "DELETE FROM carros WHERE placa = %s;"
        params = (placa,)

        with self.__database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(SQL, params)
                connection.commit()
                affected = cursor.rowcount

        print("✅ CarroDAO.delete()")
        return affected > 0
    
    def findByField(self, field: str, value) -> list[dict]:
        fields = ["placa","clientes_cpf"]
        if field not in fields:
            raise ValueError("Campo inválido para busca")
        
        SQL = f"SELECT * FROM carros WHERE {field} = %s;"
        params = (value,)
        with self.__database.get_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(SQL, params)
                resultados = cursor.fetchall()

        print(f"✅ CarroDAO.findByField('{field}') -> {len(resultados)} registros encontrados")
        return resultados
