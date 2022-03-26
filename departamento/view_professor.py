from PyQt5 import QtWidgets, uic, QtGui
from departamento.views import UtilDepartamento, InformacoaPessoa
from departamento.model import Professor
from pessoa.model import Usuario, Pessoa, Endereco
from departamento.views_usuario import AtualizarSenha
from departamento.view_disciplina import TelaDisciplinaProfessor
from banco_dados.model import ConexaoBD
import bcrypt
from PyQt5.QtWidgets import QDialog
import sys

# # global variables
# app = QtWidgets.QApplication(sys.argv)
# widget = QtWidgets.QStackedWidget()
#
#
# def executa_professor(usuario_logado=None):
#     menu_professor = MenuProfessor(usuario_logado=usuario_logado)
#     menu_professor.id_professor()
#     widget.addWidget(menu_professor)
#     widget.setFixedHeight(800)
#     widget.setFixedWidth(1600)
#     widget.show()
#     app.exec()
#
#
# class MenuProfessor(QDialog, UtilDepartamento):
#     def __init__(self, usuario_logado=None):
#         super(MenuProfessor, self).__init__()
#         uic.loadUi(
#             r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\menu_professor.ui',
#             self
#         )
#         self.usuario_logado = usuario_logado
#         self.dicionario_disciplina = {}
#         self.tela_disciplina = {}
#         self.btn = None
#         self.atualiza_senha = AtualizarSenha()
#
#         # chama funcao
#         self.exibe_informacao()
#
#     def exibe_informacao(self):
#         self.id_professor()
#         self.exibe_disciplinas()
#     # def exibe_tela(self):
#     #     super().exibe_tela()
#     #     self.id_professor()
#     #     self.exibe_disciplinas()
#     #     self.atualiza_senha.usuario_logado = self.usuario_logado
#     #     self.view.atualizar_senha_btn.clicked.connect(self.atualiza_senha.exibe_tela)
#         self.bem_vindo.setText(
#             f"Bem-vindo {self.usuario_logado['nome_pessoa']} {self.usuario_logado['sobrenome_pessoa']}")
#     #
#     def exibe_disciplinas(self):
#         comando_sql = f"SELECT * " \
#                       f"FROM departamento_disciplina DeDi " \
#                       f"INNER JOIN departamento_professor DePr " \
#                       f"ON DeDi.professor_id = DePr.id " \
#                       f"WHERE DePr.id={self.usuario_logado['id_professor']}"
#         discplinas_selecionas = self.conexao.select_all(comando_sql=comando_sql)
#
#         for numero, disciplina in enumerate(discplinas_selecionas):
#             self.btn = QtWidgets.QPushButton(disciplina[1])
#             tela = TelaDisciplinaProfessor(
#                 disciplina=disciplina[1],
#                 usuario_logado=self.usuario_logado,
#             )
#             self.btn.clicked.connect(lambda ch, tela=tela: tela.exibe_tela())
#             if numero % 2 == 0:
#                 self.layout_1.addWidget(self.btn)
#             else:
#                 self.layout_2.addWidget(self.btn)
#
#     def id_professor(self):
#         comando_sql = f"SELECT DePr.id " \
#                       f"FROM pessoa_usuario PeUs " \
#                       f"INNER JOIN departamento_professor DePr " \
#                       f"ON PeUs.id = DePr.usuario_id " \
#                       f"WHERE PeUs.id={self.usuario_logado['id_usuario']}"
#         self.usuario_logado.update(
#             {
#                 'id_professor': self.conexao.executa_fetchone(comando_sql=comando_sql)[0]
#             }
#         )
#
#
#
#
############################################
from departamento.view_base import MenuBase, DadosPessoa

app = QtWidgets.QApplication([])
widget = QtWidgets.QStackedWidget()


def executa_menu_professor(usuario_logado=None):
    tela_professor = TelaProfessor(usuario_logado=usuario_logado)
    #
    widget.addWidget(tela_professor)
    widget.setFixedHeight(864)
    widget.setFixedWidth(1536)
    widget.show()
    app.exec_()


class TelaProfessor(QDialog, DadosPessoa):
    def __init__(self, usuario_logado=None):
        super(TelaProfessor, self).__init__(usuario_logado=usuario_logado)
        uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\tela_menu_professor.ui',
            self
        )
        self.id_professor()
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

        # FIM btn singals  - MENU - #

    # DEFINE ID PROFESSOR LOGADO #
    def id_professor(self):
        comando_sql = f"SELECT DePr.id " \
                      f"FROM pessoa_usuario PeUs " \
                      f"INNER JOIN departamento_professor DePr " \
                      f"ON PeUs.id = DePr.usuario_id " \
                      f"WHERE PeUs.id={self.usuario_logado['id_usuario']}"
        self.usuario_logado.update(
            {
                'id_professor': self.conexao.executa_fetchone(comando_sql=comando_sql)[0]
            }
        )

    # FIM DEFINE ID PROFESSOR LOGADO #

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
        comando_sql = f"SELECT * " \
                      f"FROM departamento_disciplina DeDi " \
                      f"INNER JOIN departamento_professor DePr " \
                      f"ON DeDi.professor_id = DePr.id " \
                      f"WHERE DePr.id={self.usuario_logado['id_professor']}"
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
        try:
            self.menu_stacked.setCurrentWidget(self.disciplinas_disciplina)
            self.disciplina_label_disciplina.setText(f"{dict_disciplina['disciplina']}")
            self.disciplina_output_alunos_matriculados.clear()
            comando_sql = f"SELECT PePe.nome, PePe.sobrenome " \
                          f"FROM departamento_aluno_disciplina DeAlDi " \
                          f"INNER JOIN departamento_aluno DeAl " \
                          f"ON DeAlDi.aluno_id = DeAl.id " \
                          f"INNER JOIN pessoa_pessoa PePe " \
                          f"ON DeAl.pessoa_id = PePe.id " \
                          f"WHERE DeAlDi.disciplina_id={dict_disciplina['id_disciplina']};"
            alunos_matriculados = self.conexao.select_all(comando_sql=comando_sql)
            for aluno in alunos_matriculados:
                self.disciplina_output_alunos_matriculados.addItem(f"{aluno[0]} {aluno[1]}")
        except Exception as e:
            print(e)
    #
    # def att_dados_construtor(self):
    #     try:
    #         self.input_estado(input=self.att_dados_input_estado)
    #         self.input_genero(input=self.att_dados_input_genero)
    #         self.input_estado_civil(input=self.att_dados_input_estado_civil)
    #         self.input_tipo_endereco(input=self.att_dados_input_tipo_end)
    #     except Exception as e:
    #         print(e)

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
    #
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
    executa_menu_professor()
