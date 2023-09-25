import sys, re
from statistics import mean
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QCursor, QFont

grades = [
    "Low Not Achieved", "Low Achieved", "Low Merit",
    "Low Excellence", "Not Achieved", "Achieved",
    "Merit", "Excellence", "High Not Achieved",
    "High Achieved", "High Merit", "High Excellence"
]
        
class Calculator(QMainWindow):
    def __init__(self):
        super(Calculator, self).__init__()

        # Define window properties
        self.setFixedSize(1118, 750)
        self.setWindowTitle("NCEA GPA Calculator")
        
        # Custom font
        QtGui.QFontDatabase.addApplicationFont("assets/Poppins Light.ttf")
        QtGui.QFontDatabase.addApplicationFont("assets/Antic Regular.ttf")
        
        # Set the stylesheet
        with open('style.css', 'r') as css_file:
            self.setStyleSheet(css_file.read())
        
        # Define UI variables
        
        # Define where the coordinates of the first input label should be
        self.startingLabel_X = 83
        self.startingLabel_Y = 100
        
        # Define where the coordinates of the first input box should be
        self.startingInput_X = self.startingLabel_X
        self.startingInput_Y = self.startingLabel_Y + 25
        
        # Storage for input boxes so it can be accessed through dictionary
        self.inputs = {}
        
        # Store the value of all input boxes
        self.values = {}
        
        # Create all the widgets
        self.initUI()
        
    # Create and add widgets  
    def initUI(self):
        # Title
        self.header = QtWidgets.QLabel(self, objectName="title")
        self.header.setText("NCEA GPA Calculator")
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.resize(700, 50) # Resize so the text fits
        self.header.move(209, 25) # Move the title to the middle of the screen
        
        # Input boxes
        rows = 3
        columns = 4
        
        for row in range(rows):
            for column in range(columns):
                index = row * 4 + column
                grade = grades[index]
                
                self.createGradeInputs(grade, row, column)
                
        # Calculate GPA button
        self.calc = QtWidgets.QPushButton(self)
        self.calc.setText("Calculate GPA")
        self.calc.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.calc.clicked.connect(self.calculateGPA)
        self.calc.resize(252, 50)
        self.calc.move(83, 570)
        
        # Reset input button
        self.reset = QtWidgets.QPushButton(self)
        self.reset.setText("Reset Input")
        self.reset.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.reset.clicked.connect(self.resetInput)
        self.reset.resize(252, 50)
        self.reset.move(83, 645)

    # Function for creating a grade input and its respective label
    def createGradeInputs(self, grade, row, column):
        # Create input label
        self.label = QtWidgets.QLabel(self, objectName="input_title")
        self.label.setText(grade)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.resize(252, 25)
        self.label.move(self.startingLabel_X + (row * 350), self.startingLabel_Y + (column * 115)) # Move according to the row and column
        
        # Create input box
        self.input = QtWidgets.QLineEdit(self, objectName="input_box")
        self.input.setAlignment(QtCore.Qt.AlignCenter)
        self.input.setText("0")
        self.input.resize(252, 50) 
        self.input.move(self.startingInput_X + (row * 350), self.startingInput_Y + (column * 115))  # Adjust the vertical position as needed
        
        # Store input box in dictonary so it can be accessed inividually
        self.inputs[grade] = self.input
        
        # Check when text gets changed in input box
        self.input.textChanged.connect(self.onInputTextChanged)
    
    def onInputTextChanged(self):
        sender = self.sender() # Widget that changed text
        text = sender.text()
        
        # Ensure that only numbers can be typed
        numeric_text = re.sub(r'[^0-9]', '', text)
        sender.setText(numeric_text)
        
        # Set text to 0 if input box is empty
        if text == "":
            sender.setText("0")   
        elif text[0] == "0" and text != "0": # Remove the "0" in front of number when not empty
            sender.setText(text.lstrip("0"))

    # Reset the text for all input boxes (called when reset button pressed)
    def resetInput(self):
        for grade in grades:
            self.inputs[grade].setText("0")
    
    def calculateGPA(self):
        print("a")

def window():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = Calculator()
    win.show() # Show all the widgets applied to the window
    sys.exit(app.exec_()) # Close application when the X is pressed
    
# Run if ran from a script and not a library
if __name__ == "__main__":
    window()