from PyQt5 import QtWidgets, uic
from departamento.views import UtilDepartamento, InformacoaPessoa
from departamento.views_usuario import AtualizarSenha
from departamento.model import Aluno
from pessoa.model import Usuario, Pessoa, Endereco
from banco_dados.model import ConexaoBD
from departamento.view_disciplina import TelaDisciplinaAluno
import sys
from PyQt5.QtWidgets import QDialog

# global variable
app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()


def executa_aluno(usuario_logado=None):
    menu_aluno = MenuAluno(usuario_logado=usuario_logado)
    menu_aluno.id_aluno()
    widget.addWidget(menu_aluno)
    widget.setFixedHeight(800)
    widget.setFixedWidth(1600)
    widget.show()
    app.exec()


class MenuAluno(QDialog, InformacoaPessoa):
    def __init__(self, usuario_logado=None):
        super(MenuAluno, self).__init__()

        uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\menu_aluno.ui',
            self
        )
        self.usuario_logado = usuario_logado
        self.btn = None

        # funcoes construtoras
        self.exibe_informacao()

        # btns singal
        self.atualiza_btn.clicked.connect(self.abre_atualiza_senha)
        self.btn_matricular.clicked.connect(self.abre_matricular_disciplina)

    def abre_atualiza_senha(self):
        try:
            menu_atualizar_aluno = MenuAlunoAtualiza(usuario_logado=self.usuario_logado)
            widget.addWidget(menu_atualizar_aluno)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        except Exception as e:
            print(e)


    def abre_matricular_disciplina(self):
        try:
            matricular_disciplina = MatriculaDisciplina(usuario_logado=self.usuario_logado)
            widget.addWidget(matricular_disciplina)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        except Exception as e:
            print(e)


    def exibe_informacao(self):
        self.id_aluno()
        self.exibi_disciplinas()
        # messages
        self.bem_vindo.setText(
            f"Bem-vindo {self.usuario_logado['nome_pessoa']} {self.usuario_logado['sobrenome_pessoa']}")
        # send logged user
        # self.atualizar_senha.usuario_logado = self.usuario_logado
        # self.menu_atualiza.usuario_logado = self.usuario_logado
        # self.menu_matricula_disc.usuario_logado = self.usuario_logado
        # buttons
        # self.view.atualiza_btn.clicked.connect(self.menu_atualiza.exibe_tela)
        # self.view.btn_matricular.clicked.connect(self.menu_matricula_disc.exibe_tela)
        # self.view.atualizar_senha_btn.clicked.connect(self.atualizar_senha.exibe_tela)

    def exibe_tela(self):
        super().exibe_tela()


    def exibi_disciplinas(self):
        # clear no layout
        comando_sql = f"SELECT DeDi.disciplina " \
                      f"FROM departamento_aluno DeAl " \
                      f"INNER JOIN departamento_aluno_disciplina DeAlDi " \
                      f"ON DeAlDi.aluno_id = DeAl.id " \
                      f"INNER JOIN departamento_disciplina DeDi " \
                      f"ON DeDi.id = DeAlDi.disciplina_id " \
                      f"WHERE DeAl.id={self.usuario_logado['id_aluno']}"
        disciplinas_selecionadas = self.conexao.select_all(comando_sql=comando_sql)

        for numero, disciplina in enumerate(disciplinas_selecionadas):
            self.btn = QtWidgets.QPushButton(disciplina[0])
            tela = TelaDisciplinaAluno(
                disciplina=disciplina[0],
                usuario_logado=self.usuario_logado
            )
            # ALTERAR AQUI
            self.btn.clicked.connect(lambda ch, tela=tela: tela.exibe_tela())
            if numero % 2 == 0:
                self.layout_1.addWidget(self.btn)
            else:
                self.layout_2.addWidget(self.btn)

    def abre_disciplina(self, disciplina=None):
        pass

    def id_aluno(self):
        print(self.usuario_logado)
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


class MenuAlunoAtualiza(QDialog, InformacoaPessoa):  # InformacoaPessoa
    def __init__(self, usuario_logado=None):
        super(MenuAlunoAtualiza, self).__init__()

        uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\menu_atualiza_aluno.ui',
            self
        )
        self.usuario_logado = usuario_logado
        self.atualiza_btn.clicked.connect(self.atualiza_aluno)
        self.voltar_btn.clicked.connect(self.volta)
        self.exibe_output()

    # def exibe_tela(self):
    #     super().exibe_tela()
    #     self.exibe_output()
    #     self.view.atualiza_btn.clicked.connect(self.atualiza_aluno)

    def volta(self):
        try:
            menu_aluno = MenuAluno(usuario_logado=self.usuario_logado)
        except Exception as e:
            print(e)
        widget.addWidget(menu_aluno)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def atualiza_aluno(self):
        pessoa = Pessoa()
        pessoa.id = self.usuario_logado['id_pessoa']
        pessoa.atualiza_pessoa(
            nome=self.nome_input.displayText(),
            sobrenome=self.sobrenome_input.displayText(),
            data_nascimento=self.data_nasc_input.displayText(),
            genero=self.genero_input.currentText(),
            estado_civil=self.estado_civil_input.currentText(),
            endereco=Endereco(
                rua=self.rua_input.displayText(),
                numero=self.numero_input.displayText(),
                bairro=self.bairro_input.displayText(),
                cep=self.cep_input.displayText(),
                cidade=self.cidade_input.displayText(),
                estado=self.estado_input.currentText(),
                tipo_endereco=self.tipo_end_input.currentText(),
            )
        )
        self.usuario_logado['nome_pessoa'] = self.nome_input.displayText()
        self.usuario_logado['sobrenome_pessoa'] = self.sobrenome_input.displayText()
        self.usuario_logado['data_nasc_pessoa'] = self.data_nasc_input.displayText()


class MatriculaDisciplina(QDialog, UtilDepartamento):
    def __init__(self, usuario_logado=None):
        super(MatriculaDisciplina, self).__init__()
        uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\matricular_disciplina.ui',
            self
        )
        self.usuario_logado = usuario_logado

        # funcoes construtoras
        self.exibe_output()

        # btn singal
        self.matricular_disc_btn.clicked.connect(self.matricular_disciplina)
        self.voltar_btn.clicked.connect(self.volta)

    def exibe_output(self):
        super().exibe_output()
        self.exibe_disciplinas()

    def exibe_disciplinas(self):
        self.disciplina_input.clear()
        comando_sql = f"SELECT DeDi.disciplina " \
                      f"FROM departamento_disciplina DeDi " \
                      f"WHERE NOT EXISTS (" \
                      f"SELECT * " \
                      f"FROM departamento_aluno_disciplina DeAlDi " \
                      f"WHERE DeDi.id = DeAlDi.disciplina_id AND DeAlDi.aluno_id={self.usuario_logado['id_aluno']}" \
                      f")"
        disciplinas = self.conexao.select_all(comando_sql=comando_sql)
        for disciplina in disciplinas:
            self.disciplina_input.addItem(disciplina[0])

    def volta(self):
        try:
            menu_aluno = MenuAluno(usuario_logado=self.usuario_logado)
        except Exception as e:
            print(e)
        widget.addWidget(menu_aluno)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def matricular_disciplina(self):
        disc_selecionadas = self.disciplina_input.selectedItems()
        disciplinas = []
        for disciplina in disc_selecionadas:
            disciplinas.append(disciplina.text())
        disciplinas = tuple(disciplinas)

        aluno = Aluno(disciplina=disciplinas)
        aluno.id = self.usuario_logado['id_aluno']
        aluno.matricula_disciplina()
