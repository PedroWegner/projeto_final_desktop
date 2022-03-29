from PyQt5 import uic, QtWidgets
from banco_dados.model import ConexaoBD
from departamento.model import Departamento, Curso, Professor, Disciplina


class UtilDepartamento():
    def __init__(self):
        self.conexao = ConexaoBD()
        self.app = QtWidgets.QApplication([])
        self.view = None

    def exibe_output(self):
        pass

    def exibe_tela(self):
        self.view.show()
        self.app.exec()


class InformacoaPessoa(UtilDepartamento):
    def __init__(self):
        super().__init__()

    def exibe_output(self):
        super().exibe_output()
        self.exibe_estado()
        self.exibe_estado_civil()
        self.exibe_genero()
        self.exibe_tipo_endereco()

    def exibe_genero(self):
        comando_sql = "SELECT * FROM pessoa_genero"
        generos = self.conexao.select_all(comando_sql)
        for genero in generos:
            self.genero_input.addItem(genero[1])

    def exibe_estado_civil(self):
        comando_sql = "SELECT * FROM pessoa_estadocivil"
        estados_civil = self.conexao.select_all(comando_sql)
        for estado_civil in estados_civil:
            self.estado_civil_input.addItem(estado_civil[1])

    def exibe_estado(self):
        comando_sql = "SELECT * FROM pessoa_estado"
        estados = self.conexao.select_all(comando_sql)
        for estado in estados:
            self.estado_input.addItem(estado[1])

    def exibe_tipo_endereco(self):
        comando_sql = "SELECT * FROM pessoa_tipoendereco"
        tipos_endereco = self.conexao.select_all(comando_sql)
        for tipo_endereco in tipos_endereco:
            self.tipo_end_input.addItem(tipo_endereco[1])


class CadastraDepartamento(UtilDepartamento):
    def __init__(self):
        super().__init__()
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\cadastrodepartamento.ui'
        )

    def exibe_tela(self):
        super().exibe_tela()
        self.view.btn_cadastra.clicked.connect(self.cadastro_dep)

    def cadastro_dep(self):
        departamento = Departamento(
            departamento=self.view.departamento_input.displayText(),
            cod_departamento=self.view.codigo_input.displayText(),
        )
        departamento.cadastra_departamento()


class CadastraCurso(UtilDepartamento):
    def __init__(self):
        super().__init__()
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\cadastrocurso.ui'
        )

    def exibe_tela(self):
        super().exibe_tela()
        self.view.btn_cadastra.clicked.connect(self.cadastra_curso)
        self.exibe_output()

    def exibe_output(self):
        super().exibe_output()
        self.exibe_turno()
        self.exibe_departamento()

    def exibe_departamento(self):
        self.view.dep_input.clear()
        comando_sql = "SELECT * FROM departamento_departamento"
        departamentos = self.conexao.select_all(comando_sql=comando_sql)
        for departamento in departamentos:
            self.view.dep_input.addItem(departamento[1])

    def exibe_turno(self):
        comando_sql = "SELECT * FROM departamento_turno"
        turnos = self.conexao.select_all(comando_sql=comando_sql)
        for turno in turnos:
            self.view.turno_input.addItem(turno[1])

    def cadastra_curso(self):
        departamentos = self.view.dep_input.selectedItems()
        dep = []
        for departamento in departamentos:
            dep.append(departamento.text())
        dep = tuple(dep)
        curso = Curso(
            curso=self.view.curso_input.displayText(),
            cod_curso=self.view.cod_input.displayText(),
            turno=self.view.turno_input.currentText(),
            departamento=dep,
        )
        curso.cadastra_curso()


class CadastraDisciplina(UtilDepartamento):
    def __init__(self):
        super().__init__()
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\cadastradisciplina.ui'
        )

    def exibe_tela(self):
        super().exibe_tela()
        self.view.departamento_input.currentIndexChanged.connect(self.exibe_professor)
        self.view.cadastra_disci.clicked.connect(self.cadastra_disciplina)
        self.exibe_output()

    def exibe_output(self):
        super().exibe_output()
        self.exibe_departamento()

    def exibe_departamento(self):
        self.view.departamento_input.clear()
        comando_sql = "SELECT * FROM departamento_departamento"
        departamentos = self.conexao.select_all(comando_sql=comando_sql)
        for departamento in departamentos:
            self.view.departamento_input.addItem(departamento[1])

    def exibe_professor(self):
        self.view.professor_input.clear()
        comando_sql = f"SELECT PePe.nome, PePe.sobrenome " \
                      f"FROM departamento_departamento DeDe " \
                      f"INNER JOIN departamento_professor_departamento DePrDe " \
                      f"ON DeDe.id = DePrDe.departamento_id " \
                      f"INNER JOIN departamento_professor DePr " \
                      f"ON DePr.id = DePrDe.professor_id " \
                      f"INNER JOIN pessoa_pessoa PePe " \
                      f"ON DePr.pessoa_id = PePe.id " \
                      f"WHERE DeDe.departamento='{self.view.departamento_input.currentText()}';"
        professores = self.conexao.select_all(comando_sql=comando_sql)
        for professor in professores:
            self.view.professor_input.addItem(f'{professor[0]} {professor[1]}')

    def cadastra_disciplina(self):
        disciplina = Disciplina(
            disciplina=self.view.disciplina_input.displayText(),
            departamento=self.view.departamento_input.currentText(),
            cod_disciplina=self.view.cod_input.displayText(),
            professor=self.view.professor_input.currentItem().text(),
        )
        disciplina.cadastrar_disciplina()









if __name__ == '__main___':
    pass