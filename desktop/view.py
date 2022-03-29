# from PyQt5 import uic, QtWidgets
# from banco_dados.model import ConexaoBD
#
# class Teste:
#     def __init__(self):
#         self.conexao = ConexaoBD()
#     # FUNCOES INPUTS #
#     def input_departamento(self, input=None):
#         try:
#             input.clear()
#             comando_sql = "SELECT * FROM departamento_departamento"
#             departamentos = self.conexao.select_all(comando_sql=comando_sql)
#             for departamento in departamentos:
#                 input.addItem(departamento[1])
#         except Exception as e:
#             print(e)
#
#     def input_turno(self, input=None):
#         try:
#             comando_sql = "SELECT * FROM departamento_turno"
#             turnos = self.conexao.select_all(comando_sql=comando_sql)
#             for turno in turnos:
#                 input.addItem(turno[1])
#         except Exception as e:
#             print(e)
#
#     def input_professor(self, input=None, input_dep=None):
#         try:
#             input.clear()
#             comando_sql = f"SELECT PePe.nome, PePe.sobrenome " \
#                           f"FROM departamento_departamento DeDe " \
#                           f"INNER JOIN departamento_professor_departamento DePrDe " \
#                           f"ON DeDe.id = DePrDe.departamento_id " \
#                           f"INNER JOIN departamento_professor DePr " \
#                           f"ON DePr.id = DePrDe.professor_id " \
#                           f"INNER JOIN pessoa_pessoa PePe " \
#                           f"ON DePr.pessoa_id = PePe.id " \
#                           f"WHERE DeDe.departamento='{input_dep.currentText()}';"
#             professores = self.conexao.select_all(comando_sql=comando_sql)
#             for professor in professores:
#                 input.addItem(f'{professor[0]} {professor[1]}')
#         except Exception as e:
#             print(e)
#
#     def input_curso(self, input=None):
#         input.clear()
#         comando_sql = "SELECT * FROM departamento_curso"
#         cursos = self.conexao.select_all(comando_sql=comando_sql)
#         for curso in cursos:
#             input.addItem(curso[1])
#
#     def input_titulo(self, input=None):
#         comando_sql = "SELECT * FROM departamento_tituloprofessor"
#         titulos = self.conexao.select_all(comando_sql=comando_sql)
#         for titulo in titulos:
#             input.addItem(titulo[1])
#
#     def input_genero(self, input=None):
#         comando_sql = "SELECT * FROM pessoa_genero"
#         generos = self.conexao.select_all(comando_sql)
#         for genero in generos:
#             input.addItem(genero[1])
#
#     def input_estado_civil(self, input=None):
#         comando_sql = "SELECT * FROM pessoa_estadocivil"
#         estados_civil = self.conexao.select_all(comando_sql)
#         for estado_civil in estados_civil:
#             input.addItem(estado_civil[1])
#
#     def input_estado(self, input=None):
#         comando_sql = "SELECT * FROM pessoa_estado"
#         estados = self.conexao.select_all(comando_sql)
#         for estado in estados:
#             input.addItem(estado[1])
#
#     def input_tipo_endereco(self, input=None):
#         comando_sql = "SELECT * FROM pessoa_tipoendereco"
#         tipos_endereco = self.conexao.select_all(comando_sql)
#         for tipo_endereco in tipos_endereco:
#             input.addItem(tipo_endereco[1])
#
#     # FIM DOS INPUTS #
# if __name__ == '__main__':
#     pass