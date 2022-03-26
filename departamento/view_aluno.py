from PyQt5 import QtWidgets, uic
from departamento.views import UtilDepartamento, InformacoaPessoa
from departamento.views_usuario import AtualizarSenha
from departamento.model import Aluno
from pessoa.model import Usuario, Pessoa, Endereco
from banco_dados.model import ConexaoBD
from departamento.view_disciplina import TelaDisciplinaAluno
import sys
from PyQt5.QtWidgets import QDialog

# # global variable
# app = QtWidgets.QApplication(sys.argv)
# widget = QtWidgets.QStackedWidget()
#
#
# def executa_aluno(usuario_logado=None):
#     menu_aluno = MenuAluno(usuario_logado=usuario_logado)
#     menu_aluno.id_aluno()
#     widget.addWidget(menu_aluno)
#     widget.setFixedHeight(800)
#     widget.setFixedWidth(1600)
#     widget.show()
#     app.exec()
#
#
# class MenuAluno(QDialog, InformacoaPessoa):
#     def __init__(self, usuario_logado=None):
#         super(MenuAluno, self).__init__()
#
#         uic.loadUi(
#             r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\menu_aluno.ui',
#             self
#         )
#         self.usuario_logado = usuario_logado
#         self.btn = None
#
#         # funcoes construtoras
#         self.exibe_informacao()
#
#         # btns singal
#         self.atualiza_btn.clicked.connect(self.abre_atualiza_senha)
#         self.btn_matricular.clicked.connect(self.abre_matricular_disciplina)
#
#     def abre_atualiza_senha(self):
#         try:
#             menu_atualizar_aluno = MenuAlunoAtualiza(usuario_logado=self.usuario_logado)
#             widget.addWidget(menu_atualizar_aluno)
#             widget.setCurrentIndex(widget.currentIndex() + 1)
#         except Exception as e:
#             print(e)
#
#
#     def abre_matricular_disciplina(self):
#         try:
#             matricular_disciplina = MatriculaDisciplina(usuario_logado=self.usuario_logado)
#             widget.addWidget(matricular_disciplina)
#             widget.setCurrentIndex(widget.currentIndex() + 1)
#         except Exception as e:
#             print(e)
#
#
#     def exibe_informacao(self):
#         self.id_aluno()
#         self.exibi_disciplinas()
#         # messages
#         self.bem_vindo.setText(
#             f"Bem-vindo {self.usuario_logado['nome_pessoa']} {self.usuario_logado['sobrenome_pessoa']}")
#         # send logged user
#         # self.atualizar_senha.usuario_logado = self.usuario_logado
#         # self.menu_atualiza.usuario_logado = self.usuario_logado
#         # self.menu_matricula_disc.usuario_logado = self.usuario_logado
#         # buttons
#         # self.view.atualiza_btn.clicked.connect(self.menu_atualiza.exibe_tela)
#         # self.view.btn_matricular.clicked.connect(self.menu_matricula_disc.exibe_tela)
#         # self.view.atualizar_senha_btn.clicked.connect(self.atualizar_senha.exibe_tela)
#
#     def exibe_tela(self):
#         super().exibe_tela()
#
#
#     def exibi_disciplinas(self):
#         # clear no layout
#         comando_sql = f"SELECT DeDi.disciplina " \
#                       f"FROM departamento_aluno DeAl " \
#                       f"INNER JOIN departamento_aluno_disciplina DeAlDi " \
#                       f"ON DeAlDi.aluno_id = DeAl.id " \
#                       f"INNER JOIN departamento_disciplina DeDi " \
#                       f"ON DeDi.id = DeAlDi.disciplina_id " \
#                       f"WHERE DeAl.id={self.usuario_logado['id_aluno']}"
#         disciplinas_selecionadas = self.conexao.select_all(comando_sql=comando_sql)
#
#         for numero, disciplina in enumerate(disciplinas_selecionadas):
#             self.btn = QtWidgets.QPushButton(disciplina[0])
#             tela = TelaDisciplinaAluno(
#                 disciplina=disciplina[0],
#                 usuario_logado=self.usuario_logado
#             )
#             # ALTERAR AQUI
#             self.btn.clicked.connect(lambda ch, tela=tela: tela.exibe_tela())
#             if numero % 2 == 0:
#                 self.layout_1.addWidget(self.btn)
#             else:
#                 self.layout_2.addWidget(self.btn)
#
#     def abre_disciplina(self, disciplina=None):
#         pass
#
#     def id_aluno(self):
#         print(self.usuario_logado)
#         comando_sql = f"SELECT DeAl.id " \
#                       f"FROM pessoa_usuario PeUs " \
#                       f"INNER JOIN departamento_aluno DeAl " \
#                       f"ON PeUs.id = DeAl.usuario_id " \
#                       f"WHERE PeUs.id={self.usuario_logado['id_usuario']};"
#         self.usuario_logado.update(
#             {
#                 'id_aluno': self.conexao.executa_fetchone(comando_sql=comando_sql)[0],
#             }
#         )
#
#
# class MenuAlunoAtualiza(QDialog, InformacoaPessoa):  # InformacoaPessoa
#     def __init__(self, usuario_logado=None):
#         super(MenuAlunoAtualiza, self).__init__()
#
#         uic.loadUi(
#             r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\menu_atualiza_aluno.ui',
#             self
#         )
#         self.usuario_logado = usuario_logado
#         self.atualiza_btn.clicked.connect(self.atualiza_aluno)
#         self.voltar_btn.clicked.connect(self.volta)
#         self.exibe_output()
#
#     # def exibe_tela(self):
#     #     super().exibe_tela()
#     #     self.exibe_output()
#     #     self.view.atualiza_btn.clicked.connect(self.atualiza_aluno)
#
#     def volta(self):
#         try:
#             menu_aluno = MenuAluno(usuario_logado=self.usuario_logado)
#         except Exception as e:
#             print(e)
#         widget.addWidget(menu_aluno)
#         widget.setCurrentIndex(widget.currentIndex() + 1)
#
#     def atualiza_aluno(self):
#         pessoa = Pessoa()
#         pessoa.id = self.usuario_logado['id_pessoa']
#         pessoa.atualiza_pessoa(
#             nome=self.nome_input.displayText(),
#             sobrenome=self.sobrenome_input.displayText(),
#             data_nascimento=self.data_nasc_input.displayText(),
#             genero=self.genero_input.currentText(),
#             estado_civil=self.estado_civil_input.currentText(),
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
#         self.usuario_logado['nome_pessoa'] = self.nome_input.displayText()
#         self.usuario_logado['sobrenome_pessoa'] = self.sobrenome_input.displayText()
#         self.usuario_logado['data_nasc_pessoa'] = self.data_nasc_input.displayText()
#
#
# class MatriculaDisciplina(QDialog, UtilDepartamento):
#     def __init__(self, usuario_logado=None):
#         super(MatriculaDisciplina, self).__init__()
#         uic.loadUi(
#             r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\matricular_disciplina.ui',
#             self
#         )
#         self.usuario_logado = usuario_logado
#
#         # funcoes construtoras
#         self.exibe_output()
#
#         # btn singal
#         self.matricular_disc_btn.clicked.connect(self.matricular_disciplina)
#         self.voltar_btn.clicked.connect(self.volta)
#
#     def exibe_output(self):
#         super().exibe_output()
#         self.exibe_disciplinas()
#
#     def exibe_disciplinas(self):
#         self.disciplina_input.clear()
#         comando_sql = f"SELECT DeDi.disciplina " \
#                       f"FROM departamento_disciplina DeDi " \
#                       f"WHERE NOT EXISTS (" \
#                       f"SELECT * " \
#                       f"FROM departamento_aluno_disciplina DeAlDi " \
#                       f"WHERE DeDi.id = DeAlDi.disciplina_id AND DeAlDi.aluno_id={self.usuario_logado['id_aluno']}" \
#                       f")"
#         disciplinas = self.conexao.select_all(comando_sql=comando_sql)
#         for disciplina in disciplinas:
#             self.disciplina_input.addItem(disciplina[0])
#
#     def volta(self):
#         try:
#             menu_aluno = MenuAluno(usuario_logado=self.usuario_logado)
#         except Exception as e:
#             print(e)
#         widget.addWidget(menu_aluno)
#         widget.setCurrentIndex(widget.currentIndex() + 1)
#
#     def matricular_disciplina(self):
#         disc_selecionadas = self.disciplina_input.selectedItems()
#         disciplinas = []
#         for disciplina in disc_selecionadas:
#             disciplinas.append(disciplina.text())
#         disciplinas = tuple(disciplinas)
#
#         aluno = Aluno(disciplina=disciplinas)
#         aluno.id = self.usuario_logado['id_aluno']
#         aluno.matricula_disciplina()
####################################################
from departamento.view_base import MenuBase, DadosPessoa

app = QtWidgets.QApplication([])
widget = QtWidgets.QStackedWidget()


def executa_menu_aluno(usuario_logado=None):
    tela_aluno = TelaAluno(usuario_logado=usuario_logado)
    #
    widget.addWidget(tela_aluno)
    widget.setFixedHeight(864)
    widget.setFixedWidth(1536)
    widget.show()
    app.exec_()


class TelaAluno(QDialog, DadosPessoa):
    def __init__(self, usuario_logado=None):
        super(TelaAluno, self).__init__(usuario_logado=usuario_logado)
        uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\tela_menu_aluno.ui',
            self
        )
        self.id_aluno()
        self.btn = None

        # btn singals  - MENU - #
        # HOME
        self.home_construtor()
        self.menu_btn_home.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.menu_home))
        self.menu_btn_home.clicked.connect(self.home_construtor)

        # DISCIPLINAS
        self.menu_btn_disciplinas.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.menu_disciplinas))
        self.menu_btn_disciplinas.clicked.connect(self.disciplinas_construtor)

        # ATUALIZAR DADOS
        self.menu_btn_att_dados.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.menu_att_dados))
        self.menu_btn_att_dados.clicked.connect(self.att_dados_construtor)
        self.menu_btn_att_dados.clicked.connect(self.limpa_att_dados)
        self.att_dados_btn_att_dados.clicked.connect(self.att_dados)

        # ATUALIZAR SENHA
        self.menu_btn_att_senha.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.menu_att_senha))
        self.menu_btn_att_senha.clicked.connect(self.limpa_att_senha)
        self.att_senha_btn_visualizar_senha.clicked.connect(self.visualizar_senha)
        self.att_senha_btn_att_senha.clicked.connect(self.atualizar_senha)
        self.att_senha_btn_att_senha.clicked.connect(self.limpa_att_senha)

        # SOLICITAR DISCIPLINA
        self.menu_btn_solicitar_disciplina.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.menu_solicitar_disciplina))
        self.menu_btn_solicitar_disciplina.clicked.connect(self.solicitar_disciplina_construtor)
        self.solicitar_disciplina_btn_solicitar_disciplina.clicked.connect(self.solicitar_disciplina)
        self.solicitar_disciplina_btn_solicitar_disciplina.clicked.connect(self.solicitar_disciplina_construtor)

        # FIM btn singals  - MENU - #

    # DEFINE ID ALUNO LOGADO #
    def id_aluno(self):

        comando_sql = f"SELECT DeAl.id " \
                      f"FROM pessoa_usuario PeUs " \
                      f"INNER JOIN departamento_aluno DeAl " \
                      f"ON PeUs.id = DeAl.usuario_id " \
                      f"WHERE PeUs.id={self.usuario_logado['id_usuario']};"
        self.usuario_logado.update(
            {
                'id_aluno': self.conexao.executa_fetchone(comando_sql=comando_sql)[0],
            }
        )

    # FIM DEFINE ID ALUNO LOGADO #

    # CONSTRUTORES DE TELA #
    def home_construtor(self):
        self.home_label_bem_vindo.setText(
            f"Bem-vindo {self.usuario_logado['nome_pessoa']} {self.usuario_logado['sobrenome_pessoa']}"
        )

    def disciplinas_construtor(self):
        # coluna 1
        for i in reversed(range(self.disciplinas_layout_disciplina_1.count())):
            displina_removida = self.disciplinas_layout_disciplina_1.itemAt(i).widget()
            self.disciplinas_layout_disciplina_1.removeWidget(displina_removida)
            displina_removida.setParent(None)
        # coluna 2
        for i in reversed(range(self.disciplinas_layout_disciplina_2.count())):
            displina_removida = self.disciplinas_layout_disciplina_2.itemAt(i).widget()
            self.disciplinas_layout_disciplina_2.removeWidget(displina_removida)
            displina_removida.setParent(None)
        #
        comando_sql = f"SELECT DeDi.id, DeDi.disciplina " \
                      f"FROM departamento_aluno DeAl " \
                      f"INNER JOIN departamento_aluno_disciplina DeAlDi " \
                      f"ON DeAlDi.aluno_id = DeAl.id " \
                      f"INNER JOIN departamento_disciplina DeDi " \
                      f"ON DeDi.id = DeAlDi.disciplina_id " \
                      f"WHERE DeAl.id={self.usuario_logado['id_aluno']}"
        disciplinas_selecionadas = self.conexao.select_all(comando_sql=comando_sql)

        for numero, disciplina in enumerate(disciplinas_selecionadas):
                self.btn = QtWidgets.QPushButton(disciplina[1])
                dict_discplina = {
                    'id_disciplina': disciplina[0],
                    'disciplina': disciplina[1],
                }
                self.btn.clicked.connect(lambda ch, dict=dict_discplina: self.disciplina_construtor(dict_disciplina=dict))
                if numero % 2 == 0:
                    self.disciplinas_layout_disciplina_1.addWidget(self.btn)
                else:
                    self.disciplinas_layout_disciplina_2.addWidget(self.btn)

    def disciplina_construtor(self, dict_disciplina=None):
        self.menu_stacked.setCurrentWidget(self.disciplinas_disciplina)
        self.disciplina_label_disciplina.setText(f"{dict_disciplina['disciplina']}")

    def solicitar_disciplina_construtor(self):
        self.input_disciplinas(input=self.solicitar_disciplina_input_disciplinas)

    # FIM CONSTRUTORES DE TELA #

    # FUNCOES DE TELA #

    # DISCIPLINAS #



    # FIM DISCIPLINAS #

    # ATT DADOS #
    # def att_dados(self):
    #     super().att_dados(
    #         input_nome=self.att_dados_input_nome,
    #         input_sobrenome=self.att_dados_input_sobrenome,
    #         input_data_nasc=self.att_dados_input_data_nasc,
    #         input_genero=self.att_dados_input_genero,
    #         input_estado_civil=self.att_dados_input_estado_civil,
    #         input_rua=self.att_dados_input_rua,
    #         input_numero=self.att_dados_input_numero,
    #         input_bairro=self.att_dados_input_bairro,
    #         input_cep=self.att_dados_input_cep,
    #         input_cidade=self.att_dados_input_cidade,
    #         input_estado=self.att_dados_input_estado,
    #         input_tipo_end=self.att_dados_input_tipo_end,
    #     )
    # # FIM ATT DADOS #
    #
    # # SENHA #
    # def visualizar_senha(self):
    #     super().visualizar_senha(
    #         (
    #             self.att_senha_input_senha_antiga,
    #             self.att_senha_input_verifica_1,
    #             self.att_senha_input_verifica_2,
    #         )
    #     )
    #
    # def atualizar_senha(self):
    #     super().atualizar_senha(
    #         input_senha_antiga=self.att_senha_input_senha_antiga,
    #         input_senha_nova_1=self.att_senha_input_verifica_1,
    #         input_senha_nova_2=self.att_senha_input_verifica_2,
    #     )
    # FIM SENHA #

    # SOLICITA DISCIPLINA #
    def solicitar_disciplina(self):
        disc_selecionadas = self.solicitar_disciplina_input_disciplinas.selectedItems()
        disciplinas = []
        for disciplina in disc_selecionadas:
            disciplinas.append(disciplina.text())
        disciplinas = tuple(disciplinas)

        aluno = Aluno(disciplina=disciplinas)
        aluno.id = self.usuario_logado['id_aluno']
        aluno.matricula_disciplina()
    # FIM SOLICITA DISCIPLINA #

    # FIM FUNCOES DE TELA #

    # # FUNCOES DE LIMPA CAMPO #
    # def limpa_att_senha(self):
    #     self.att_senha_input_senha_antiga.clear()
    #     self.att_senha_input_verifica_1.clear()
    #     self.att_senha_input_verifica_2.clear()
    #
    # def limpa_att_dados(self):
    #     self.limpa_pessoa(
    #         rua=self.att_dados_input_rua,
    #         numero=self.att_dados_input_numero,
    #         bairro=self.att_dados_input_bairro,
    #         cep=self.att_dados_input_cep,
    #         cidade=self.att_dados_input_cidade,
    #         nome=self.att_dados_input_nome,
    #         sobrenome=self.att_dados_input_sobrenome,
    #         data_nasc=self.att_dados_input_data_nasc,
    #     )
    # # FIM FUNCOES DE LIMPA CAMPO #


##


if __name__ == '__main__':
    executa_menu_aluno()
