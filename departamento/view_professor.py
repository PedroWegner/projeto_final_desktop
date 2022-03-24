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

# global variables
app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()


def executa_professor(usuario_logado=None):
    menu_professor = MenuProfessor(usuario_logado=usuario_logado)
    menu_professor.id_professor()
    widget.addWidget(menu_professor)
    widget.setFixedHeight(800)
    widget.setFixedWidth(1600)
    widget.show()
    app.exec()


class MenuProfessor(QDialog, UtilDepartamento):
    def __init__(self, usuario_logado=None):
        super(MenuProfessor, self).__init__()
        uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\menu_professor.ui',
            self
        )
        self.usuario_logado = usuario_logado
        self.dicionario_disciplina = {}
        self.tela_disciplina = {}
        self.btn = None
        self.atualiza_senha = AtualizarSenha()

        # chama funcao
        self.exibe_informacao()

    def exibe_informacao(self):
        self.id_professor()
        self.exibe_disciplinas()
    # def exibe_tela(self):
    #     super().exibe_tela()
    #     self.id_professor()
    #     self.exibe_disciplinas()
    #     self.atualiza_senha.usuario_logado = self.usuario_logado
    #     self.view.atualizar_senha_btn.clicked.connect(self.atualiza_senha.exibe_tela)
        self.bem_vindo.setText(
            f"Bem-vindo {self.usuario_logado['nome_pessoa']} {self.usuario_logado['sobrenome_pessoa']}")
    #
    def exibe_disciplinas(self):
        comando_sql = f"SELECT * " \
                      f"FROM departamento_disciplina DeDi " \
                      f"INNER JOIN departamento_professor DePr " \
                      f"ON DeDi.professor_id = DePr.id " \
                      f"WHERE DePr.id={self.usuario_logado['id_professor']}"
        discplinas_selecionas = self.conexao.select_all(comando_sql=comando_sql)

        for numero, disciplina in enumerate(discplinas_selecionas):
            self.btn = QtWidgets.QPushButton(disciplina[1])
            tela = TelaDisciplinaProfessor(
                disciplina=disciplina[1],
                usuario_logado=self.usuario_logado,
            )
            self.btn.clicked.connect(lambda ch, tela=tela: tela.exibe_tela())
            if numero % 2 == 0:
                self.layout_1.addWidget(self.btn)
            else:
                self.layout_2.addWidget(self.btn)

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




