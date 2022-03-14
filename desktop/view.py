from PyQt5 import uic, QtWidgets

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    view = uic.loadUi('gui/main.ui')

    view.show()
    app.exec()
