import sys
import typing
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

style = """
    QWidget {
        background-color: #272822;
        color: white;
    }


    QLabel#title {
        text-align: center;
        font-size: 20pt;
    }

"""

class Calculator(QMainWindow):
    def __init__(self):
        super(Calculator, self).__init__()
        
        # Define window properties
        self.setFixedSize(1250, 750)
        self.setWindowTitle("NCEA GPA Calculator")
        self.setStyleSheet(style)
        
        self.initUI()
    
    # Create and add widgets  
    def initUI(self):
        # Title
        self.header = QtWidgets.QLabel(self, objectName="title")
        self.header.setText("NCEA GPA Calculator")
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.resize(1250, 50)
        self.header.move(0, 15)

def window():
    app = QApplication(sys.argv)
    win = Calculator()
    win.show() # Show all the widgets applied to the window
    sys.exit(app.exec_()) # Close application when the X is pressed
    
if __name__ == "__main__": # Run if ran from a script and not a library
    window()