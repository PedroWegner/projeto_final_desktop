from PyQt5 import QtWidgets, uic
from pessoa.model import Usuario, Pessoa, Endereco
from departamento.view_base import MenuBase
from departamento.model import Curso, Disciplina, Departamento, Aluno, Professor
from PyQt5.QtWidgets import QDialog

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


class TelaAdministrador(QDialog, MenuBase):
    def __init__(self, usuario_logado=None):
        super(TelaAdministrador, self).__init__(usuario_logado=usuario_logado)
        uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\tela_menu_administrador.ui',
            self
        )

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
        self.professor_btn_cad_professor.clicked.connect(self.limpa_professor) # TENTAR COM EXPRESSAO LAMBDA ENVIANDO UM DICIONARIO

        # FIM btn singals - HOME #

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
                tipo_usuario=tipo_cadastro
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

    # FIM FUNCOES DE LIMPA CAMPO #


if __name__ == '__main__':
    pass