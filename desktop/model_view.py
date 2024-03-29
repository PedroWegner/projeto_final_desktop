import bcrypt
from PyQt5 import uic, QtWidgets
from banco_dados.model import ConexaoBD
from departamento.view_aluno import executa_menu_aluno
from departamento.view_professor import executa_menu_professor
from departamento.view_administrador import executa_menu_adm


class TelaLogin:
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
        self.checa_tipo_usuario()

    def exibe(self):
        self.view.login_btn.clicked.connect(self.login)
        self.view.login_btn.clicked.connect(self.exibe_tela_restricao)

        self.view.show()
        self.app.exec()

    def exibe_tela_restricao(self):
        if self.usuario_logado['tipo_usuario'] == self.tipos_usuario['Aluno']:
            executa_menu_aluno(usuario_logado=self.usuario_logado)
        elif self.usuario_logado['tipo_usuario'] == self.tipos_usuario['Professor']:
            executa_menu_professor(usuario_logado=self.usuario_logado)
        elif self.usuario_logado['tipo_usuario'] == self.tipos_usuario['Administrador']:
            executa_menu_adm(usuario_logado=self.usuario_logado)

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
        tipos_usuario = self.conexao.select_all(comando_sql=comando_sql)
        for x, tipo_usuario in enumerate(tipos_usuario):
            self.tipos_usuario[tipo_usuario[1]] = tipo_usuario[0]


if __name__ == '__main__':
    view = TelaLogin()
    view.exibe()
