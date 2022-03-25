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
#
# # global variable
# app = QtWidgets.QApplication(sys.argv)
# widget = QtWidgets.QStackedWidget()
#
#
# def executa_administrador(usuario_logado=None):
#     menu_administrador = MenuAdministrador(usuario_logado=usuario_logado)
#     widget.addWidget(menu_administrador)
#     widget.setFixedHeight(800)
#     widget.setFixedWidth(1600)
#     widget.show()
#     app.exec()
#
#
# class UtilAdmnistrador:
#     def __init__(self, usuario_logado=None):
#         self.conexao = ConexaoBD()
#         self.usuario_logado = usuario_logado
#
#     def volta(self):
#         try:
#             menu_adm = MenuAdministrador(self.usuario_logado)
#             widget.addWidget(menu_adm)
#             widget.setCurrentIndex(widget.currentIndex() + 1)
#         except Exception as e:
#             print(e)
#
#     def exibe_informacao(self):
#         pass
#
#     def exibe_genero(self):
#         comando_sql = "SELECT * FROM pessoa_genero"
#         generos = self.conexao.select_all(comando_sql)
#         for genero in generos:
#             self.genero_input.addItem(genero[1])
#
#     def exibe_estado_civil(self):
#         comando_sql = "SELECT * FROM pessoa_estadocivil"
#         estados_civil = self.conexao.select_all(comando_sql)
#         for estado_civil in estados_civil:
#             self.estado_civil_input.addItem(estado_civil[1])
#
#     def exibe_estado(self):
#         comando_sql = "SELECT * FROM pessoa_estado"
#         estados = self.conexao.select_all(comando_sql)
#         for estado in estados:
#             self.estado_input.addItem(estado[1])
#
#     def exibe_tipo_endereco(self):
#         comando_sql = "SELECT * FROM pessoa_tipoendereco"
#         tipos_endereco = self.conexao.select_all(comando_sql)
#         for tipo_endereco in tipos_endereco:
#             self.tipo_end_input.addItem(tipo_endereco[1])
#
#
# class MenuAdministrador(QDialog):
#     def __init__(self, usuario_logado=None):
#         super(MenuAdministrador, self).__init__()
#         uic.loadUi(
#             r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\menu_adm.ui',
#             self
#         )
#         self.usuario_logado = usuario_logado
#
#         # btns signals
#         self.cadastro_dep.clicked.connect(self.abre_cadastro_departamento)
#         self.cadastra_curso.clicked.connect(self.abre_cadastro_curso)
#         self.cadastra_disciplina.clicked.connect(self.abre_cadastro_disciplina)
#         self.cadastro_aluno.clicked.connect(self.abre_cadastro_aluno)
#         self.cadastro_professor.clicked.connect(self.abre_cadastro_professor)
#
#     def abre_cadastro_departamento(self):
#         try:
#             tela_cadastro_dep = CadastraDepartamento(usuario_logado=self.usuario_logado)
#             widget.addWidget(tela_cadastro_dep)
#             widget.setCurrentIndex(widget.currentIndex() + 1)
#         except Exception as e:
#             print(e)
#
#     def abre_cadastro_curso(self):
#         try:
#             tela_cadastro_curso = CadastraCurso(usuario_logado=self.usuario_logado)
#             widget.addWidget(tela_cadastro_curso)
#             widget.setCurrentIndex(widget.currentIndex() + 1)
#         except Exception as e:
#             print(e)
#
#     def abre_cadastro_disciplina(self):
#         try:
#             tela_cadastro_disciplina = CadastraDisciplina(usuario_logado=self.usuario_logado)
#             widget.addWidget(tela_cadastro_disciplina)
#             widget.setCurrentIndex(widget.currentIndex() + 1)
#         except Exception as e:
#             print(e)
#
#     def abre_cadastro_aluno(self):
#         try:
#             tela_cadastro_aluno = CadastraAluno(usuario_logado=self.usuario_logado)
#             widget.addWidget(tela_cadastro_aluno)
#             widget.setCurrentIndex(widget.currentIndex() + 1)
#         except Exception as e:
#             print(e)
#
#     def abre_cadastro_professor(self):
#         try:
#             tela_cadastro_professor = CadastraProfessor(usuario_logado=self.usuario_logado)
#             widget.addWidget(tela_cadastro_professor)
#             widget.setCurrentIndex(widget.currentIndex() + 1)
#         except Exception as e:
#             print(e)
#
#
# class CadastraDepartamento(QDialog, UtilAdmnistrador):
#     def __init__(self, usuario_logado=None):
#         super(CadastraDepartamento, self).__init__(usuario_logado=usuario_logado)
#         uic.loadUi(
#             r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\cadastrodepartamento.ui',
#             self
#         )
#
#         # btn singal
#         self.voltar_btn.clicked.connect(self.volta)
#         self.btn_cadastra.clicked.connect(self.cadastro_dep)
#         # self.btn_cadastra.clicked.connect(self.volta)
#
#     def cadastro_dep(self):
#         departamento = Departamento(
#             departamento=self.departamento_input.displayText(),
#             cod_departamento=self.codigo_input.displayText(),
#         )
#         departamento.cadastra_departamento()
#
#
# class CadastraCurso(QDialog, UtilAdmnistrador):
#     def __init__(self, usuario_logado=None):
#         super(CadastraCurso, self).__init__(usuario_logado=usuario_logado)
#         uic.loadUi(
#             r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\cadastrocurso.ui',
#             self
#         )
#
#         # funcoes construtoras
#         self.exibe_informacao()
#
#         # btn signal
#         self.voltar_btn.clicked.connect(self.volta)
#         self.btn_cadastra.clicked.connect(self.cadastra_curso)
#
#     def exibe_informacao(self):
#         super().exibe_informacao()
#         self.exibe_departamento()
#         self.exibe_turno()
#
#     def exibe_departamento(self):
#         self.dep_input.clear()
#         comando_sql = "SELECT * FROM departamento_departamento"
#         departamentos = self.conexao.select_all(comando_sql=comando_sql)
#         for departamento in departamentos:
#             self.dep_input.addItem(departamento[1])
#
#     def exibe_turno(self):
#         comando_sql = "SELECT * FROM departamento_turno"
#         turnos = self.conexao.select_all(comando_sql=comando_sql)
#         for turno in turnos:
#             self.turno_input.addItem(turno[1])
#
#     def cadastra_curso(self):
#         departamentos = self.dep_input.selectedItems()
#         dep = []
#         for departamento in departamentos:
#             dep.append(departamento.text())
#         dep = tuple(dep)
#         curso = Curso(
#             curso=self.curso_input.displayText(),
#             cod_curso=self.cod_input.displayText(),
#             turno=self.turno_input.currentText(),
#             departamento=dep,
#         )
#         curso.cadastra_curso()
#
#
# class CadastraDisciplina(QDialog, UtilAdmnistrador):
#     def __init__(self, usuario_logado=None):
#         super(CadastraDisciplina, self).__init__(usuario_logado=usuario_logado)
#         uic.loadUi(
#             r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\cadastradisciplina.ui',
#             self
#         )
#
#         # funcoes construtoras
#         self.exibe_informacao()
#
#         # btn signal
#         self.voltar_btn.clicked.connect(self.volta)
#         self.cadastra_disci.clicked.connect(self.cadastra_disciplina)
#
#     def exibe_informacao(self):
#         super().exibe_informacao()
#         self.exibe_departamento()
#         self.exibe_professor()
#
#     def exibe_departamento(self):
#         self.departamento_input.clear()
#         comando_sql = "SELECT * FROM departamento_departamento"
#         departamentos = self.conexao.select_all(comando_sql=comando_sql)
#         for departamento in departamentos:
#             self.departamento_input.addItem(departamento[1])
#
#     def exibe_professor(self):
#         self.professor_input.clear()
#         comando_sql = f"SELECT PePe.nome, PePe.sobrenome " \
#                       f"FROM departamento_departamento DeDe " \
#                       f"INNER JOIN departamento_professor_departamento DePrDe " \
#                       f"ON DeDe.id = DePrDe.departamento_id " \
#                       f"INNER JOIN departamento_professor DePr " \
#                       f"ON DePr.id = DePrDe.professor_id " \
#                       f"INNER JOIN pessoa_pessoa PePe " \
#                       f"ON DePr.pessoa_id = PePe.id " \
#                       f"WHERE DeDe.departamento='{self.departamento_input.currentText()}';"
#         professores = self.conexao.select_all(comando_sql=comando_sql)
#         for professor in professores:
#             self.professor_input.addItem(f'{professor[0]} {professor[1]}')
#
#     def cadastra_disciplina(self):
#         disciplina = Disciplina(
#             disciplina=self.disciplina_input.displayText(),
#             departamento=self.departamento_input.currentText(),
#             cod_disciplina=self.cod_input.displayText(),
#             professor=self.professor_input.currentItem().text(),
#         )
#         disciplina.cadastrar_disciplina()
#
#
# class CadastraProfessor(QDialog, UtilAdmnistrador):
#     def __init__(self, usuario_logado):
#         super(CadastraProfessor, self).__init__(usuario_logado=usuario_logado)
#         uic.loadUi(
#             r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\cadastro_professor.ui',
#             self
#         )
#         self.tipo_cadastro = None
#
#         # funcoes construtoras
#         self.exibe_informacao()
#         self.tipo_tela()
#
#         # btn signal
#         self.voltar_btn.clicked.connect(self.volta)
#         self.btn_cadastra.clicked.connect(self.cadastra_professor)
#
#     def exibe_informacao(self):
#         super().exibe_informacao()
#         self.exibe_departamento()
#         self.exibe_genero()
#         self.exibe_titulo()
#         self.exibe_estado()
#         self.exibe_estado_civil()
#         self.exibe_tipo_endereco()
#
#     def tipo_tela(self):
#         self.tipo_cadastro = self.conexao.executa_fetchone(
#             comando_sql='SELECT id FROM pessoa_tipousuario WHERE tipo_usuario="Professor"'
#         )[0]
#
#     def exibe_departamento(self):
#         self.dep_input.clear()
#         comando_sql = "SELECT * FROM departamento_departamento"
#         departamentos = self.conexao.select_all(comando_sql=comando_sql)
#         for departamento in departamentos:
#             self.dep_input.addItem(departamento[1])
#
#     def exibe_titulo(self):
#         comando_sql = "SELECT * FROM departamento_tituloprofessor"
#         titulos = self.conexao.select_all(comando_sql=comando_sql)
#         for titulo in titulos:
#             self.titulo_input.addItem(titulo[1])
#
#     def cadastra_professor(self):
#         pessoa = Pessoa(
#             nome=self.nome_input.displayText(),
#             sobrenome=self.sobrenome_input.displayText(),
#             data_nascimento=self.data_nasc_input.displayText(),
#             cpf=self.cpf_input.displayText(),
#             estado_civil=self.estado_civil_input.currentText(),
#             genero=self.genero_input.currentText(),
#             endereco=Endereco(
#                 rua=self.rua_input.displayText(),
#                 numero=self.numero_input.displayText(),
#                 bairro=self.bairro_input.displayText(),
#                 cep=self.cep_input.displayText(),
#                 cidade=self.cidade_input.displayText(),
#                 estado=self.estado_input.currentText(),
#                 tipo_endereco=self.tipo_end_input.currentText(),
#             )
#         )
#         pessoa.cadastrar_pessoa()
#
#         departamentos = self.dep_input.selectedItems()
#         departamento = []
#         for dep in departamentos:
#             departamento.append(dep.text())
#         departamento = tuple(departamento)
#
#         professor = Professor(
#             titulo=self.titulo_input.currentText(),
#             usuario=Usuario(
#                 pessoa=pessoa,
#                 tipo_usuario=self.tipo_cadastro,
#             ),
#             pessoa=pessoa,
#             departamento=departamento
#         )
#         professor.cadastrar_professor()
#
#
# class CadastraAluno(QDialog, UtilAdmnistrador):
#     def __init__(self, usuario_logado=None):
#         super(CadastraAluno, self).__init__(usuario_logado=usuario_logado)
#         uic.loadUi(
#             r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\cadastro_aluno.ui',
#             self
#         )
#         self.tipo_cadastro = None
#
#         # funcoes construtoras
#         self.exibe_informacao()
#         self.tipo_tela()
#
#         # btn signal
#         self.voltar_btn.clicked.connect(self.volta)
#         self.cadastrar_aluno_btn.clicked.connect(self.cadastro_de_aluno)
#
#     def exibe_informacao(self):
#         super().exibe_informacao()
#         self.exibe_curso()
#         self.exibe_genero()
#         self.exibe_estado()
#         self.exibe_estado_civil()
#         self.exibe_tipo_endereco()
#
#     def tipo_tela(self):
#         self.tipo_cadastro = self.conexao.executa_fetchone(
#             comando_sql='SELECT id FROM pessoa_tipousuario WHERE tipo_usuario="Aluno"'
#         )[0]
#
#     def exibe_curso(self):
#         self.curso_input.clear()
#         comando_sql = "SELECT * FROM departamento_curso"
#         cursos = self.conexao.select_all(comando_sql=comando_sql)
#         for curso in cursos:
#             self.curso_input.addItem(curso[1])
#
#     def cadastro_de_aluno(self):
#         pessoa = Pessoa(
#             nome=self.nome_input.displayText(),
#             sobrenome=self.sobrenome_input.displayText(),
#             data_nascimento=self.data_nasc_input.displayText(),
#             cpf=self.cpf_input.displayText(),
#             estado_civil=self.estado_civil_input.currentText(),
#             genero=self.genero_input.currentText(),
#             endereco=Endereco(
#                 rua=self.rua_input.displayText(),
#                 numero=self.numero_input.displayText(),
#                 bairro=self.bairro_input.displayText(),
#                 cep=self.cep_input.displayText(),
#                 cidade=self.cidade_input.displayText(),
#                 estado=self.estado_input.currentText(),
#                 tipo_endereco=self.tipo_end_input.currentText(),
#             )
#         )
#         pessoa.cadastrar_pessoa()
#
#         cursos = self.curso_input.selectedItems()
#         curso = []
#         for cur in cursos:
#             curso.append(cur.text())
#         curso = tuple(curso)
#
#         aluno = Aluno(
#             pessoa=pessoa,
#             usuario=Usuario(
#                 pessoa=pessoa,
#                 tipo_usuario=self.tipo_cadastro
#             ),
#             curso=curso
#         )
#         aluno.cadastra_aluno()
#
#
# class AtualizaAluno(InformacoaPessoa):
#     def __init__(self):
#         super().__init__()
#         self.view = uic.loadUi(
#             r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\atualizar_aluno.ui')
#         self.exibe_output()
#
#     def exibe_tela(self):
#         super().exibe_tela()
#         self.view.pushButton.clicked.connect(self.atualiza_aluno)
#
#     def exibe_output(self):
#         super().exibe_output()
#         self.exibe_aluno()
#
#     def exibe_aluno(self):
#         comando_sql = "SELECT * FROM departamento_aluno"
#         alunos = self.conexao.select_all(comando_sql)
#         for aluno in alunos:
#             self.view.lista_aluno.addItem(str(aluno[0]))
#
#     def atualiza_aluno(self):
#         aluno = Aluno(
#             pessoa=self.view.lista_aluno.currentText()
#         )
#         aluno.atualiza_aluno(
#             nome=self.view.nome_input.displayText(),
#             sobrenome=self.view.sobrenome_input.displayText(),
#             data_nascimento=self.view.data_nasc_input.displayText(),
#             estado_civil=self.view.estado_civil_input.currentText(),
#             genero=self.view.genero_input.currentText(),
#             endereco=Endereco(
#                 rua=self.view.rua_input.displayText(),
#                 numero=self.view.numero_input.displayText(),
#                 bairro=self.view.bairro_input.displayText(),
#                 cep=self.view.cep_input.displayText(),
#                 cidade=self.view.cidade_input.displayText(),
#                 estado=self.view.estado_input.currentText(),
#                 tipo_endereco=self.view.tipo_end_input.currentText(),
#             )
#         )
#
#
# class VisualizaAluno():  # ARRUMA AQUI
#     def __init__(self):
#         self.conexao = ConexaoBD()
#         self.app = QtWidgets.QApplication([])
#         self.view = uic.loadUi(
#             r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\visualiza_aluno.ui')
#
#     def exibe_tela(self):
#         self.exibe_aluno()
#         self.view.show()
#         self.app.exec()
#
#     def exibe_aluno(self):
#         self.view.listWidget.clear()
#         comando_sql = "SELECT * FROM departamento_aluno"
#         qtd_aluno = self.conexao.select_all(comando_sql=comando_sql)
#         aluno = Aluno()
#         for i in range(len(qtd_aluno)):
#             self.view.listWidget.addItem(aluno.exibe_aluno(id_aluno=qtd_aluno[i][0])[0])


######################################################
widget = QtWidgets.QStackedWidget()
app = QtWidgets.QApplication([])

def executa_menu_adm(usuario_logado=None):
    try:
        tela_administrador = TelaAdministrador(usuario_logado=usuario_logado)
        #
        widget.addWidget(tela_administrador)
        widget.setFixedHeight(864)
        widget.setFixedWidth(1536)
        widget.show()
        app.exec_()
    except Exception as e:
        print(e)


class TelaAdministrador(QDialog):
    def __init__(self, usuario_logado=None):
        super(TelaAdministrador, self).__init__()
        uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\primeiro_teste_tela_integrada.ui',
            self
        )
        self.conexao = ConexaoBD()
        self.usuario_logado = usuario_logado

        # btn singals  - HOME - #
        # HOME
        self.menu_btn_home.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.menu_home))
        self.home_label_bem_vindo.setText(
            f"Bem-Vindo {self.usuario_logado['nome_pessoa']} {self.usuario_logado['sobrenome_pessoa']}"
        )
        # DEPARTAMENTO
        self.menu_btn_cad_departamento.clicked.connect(
            lambda: self.menu_stacked.setCurrentWidget(self.menu_cad_departamento)
        )
        self.menu_btn_cad_departamento.clicked.connect(self.limpa_departamento)
        self.departamento_btn_cad_departamento.clicked.connect(self.cad_departamento)
        self.departamento_btn_cad_departamento.clicked.connect(self.limpa_departamento)

        # CURSO
        self.menu_btn_cad_curso.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.menu_cad_curso))
        self.menu_btn_cad_curso.clicked.connect(self.curso_construtor)
        self.menu_btn_cad_curso.clicked.connect(self.limpa_curso)
        self.curso_btn_cad_curso.clicked.connect(self.cad_curso)
        self.curso_btn_cad_curso.clicked.connect(self.limpa_curso)

        # DISCIPLINA
        self.menu_btn_cad_disciplina.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.menu_cad_disciplina))
        self.menu_btn_cad_disciplina.clicked.connect(self.disciplina_construtor)
        self.menu_btn_cad_disciplina.clicked.connect(self.limpa_disciplina)
        self.disciplina_btn_cad_disciplina.clicked.connect(self.cad_disciplina)
        self.disciplina_btn_cad_disciplina.clicked.connect(self.limpa_disciplina)

        # ALUNO
        self.menu_btn_cad_aluno.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.menu_cad_aluno))
        self.menu_btn_cad_aluno.clicked.connect(self.aluno_construtor)
        self.menu_btn_cad_aluno.clicked.connect(self.limpa_aluno)
        self.aluno_btn_cad_aluno.clicked.connect(self.cad_aluno)
        self.aluno_btn_cad_aluno.clicked.connect(self.limpa_aluno)


        # PROFESSOR
        self.menu_btn_cad_professor.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.menu_cad_professor))
        self.menu_btn_cad_professor.clicked.connect(self.professor_construtor)
        self.menu_btn_cad_professor.clicked.connect(self.limpa_professor)
        self.professor_btn_cad_professor.clicked.connect(self.cad_professor)
        self.professor_btn_cad_professor.clicked.connect(self.limpa_professor)

        # FIM btn singals - HOME #

    # FUNCOES INPUTS #
    def input_departamento(self, input=None):
        try:
            input.clear()
            comando_sql = "SELECT * FROM departamento_departamento"
            departamentos = self.conexao.select_all(comando_sql=comando_sql)
            for departamento in departamentos:
                input.addItem(departamento[1])
        except Exception as e:
            print(e)

    def input_turno(self, input=None):
        try:
            comando_sql = "SELECT * FROM departamento_turno"
            turnos = self.conexao.select_all(comando_sql=comando_sql)
            for turno in turnos:
                input.addItem(turno[1])
        except Exception as e:
            print(e)

    def input_professor(self, input=None, input_dep=None):
        try:
            input.clear()
            comando_sql = f"SELECT PePe.nome, PePe.sobrenome " \
                          f"FROM departamento_departamento DeDe " \
                          f"INNER JOIN departamento_professor_departamento DePrDe " \
                          f"ON DeDe.id = DePrDe.departamento_id " \
                          f"INNER JOIN departamento_professor DePr " \
                          f"ON DePr.id = DePrDe.professor_id " \
                          f"INNER JOIN pessoa_pessoa PePe " \
                          f"ON DePr.pessoa_id = PePe.id " \
                          f"WHERE DeDe.departamento='{input_dep.currentText()}';"
            professores = self.conexao.select_all(comando_sql=comando_sql)
            for professor in professores:
                input.addItem(f'{professor[0]} {professor[1]}')
        except Exception as e:
            print(e)

    def input_curso(self, input=None):
        input.clear()
        comando_sql = "SELECT * FROM departamento_curso"
        cursos = self.conexao.select_all(comando_sql=comando_sql)
        for curso in cursos:
            input.addItem(curso[1])

    def input_titulo(self, input=None):
        comando_sql = "SELECT * FROM departamento_tituloprofessor"
        titulos = self.conexao.select_all(comando_sql=comando_sql)
        for titulo in titulos:
            input.addItem(titulo[1])

    def input_genero(self, input=None):
        comando_sql = "SELECT * FROM pessoa_genero"
        generos = self.conexao.select_all(comando_sql)
        for genero in generos:
            input.addItem(genero[1])

    def input_estado_civil(self, input=None):
        comando_sql = "SELECT * FROM pessoa_estadocivil"
        estados_civil = self.conexao.select_all(comando_sql)
        for estado_civil in estados_civil:
            input.addItem(estado_civil[1])

    def input_estado(self, input=None):
        comando_sql = "SELECT * FROM pessoa_estado"
        estados = self.conexao.select_all(comando_sql)
        for estado in estados:
            input.addItem(estado[1])

    def input_tipo_endereco(self, input=None):
        comando_sql = "SELECT * FROM pessoa_tipoendereco"
        tipos_endereco = self.conexao.select_all(comando_sql)
        for tipo_endereco in tipos_endereco:
            input.addItem(tipo_endereco[1])

    # FIM DOS INPUTS #

    # CONSTRUTORES DE TELA #

    def curso_construtor(self):
        try:
            self.input_departamento(input=self.curso_input_departamento)
            self.input_turno(input=self.curso_input_turno)
        except Exception as e:
            print(e)

    def disciplina_construtor(self):
        try:
            self.input_departamento(input=self.disciplina_input_departamento)
            self.input_professor(
                input=self.disciplina_input_professor,
                input_dep=self.disciplina_input_departamento
            )
        except Exception as e:
            print(e)

    def aluno_construtor(self):
        try:
            self.input_tipo_endereco(input=self.aluno_input_tipo_end)
            self.input_genero(input=self.aluno_input_genero)
            self.input_estado_civil(input=self.aluno_input_estado_civil)
            self.input_estado(input=self.aluno_input_estado)
            self.input_curso(input=self.aluno_input_curso)
        except Exception as e:
            print(e)

    def professor_construtor(self):
        try:
            self.input_tipo_endereco(input=self.professor_input_tipo_end)
            self.input_genero(input=self.professor_input_genero)
            self.input_estado_civil(input=self.professor_input_estado_civil)
            self.input_estado(input=self.professor_input_estado)
            self.input_titulo(input=self.professor_input_titulo)
            self.input_departamento(input=self.professor_input_departamento)
        except Exception as e:
            print(e)

    # FIM DOS CONSTRUTORES #

    # FUNCOES DE CADASTRO #
    def cad_departamento(self):
        departamento = Departamento(
            departamento=self.departamento_input_departamento.displayText(),
            cod_departamento=self.departamento_input_codigo.displayText(),
        )
        departamento.cadastra_departamento()

    def cad_curso(self):
        departamentos = self.curso_input_departamento.selectedItems()
        dep = []
        for departamento in departamentos:
            dep.append(departamento.text())
        dep = tuple(dep)
        curso = Curso(
            curso=self.curso_input_curso.displayText(),
            cod_curso=self.curso_input_codigo.displayText(),
            turno=self.curso_input_turno.currentText(),
            departamento=dep,
        )
        curso.cadastra_curso()

    def cad_disciplina(self):
        disciplina = Disciplina(
            disciplina=self.disciplina_input_disciplina.displayText(),
            departamento=self.disciplina_input_departamento.currentText(),
            cod_disciplina=self.disciplina_input_codigo.displayText(),
            professor=self.disciplina_input_professor.currentItem().text(),
        )
        disciplina.cadastrar_disciplina()

    def cad_aluno(self):
        tipo_cadastro = self.conexao.executa_fetchone(
            comando_sql='SELECT id FROM pessoa_tipousuario WHERE tipo_usuario="Aluno"'
        )[0]

        pessoa = Pessoa(
            nome=self.aluno_input_nome.displayText(),
            sobrenome=self.aluno_input_sobrenome.displayText(),
            data_nascimento=self.aluno_input_data_nasc.displayText(),
            cpf=self.aluno_input_cpf.displayText(),
            estado_civil=self.aluno_input_estado_civil.currentText(),
            genero=self.aluno_input_genero.currentText(),
            endereco=Endereco(
                rua=self.aluno_input_rua.displayText(),
                numero=self.aluno_input_numero.displayText(),
                bairro=self.aluno_input_bairro.displayText(),
                cep=self.aluno_input_cep.displayText(),
                cidade=self.aluno_input_cidade.displayText(),
                estado=self.aluno_input_estado.currentText(),
                tipo_endereco=self.aluno_input_tipo_end.currentText(),
            )
        )
        pessoa.cadastrar_pessoa()

        cursos = self.aluno_input_curso.selectedItems()
        curso = []
        for cur in cursos:
            curso.append(cur.text())
        curso = tuple(curso)

        aluno = Aluno(
            pessoa=pessoa,
            usuario=Usuario(
                pessoa=pessoa,
                tipo_usuario=tipo_cadastro # PRECISA REVISAR AQUUIIIIIIIIIIIIIIIIIIIIIIIII
            ),
            curso=curso
        )
        aluno.cadastra_aluno()

    def cad_professor(self):
        tipo_cadastro = self.conexao.executa_fetchone(
            comando_sql='SELECT id FROM pessoa_tipousuario WHERE tipo_usuario="Professor"'
        )[0]

        pessoa = Pessoa(
            nome=self.professor_input_nome.displayText(),
            sobrenome=self.professor_input_sobrenome.displayText(),
            data_nascimento=self.professor_input_data_nasc.displayText(),
            cpf=self.professor_input_cpf.displayText(),
            estado_civil=self.professor_input_estado_civil.currentText(),
            genero=self.professor_input_genero.currentText(),
            endereco=Endereco(
                rua=self.professor_input_rua.displayText(),
                numero=self.professor_input_numero.displayText(),
                bairro=self.professor_input_bairro.displayText(),
                cep=self.professor_input_cep.displayText(),
                cidade=self.professor_input_cidade.displayText(),
                estado=self.professor_input_estado.currentText(),
                tipo_endereco=self.professor_input_tipo_end.currentText(),
            )
        )
        pessoa.cadastrar_pessoa()

        departamentos = self.professor_input_departamento.selectedItems()
        departamento = []
        for dep in departamentos:
            departamento.append(dep.text())
        departamento = tuple(departamento)

        professor = Professor(
            titulo=self.professor_input_titulo.currentText(),
            usuario=Usuario(
                pessoa=pessoa,
                tipo_usuario=tipo_cadastro,
            ),
            pessoa=pessoa,
            departamento=departamento
        )
        professor.cadastrar_professor()

    # FIM DAS FUNCOES DE CADASTRO #

    # FUNCOES DE LIMPA CAMPO #
    def limpa_departamento(self):
        self.departamento_input_departamento.clear()
        self.departamento_input_codigo.clear()

    def limpa_curso(self):
        self.curso_input_curso.clear()
        self.curso_input_codigo.clear()

    def limpa_disciplina(self):
        self.disciplina_input_disciplina.clear()
        self.disciplina_input_codigo.clear()

    def limpa_aluno(self):
        self.limpa_pessoa(
            rua=self.aluno_input_rua,
            numero=self.aluno_input_numero,
            bairro=self.aluno_input_bairro,
            cep=self.aluno_input_cep,
            cidade=self.aluno_input_cidade,
            nome=self.aluno_input_nome,
            sobrenome=self.aluno_input_sobrenome,
            data_nasc=self.aluno_input_data_nasc,
            cpf=self.aluno_input_cpf
        )

    def limpa_professor(self):
        self.limpa_pessoa(
            rua=self.professor_input_rua,
            numero=self.professor_input_numero,
            bairro=self.professor_input_bairro,
            cep=self.professor_input_cep,
            cidade=self.professor_input_cidade,
            nome=self.professor_input_nome,
            sobrenome=self.professor_input_sobrenome,
            data_nasc=self.professor_input_data_nasc,
            cpf=self.professor_input_cpf
        )

    def limpa_pessoa(self, rua=None, numero=None, bairro=None, cep=None, cidade=None, nome=None, sobrenome=None, data_nasc=None, cpf=None):
        rua.clear()
        numero.clear()
        bairro.clear()
        cep.clear()
        cidade.clear()
        nome.clear()
        sobrenome.clear()
        data_nasc.clear()
        cpf.clear()

    # FIM FUNCOES DE LIMPA CAMPO #


if __name__ == '__main__':
    excuta_isso()