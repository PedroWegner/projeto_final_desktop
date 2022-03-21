import bcrypt
from PyQt5 import uic, QtWidgets
from banco_dados.model import ConexaoBD
from departamento.views import CadastraDepartamento, CadastraCurso, CadastraDisciplina
from departamento.view_aluno import CadastraAluno, VisualizaAluno, AtualizaAluno, MenuAluno
from departamento.view_professor import CadastraProfessor, MenuProfessor


class TelaLogin():
    def __init__(self):
        self.conexao = ConexaoBD()
        self.app = QtWidgets.QApplication([])
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\desktop\gui\telalogin.ui'
        )
        self.usuario = None
        self.tipos_usuario = {}
        self.usuario_logado = {
            'tipo_usuario': None
        }
        self.menu_aluno = MenuAluno()
        self.menu_professor = MenuProfessor()
        self.menu_admin = AreaAdministrativa()
        self.checa_tipo_usuario()

    def exibe(self):
        self.view.login_btn.clicked.connect(self.login)
        self.view.login_btn.clicked.connect(self.exibe_tela_restricao)

        self.view.show()
        self.app.exec()

    def exibe_tela_restricao(self):
        if self.usuario_logado['tipo_usuario'] == self.tipos_usuario['Aluno']:
            self.menu_aluno.usuario_logado = self.usuario_logado
            self.menu_aluno.exibe_tela()
            return
        elif self.usuario_logado['tipo_usuario'] == self.tipos_usuario['Professor']:
            self.menu_professor.usuario_logado = self.usuario_logado
            self.menu_professor.exibe_tela()
        elif self.usuario_logado['tipo_usuario'] == self.tipos_usuario['Administrador']:
            self.menu_admin.usuario_logado = self.usuario_logado
            self.menu_admin.exibe()

    def login(self):
        usuario_entrada = self.view.usuario_input.displayText()
        senha_entrada = self.view.senha_input.text()
        comando_sql = f"SELECT senha from pessoa_usuario WHERE usuario='{usuario_entrada}'"
        senha_criptografada = None
        try:
            senha_criptografada = self.conexao.executa_fetchone(comando_sql=comando_sql)[0]
        except:
            print('deu erro')
            return

        if bcrypt.checkpw(senha_entrada.encode('utf-8'), senha_criptografada.encode('utf-8')):
            comando_sql = f"SELECT PeUs.id, PePe.id, " \
                          f"PePe.nome, PePe.sobrenome, PePe.data_nascimento, PePe.cpf, " \
                          f"PeUs.usuario, PeUs.email, PeUs.tipo_usuario_id " \
                          f"FROM pessoa_usuario PeUs " \
                          f"INNER JOIN pessoa_pessoa PePe " \
                          f"ON PeUs.pessoa_id = PePe.id " \
                          f"WHERE PeUs.usuario = '{usuario_entrada}';"
            self.usuario_logado = self.conexao.executa_fetchone(comando_sql)
            self.usuario_logado = {
                'id_usuario': self.usuario_logado[0],
                'id_pessoa': self.usuario_logado[1],
                'nome_pessoa': self.usuario_logado[2],
                'sobrenome_pessoa': self.usuario_logado[3],
                'data_nasc_pessoa': self.usuario_logado[4],
                'cpf_pessoa': self.usuario_logado[5],
                'usuario': self.usuario_logado[6],
                'email_usuario': self.usuario_logado[7],
                'tipo_usuario': self.usuario_logado[8],
            }
        else:
            print("Usuario não logado")

    def checa_tipo_usuario(self):
        comando_sql = f"SELECT * FROM pessoa_tipousuario"
        self.tipos_usuario = self.conexao.select_all(comando_sql=comando_sql)
        self.tipos_usuario = {
            self.tipos_usuario[0][1]: self.tipos_usuario[0][0],
            self.tipos_usuario[1][1]: self.tipos_usuario[1][0],
            self.tipos_usuario[2][1]: self.tipos_usuario[2][0],
        }

    """
    self.tipo_tela_usuario = None
    
    NA CONDICAO, TENDO O TIPO DO USUARIO:
    self.tipo_tela_usuario = TELA_COM_RESTRICAO()
    """


class AreaAdministrativa():
    def __init__(self, usuario_logado=None):
        self.app = QtWidgets.QApplication([])
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\desktop\gui\main.ui'
        )
        self.usuario_logado = usuario_logado
        self.cadastro_aluno = CadastraAluno()
        self.visualiza_aluno = VisualizaAluno()
        self.atualiza_aluno = AtualizaAluno()
        self.cadastro_dep = CadastraDepartamento()
        self.cadastra_curso = CadastraCurso()
        self.cadastra_professor = CadastraProfessor()
        self.cadastra_disciplina = CadastraDisciplina()

    def exibe(self):
        self.view.cadastro_aluno.clicked.connect(self.cadastro_aluno.exibe_tela)
        self.view.visu_aluno.clicked.connect(self.visualiza_aluno.exibe_tela)
        self.view.att_aluno.clicked.connect(self.atualiza_aluno.exibe_tela)
        self.view.cadastro_dep.clicked.connect(self.cadastro_dep.exibe_tela)
        self.view.cadastra_curso.clicked.connect(self.cadastra_curso.exibe_tela)
        self.view.cadastra_curso.clicked.connect(self.cadastra_curso.exibe_tela)
        self.view.cadastro_professor.clicked.connect(self.cadastra_professor.exibe_tela)
        self.view.cadastra_disciplina.clicked.connect(self.cadastra_disciplina.exibe_tela)
        self.view.show()
        self.app.exec()


if __name__ == '__main__':
    view = TelaLogin()
    view.exibe()
