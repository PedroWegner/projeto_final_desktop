from PyQt5 import uic, QtWidgets
from departamento.views import CadastraAluno, VisualizaAluno, AtualizaAluno, CadastraDepartamento, CadastraCurso, \
    CadastraProfessor


class ViewMenu():
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.view = uic.loadUi('gui/main.ui')
        self.cadastro_aluno = CadastraAluno()
        self.visualiza_aluno = VisualizaAluno()
        self.atualiza_aluno = AtualizaAluno()
        self.cadastro_dep = CadastraDepartamento()
        self.cadastra_curso = CadastraCurso()
        self.cadastra_professor = CadastraProfessor()

    def exibe(self):
        self.view.cadastro_aluno.clicked.connect(self.cadastro_aluno.exibe_tela)
        self.view.visu_aluno.clicked.connect(self.visualiza_aluno.exibe_tela)
        self.view.att_aluno.clicked.connect(self.atualiza_aluno.exibe_tela)
        self.view.cadastro_dep.clicked.connect(self.cadastro_dep.exibe_tela)
        self.view.cadastra_curso.clicked.connect(self.cadastra_curso.exibe_tela)
        self.view.cadastra_curso.clicked.connect(self.cadastra_curso.exibe_tela)
        self.view.cadastro_professor.clicked.connect(self.cadastra_professor.exibe_tela)

        self.view.show()
        self.app.exec()


if __name__ == '__main__':
    view = ViewMenu()
    view.exibe()
