from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog
from departamento.view_base import DadosPessoa

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
        try:
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
            self.menu_btn_modulos.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.menu_modulos))
            self.menu_btn_modulos.clicked.connect(self.modulos_construtor)

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
        except Exception as e:
            print(e)

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

    def modulos_construtor(self):
        try:
            # coluna 1
            for i in reversed(range(self.modulos_layout_modulo_1.count())):
                modulo_removido = self.modulos_layout_modulo_1.itemAt(i).widget()
                self.modulos_layout_modulo_1.removeWidget(modulo_removido)
                modulo_removido.setParent(None)
            # coluna 2
            for i in reversed(range(self.modulos_layout_modulo_2.count())):
                modulo_removido = self.modulos_layout_modulo_2.itemAt(i).widget()
                self.modulos_layout_modulo_2.removeWidget(modulo_removido)
                modulo_removido.setParent(None)
            #
            comando_sql = f"SELECT * " \
                          f"FROM departamento_modulo DeMo " \
                          f"INNER JOIN departamento_professor_modulo DePrMo " \
                          f"ON DePrMo.modulo_id = DeMo.id " \
                          f"INNER JOIN departamento_professor DePr " \
                          f"ON DePrMo.professor_id = DePr.id " \
                          f"WHERE DePr.id={self.usuario_logado['id_professor']}"
            modulos_selecionados = self.conexao.select_all(comando_sql=comando_sql)
            for x, modulo in enumerate(modulos_selecionados):
                self.btn = QtWidgets.QPushButton(modulo[1])
                dict_modulo = {
                    'id_modulo': modulo[0],
                    'modulo': modulo[1],
                }
                self.btn.clicked.connect(lambda ch, dict=dict_modulo: self.modulo_construtor(dict_modulo=dict))
                if x % 2 == 0:
                    self.modulos_layout_modulo_1.addWidget(self.btn)
                else:
                    self.modulos_layout_modulo_2.addWidget(self.btn)
        except Exception as e:
            print(e)

    def modulo_construtor(self, dict_modulo=None):
        try:
            self.menu_stacked.setCurrentWidget(self.modulos_modulo)
            self.modulo_label_modulo.setText(f"{dict_modulo['modulo']}")
            self.modulo_output_alunos_matriculados.clear()
            comando_sql = f"SELECT PePe.nome, PePe.sobrenome " \
                          f"FROM departamento_aluno_modulo DeAlMo " \
                          f"INNER JOIN departamento_aluno DeAl " \
                          f"ON DeAlMo.aluno_id = DeAl.id " \
                          f"INNER JOIN pessoa_pessoa PePe " \
                          f"ON DeAl.pessoa_id = PePe.id " \
                          f"WHERE DeAlMo.modulo_id={dict_modulo['id_modulo']};"
            alunos_matriculados = self.conexao.select_all(comando_sql=comando_sql)
            for aluno in alunos_matriculados:
                self.modulo_output_alunos_matriculados.addItem(f"{aluno[0]} {aluno[1]}")
        except Exception as e:
            print(e)

    # FIM CONSTRUTORES DE TELA #

    # FUNCOES DE TELA #

    # DISCIPLINAS #

    # FIM DISCIPLINAS #
##


if __name__ == '__main__':
    executa_menu_professor()
