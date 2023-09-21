import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

style = """
    * {
        background-color: #272822;
        color: #f8f8f2;
        font-family: Verdana;
    }


    QLabel#title {
        text-align: center;
        font-size: 20pt;
        border: 3px solid #2cde85;
        border-radius: 20px;
    }
    
    QLabel#test {
        border: 3px solid white;
    }

"""

grades = [
    "Low Not Achieved", "Not Achieved", "High Not Achieved",
    "Low Achieved", "Achieved", "High Achieved",
    "Low Merit", "Merit", "High Merit",
    "Low Excellence", "Excellence", "High Excellence"
]

class Calculator(QMainWindow):
    def __init__(self):
        super(Calculator, self).__init__()
        
        # Define window properties
        self.setFixedSize(1250, 750)
        self.setWindowTitle("NCEA GPA Calculator")
        self.setStyleSheet(style)
        
        self.initUI()
    
    # Function for creating a grade input and its respective label
    def createGradeInputs(self, grade, x, y):
        # Default properties of the label for the grade input
        self.label = QtWidgets.QLabel(self)
        self.label.setText(grade)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.move(x, y)

        self.input = QtWidgets.QLineEdit(self)
        self.input.setAlignment(QtCore.Qt.AlignCenter)
        self.input.resize(150, 75)
        self.input.move(x, y + 50)  # Adjust the vertical position as needed
        
    # Create and add widgets  
    def initUI(self):
        # Title
        self.header = QtWidgets.QLabel(self, objectName="title")
        self.header.setText("NCEA GPA Calculator")
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.resize(700, 50) # Resize so the text fits
        self.header.move(275, 25) # Move the title to the middle of the screen
        
        # Input boxes
        num_rows = 4
        num_columns = 3

def window():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = Calculator()
    win.show() # Show all the widgets applied to the window
    sys.exit(app.exec_()) # Close application when the X is pressed
    
# Run if ran from a script and not a library
if __name__ == "__main__":
    window()