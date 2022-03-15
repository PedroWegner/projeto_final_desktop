from PyQt5 import uic, QtWidgets
from banco_dados.model import ConexaoBD
from pessoa.model import Pessoa, Endereco, Usuario
from departamento.model import Aluno



if __name__ == '__main__':
    view_aluno = CadastraAluno()

    view_aluno.exibe_tela()
