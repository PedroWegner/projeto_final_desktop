from PyQt5 import QtWidgets, uic, QtGui
from departamento.views import UtilDepartamento, InformacoaPessoa
from departamento.model import Professor
from pessoa.model import Usuario, Pessoa, Endereco
from banco_dados.model import ConexaoBD
import bcrypt


class CadastraProfessor(InformacoaPessoa):
    def __init__(self):
        super().__init__()
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\cadastro_professor.ui'
        )
        self.tipo_cadastro = None

    def exibe_output(self):
        super().exibe_output()
        self.exibe_departamento()
        self.exibe_titulo()

    def exibe_tela(self):
        self.view.btn_cadastra.clicked.connect(self.cadastra_professor)
        self.tipo_tela()
        super().exibe_tela()
        self.exibe_output()

    def tipo_tela(self):
        self.tipo_cadastro = self.conexao.executa_fetchone(
            comando_sql='SELECT id FROM pessoa_tipousuario WHERE tipo_usuario="Professor"'
        )[0]

    def exibe_departamento(self):
        self.view.dep_input.clear()
        comando_sql = "SELECT * FROM departamento_departamento"
        departamentos = self.conexao.select_all(comando_sql=comando_sql)
        for departamento in departamentos:
            self.view.dep_input.addItem(departamento[1])

    def exibe_titulo(self):
        comando_sql = "SELECT * FROM departamento_tituloprofessor"
        titulos = self.conexao.select_all(comando_sql=comando_sql)
        for titulo in titulos:
            self.view.titulo_input.addItem(titulo[1])

    def cadastra_professor(self):
        pessoa = Pessoa(
            nome=self.view.nome_input.displayText(),
            sobrenome=self.view.sobrenome_input.displayText(),
            data_nascimento=self.view.data_nasc_input.displayText(),
            cpf=self.view.cpf_input.displayText(),
            estado_civil=self.view.estado_civil_input.currentText(),
            genero=self.view.genero_input.currentText(),
            endereco=Endereco(
                rua=self.view.rua_input.displayText(),
                numero=self.view.numero_input.displayText(),
                bairro=self.view.bairro_input.displayText(),
                cep=self.view.cep_input.displayText(),
                cidade=self.view.cidade_input.displayText(),
                estado=self.view.estado_input.currentText(),
                tipo_endereco=self.view.tipo_end_input.currentText(),
            )
        )
        pessoa.cadastrar_pessoa()

        departamentos = self.view.dep_input.selectedItems()
        departamento = []
        for dep in departamentos:
            departamento.append(dep.text())
        departamento = tuple(departamento)

        professor = Professor(
            titulo=self.view.titulo_input.currentText(),
            usuario=Usuario(
                pessoa=pessoa,
                tipo_usuario=self.tipo_cadastro,
            ),
            pessoa=pessoa,
            departamento=departamento
        )
        professor.cadastrar_professor()


class MenuProfessor(UtilDepartamento):
    def __init__(self, usuario_logado=None):
        super().__init__()
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\menu_professor.ui'
        )
        self.usuario_logado = usuario_logado
        self.dicionario_disciplina = {}
        self.tela_disciplina = {}
        self.btn = None
        self.atualiza_senha = AtualizarSenha()

    def exibe_tela(self):
        super().exibe_tela()
        self.id_professor()
        self.exibe_materias()
        self.atualiza_senha.usuario_logado = self.usuario_logado
        self.view.atualizar_senha_btn.clicked.connect(self.atualiza_senha.exibe_tela)
        self.view.bem_vindo.setText(
            f"Bem-vindo {self.usuario_logado['nome_pessoa']} {self.usuario_logado['sobrenome_pessoa']}")

    def exibe_materias(self):
        comando_sql = f"SELECT * " \
                      f"FROM departamento_disciplina DeDi " \
                      f"INNER JOIN departamento_professor DePr " \
                      f"ON DeDi.professor_id = DePr.id " \
                      f"WHERE DePr.id={self.usuario_logado['id_professor']}"
        discplinas_selecionas = self.conexao.select_all(comando_sql=comando_sql)

        for numero, disciplina in enumerate(discplinas_selecionas):
            self.btn = QtWidgets.QPushButton(disciplina[1])
            tela = TelaDisciplina(
                disciplina=disciplina[1],
                usuario_logado=self.usuario_logado,
            )
            self.btn.clicked.connect(lambda ch, tela=tela: tela.exibe_tela())
            if numero % 2 == 0:
                self.view.layout_1.addWidget(self.btn)
            else:
                self.view.layout_2.addWidget(self.btn)

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


class TelaDisciplina(UtilDepartamento):
    def __init__(self, disciplina=None, usuario_logado=None):
        super().__init__()
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\tela_disciplina.ui'
        )
        self.disciplina = disciplina
        self.usuario_logado = usuario_logado

    def exibe_tela(self):
        super().exibe_tela()
        self.view.label.setText(self.disciplina)

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

