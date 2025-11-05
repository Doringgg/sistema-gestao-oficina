import mysql.connector
from mysql.connector import pooling
import sys


class Database:

    __pool = None

    def __init__(self, pool_name="mypool",pool_size=25, pool_reset_session=True,
                 host="127.0.0.1", user="root",password="",database="oficina",port=3306):
        
        self.pool_name = pool_name
        self.pool_size = pool_size
        self.pool_reset_session = pool_reset_session
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    def connect(self):
        if Database.__pool is None:
            try:
                Database.__pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name=self.pool_name,
                    pool_size=self.pool_size,
                    pool_reset_session=self.pool_reset_session,
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    port=self.port
                )
                conection = Database.__pool.get_connection()
                print("⬆️  Conectado ao MySQL com sucesso!")
                conection.close()
            except mysql.connector.Error as error:
                print(f"❌ Falha ao conectar ao MySQL: {error}")
                sys.exit(1)
        return Database.__pool
    
    def get_connection(self):
        pool = self.connect()
        return pool.get_connection()
