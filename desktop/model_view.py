from PyQt5 import uic, QtWidgets
from departamento.views import CadastraAluno, VisualizaAluno, AtualizaAluno


class ViewMenu():
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.view = uic.loadUi('gui/main.ui')
        self.cadastro_aluno = CadastraAluno()
        self.visualiza_aluno = VisualizaAluno()
        self.atualiza_aluno = AtualizaAluno()

    def exibe(self):
        self.view.cadastro_aluno.clicked.connect(self.cadastro_aluno.exibe_tela)
        self.view.visu_aluno.clicked.connect(self.visualiza_aluno.exibe_tela)
        self.view.att_aluno.clicked.connect(self.atualiza_aluno.exibe_tela)

        self.view.show()
        self.app.exec()


if __name__ == '__main__':
    view = ViewMenu()
    view.exibe()
