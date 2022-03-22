from PyQt5 import QtWidgets, uic
from departamento.views import UtilDepartamento, InformacoaPessoa
from departamento.model import Aluno
from pessoa.model import Usuario, Pessoa, Endereco
from banco_dados.model import ConexaoBD


class CadastraAluno(InformacoaPessoa):
    def __init__(self):
        super().__init__()
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\cadastro_aluno.ui')
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
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\atualizar_aluno.ui')
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
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\visualiza_aluno.ui')

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


class MenuAluno(UtilDepartamento):
    def __init__(self, usuario_logado=None):
        super().__init__()
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\menu_aluno.ui'
        )
        self.usuario_logado = usuario_logado
        self.menu_atualiza = MenuAlunoAtualiza()
        self.menu_matricula_disc = MatriculaDisciplina()

    def exibe_tela(self):
        super().exibe_tela()
        self.id_aluno()
        self.menu_atualiza.usuario_logado = self.usuario_logado
        self.menu_matricula_disc.usuario_logado = self.usuario_logado
        self.view.atualiza_btn.clicked.connect(self.menu_atualiza.exibe_tela)
        self.view.btn_matricular.clicked.connect(self.menu_matricula_disc.exibe_tela)

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


class MenuAlunoAtualiza(InformacoaPessoa):
    def __init__(self, usuario_logado=None):
        super().__init__()
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\menu_atualiza_aluno.ui'
        )
        self.usuario_logado = usuario_logado

    def exibe_tela(self):
        super().exibe_tela()
        self.exibe_output()
        self.view.atualiza_btn.clicked.connect(self.atualiza_aluno)

    def atualiza_aluno(self):
        pessoa = Pessoa()
        pessoa.id = self.usuario_logado['id_pessoa']
        pessoa.atualiza_pessoa(
            nome=self.view.nome_input.displayText(),
            sobrenome=self.view.sobrenome_input.displayText(),
            data_nascimento=self.view.data_nasc_input.displayText(),
            genero=self.view.genero_input.currentText(),
            estado_civil=self.view.estado_civil_input.currentText(),
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


class MatriculaDisciplina(UtilDepartamento):
    def __init__(self, usuario_logado=None):
        super().__init__()
        self.view = uic.loadUi(
            r'C:\Users\pedro\Desktop\Trabalho Final Senai\projeto_final_desktop\departamento\gui\matricular_disciplina.ui'
        )
        self.usuario_logado = usuario_logado

    def exibe_tela(self):
        super().exibe_tela()
        self.view.matricular_disc_btn.clicked.connect(self.matricular_disciplina)
        self.exibe_output()

    def exibe_output(self):
        super().exibe_output()
        self.exibe_disciplinas()

    def exibe_disciplinas(self):
        self.view.disciplina_input.clear()
        comando_sql = f"SELECT DeDi.disciplina " \
                      f"FROM departamento_disciplina DeDi " \
                      f"WHERE NOT EXISTS (" \
                      f"SELECT * " \
                      f"FROM departamento_aluno_disciplina DeAlDi " \
                      f"WHERE DeDi.id = DeAlDi.disciplina_id AND DeAlDi.aluno_id={self.usuario_logado['id_aluno']}" \
                      f")"
        disciplinas = self.conexao.select_all(comando_sql=comando_sql)
        for disciplina in disciplinas:
            self.view.disciplina_input.addItem(disciplina[0])

    def matricular_disciplina(self):
        disc_selecionadas = self.view.disciplina_input.selectedItems()
        disciplinas = []
        for disciplina in disc_selecionadas:
            disciplinas.append(disciplina.text())
        disciplinas = tuple(disciplinas)

        aluno = Aluno(disciplina=disciplinas)
        aluno.id = self.usuario_logado['id_aluno']
        aluno.matricula_disciplina()

