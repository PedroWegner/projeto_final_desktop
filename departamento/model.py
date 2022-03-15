"""
DOCUMENTAR
"""
from banco_dados.model import ConexaoBD
from pessoa.model import Pessoa


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


class Departamento(DepartamentoUtil, object):
    def __init__(self, departamento=None, sigla_dep=None):
        super().__init__()
        self.id = None
        self.departamento = departamento
        self.sigla_dep = sigla_dep

    def cadastra_departamento(self):
        conexao = ConexaoBD()

        self.departamento = 'Matemática'
        self.sigla_dep = 'ML'

        comando_sql = "INSERT INTO curso_departamento (departamento, sigla_dep) VALUES (%s, %s)"
        tupla = (self.departamento, self.sigla_dep)

        conexao.executa_insert(comando_sql, tupla)


class Dep(DepartamentoUtil, object):
    def __init__(self, curso=None, cod_curso=None, turno=None, departamento=None):
        super().__init__()
        self.id = None
        self.curso = curso
        self.cod_curso = cod_curso
        self.turno = turno
        self.departamento = departamento  # o django criou uma tabela de muitos para muitos

    def cadastra_curso(self):
        self.exibe_departamento()
        self.exibe_turno()

        self.turno = int(input("Selecione o id do turno: "))
        self.departamento = input("Selecione o id do departamento( para mais de um departamento, digitar '1, 2, 3'): ")
        deps = self.departamento
        if len(self.departamento) > 1:
            deps = self.departamento.split(',')

        self.curso = 'Matemática'
        self.cod_curso = 'MTA'

        comando_sql = "INSERT INTO curso_curso (curso, cod_curso, turno_id) VALUES (%s, %s, %s);"
        tupla = (self.curso, self.cod_curso, self.turno)
        self.conexao.executa_insert(comando_sql, tupla)

        comando_sql = 'SELECT id FROM curso_curso ORDER BY id DESC LIMIT 1'
        self.id = self.conexao.executa_fetchone(comando_sql=comando_sql)[0]

        if len(deps) > 1:
            for departamento in deps:
                comando_sql = 'INSERT INTO departamento (curso_id, departamento_id) VALUES (%s, %s)'
                tupla = (self.id, departamento)
                self.conexao.executa_insert(comando_sql, tupla)
        else:
            comando_sql = 'INSERT INTO departamento (curso_id, departamento_id) VALUES (%s, %s)'
            tupla = (self.id, self.departamento)
            self.conexao.executa_insert(comando_sql, tupla)


class Disciplina(DepartamentoUtil, object):
    def __init__(self, disciplina=None, departamento=None, pre_requisito=False):
        super().__init__()
        self.id = None
        self.disciplina = disciplina
        self.departamento = departamento
        self.pre_requisito = pre_requisito

    def cadastrar_disciplina(self):
        self.exibe_departamento()
        self.departamento = input("Selecione o id do departamento: ")

        self.disciplina = 'Calculo Diferencial e Integral'
        self.pre_requisito = True

        comando_sql = "INSERT INTO departamento_disciplina (disciplina, departamento_id, pre_requisito) VALUES (%s, %s, %s)"
        tupla = (self.disciplina, self.departamento, self.pre_requisito)
        self.conexao.executa_insert(comando_sql=comando_sql, tupla=tupla)


class Aluno(DepartamentoUtil, object):
    def __init__(self, usuario=None, curso=None, disciplina=None, pessoa=None):
        super().__init__()
        self.id = None
        self.pessoa = pessoa
        self.usuario = usuario
        self.curso = curso
        self.disciplina = disciplina
        # self.cadastra_aluno()

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
        comando_sql = "INSERT INTO departamento_aluno (pessoa_id, usuario_id) VALUES (%s, %s)"

        tupla = (
            self.pessoa.id,
            self.usuario.id,
        )

        self.conexao.executa_insert(
            comando_sql=comando_sql,
            tupla=tupla,
        )

        comando_sql = 'SELECT id FROM departamento_aluno ORDER BY id DESC LIMIT 1'
        self.id = self.conexao.executa_fetchone(comando_sql=comando_sql)[0]

        comando_sql = "INSERT INTO departamento_aluno_curso (aluno_id, curso_id) VALUES (%s, %s)"

        tupla = (
            self.id,
            self.conexao.select_id('departamento_curso', 'curso', self.curso)[0]
        )

        self.conexao.executa_insert(
            comando_sql=comando_sql,
            tupla=tupla
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


class Professor(DepartamentoUtil, object):
    def __init__(self, titulo=None, usuario=None, pessoa=None):
        super().__init__()
        self.id = None
        self.pesso = pessoa
        self.titulo = titulo
        self.usuario = usuario

    def cadastra_professor(self):
        comando_sql = "INSERT INTO departamento_professor (titulo_id, usuario_id) VALUES (%s %s)"
        tupla = (
            self.conexao.select_id('departamento_tituloprofessor',
                                   'titulo', self.titulo)[0],
            self.usuario.id,

        )

        self.conexao.executa_insert(
            comando_sql=comando_sql,
            tupla=tupla,
        )
