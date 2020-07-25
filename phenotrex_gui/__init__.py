"""Top-level package for Phenotrex-GUI."""
import sys

from PyQt5 import QtWidgets

from phenotrex_gui.ui.main_window import MainWindow

__author__ = """Lukas Lüftinger"""
__email__ = 'lukas.lueftinger@outlook.com'
__version__ = '0.0.1'


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
