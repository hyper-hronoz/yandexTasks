from os import terminal_size
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QMessageBox
from res.dist.templates.ViewTemplate import Ui_MainWindow as Window

class PopUpError(Exception):
    def __init__(self, context, message) -> None:
        self.message = message
        QMessageBox.about(context, "Error", message)

    def __str__(self):
        return f'{self.salary} -> {self.message}'

class MainView(QMainWindow):
    
    def __init__(self):
        super(MainView, self).__init__()
        self.window = Window()
        self.window.setupUi(self)

    def setImage(self, pixmap):
        self.window.label.setPixmap(pixmap)


