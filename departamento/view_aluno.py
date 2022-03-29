from PyQt5 import QtWidgets, uic
from departamento.model import Aluno
from PyQt5.QtWidgets import QDialog
from departamento.view_base import DadosPessoa

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

if __name__ == '__main__':
    executa_menu_aluno()
