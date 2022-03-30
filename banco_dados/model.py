"""
DOCUMENTAR
"""
import mysql.connector


class ConexaoBD(object):
    def __init__(self, host='localhost', user='root', password='', db='escola_de_lingua'):
        if not db:
            pass  # levantar exceção
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.conecta = None
        self.cursor = None

    def conectar(self):
        self.conecta = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db,
        )

        self.cursor = self.conecta.cursor()

    def desconecta(self):
        self.conecta.close()

    def select_all(self, comando_sql):
        self.conectar()
        self.cursor.execute(comando_sql)
        resultado = self.cursor.fetchall()
        self.desconecta()
        return resultado

    def executa_insert(self, comando_sql, tupla):
        self.conectar()
        self.cursor.execute(comando_sql, tupla)
        self.conecta.commit()
        self.desconecta()

    def executa_update(self, comando_sql):
        self.conectar()
        self.cursor.execute(comando_sql)
        self.conecta.commit()
        self.desconecta()

    def executa_fetchone(self, comando_sql):
        self.conectar()
        self.cursor.execute(comando_sql)
        resultado = self.cursor.fetchone()
        self.desconecta()
        return resultado

    def select_id(self, tabela, campo, valor):
        comando_sql = f"SELECT id FROM {tabela} WHERE {campo}='{valor}' ORDER BY id DESC LIMIT 1"
        return self.executa_fetchone(comando_sql)

    # def update_unitario(self, tabela, campo, valor, id_obj):
    #     self.conecta()
    #     comando_sql = f"UPDATE {tabela} SET {campo}={valor} WHERE id={id_obj}"
    #     self.cursor.execute(comando_sql)
    #     self.conecta.commit
    #     self.desconecta()
