from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *

class mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("VG_UI/mainwindow.ui", self)
        self.set_actions()

    def set_actions(self):
        self.B1.clicked.connect(self.buttonclicked)

    def buttonclicked(self):
        QMessageBox.about(self, "click", "yes")