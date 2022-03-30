from PyQt5 import QtWidgets, uic
from pessoa.model import Usuario, Pessoa, Endereco
from departamento.view_base import MenuBase
from departamento.model import Modulo, Disciplina, Departamento, Aluno, Professor
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
    tela_administrador = TelaAdministrador(usuario_logado=usuario_logado)
    #
    widget.addWidget(tela_administrador)
    widget.setFixedHeight(864)
    widget.setFixedWidth(1536)
    widget.show()
    app.exec_()



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
        self.menu_btn_cad_departamento.clicked.connect(self.departamento_construtor)
        self.departamento_btn_cad_departamento.clicked.connect(self.cad_departamento)

        # MODULO
        self.menu_btn_cad_modulo.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.menu_cad_modulo))
        self.menu_btn_cad_modulo.clicked.connect(self.modulo_construtor)
        self.modulo_btn_cad_modulo.clicked.connect(self.cad_modulo)
        self.modulo_btn_cad_modulo.clicked.connect(self.modulo_construtor)

        # # ALUNO
        try:
            self.menu_btn_cad_aluno.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.menu_cad_aluno))
            self.menu_btn_cad_aluno.clicked.connect(self.aluno_construtor)
            self.aluno_btn_cad_aluno.clicked.connect(self.cad_aluno)
            self.aluno_btn_cad_aluno.clicked.connect(self.aluno_construtor)

        except Exception as e:
            print(e)

        # # PROFESSOR
        try:
            self.menu_btn_cad_professor.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.menu_cad_professor))
            self.menu_btn_cad_professor.clicked.connect(self.professor_construtor)
            self.professor_btn_cad_professor.clicked.connect(self.cad_professor)
            self.professor_btn_cad_professor.clicked.connect(self.professor_construtor)
        except Exception as e:
            print(e)
        # PROFESSOR MODULO #
        self.menu_btn_professor_modulo.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.menu_professor_modulo))
        self.menu_btn_professor_modulo.clicked.connect(self.professor_modulo_construtor)
        # comando apaixo usado para alterar os modulos de acordo com o professor selecionado.
        self.professor_modulo_input_professor.currentTextChanged.connect(self.input_professor_modulo)
        self.professor_modulo_btn_vincula.clicked.connect(self.cad_professor_modulo)
        self.professor_modulo_btn_vincula.clicked.connect(self.input_professor_modulo)

        # ALUNO MODULO #
        self.menu_btn_aluno_modulo.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.menu_aluno_modulo))
        self.menu_btn_aluno_modulo.clicked.connect(self.aluno_modulo_construtor)
        # comando abaixo muda modulo de acordo com aluno
        self.aluno_modulo_input_aluno.currentTextChanged.connect(self.input_aluno_modulo)
        self.aluno_modulo_btn_matricular.clicked.connect(self.cad_aluno_modulo)
        self.aluno_modulo_btn_matricular.clicked.connect(self.input_aluno_modulo)

        # FIM btn singals - HOME #


    # CONSTRUTORES DE TELA #
    def departamento_construtor(self):
        try:
            self.limpa_departamento()
            self.input_lingua(input=self.departamento_input_lingua)
        except Exception as e:
            print(e)

    def modulo_construtor(self):
        try:
            self.limpa_modulo()
            self.input_departamento(input=self.modulo_input_departamento)
            self.input_lingua(input=self.modulo_input_lingua)
            self.input_nivel(input=self.modulo_input_nivel)
        except Exception as e:
            print(e)

    def aluno_construtor(self):
        try:
            self.limpa_aluno()
            self.input_tipo_endereco(input=self.aluno_input_tipo_end)
            self.input_genero(input=self.aluno_input_genero)
            self.input_estado_civil(input=self.aluno_input_estado_civil)
            self.input_estado(input=self.aluno_input_estado)
        except Exception as e:
            print(e)

    def professor_construtor(self):
        try:
            self.limpa_professor()
            self.input_tipo_endereco(input=self.professor_input_tipo_end)
            self.input_genero(input=self.professor_input_genero)
            self.input_estado_civil(input=self.professor_input_estado_civil)
            self.input_estado(input=self.professor_input_estado)
            self.input_lingua(input=self.professor_input_lingua)
            self.input_nivel(input=self.professor_input_nivel)
        except Exception as e:
            print(e)

    def professor_modulo_construtor(self):
        self.input_professor(input=self.professor_modulo_input_professor)
        self.input_professor_modulo()

    def aluno_modulo_construtor(self):
        self.input_aluno(input=self.aluno_modulo_input_aluno)


    # FIM DOS CONSTRUTORES #

    # FUNCOES DE CADASTRO # Ja alterado
    def cad_departamento(self):
        departamento = Departamento(
            cod_departamento=self.departamento_input_codigo.displayText(),
            lingua=self.departamento_input_lingua.currentText(),
        )
        departamento.cadastra_departamento()

    def cad_modulo(self):
        modulo = Modulo(
            modulo=self.modulo_input_modulo.displayText(),
            cod_modulo=self.modulo_input_codigo.displayText(),
            departamento=self.modulo_input_departamento.currentText(),
            lingua=self.modulo_input_lingua.currentText(),
            nivel=self.modulo_input_nivel.currentText(),
        )
        modulo.cadastra_modulo()

    def cad_aluno(self):
        try:
            tipo_cadastro = self.conexao.executa_fetchone(
                comando_sql='SELECT id FROM pessoa_tipousuario WHERE tipo_usuario="Aluno"'
            )[0]

            pessoa = Pessoa(
                nome=self.aluno_input_nome.displayText(),
                sobrenome=self.aluno_input_sobrenome.displayText(),
                data_nascimento=self.aluno_input_data_nasc.displayText(),
                cpf=self.aluno_input_cpf.displayText(),
                celular=self.aluno_input_celular.displayText(),
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
            aluno = Aluno(
                pessoa=pessoa,
                usuario=Usuario(
                    pessoa=pessoa,
                    tipo_usuario=tipo_cadastro
                )
            )
            aluno.cadastra_aluno()
        except Exception as e:
            print(e)
    #

    def cad_professor(self):
        try:
            tipo_cadastro = self.conexao.executa_fetchone(
                comando_sql='SELECT id FROM pessoa_tipousuario WHERE tipo_usuario="Professor"'
            )[0]

            pessoa = Pessoa(
                nome=self.professor_input_nome.displayText(),
                sobrenome=self.professor_input_sobrenome.displayText(),
                data_nascimento=self.professor_input_data_nasc.displayText(),
                cpf=self.professor_input_cpf.displayText(),
                celular=self.professor_input_celular.displayText(),
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
            professor = Professor(
                usuario=Usuario(
                    pessoa=pessoa,
                    tipo_usuario=tipo_cadastro,
                ),
                pessoa=pessoa,
                lingua=self.professor_input_lingua.currentText(),
                nivel=self.professor_input_nivel.currentText(),
            )
            professor.cadastrar_professor()
        except Exception as e:
            print(e)

    def cad_professor_modulo(self):
        try:
            modulos = self.professor_modulo_input_modulo.selectedItems()
            lista_modulo = []
            for modulo in modulos:
                lista_modulo.append(modulo.text().split(' -')[0])
            lista_modulo = tuple(lista_modulo)
            professor = Professor(
                pessoa=self.professor_modulo_input_professor.currentText(),
                modulo=lista_modulo
            )
            professor.vincula_professor_modulo()
        except Exception as e:
            print(e)

    def cad_aluno_modulo(self):
        try:
            modulos = self.aluno_modulo_input_modulo.selectedItems()
            lista_modulos = []
            for modulo in modulos:
                lista_modulos.append((modulo.text()).split(' -')[0])
            lista_modulos = tuple(lista_modulos)
            aluno = Aluno(
                pessoa=self.aluno_modulo_input_aluno.currentText(),
                modulo=lista_modulos
            )
            aluno.matricula_aluno_modulo()

        except Exception as e:
            print(e)

    # FIM DAS FUNCOES DE CADASTRO #

    # FUNCOES DE LIMPA CAMPO #
    def limpa_departamento(self):
        self.departamento_input_codigo.clear()

    def limpa_modulo(self):
        self.modulo_input_modulo.clear()
        self.modulo_input_codigo.clear()

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
            cpf=self.aluno_input_cpf,
            celular=self.aluno_input_celular,
        )
    #
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
            cpf=self.professor_input_cpf,
            celular=self.professor_input_celular,
        )

    # FIM FUNCOES DE LIMPA CAMPO #

    # OUTRAS FUNCOES #
    def input_professor_modulo(self):
        try:
            super().input_professor_modulo(
                input=self.professor_modulo_input_modulo,
                nome=(self.professor_modulo_input_professor.currentText()).split(' ')[0],
                sobrenome=(self.professor_modulo_input_professor.currentText()).split(' ')[1],
            )
        except Exception as e:
            pass


    def input_aluno_modulo(self):
        try:
            super().input_aluno_modulo(
                input=self.aluno_modulo_input_modulo,
                nome=(self.aluno_modulo_input_aluno.currentText()).split(' ')[0],
                sobrenome=(self.aluno_modulo_input_aluno.currentText()).split(' ')[1],
            )
        except Exception as e:
            pass

if __name__ == '__main__':
    pass