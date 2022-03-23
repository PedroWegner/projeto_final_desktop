from PyQt5 import uic, QtWidgets
from departamento.views import UtilDepartamento
from pessoa.model import Usuario
import bcrypt

# ALTERAR O MODULO DESTA CLASS
class AtualizarSenha(UtilDepartamento):
    def __init__(self, usuario_logado=None):
        super().__init__()
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\atualizar_senha.ui'
        )
        self.usuario_logado = usuario_logado

    def exibe_tela(self):
        super().exibe_tela()
        self.view.visualizar_senha_btn.clicked.connect(self.visualizar_senha)
        self.view.atualizar_senha_btn.clicked.connect(self.atualizar_senha)

    def visualizar_senha(self):
        self.view.senha_antiga.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.view.nova_input_1.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.view.nova_input_2.setEchoMode(QtWidgets.QLineEdit.Normal)

    def atualizar_senha(self):
        comando_sql = f"SELECT senha FROM pessoa_usuario WHERE usuario='{self.usuario_logado['usuario']}'"
        senha_criptografada = None
        senha_antiga = self.view.senha_antiga.text()
        senha_nova_1 = self.view.nova_input_1.text()
        senha_nova_2 = self.view.nova_input_2.text()

        try:
            senha_criptografada = self.conexao.executa_fetchone(comando_sql=comando_sql)[0]
        except:
            print('deu erro')
            return

        if bcrypt.checkpw(senha_antiga.encode('utf-8'), senha_criptografada.encode('utf-8')):
            if senha_nova_1 == senha_nova_2:
                usuario = Usuario()
                usuario.id = self.usuario_logado['id_usuario']
                usuario.atualiza_senha(senha_nova=senha_nova_1)
            else:
                print("Senhas incompativeis")
