import sys, re, ctypes, time
from math import ceil, floor
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QCursor

grades = [
    "Low Not Achieved", "Low Achieved", "Low Merit",
    "Low Excellence", "Not Achieved", "Achieved",
    "Merit", "Excellence", "High Not Achieved",
    "High Achieved", "High Merit", "High Excellence"
]

grade_multiplier = {
    "Low Not Achieved" : 1,
    "Not Achieved" : 2,
    "High Not Achieved" : 3,
    "Low Achieved" : 4,
    "Achieved" : 5,
    "High Achieved" : 6,
    "Low Merit" : 7,
    "Merit" : 8,
    "High Merit" : 9,
    "Low Excellence" : 10,
    "Excellence" : 11,
    "High Excellence" : 12
}
        
class Calculator(QMainWindow):
    def __init__(self):
        super(Calculator, self).__init__()

        # Define window properties
        self.setFixedSize(1118, 750)
        self.setWindowTitle("NCEA GPA Calculator")
        self.setWindowIcon(QtGui.QIcon("assets/images/icon.jpg")) # Window icon
        
        # Taskbar icon - seems like using ctypes is the only option???
        myappid = u'mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        time.sleep(1)
                
        # Custom font
        QtGui.QFontDatabase.addApplicationFont("assets/fonts/Poppins Light.ttf")
        QtGui.QFontDatabase.addApplicationFont("assets/fonts/Antic Regular.ttf")
        
        # Set the stylesheet
        with open('style.css', 'r') as css:
            self.setStyleSheet(css.read())
        
        # GPA variables
        self.inputs = {} # Storage for input boxes so it can be accessed through dictionary
        
        # Global variables for QLabel so it can be accessed in another function (idk if there's a better way to do it but it works so yes)
        self.gpa_label = None
        self.excellences_label = None
        self.high_excellences_label = None
        
        # Define UI variables
        # Define where the coordinates of the first input label should be
        self.startingLabel_X = 83
        self.startingLabel_Y = 100
        
        # Define where the coordinates of the first input box should be
        self.startingInput_X = self.startingLabel_X
        self.startingInput_Y = self.startingLabel_Y + 25
        
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
        
        # Reset input button
        self.reset = QtWidgets.QPushButton(self)
        self.reset.setText("Reset Input")
        self.reset.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.reset.clicked.connect(self.resetInput)
        self.reset.resize(252, 50)
        self.reset.move(83, 570)
        
        # Help button
        self.calc = QtWidgets.QPushButton(self)
        self.calc.setText("Help")
        self.calc.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.calc.resize(252, 50)
        self.calc.move(83, 645)
        
        # GPA display
        self.gpa_display = QtWidgets.QLabel(self, objectName="gpaDisplay")
        self.gpa_display.setText("GPA: No Input Given")
        self.gpa_display.setAlignment(QtCore.Qt.AlignCenter)
        self.gpa_display.resize(602, 50)
        self.gpa_display.move(433, 570)
        self.gpa_label = self.gpa_display
        
        # Labels for calculating how much excellences/high excellences needed to get their GPA to the respective grade
        self.excellences = QtWidgets.QLabel(self)
        self.excellences.setText("For Excellence:<br> ??? more Excellences required <br> ??? more High Excellences required")
        self.excellences.setAlignment(QtCore.Qt.AlignCenter)
        self.excellences.resize(311, 100)
        self.excellences.move(398, 620)
        self.excellences_label = self.excellences
        
        self.h_excellences = QtWidgets.QLabel(self)
        self.h_excellences.setText("For High Excellence:<br> ??? more High Excellences required")
        self.h_excellences.setAlignment(QtCore.Qt.AlignCenter)
        self.h_excellences.resize(311, 50)
        self.h_excellences.move(769, 645)
        self.high_excellences_label = self.h_excellences
    
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
        self.calculateGPA() # Calculate GPA
        
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
        
        """
        # Limit the amount of characters to 4
        if len(text) > 4:
            sender.setText(text[:4])
        """

    # Reset the text for all input boxes (called when reset button pressed)
    def resetInput(self):
        # Reset text
        self.gpa_display.setText("GPA: No Input Given")
        self.excellences.setText("For Excellence:<br> ??? more Excellences required <br> ??? more High Excellences required")
        self.h_excellences.setText("For High Excellence:<br> ??? more High Excellences required")
        
        # Reset inputs
        for grade in grades:
            self.inputs[grade].setText("0")

    def calculateGPA(self): # TODO: there has to be some way to optimise this so do that later
        totalGradeAmount = 0
        gradeWorth = 0 # Grade amount
        
        for grade in grades:
            currentInputBox = self.inputs[grade]
            
            if currentInputBox.text():
                currentInputValue = int(currentInputBox.text())
            
                # Skip if a grade has no input
                if currentInputValue != 0:
                    multiplier = grade_multiplier[grade]
                    
                    totalGradeAmount += currentInputValue
                    
                    # Use the multiplier to add 'worth'? to the grades
                    value = currentInputValue * multiplier
                    gradeWorth += value
        
        # Make sure that input is given
        if totalGradeAmount != 0:
            # Get average (round to 2 decimal places)
            gpa = round((gradeWorth / totalGradeAmount), 2)
            
            # TODO: there's probably an easier way to do this so find it later
            rounded_grade = gpa
            
            # Custom round (round up if decimal is <= 0.5 and down if > 0.5)
            if not gpa.is_integer():
                decimal = gpa - int(gpa)
                
                if decimal >= 0.5:
                    rounded_grade = ceil(gpa)
                else:
                    rounded_grade = floor(gpa)
            
            rounded_grade = next((grade for grade, value in grade_multiplier.items() if value == rounded_grade), None)
            
            self.gpa_display.setText(f"GPA: {gpa} ({rounded_grade})")
            
            # Calculate how many Excellences and High Excellences needed for a GPA of 11 or 12 respectively
            # Just used basic algebra to form an equation and rearranged for x in terms of totalGradeAmount and gradeWorth
            if gpa < 10.5:
                excellences_needed = ceil((21 * totalGradeAmount) - (2 * gradeWorth))
                high_excellences_needed = ceil(((21 * totalGradeAmount) - (2 * gradeWorth))/3)
                self.excellences_label.setText(f"For Excellence:<br>{excellences_needed} more Excellences required<br>{high_excellences_needed} more High Excellences Needed")
            else:
                self.excellences_label.setText("For Excellence:<br>Your GPA is already >= Excellence")

            if gpa < 11.5:
                high_excellences_needed = ceil((23 * totalGradeAmount) - (2 * gradeWorth))
                self.high_excellences_label.setText(f"For High Excellence:<br>{high_excellences_needed} more High Excellences required")
            else:
                self.high_excellences_label.setText("For High Excellence:<br>Your GPA is already High Excellence")
        else:
            self.gpa_display.setText("GPA: No Input Given")
            self.excellences_label.setText("For Excellence:<br> ??? more Excellences required<br> ??? more  High Excellences required")
            self.high_excellences_label.setText("For High Excellence:<br> ??? more High Excellences required")
            
def window():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = Calculator()
    win.show() # Show all the widgets applied to the window
    sys.exit(app.exec_()) # Close application when the X is pressed
    
# Run if ran from a script and not a library
if __name__ == "__main__":
    window()