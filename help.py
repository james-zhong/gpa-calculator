import sys, ctypes, time
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QCursor

class Manual(QWidget):
    def __init__(self):
        super(Manual, self).__init__()
        
        # Define window properties
        self.setFixedSize(750, 600)
        self.setWindowTitle("Users Manual")
        self.setWindowIcon(QtGui.QIcon("assets/images/help.png")) # Window icon
        
        # Taskbar icon - seems like using ctypes is the only option???
        myappid = u'mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        time.sleep(1)
        
        # Custom font
        QtGui.QFontDatabase.addApplicationFont("assets/fonts/Poppins Light.ttf")
        QtGui.QFontDatabase.addApplicationFont("assets/fonts/Antic Regular.ttf")
        
        # Set the stylesheet
        with open('assets/styles/style_help.css', 'r') as css:
            self.setStyleSheet(css.read())
        
    def initUI(self):
        NotImplemented