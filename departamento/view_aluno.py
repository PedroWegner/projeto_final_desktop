import os
import shutil

from PyQt5 import QtWidgets, uic
from departamento.model import Aluno
from PyQt5.QtWidgets import QDialog, QFileDialog
from departamento.view_base import DadosPessoa

app = QtWidgets.QApplication([])
widget = QtWidgets.QStackedWidget()


def executa_menu_aluno(usuario_logado=None):
    try:
        tela_aluno = TelaAluno(usuario_logado=usuario_logado)
        #
        widget.addWidget(tela_aluno)
        widget.setFixedHeight(864)
        widget.setFixedWidth(1536)
        widget.show()
        app.exec_()
    except Exception as e:
        print(e)


class TelaAluno(QDialog, DadosPessoa):
    def __init__(self, usuario_logado=None):
        try:
            super(TelaAluno, self).__init__(usuario_logado=usuario_logado)
            uic.loadUi(
                r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\tela_menu_aluno.ui',
                self
            )
            self.id_aluno()
            self.btn = None
            self.btn_aula = None

            # btn singals  - MENU - #
            # HOME
            self.home_construtor()
            self.menu_btn_home.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.menu_home))
            self.menu_btn_home.clicked.connect(self.home_construtor)

            # MODULOS
            self.menu_btn_modulos.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.menu_modulos))
            self.menu_btn_modulos.clicked.connect(self.modulos_construtor)

            # ATUALIZAR DADOS
            self.menu_btn_att_dados.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.menu_att_dados))
            self.menu_btn_att_dados.clicked.connect(self.att_dados_construtor)
            self.menu_btn_att_dados.clicked.connect(self.limpa_att_dados)
            self.att_dados_btn_att_dados.clicked.connect(self.att_dados)
            self.att_dados_btn_att_dados.clicked.connect(self.limpa_att_dados)

            # ATUALIZAR SENHA
            self.menu_btn_att_senha.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.menu_att_senha))
            self.menu_btn_att_senha.clicked.connect(self.limpa_att_senha)
            self.att_senha_btn_visualizar_senha.clicked.connect(self.visualizar_senha)
            self.att_senha_btn_att_senha.clicked.connect(self.atualizar_senha)
            self.att_senha_btn_att_senha.clicked.connect(self.limpa_att_senha)

        except Exception as e:
            print(e)
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

            comando_sql = f"SELECT DeMo.id, DeMo.modulo " \
                          f"FROM departamento_aluno DeAl " \
                          f"INNER JOIN departamento_aluno_modulo DeAlMo " \
                          f"ON DeAlMo.aluno_id = DeAl.id " \
                          f"INNER JOIN departamento_modulo DeMo " \
                          f"ON DeAlMo.modulo_id = DeMo.id " \
                          f"WHERE DeAl.id={self.usuario_logado['id_aluno']};"
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
        self.menu_stacked.setCurrentWidget(self.modulos_modulo)
        self.modulo_label_modulo.setText(f"{dict_modulo['modulo']}")

        for i in reversed(range(self.modulo_layout_aula.count())):
            aula_removida = self.modulo_layout_aula.itemAt(i).widget()
            self.modulo_layout_aula.removeWidget(aula_removida)
            aula_removida.setParent(None)

        comando_sql = f"SELECT DeAu.* " \
                      f"FROM departamento_aula_modulo DeAuMo " \
                      f"INNER JOIN departamento_aula DeAu " \
                      f"ON DeAuMo.aula_id = DeAu.id " \
                      f"WHERE DeAuMo.modulo_id ={dict_modulo['id_modulo']}"
        aulas = self.conexao.select_all(comando_sql=comando_sql)
        for x, aula in enumerate(aulas):
            dict_aula = {
                'id_aula': aula[0],
                'aula': aula[1],
                'conteudo': aula[2],
                'data_post': aula[3],
                'aula_gravada': aula[4],
                'professor': aula[5],
                'conteudo_download': aula[6],
                'nivel': aula[7],
            }
            self.btn_aula = QtWidgets.QPushButton(dict_aula['aula'])
            self.btn_aula.clicked.connect(lambda cd, dict=dict_aula: self.aula_construtor(dict_aula=dict_aula))
            self.modulo_layout_aula.addWidget(self.btn_aula)

            ##


    def aula_construtor(self, dict_aula=None):
        self.menu_stacked.setCurrentWidget(self.modulo_aula)
        self.aula_label_aula.setText(f"{dict_aula['aula']}")
        self.aula_label_conteudo.setText(f"{dict_aula['conteudo']}")
        self.aula_btn_download_conteudo.clicked.connect(lambda: self.salva_arquivo(arquivo_download=dict_aula['conteudo_download']))

    def salva_arquivo(self, arquivo_download=None):
        try:
            diretorio_arquivo = fr'C:\Users\pedro\Desktop\Trabalho Final Senai\trabalho_final_web\media\{arquivo_download}'
            diretorio_download, extensao = QFileDialog.getSaveFileName(
                parent=self.menu_stacked,
                caption='Salvar arquivo',
                directory=r'C:\Users\pedro\Desktop',
                initialFilter="Text files (*.txt)",
                filter=".txt",
            )
            diretorio_download = diretorio_download + extensao
            shutil.copy(diretorio_arquivo, diretorio_download)
        except Exception as e:
            print(e)

        # shutil.copy()

    # FIM CONSTRUTORES DE TELA #

    # FUNCOES DE TELA #

    # FIM FUNCOES DE TELA #

if __name__ == '__main__':
    executa_menu_aluno()
