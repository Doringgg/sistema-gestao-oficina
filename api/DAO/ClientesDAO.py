from api.Model.clientes import Cliente

class ClienteDAO:
    def __init__(self,database_dependency):
        print("⬆️  ClientesDAO.__init__()")
        self.__database = database_dependency

    def create(self, objCliente: Cliente) -> None:
        SQL = "INSERT INTO clientes (cpf,nome,telefone) VALUES (%s,%s,%s);"
        params = (objCliente.cpf, objCliente.nome, objCliente.telefone)

        with self.__database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(SQL, params)
                connection.commit()
                affected = cursor.rowcount
        if not affected:
            raise Exception("Falha ao inserir cliente")
        print("✅ ClientesDAO.create()")

    def readALL(self)-> list[dict]:
        SQL = "SELECT * FROM clientes;"

        with self.__database.get_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(SQL)
                resultados = cursor.fetchall()
        
        print(f"✅ ClientesDAO.readAll() -> {len(resultados)} registros encontrados")
        return resultados
    
    def readByCPF(self, cpf) -> dict | None:
        SQL = "SELECT * FROM clientes WHERE cpf = %s;"
        params = (cpf,)

        with self.__database.get_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(SQL, params)
                resultados = cursor.fetchone()

        print("✅ ClientesDAO.readByCPF()")
        return resultados
        
    def update(self, objCliente: Cliente) -> bool:
        SQL = "UPDATE clientes SET nome = %s, telefone =%s WHERE cpf = %s;"
        params = (objCliente.nome, objCliente.telefone, objCliente.cpf)

        with self.__database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(SQL, params)
                connection.commit()
                affected = cursor.rowcount

        print("✅ ClientesDAO.update()")
        return affected > 0
    
    def delete(self, cliente: Cliente) -> bool:
        SQL = "DELETE FROM clientes WHERE cpf = %s;"
        params = (cliente.cpf,)

        with self.__database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(SQL, params)
                connection.commit()
                affected = cursor.rowcount
        
        print("✅ ClientesDAO.delete()")
        return affected > 0