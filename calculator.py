import sys, re, ctypes, time, pickle, help
from math import ceil, floor
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QCursor

grades = [
    "Low Not Achieved", 
    "Low Achieved", 
    "Low Merit",
    "Low Excellence", 
    "Not Achieved", 
    "Achieved",
    "Merit", 
    "Excellence", 
    "High Not Achieved",
    "High Achieved", 
    "High Merit", 
    "High Excellence"
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

reversed_grade_multiplier = {value: grade for grade, value, in grade_multiplier.items()}

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
        with open('assets/styles/style_main.css', 'r') as css:
            self.setStyleSheet(css.read())
        
        # GPA variables
        
        # Try loading from save
        
        self.inputs = {}
        
        # Global variables for QLabel so it can be accessed in another function (idk if there's a better way to do it but it works so yes)
        self.gpa_label = None
        self.excellences_label = None
        self.high_excellences_label = None
        self.save_outcome = None
        self.load_outcome = None
        
        # Define UI variables
        # Define where the coordinates of the first input label should be
        self.startingLabel_X = 83
        self.startingLabel_Y = 115
        
        # Define where the coordinates of the first input box should be
        self.startingInput_X = self.startingLabel_X
        self.startingInput_Y = self.startingLabel_Y + 25
        
        # Create all the widgets
        self.init_ui()
    
    # Create and add widgets  
    def init_ui(self):
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
                
                self.create_grade_input(grade, row, column)
        
        # Reset input button
        self.reset = QtWidgets.QPushButton(self)
        self.reset.setText("Reset Input")
        self.reset.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.reset.clicked.connect(self.reset_input)
        self.reset.resize(252, 50)
        self.reset.move(83, 570)
        
        # Help button
        self.help_button = QtWidgets.QPushButton(self)
        self.help_button.setText("Help")
        self.help_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.help_button.clicked.connect(self.show_help_window)
        self.help_button.resize(252, 50)
        self.help_button.move(83, 645)
        
        # GPA display
        self.gpa_display = QtWidgets.QLabel(self, objectName="gpa_display")
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
        
        # Save data outcome
        self.save_label = QtWidgets.QLabel(self)
        self.save_label.resize(275, 50)
        self.save_label.move(50, 0)
        self.save_outcome = self.save_label
        
        # Load data outcome
        self.load_label = QtWidgets.QLabel(self)
        self.load_label.resize(275, 50)
        self.load_label.move(50, 55)
        self.load_outcome = self.load_label
        
        # Save data button
        self.save_button = QtWidgets.QPushButton(self, objectName="save")
        self.save_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.save_button.clicked.connect(self.save)
        self.save_button.resize(50, 50)
        
        # Load data button
        self.load_button = QtWidgets.QPushButton(self, objectName="load")
        self.load_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.load_button.clicked.connect(self.load)
        
        self.load_button.resize(50, 50)
        self.load_button.move(0, 55)
    
    # Function for creating a grade input and its respective label
    def create_grade_input(self, grade, row, column):
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
        self.input.textChanged.connect(self.input_text_changed)
    
    def input_text_changed(self):
        self.calculate_gpa() # Calculate GPA
        
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

    def reset_input(self):
        # Reset text
        self.gpa_display.setText("GPA: No Input Given")
        self.excellences.setText("For Excellence:<br> ??? more Excellences required <br> ??? more High Excellences required")
        self.h_excellences.setText("For High Excellence:<br> ??? more High Excellences required")
        
        # Reset inputs
        for grade in grades:
            self.inputs[grade].setText("0")

    def calculate_gpa(self):
        totalGradeAmount = 0
        gradeWorth = 0
        grades = self.inputs.keys()

        # Get all the inputs to convert into grade worth and total amount of grades received
        for grade in grades:
            currentInputBox = self.inputs[grade]
            currentInputValue = currentInputBox.text()
            
            if currentInputValue:
                currentInputValue = int(currentInputValue)
                multiplier = grade_multiplier[grade]
                
                if currentInputValue != 0:
                    # Calculate total grades received
                    totalGradeAmount += currentInputValue
                    
                    # Calculate grade worth
                    value = currentInputValue * multiplier
                    gradeWorth += value
        
        if totalGradeAmount != 0:
            gpa = round((gradeWorth / totalGradeAmount), 2)
            rounded_grade = round(gpa)
            
            # (Is there a built in function for this???)
            # Custom round - round up when decimal portion is >= 0.5 and round down when < 0.5
            if not gpa.is_integer():
                decimal = gpa - int(gpa)
                
                if decimal >= 0.5:
                    rounded_grade = ceil(gpa)
                else:
                    rounded_grade = floor(gpa)
            
            # Get the GPA in word form and display it
            rounded_grade = reversed_grade_multiplier[rounded_grade]
            self.gpa_display.setText(f"GPA: {gpa} ({rounded_grade})")

            # Calculate amount of E/High E required to raise grade to respective amount 
            excellences_needed = ceil((21 * totalGradeAmount) - (2 * gradeWorth))
            high_excellences_for_e = ceil(((21 * totalGradeAmount) - (2 * gradeWorth)) / 3)
            high_excellences_needed = ceil((23 * totalGradeAmount) - (2 * gradeWorth))

            # Displaying GPA requirements
            if gpa < 10.5:
                self.excellences_label.setText(f"For Excellence:<br>{excellences_needed} more Excellences required<br>{high_excellences_for_e} more High Excellences Needed")
            else:
                self.excellences_label.setText("For Excellence:<br>Your GPA is already ≥ Excellence")

            if gpa < 11.5:
                self.high_excellences_label.setText(f"For High Excellence:<br>{high_excellences_needed} more High Excellences required")
            else:
                self.high_excellences_label.setText("For High Excellence:<br>Your GPA is already High Excellence")
        else:
            self.gpa_display.setText("GPA: No Input Given")
            self.excellences_label.setText("For Excellence:<br> ??? more Excellences required<br> ??? more High Excellences required")
            self.high_excellences_label.setText("For High Excellence:<br> ??? more High Excellences required")

    def show_help_window(self):
        self.helpWindow = help.Manual()
        self.helpWindow.show()

    # Loading and saving data functions
    def save(self):
        try:
            with open("assets/save/data.vault", "wb") as file:
                # Convert data to be saved into strings (pickle cannot serialize QLineEdit)
                data = {grade: self.inputs[grade].text() for grade in grades}
                pickle.dump(data, file)
                
            self.save_outcome.setText("Saved successfully")
        except:
            self.save_outcome.setText("Could not save")
        
        timer = QtCore.QTimer(self)
        timer.timeout.connect(lambda: self.save_outcome.setText(""))
        timer.start(1250)

    def load(self):
        try:
            with open("assets/save/data.vault", "rb") as file:
                self.values = dict(pickle.load(file))
                
                # Change all the input to last save
                for grade in grades:
                    self.inputs[grade].setText(self.values[grade])
                
                # Display outcome
                self.load_outcome.setText("Loaded last saved data")
        except:
            self.load_outcome.setText("Did not load. Save does not exist")
        
        
        timer = QtCore.QTimer(self)
        timer.timeout.connect(lambda: self.load_outcome.setText(""))
        timer.start(1250)

def window():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = Calculator()
    win.show() # Show all the widgets applied to the window
    sys.exit(app.exec_()) # Close application when the X is pressed

# Run if ran from this script
if __name__ == "__main__":
    window()