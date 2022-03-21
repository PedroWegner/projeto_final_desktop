from PyQt5 import QtWidgets, uic
from departamento.views import UtilDepartamento, InformacoaPessoa
from departamento.model import Professor
from pessoa.model import Usuario, Pessoa, Endereco
from banco_dados.model import ConexaoBD

class CadastraProfessor(InformacoaPessoa):
    def __init__(self):
        super().__init__()
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\cadastroprofessor.ui'
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
    def __init__(self):
        super().__init__()
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\menuprofessor.ui'
        )