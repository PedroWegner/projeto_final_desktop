"""
DOCUMENTAR
"""
from banco_dados.model import ConexaoBD
from pessoa.model import Pessoa
from datetime import datetime


class DepartamentoUtil(object):
    def __init__(self):
        self.conexao = ConexaoBD()

    def exibe_turno(self):
        comando_sql = "SELECT * FROM curso_turno"
        lista = self.conexao.select_all(comando_sql=comando_sql)
        for linha in lista:
            turno = f'Id - {linha[0]}: {linha[1]}'
            print(turno)

    def exibe_departamento(self):
        comando_sql = "SELECT * from curso_departamento"
        lista = self.conexao.select_all(comando_sql=comando_sql)
        for linha in lista:
            departamento = f'Id- {linha[0]}: {linha[1]}, {linha[2]}'
            print(departamento)


# CLASSE NOVA #
class Departamento(DepartamentoUtil):
    def __init__(self, cod_departamento=None, lingua=None):
        super().__init__()
        self.id = None
        self.cod_departamento = cod_departamento
        self.lingua = lingua

    def cadastra_departamento(self):
        comando_sql = "INSERT INTO departamento_depatarmanto (cod_departamento, lingua_id) VALLUES (%s, %s)"

        tupla = (
            self.cod_departamento,
            self.conexao.select_id('departamento_lingua', 'lingua', self.lingua)[0]
        )
        print(comando_sql, tupla)
        self.conexao.executa_insert(
            comando_sql=comando_sql,
            tupla=tupla,
        )


# class Departamento(DepartamentoUtil, object):
#     def __init__(self, departamento=None, cod_departamento=None):
#         super().__init__()
#         self.id = None
#         self.departamento = departamento
#         self.cod_departamento = cod_departamento
#
#     def cadastra_departamento(self):
#         comando_sql = "INSERT INTO departamento_departamento (departamento, cod_departamento) VALUES (%s, %s)"
#
#         tupla = (
#             self.departamento,
#             self.cod_departamento,
#         )
#
#         self.conexao.executa_insert(comando_sql, tupla)

class Modulo(DepartamentoUtil):
    def __init__(self, modulo=None, cod_modulo=None, departamento=None, lingua=None, nivel=None):
        super().__init__()
        self.id = None
        self.modulo = modulo
        self.cod_modulo = cod_modulo
        self.departamento = departamento
        self.lingua = lingua
        self.nivel = nivel

    def cadastra_modulo(self):
        comando_sql = "INSERT INTO departamento_modulo (modulo, cod_modulo, departamento_id, lingua_id, nivel_id) VALUES " \
                      "(%s, %s, %s, %s, %s)"

        tupla = (
            self.modulo,
            self.cod_modulo,
            self.conexao.select_id('departamento_departamento', 'cod_departamento', self.departamento)[0],
            self.conexao.select_id('departamento_lingua', 'lingua', self.lingua)[0],
            self.conexao.select_id('departamento_nivellingua', 'nivel', self.nivel)[0],
        )

        self.conexao.executa_insert(
            comando_sql=comando_sql,
            tupla=tupla,
        )


# class Curso(DepartamentoUtil, object):
#     def __init__(self, curso=None, cod_curso=None, turno=None, departamento=None):
#         super().__init__()
#         self.id = None
#         self.curso = curso
#         self.cod_curso = cod_curso
#         self.turno = turno
#         self.departamento = departamento  # o django criou uma tabela de muitos para muitos
#
#     def cadastra_curso(self):
#         comando_sql = "INSERT INTO departamento_curso (curso, cod_curso, turno_id) VALUES (%s, %s, %s)"
#         tupla = (
#             self.curso,
#             self.cod_curso,
#             self.conexao.select_id('departamento_turno', 'turno', self.turno)[0]
#         )
#
#         self.conexao.executa_insert(comando_sql=comando_sql, tupla=tupla)
#
#         comando_sql = "SELECT id FROM departamento_curso ORDER BY id DESC LIMIT 1"
#         self.id = self.conexao.executa_fetchone(comando_sql=comando_sql)[0]
#
#         for i in range(len(self.departamento)):
#             comando_sql = "INSERT INTO departamento_curso_departamento (curso_id, departamento_id) VALUES (%s, %s)"
#             tupla = (
#                 self.id,
#                 self.conexao.select_id('departamento_departamento', 'departamento', f'{self.departamento[i]}')[0],
#             )
#             self.conexao.executa_insert(
#                 comando_sql=comando_sql,
#                 tupla=tupla
#             )


class Disciplina(DepartamentoUtil, object):
    def __init__(self, disciplina=None, departamento=None, cod_disciplina=None, professor=None, pre_requisito=False):
        super().__init__()
        self.id = None
        self.disciplina = disciplina
        self.departamento = departamento
        self.cod_disciplina = cod_disciplina
        self.professor = professor
        # self.pre_requisito = pre_requisito

    def cadastrar_disciplina(self):
        comando_sql = f"SELECT DePr.id " \
                      f"FROM departamento_professor DePr " \
                      f"INNER JOIN pessoa_pessoa PePe " \
                      f"ON PePe.id = DePr.pessoa_id " \
                      f"WHERE PePe.nome='{self.professor.split(' ')[0]}' " \
                      f"AND PePe.sobrenome='{self.professor.split(' ')[1]}'"
        self.professor = self.conexao.executa_fetchone(comando_sql)[0]
        comando_sql = f"INSERT INTO departamento_disciplina (disciplina, cod_disciplina, departamento_id, professor_id) " \
                      f"VALUES (%s, %s, %s, %s)"
        tupla = (
            self.disciplina,
            self.cod_disciplina,
            self.conexao.select_id('departamento_departamento', 'departamento', self.departamento)[0],
            self.professor,

        )
        print(tupla)

        self.conexao.executa_insert(
            comando_sql=comando_sql,
            tupla=tupla,
        )


class Aluno(DepartamentoUtil, object):
    def __init__(self, usuario=None, modulo=None, curso=None, disciplina=None, pessoa=None):
        super().__init__()
        self.id = None
        self.pessoa = pessoa
        self.usuario = usuario
        self.modulo = modulo
        # self.curso = curso
        # self.disciplina = disciplina

    def exibe_aluno(self, id_aluno):
        comando_sql = f"SELECT * FROM departamento_aluno WHERE id={id_aluno}"
        resultado = self.conexao.executa_fetchone(comando_sql=comando_sql)

        self.id = resultado[0]
        self.usuario = resultado[1]

        comando_sql = f"SELECT PeUsuario.usuario " \
                      f"FROM trabalho_final.departamento_aluno DepAluno " \
                      f"INNER JOIN trabalho_final.pessoa_usuario PeUsuario ON DepAluno.usuario_id = PeUsuario.Id " \
                      f"WHERE DepAluno.id={self.id};"
        resultado = self.conexao.executa_fetchone(comando_sql=comando_sql)
        return resultado

    def cadastra_aluno(self):
        self.usuario.cadastrar_usuario()
        comando_sql = "INSERT INTO departamento_aluno (pessoa_id, usuario_id) VALUES (%s, %s)"

        tupla = (
            self.pessoa.id,
            self.usuario.id,
        )

        self.conexao.executa_insert(
            comando_sql=comando_sql,
            tupla=tupla,
        )

    def atualiza_aluno(self, nome=None, sobrenome=None, data_nascimento=None,
                       genero=None, endereco=None, estado_civil=None):
        att_pessoa = Pessoa()
        att_pessoa.atualiza_pessoa(
            id=self.pessoa,
            nome=nome,
            sobrenome=sobrenome,
            data_nascimento=data_nascimento,
            genero=genero,
            endereco=endereco,
            estado_civil=estado_civil,
        )

    def matricula_aluno_modulo(self):
        try:
            comando_sql = f"SELECT DeAl.id " \
                          f"FROM departamento_aluno DeAl " \
                          f"INNER JOIN pessoa_pessoa PePe " \
                          f"ON DeAl.pessoa_id = PePe.id " \
                          f"WHERE PePe.nome='{self.pessoa.split(' ')[0]}' " \
                          f"AND PePe.sobrenome='{self.pessoa.split(' ')[1]}';"
            self.id = self.conexao.executa_fetchone(comando_sql=comando_sql)[0]

            comando_sql = "INSERT INTO departamento_aluno_modulo (aluno_id, modulo_id) VALUES (%s, %s)"

            for modulo in range(len(self.modulo)):
                tupla = (
                    self.id,
                    self.conexao.select_id('departamento_modulo', 'modulo', self.modulo[modulo])[0],
                )
                self.conexao.executa_insert(
                    comando_sql=comando_sql,
                    tupla=tupla
                )
        except Exception as e:
            print(e)


class Professor(DepartamentoUtil, object):
    def __init__(self, usuario=None, pessoa=None, departamento=None, disciplina=None, lingua=None, nivel=None,
                 modulo=None):
        super().__init__()
        self.id = None
        self.pessoa = pessoa
        self.usuario = usuario
        self.departamento = departamento
        self.disciplina = disciplina
        self.lingua = lingua
        self.nivel = nivel
        self.modulo = modulo

    def cadastrar_professor(self):
        try:
            self.usuario.cadastrar_usuario()
            comando_sql = "INSERT INTO departamento_professor (departamento_id, lingua_id, nivel_id, pessoa_id, usuario_id) " \
                          "VALUES (%s, %s, %s, %s, %s)"
            tupla = (
                self.conexao.select_id('departamento_lingua', 'lingua', self.lingua)[0],
                self.conexao.select_id('departamento_lingua', 'lingua', self.lingua)[0],
                self.conexao.select_id('departamento_nivellingua', 'nivel', self.nivel)[0],
                self.pessoa.id,
                self.usuario.id,
            )

            self.conexao.executa_insert(
                comando_sql=comando_sql,
                tupla=tupla,
            )
        except Exception as e:
            print(e)

    def vincula_professor_modulo(self):
        comando_sql = f"SELECT DePr.id " \
                      f"FROM departamento_professor DePr " \
                      f"INNER JOIN pessoa_pessoa PePe " \
                      f"ON DePr.pessoa_id = PePe.id " \
                      f"WHERE PePe.nome = '{self.pessoa.split(' ')[0]}' " \
                      f"AND PePe.sobrenome='{self.pessoa.split(' ')[1]}';"

        self.id = self.conexao.executa_fetchone(comando_sql=comando_sql)[0]

        comando_sql = "INSERT INTO departamento_professor_modulo (professor_id, modulo_id) VALUES (%s, %s)"
        for modulo in range(len(self.modulo)):
            tupla = (
                self.id,
                self.conexao.select_id('departamento_modulo', 'modulo', self.modulo[modulo])[0],
            )
            self.conexao.executa_insert(
                comando_sql=comando_sql,
                tupla=tupla,
            )


class Aula(DepartamentoUtil):
    def __init__(self, aula=None, conteudo=None, data_post=None, aula_gravada=None, professor=None, conteudo_aula=None,
                 nivel=None):
        super().__init__()
        self.aula = aula
        self.conteudo = conteudo
        self.data_post = datetime.now()
        self.aula_gravada = aula_gravada
        self.professor = professor
        self.conteudo_aula = conteudo_aula
        self.nivel = nivel

    def cadastrar_aula(self):
        comando_sql = "INSERT INTO departamento_aula (aula, conteudo, data_post, aula_gravada, professor_id, conteudo_download, nivel_id) " \
                      "VALUES (%s, %s, %s, %s, %s, %s, %s)"

        tupla = (
            self.aula,
            self.conteudo,
            self.data_post,
            self.aula_gravada,
            self.professor,
            self.conteudo_aula,
            self.conexao.select_id('departamento_nivellingua', 'nivel', self.nivel)[0],
        )
        try:
            self.conexao.executa_insert(
                comando_sql=comando_sql,
                tupla=tupla
            )
        except Exception as e:
            print(e)
