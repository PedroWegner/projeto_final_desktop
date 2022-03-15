from PyQt5 import uic, QtWidgets
from banco_dados.model import ConexaoBD
from pessoa.model import Pessoa, Endereco, Usuario
from departamento.model import Aluno


class UtilAluno():
    def __init__(self):
        self.conexao = ConexaoBD()
        self.app = QtWidgets.QApplication([])
        self.view = None

    def exibe_tela(self):
        self.view.show()
        self.app.exec()

    def exibe_output(self):
        self.exibe_estado()
        self.exibe_estado_civil()
        self.exibe_genero()
        self.exibe_tipo_endereco()

    def exibe_genero(self):
        comando_sql = "SELECT * FROM pessoa_genero"
        generos = self.conexao.select_all(comando_sql)
        for genero in generos:
            self.view.genero_input.addItem(genero[1])

    def exibe_estado_civil(self):
        comando_sql = "SELECT * FROM pessoa_estadocivil"
        estados_civil = self.conexao.select_all(comando_sql)
        for estado_civil in estados_civil:
            self.view.estado_civil_input.addItem(estado_civil[1])

    def exibe_estado(self):
        comando_sql = "SELECT * FROM pessoa_estado"
        estados = self.conexao.select_all(comando_sql)
        for estado in estados:
            self.view.estado_input.addItem(estado[1])

    def exibe_tipo_endereco(self):
        comando_sql = "SELECT * FROM pessoa_tipoendereco"
        tipos_endereco = self.conexao.select_all(comando_sql)
        for tipo_endereco in tipos_endereco:
            self.view.tipo_end_input.addItem(tipo_endereco[1])


class CadastraAluno(UtilAluno):
    def __init__(self):
        super().__init__()
        # self.conexao = ConexaoBD()
        # self.app = QtWidgets.QApplication([])
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\cadastroaluno.ui')
        self.tipo_cadastro = None
        self.exibe_output()
        # self.exibe_estado()
        # self.exibe_estado_civil()
        # self.exibe_genero()
        # self.exibe_tipo_endereco()
        # self.exibe_curso()
        self.tipo_tela()

    def exibe_output(self):
        super().exibe_output()
        self.exibe_curso()

    def exibe_tela(self):
        super().exibe_tela()
        self.view.pushButton.clicked.connect(self.cadastro_de_pessoa)

    def tipo_tela(self):
        self.tipo_cadastro = self.conexao.executa_fetchone(
            comando_sql='SELECT id FROM pessoa_tipousuario WHERE tipo_usuario="Aluno"'
        )[0]

    def exibe_curso(self):
        comando_sql = "SELECT * FROM departamento_curso"
        cursos = self.conexao.select_all(comando_sql)
        for curso in cursos:
            self.view.curso_input.addItem(curso[1])

    # def exibe_genero(self):
    #     comando_sql = "SELECT * FROM pessoa_genero"
    #     generos = self.conexao.select_all(comando_sql)
    #     for genero in generos:
    #         self.view.genero_input.addItem(genero[1])
    #
    # def exibe_estado_civil(self):
    #     comando_sql = "SELECT * FROM pessoa_estadocivil"
    #     estados_civil = self.conexao.select_all(comando_sql)
    #     for estado_civil in estados_civil:
    #         self.view.estado_civil_input.addItem(estado_civil[1])
    #
    # def exibe_estado(self):
    #     comando_sql = "SELECT * FROM pessoa_estado"
    #     estados = self.conexao.select_all(comando_sql)
    #     for estado in estados:
    #         self.view.estado_input.addItem(estado[1])
    #
    # def exibe_tipo_endereco(self):
    #     comando_sql = "SELECT * FROM pessoa_tipoendereco"
    #     tipos_endereco = self.conexao.select_all(comando_sql)
    #     for tipo_endereco in tipos_endereco:
    #         self.view.tipo_end_input.addItem(tipo_endereco[1])
    #
    # def exibe_curso(self):
    #     comando_sql = "SELECT * FROM departamento_curso"
    #     cursos = self.conexao.select_all(comando_sql)
    #     for curso in cursos:
    #         self.view.curso_input.addItem(curso[1])

    def cadastro_de_pessoa(self):
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
        aluno = Aluno(
            pessoa=pessoa,
            usuario=Usuario(
                pessoa=pessoa,
                tipo_usuario=self.tipo_cadastro
            ),
            curso=self.view.curso_input.currentText()
        )
        aluno.cadastra_aluno()


class AtualizaAluno(UtilAluno):
    def __init__(self):
        super().__init__()
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\atualizaraluno.ui')
        self.exibe_output()

    def exibe_tela(self):
        super().exibe_tela()
        self.view.pushButton.clicked.connect(self.atualiza_aluno)

    def exibe_output(self):
        super().exibe_output()
        self.exibe_aluno()

    def exibe_aluno(self):
        comando_sql = "SELECT * FROM departamento_aluno"
        alunos = self.conexao.select_all(comando_sql)
        for aluno in alunos:
            self.view.lista_aluno.addItem(str(aluno[0]))

    def atualiza_aluno(self):
        aluno = Aluno(
            pessoa=self.view.lista_aluno.currentText()
        )
        aluno.atualiza_aluno(nome=self.view.nome_input.displayText(),
                             sobrenome=self.view.sobrenome_input.displayText(),
                             data_nascimento=self.view.data_nasc_input.displayText(),
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


class VisualizaAluno():
    def __init__(self):
        self.conexao = ConexaoBD()
        self.app = QtWidgets.QApplication([])
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\visualizaaluno.ui')

    def exibe_tela(self):
        self.exibe_aluno()

        self.view.show()
        self.app.exec()

    def exibe_aluno(self):
        # qtd_lista = self.view.listWidget.count()
        # print(qtd_lista)
        # for i in range(int(qtd_lista)):
        #     self.view.listWidget.row(i)

        comando_sql = "SELECT * FROM departamento_aluno"
        qtd_aluno = self.conexao.select_all(comando_sql=comando_sql)
        aluno = Aluno()
        for i in range(len(qtd_aluno)):
            self.view.listWidget.addItem(aluno.exibe_aluno(id_aluno=qtd_aluno[i][0])[0])
