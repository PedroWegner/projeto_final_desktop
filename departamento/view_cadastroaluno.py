from PyQt5 import uic, QtWidgets
from banco_dados.model import ConexaoBD
from pessoa.model import Pessoa, Endereco, Usuario
from departamento.model import Aluno

conexao = ConexaoBD()
tipo_cadastro = conexao.executa_fetchone(
    comando_sql='SELECT id FROM pessoa_tipousuario WHERE tipo_usuario="Aluno"'
)[0]


def exibe_genero():
    comando_sql = "SELECT * FROM pessoa_genero"
    generos = conexao.select_all(comando_sql)
    for genero in generos:
        view.genero_input.addItem(genero[1])


def exibe_estado_civil():
    comando_sql = "SELECT * FROM pessoa_estadocivil"
    estados_civil = conexao.select_all(comando_sql)
    for estado_civil in estados_civil:
        view.estado_civil_input.addItem(estado_civil[1])


def exibe_estado():
    comando_sql = "SELECT * FROM pessoa_estado"
    estados = conexao.select_all(comando_sql)
    for estado in estados:
        view.estado_input.addItem(estado[1])


def exibe_tipo_endereco():
    comando_sql = "SELECT * FROM pessoa_tipoendereco"
    tipos_endereco = conexao.select_all(comando_sql)
    for tipo_endereco in tipos_endereco:
        view.tipo_end_input.addItem(tipo_endereco[1])


def exibe_curso():
    comando_sql = "SELECT * FROM departamento_curso"
    cursos = conexao.select_all(comando_sql)
    for curso in cursos:
        view.curso_input.addItem(curso[1])


def cadastro_de_pessoa():
    aluno = Aluno(
        Usuario(
            pessoa=Pessoa(
                nome=view.nome_input.displayText(),
                sobrenome=view.sobrenome_input.displayText(),
                data_nascimento=view.data_nasc_input.displayText(),
                cpf=view.cpf_input.displayText(),
                estado_civil=view.estado_civil_input.currentText(),
                genero=view.genero_input.currentText(),
                endereco=Endereco(
                    rua=view.rua_input.displayText(),
                    numero=view.numero_input.displayText(),
                    bairro=view.bairro_input.displayText(),
                    cep=view.cep_input.displayText(),
                    cidade=view.cidade_input.displayText(),
                    estado=view.estado_input.currentText(),
                    tipo_endereco=view.tipo_end_input.currentText(),
                ),
            ),
            tipo_perfil=tipo_cadastro
        ),
        curso=view.curso_input.currentText(),
    )


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    view = uic.loadUi('gui/cadastroaluno.ui')

    exibe_estado()
    exibe_estado_civil()
    exibe_genero()
    exibe_tipo_endereco()
    exibe_curso()

    view.pushButton.clicked.connect(cadastro_de_pessoa)

    view.show()
    app.exec()
