from PyQt5 import QtWidgets, uic
from departamento.views import UtilDepartamento, InformacoaPessoa
from departamento.views_usuario import AtualizarSenha
from departamento.model import Aluno
from pessoa.model import Usuario, Pessoa, Endereco
from banco_dados.model import ConexaoBD
from departamento.view_disciplina import TelaDisciplinaAluno
from departamento.model import Curso, Disciplina, Departamento, Aluno, Professor
from PyQt5.QtWidgets import QDialog
import sys

# global variable
app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()


def executa_administrador(usuario_logado=None):
    menu_administrador = MenuAdministrador(usuario_logado=usuario_logado)
    widget.addWidget(menu_administrador)
    widget.setFixedHeight(800)
    widget.setFixedWidth(1600)
    widget.show()
    app.exec()


class UtilAdmnistrador:
    def __init__(self, usuario_logado=None):
        self.conexao = ConexaoBD()
        self.usuario_logado = usuario_logado

    def volta(self):
        try:
            menu_adm = MenuAdministrador(self.usuario_logado)
            widget.addWidget(menu_adm)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        except Exception as e:
            print(e)

    def exibe_informacao(self):
        pass

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


class MenuAdministrador(QDialog):
    def __init__(self, usuario_logado=None):
        super(MenuAdministrador, self).__init__()
        uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\menu_adm.ui',
            self
        )
        self.usuario_logado = usuario_logado

        # btns signals
        self.cadastro_dep.clicked.connect(self.abre_cadastro_departamento)
        self.cadastra_curso.clicked.connect(self.abre_cadastro_curso)
        self.cadastra_disciplina.clicked.connect(self.abre_cadastro_disciplina)
        self.cadastro_aluno.clicked.connect(self.abre_cadastro_aluno)
        self.cadastro_professor.clicked.connect(self.abre_cadastro_professor)

    def abre_cadastro_departamento(self):
        try:
            tela_cadastro_dep = CadastraDepartamento(usuario_logado=self.usuario_logado)
            widget.addWidget(tela_cadastro_dep)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        except Exception as e:
            print(e)

    def abre_cadastro_curso(self):
        try:
            tela_cadastro_curso = CadastraCurso(usuario_logado=self.usuario_logado)
            widget.addWidget(tela_cadastro_curso)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        except Exception as e:
            print(e)

    def abre_cadastro_disciplina(self):
        try:
            tela_cadastro_disciplina = CadastraDisciplina(usuario_logado=self.usuario_logado)
            widget.addWidget(tela_cadastro_disciplina)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        except Exception as e:
            print(e)

    def abre_cadastro_aluno(self):
        try:
            tela_cadastro_aluno = CadastraAluno(usuario_logado=self.usuario_logado)
            widget.addWidget(tela_cadastro_aluno)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        except Exception as e:
            print(e)

    def abre_cadastro_professor(self):
        try:
            tela_cadastro_professor = CadastraProfessor(usuario_logado=self.usuario_logado)
            widget.addWidget(tela_cadastro_professor)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        except Exception as e:
            print(e)


class CadastraDepartamento(QDialog, UtilAdmnistrador):
    def __init__(self, usuario_logado=None):
        super(CadastraDepartamento, self).__init__(usuario_logado=usuario_logado)
        uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\cadastrodepartamento.ui',
            self
        )

        # btn singal
        self.voltar_btn.clicked.connect(self.volta)
        self.btn_cadastra.clicked.connect(self.cadastro_dep)
        # self.btn_cadastra.clicked.connect(self.volta)

    def cadastro_dep(self):
        departamento = Departamento(
            departamento=self.departamento_input.displayText(),
            cod_departamento=self.codigo_input.displayText(),
        )
        departamento.cadastra_departamento()


class CadastraCurso(QDialog, UtilAdmnistrador):
    def __init__(self, usuario_logado=None):
        super(CadastraCurso, self).__init__(usuario_logado=usuario_logado)
        uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\cadastrocurso.ui',
            self
        )

        # funcoes construtoras
        self.exibe_informacao()

        # btn signal
        self.voltar_btn.clicked.connect(self.volta)
        self.btn_cadastra.clicked.connect(self.cadastra_curso)

    def exibe_informacao(self):
        super().exibe_informacao()
        self.exibe_departamento()
        self.exibe_turno()

    def exibe_departamento(self):
        self.dep_input.clear()
        comando_sql = "SELECT * FROM departamento_departamento"
        departamentos = self.conexao.select_all(comando_sql=comando_sql)
        for departamento in departamentos:
            self.dep_input.addItem(departamento[1])

    def exibe_turno(self):
        comando_sql = "SELECT * FROM departamento_turno"
        turnos = self.conexao.select_all(comando_sql=comando_sql)
        for turno in turnos:
            self.turno_input.addItem(turno[1])

    def cadastra_curso(self):
        departamentos = self.dep_input.selectedItems()
        dep = []
        for departamento in departamentos:
            dep.append(departamento.text())
        dep = tuple(dep)
        curso = Curso(
            curso=self.curso_input.displayText(),
            cod_curso=self.cod_input.displayText(),
            turno=self.turno_input.currentText(),
            departamento=dep,
        )
        curso.cadastra_curso()


class CadastraDisciplina(QDialog, UtilAdmnistrador):
    def __init__(self, usuario_logado=None):
        super(CadastraDisciplina, self).__init__(usuario_logado=usuario_logado)
        uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\cadastradisciplina.ui',
            self
        )

        # funcoes construtoras
        self.exibe_informacao()

        # btn signal
        self.voltar_btn.clicked.connect(self.volta)
        self.cadastra_disci.clicked.connect(self.cadastra_disciplina)

    def exibe_informacao(self):
        super().exibe_informacao()
        self.exibe_departamento()
        self.exibe_professor()

    def exibe_departamento(self):
        self.departamento_input.clear()
        comando_sql = "SELECT * FROM departamento_departamento"
        departamentos = self.conexao.select_all(comando_sql=comando_sql)
        for departamento in departamentos:
            self.departamento_input.addItem(departamento[1])

    def exibe_professor(self):
        self.professor_input.clear()
        comando_sql = f"SELECT PePe.nome, PePe.sobrenome " \
                      f"FROM departamento_departamento DeDe " \
                      f"INNER JOIN departamento_professor_departamento DePrDe " \
                      f"ON DeDe.id = DePrDe.departamento_id " \
                      f"INNER JOIN departamento_professor DePr " \
                      f"ON DePr.id = DePrDe.professor_id " \
                      f"INNER JOIN pessoa_pessoa PePe " \
                      f"ON DePr.pessoa_id = PePe.id " \
                      f"WHERE DeDe.departamento='{self.departamento_input.currentText()}';"
        professores = self.conexao.select_all(comando_sql=comando_sql)
        for professor in professores:
            self.professor_input.addItem(f'{professor[0]} {professor[1]}')

    def cadastra_disciplina(self):
        disciplina = Disciplina(
            disciplina=self.disciplina_input.displayText(),
            departamento=self.departamento_input.currentText(),
            cod_disciplina=self.cod_input.displayText(),
            professor=self.professor_input.currentItem().text(),
        )
        disciplina.cadastrar_disciplina()


class CadastraProfessor(QDialog, UtilAdmnistrador):
    def __init__(self, usuario_logado):
        super(CadastraProfessor, self).__init__(usuario_logado=usuario_logado)
        uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\cadastro_professor.ui',
            self
        )
        self.tipo_cadastro = None

        # funcoes construtoras
        self.exibe_informacao()
        self.tipo_tela()

        # btn signal
        self.voltar_btn.clicked.connect(self.volta)
        self.btn_cadastra.clicked.connect(self.cadastra_professor)

    def exibe_informacao(self):
        super().exibe_informacao()
        self.exibe_departamento()
        self.exibe_genero()
        self.exibe_titulo()
        self.exibe_estado()
        self.exibe_estado_civil()
        self.exibe_tipo_endereco()

    def tipo_tela(self):
        self.tipo_cadastro = self.conexao.executa_fetchone(
            comando_sql='SELECT id FROM pessoa_tipousuario WHERE tipo_usuario="Professor"'
        )[0]

    def exibe_departamento(self):
        self.dep_input.clear()
        comando_sql = "SELECT * FROM departamento_departamento"
        departamentos = self.conexao.select_all(comando_sql=comando_sql)
        for departamento in departamentos:
            self.dep_input.addItem(departamento[1])

    def exibe_titulo(self):
        comando_sql = "SELECT * FROM departamento_tituloprofessor"
        titulos = self.conexao.select_all(comando_sql=comando_sql)
        for titulo in titulos:
            self.titulo_input.addItem(titulo[1])

    def cadastra_professor(self):
        pessoa = Pessoa(
            nome=self.nome_input.displayText(),
            sobrenome=self.sobrenome_input.displayText(),
            data_nascimento=self.data_nasc_input.displayText(),
            cpf=self.cpf_input.displayText(),
            estado_civil=self.estado_civil_input.currentText(),
            genero=self.genero_input.currentText(),
            endereco=Endereco(
                rua=self.rua_input.displayText(),
                numero=self.numero_input.displayText(),
                bairro=self.bairro_input.displayText(),
                cep=self.cep_input.displayText(),
                cidade=self.cidade_input.displayText(),
                estado=self.estado_input.currentText(),
                tipo_endereco=self.tipo_end_input.currentText(),
            )
        )
        pessoa.cadastrar_pessoa()

        departamentos = self.dep_input.selectedItems()
        departamento = []
        for dep in departamentos:
            departamento.append(dep.text())
        departamento = tuple(departamento)

        professor = Professor(
            titulo=self.titulo_input.currentText(),
            usuario=Usuario(
                pessoa=pessoa,
                tipo_usuario=self.tipo_cadastro,
            ),
            pessoa=pessoa,
            departamento=departamento
        )
        professor.cadastrar_professor()


class CadastraAluno(QDialog, UtilAdmnistrador):
    def __init__(self, usuario_logado=None):
        super(CadastraAluno, self).__init__(usuario_logado=usuario_logado)
        uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\cadastro_aluno.ui',
            self
        )
        self.tipo_cadastro = None

        # funcoes construtoras
        self.exibe_informacao()
        self.tipo_tela()

        # btn signal
        self.voltar_btn.clicked.connect(self.volta)
        self.cadastrar_aluno_btn.clicked.connect(self.cadastro_de_aluno)

    def exibe_informacao(self):
        super().exibe_informacao()
        self.exibe_curso()
        self.exibe_genero()
        self.exibe_estado()
        self.exibe_estado_civil()
        self.exibe_tipo_endereco()

    def tipo_tela(self):
        self.tipo_cadastro = self.conexao.executa_fetchone(
            comando_sql='SELECT id FROM pessoa_tipousuario WHERE tipo_usuario="Aluno"'
        )[0]

    def exibe_curso(self):
        self.curso_input.clear()
        comando_sql = "SELECT * FROM departamento_curso"
        cursos = self.conexao.select_all(comando_sql=comando_sql)
        for curso in cursos:
            self.curso_input.addItem(curso[1])

    def cadastro_de_aluno(self):
        pessoa = Pessoa(
            nome=self.nome_input.displayText(),
            sobrenome=self.sobrenome_input.displayText(),
            data_nascimento=self.data_nasc_input.displayText(),
            cpf=self.cpf_input.displayText(),
            estado_civil=self.estado_civil_input.currentText(),
            genero=self.genero_input.currentText(),
            endereco=Endereco(
                rua=self.rua_input.displayText(),
                numero=self.numero_input.displayText(),
                bairro=self.bairro_input.displayText(),
                cep=self.cep_input.displayText(),
                cidade=self.cidade_input.displayText(),
                estado=self.estado_input.currentText(),
                tipo_endereco=self.tipo_end_input.currentText(),
            )
        )
        pessoa.cadastrar_pessoa()

        cursos = self.curso_input.selectedItems()
        curso = []
        for cur in cursos:
            curso.append(cur.text())
        curso = tuple(curso)

        aluno = Aluno(
            pessoa=pessoa,
            usuario=Usuario(
                pessoa=pessoa,
                tipo_usuario=self.tipo_cadastro
            ),
            curso=curso
        )
        aluno.cadastra_aluno()


class AtualizaAluno(InformacoaPessoa):
    def __init__(self):
        super().__init__()
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\atualizar_aluno.ui')
        self.exibe_output()

    def exibe_tela(self):
        super().exibe_tela()
        self.view.pushButton.clicked.connect(self.atualiza_aluno)

    def exibe_output(self):
        super().exibe_output()
        self.exibe_aluno()

    def exibe_aluno(self):
        comando_sql = "SELECT * FROM departamento_aluno"
        alunos = self.conexao.select_all(comando_sql)
        for aluno in alunos:
            self.view.lista_aluno.addItem(str(aluno[0]))

    def atualiza_aluno(self):
        aluno = Aluno(
            pessoa=self.view.lista_aluno.currentText()
        )
        aluno.atualiza_aluno(
            nome=self.view.nome_input.displayText(),
            sobrenome=self.view.sobrenome_input.displayText(),
            data_nascimento=self.view.data_nasc_input.displayText(),
            estado_civil=self.view.estado_civil_input.currentText(),
            genero=self.view.genero_input.currentText(),
            endereco=Endereco(
                rua=self.view.rua_input.displayText(),
                numero=self.view.numero_input.displayText(),
                bairro=self.view.bairro_input.displayText(),
                cep=self.view.cep_input.displayText(),
                cidade=self.view.cidade_input.displayText(),
                estado=self.view.estado_input.currentText(),
                tipo_endereco=self.view.tipo_end_input.currentText(),
            )
        )


class VisualizaAluno():  # ARRUMA AQUI
    def __init__(self):
        self.conexao = ConexaoBD()
        self.app = QtWidgets.QApplication([])
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\visualiza_aluno.ui')

    def exibe_tela(self):
        self.exibe_aluno()
        self.view.show()
        self.app.exec()

    def exibe_aluno(self):
        self.view.listWidget.clear()
        comando_sql = "SELECT * FROM departamento_aluno"
        qtd_aluno = self.conexao.select_all(comando_sql=comando_sql)
        aluno = Aluno()
        for i in range(len(qtd_aluno)):
            self.view.listWidget.addItem(aluno.exibe_aluno(id_aluno=qtd_aluno[i][0])[0])
