from PyQt5 import uic, QtWidgets
from banco_dados.model import ConexaoBD
from pessoa.model import Pessoa, Endereco, Usuario
from departamento.model import Aluno, Departamento, Curso, Professor


class UtilDepartamento():
    def __init__(self):
        self.conexao = ConexaoBD()
        self.app = QtWidgets.QApplication([])
        self.view = None

    def exibe_output(self):
        pass

    def exibe_tela(self):
        self.view.show()
        self.app.exec()


class InformacoaPessoa(UtilDepartamento):
    def __init__(self):
        super().__init__()

    def exibe_output(self):
        super().exibe_output()
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


class CadastraDepartamento(UtilDepartamento):
    def __init__(self):
        super().__init__()
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\cadastrodepartamento.ui'
        )

    def exibe_tela(self):
        super().exibe_tela()
        self.view.btn_cadastra.clicked.connect(self.cadastro_dep)

    def cadastro_dep(self):
        departamento = Departamento(
            departamento=self.view.departamento_input.displayText(),
            cod_departamento=self.view.codigo_input.displayText(),
        )
        departamento.cadastra_departamento()


class CadastraCurso(UtilDepartamento):
    def __init__(self):
        super().__init__()
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\cadastrocurso.ui'
        )

    def exibe_tela(self):
        self.exibe_output()
        super().exibe_tela()

    def exibe_output(self):
        self.view.btn_cadastra.clicked.connect(self.cadastra_curso)
        super().exibe_output()
        self.exibe_turno()
        self.exibe_departamento()

    def exibe_departamento(self):
        self.view.dep_input.clear()
        comando_sql = "SELECT * FROM departamento_departamento"
        departamentos = self.conexao.select_all(comando_sql=comando_sql)
        for departamento in departamentos:
            self.view.dep_input.addItem(departamento[1])

    def exibe_turno(self):
        comando_sql = "SELECT * FROM departamento_turno"
        turnos = self.conexao.select_all(comando_sql=comando_sql)
        for turno in turnos:
            self.view.turno_input.addItem(turno[1])

    def cadastra_curso(self):
        departamentos = self.view.dep_input.selectedItems()
        dep = []
        for departamento in departamentos:
            dep.append(departamento.text())
        dep = tuple(dep)
        curso = Curso(
            curso=self.view.curso_input.displayText(),
            cod_curso=self.view.cod_input.displayText(),
            turno=self.view.turno_input.currentText(),
            departamento=dep,
        )
        curso.cadastra_curso()


class CadastraAluno(InformacoaPessoa):
    def __init__(self):
        super().__init__()
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\cadastroaluno.ui')
        self.tipo_cadastro = None

    def exibe_output(self):
        self.tipo_tela()
        super().exibe_output()
        self.exibe_curso()

    def exibe_tela(self):
        self.exibe_output()
        super().exibe_tela()
        self.view.pushButton.clicked.connect(self.cadastro_de_pessoa)

    def tipo_tela(self):
        self.tipo_cadastro = self.conexao.executa_fetchone(
            comando_sql='SELECT id FROM pessoa_tipousuario WHERE tipo_usuario="Aluno"'
        )[0]

    def exibe_curso(self):
        self.view.curso_input.clear()
        comando_sql = "SELECT * FROM departamento_curso"
        cursos = self.conexao.select_all(comando_sql=comando_sql)
        for curso in cursos:
            self.view.curso_input.addItem(curso[1])

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

        cursos = self.view.curso_input.selectedItems()
        curso = []
        for cur in cursos:
            curso.append(cur.text())
        curso = tuple(curso)

        aluno = Aluno(
            pessoa=pessoa,
            usuario=Usuario(
                pessoa=pessoa,
                tipo_usuario=self.tipo_cadastro
            ),
            curso=curso
        )
        aluno.cadastra_aluno()


class AtualizaAluno(InformacoaPessoa):
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
        aluno.atualiza_aluno(
            nome=self.view.nome_input.displayText(),
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


class VisualizaAluno():  # ARRUMA AQUI
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
        self.view.listWidget.clear()
        comando_sql = "SELECT * FROM departamento_aluno"
        qtd_aluno = self.conexao.select_all(comando_sql=comando_sql)
        aluno = Aluno()
        for i in range(len(qtd_aluno)):
            self.view.listWidget.addItem(aluno.exibe_aluno(id_aluno=qtd_aluno[i][0])[0])


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


class MenuAluno(UtilDepartamento):
    def __init__(self):
        super().__init__()
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\menualuno.ui'
        )
        self.tipo_usuario = None
        self.tipo_tela()

    def tipo_tela(self):
        self.tipo_usuario = self.conexao.executa_fetchone(
            comando_sql='SELECT id FROM pessoa_tipousuario WHERE tipo_usuario="Aluno"'
        )[0]


class MenuProfessor(UtilDepartamento):
    def __init__(self):
        super().__init__()
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\menuprofessor.ui'
        )