from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog
from departamento.view_base import DadosPessoa
from departamento.model import Aula
from datetime import datetime, date
import os
import shutil

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
            self.btn_modulo = None
            self.btn_aula = None

            # btn singals  - MENU - #
            # HOME
            self.home_construtor()
            self.menu_btn_home.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.menu_home))
            self.menu_btn_home.clicked.connect(self.home_construtor)

            # MODULOS
            self.menu_btn_modulos.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.menu_modulos))
            self.menu_btn_modulos.clicked.connect(self.modulos_construtor)

            # CRIAR AULA #

            self.menu_btn_aulas.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.menu_aulas))
            self.menu_btn_aulas.clicked.connect(self.aulas_construtor)
            #
            self.criar_aula_btn_criar_aula.clicked.connect(self.cad_criar_aula)
            self.criar_aula_btn_escolher_video.clicked.connect(
                lambda: self.seleciona_arquivo(input=self.criar_aula_input_video)
            )
            self.criar_aula_btn_escolher_conteudo.clicked.connect(
                lambda: self.seleciona_arquivo(input=self.criar_aula_input_conteudo_download)
            )
            self.aulas_btn_criar_aula.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.aulas_criar_aula))
            self.aulas_btn_criar_aula.clicked.connect(self.criar_aula_construtor)

            self.aulas_btn_vincula_aula_modulo.clicked.connect(lambda: self.menu_stacked.setCurrentWidget(self.aulas_vincula_aula_modulo))
            self.aulas_btn_vincula_aula_modulo.clicked.connect(self.vincula_aula_modulo_construtor)

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
                self.btn_modulo = QtWidgets.QPushButton(modulo[1])
                dict_modulo = {
                    'id_modulo': modulo[0],
                    'modulo': modulo[1],
                }
                self.btn_modulo.clicked.connect(lambda ch, dict=dict_modulo: self.modulo_construtor(dict_modulo=dict))
                if x % 2 == 0:
                    self.modulos_layout_modulo_1.addWidget(self.btn_modulo)
                else:
                    self.modulos_layout_modulo_2.addWidget(self.btn_modulo)
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

    def aulas_construtor(self):
        try:
            comando_sql = f"SELECT DeAu.id, DeAu.aula " \
                          f"FROM departamento_aula DeAu " \
                          f"WHERE DeAu.professor_id={self.usuario_logado['id_professor']}"
            aulas = self.conexao.select_all(comando_sql=comando_sql)
            for i in reversed(range(self.aulas_layout_aula_pronta.count())):
                objeto = self.aulas_layout_aula_pronta.itemAt(i).widget()
                self.aulas_layout_aula_pronta.removeWidget(objeto)
                objeto.setParent(None)
            if not aulas:
                aulas_label_aulas = QtWidgets.QLabel('Não há aulas cadastradas')
                self.aulas_layout_aula_pronta.addWidget(aulas_label_aulas)
            else:
                for x, aula in enumerate(aulas):
                    self.btn_aula = QtWidgets.QPushButton(aula[1])
                    id_aula = aula[0]
                    self.btn_aula.clicked.connect(lambda cd, id=id_aula: self.aula_construtor(id_aula=id_aula))
                    self.aulas_layout_aula_pronta.addWidget(self.btn_aula)
        except Exception as e:
            print(e)

    def aula_construtor(self, id_aula=None):
        try:
            comando_sql = f"SELECT * FROM departamento_aula WHERE id={id_aula}"
            dados = self.conexao.executa_fetchone(comando_sql=comando_sql)
            self.menu_stacked.setCurrentWidget(self.aulas_aula)
            self.aula_label_aula.setText(f"{dados[1]}")
            self.aula_label_conteudo.setText(f"{dados[2]}")

        except Exception as e:
            print(e)

    def vincula_aula_modulo_construtor(self):
        try:
            self.input_vincula_aula(input=self.vincula_aula_modulo_input_aula)
            self.input_vincula_modulo(input=self.vincula_aula_modulo_input_modulo)
        except Exception as e:
            print(e)

    def criar_aula_construtor(self):
        self.input_nivel(input=self.criar_aula_input_nivel)


    def input_vincula_aula(self, input=None):
        try:
            input.clear()
            comando_sql = f"SELECT DeAu.aula " \
                          f"FROM departamento_aula DeAu " \
                          f"WHERE DeAu.professor_id={self.usuario_logado['id_professor']}"
            aulas = self.conexao.select_all(comando_sql=comando_sql)
            for aula in aulas:
                input.addItem(f'{aula[0]}')
        except Exception as e:
            print(e)

    def input_vincula_modulo(self, input=None):
        try:
            input.clear()
            comando_sql = f"SELECT DeMo.id, DeMo.modulo, DeMo.nivel_id " \
                          f"FROM departamento_professor_modulo DePrMo " \
                          f"INNER JOIN departamento_modulo DeMo " \
                          f"ON DeMo.id = DePrMo.modulo_id WHERE professor_id = {self.usuario_logado['id_professor']};"
            modulos = self.conexao.select_all(comando_sql=comando_sql)
            for modulo in modulos:
                input.addItem(f'{modulo[1]}')
        except Exception as e:
            print(e)

    # FIM CONSTRUTORES DE TELA #

    # FUNCOES DE TELA #
    def cad_criar_aula(self):
        try:
            # ARQUIVOS
            video_aula = self.arquivo(input=self.criar_aula_input_video)
            conteudo_aula = self.arquivo(input=self.criar_aula_input_conteudo_download)
            #
            ano = date.today().strftime("%Y")
            mes = date.today().strftime("%m")

            # VIDEO AULA
            arquivo_video_aula = {
                'pasta_especifica': 'aula',
                'arquivo': video_aula,
                'ano': ano,
                'mes': mes,
            }
            self.copia_arquivo(
                dict=arquivo_video_aula,
                input=self.criar_aula_input_video,
            )

            # CONTEUDO AULA
            arquivo_conteudo_aula = {
                'pasta_especifica': 'conteudo_aula',
                'arquivo': conteudo_aula,
                'ano': ano,
                'mes': mes,

            }
            self.copia_arquivo(
                dict=arquivo_conteudo_aula,
                input=self.criar_aula_input_conteudo_download,
            )
            aula = Aula(
                aula=self.criar_aula_input_titulo_aula.displayText(),
                conteudo=self.criar_aula_input_conteudo.toPlainText(),
                aula_gravada=fr"{arquivo_video_aula['pasta_especifica']}\{arquivo_video_aula['ano']}\{arquivo_video_aula['mes']}\{arquivo_video_aula['arquivo']}",
                professor=self.usuario_logado['id_professor'],
                conteudo_aula=fr"{arquivo_conteudo_aula['pasta_especifica']}\{arquivo_conteudo_aula['ano']}\{arquivo_conteudo_aula['mes']}\{arquivo_conteudo_aula['arquivo']}",
                nivel=self.criar_aula_input_nivel.currentText()
            )
            aula.cadastrar_aula()

        except Exception as e:
            print(e)


    # DISCIPLINAS #

    # FIM DISCIPLINAS #


##


if __name__ == '__main__':
    data = date.today().strftime(r"%Y\%m")
    caminho_destino = fr'C:\Users\pedro\Desktop\Trabalho Final Senai\trabalho_final_web\media\conteudo_aula\{data}'
    print(caminho_destino)
