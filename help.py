import ctypes, time, help_text
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow

# UI for different pages
def page_1(self):
    self.page_title.setText("<u>Overview</u>")
    self.page_desc.setText(help_text.overview_desc)
    
def page_2(self):
    self.page_title.setText("<u>Discretion</u>")
    self.page_desc.setText(help_text.warning_desc)

def page_3(self):
    self.page_title.setText("<u>Usage</u>")
    self.page_desc.setText(help_text.ui_desc)

def page_4(self):
    self.page_title.setText("<u>Credits</u>")
    self.page_desc.setText(help_text.credits_desc)

# Dictionary to map current page number
page_functions = {
    1: page_1,
    2: page_2,
    3: page_3,
    4: page_4
}

class Manual(QMainWindow):
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
            
        # Draw all widgets
        self.init_ui()
        
        # Page tracking variables
        self.current_page = 1
        self.total_pages = 4
        
        # Global variable for the page display QLabel
        self.page_count_display = None
        
    def init_ui(self):
        # Title
        self.header = QtWidgets.QLabel(self, objectName="header")
        self.header.setText("User Manual")
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.resize(750, 100)
        
        # Page navigation
        self.page_display = QtWidgets.QLabel(self, objectName="page_display")
        self.page_display.setText("1 / 4")
        self.page_display.setAlignment(QtCore.Qt.AlignCenter)
        self.page_display.resize(200, 50)
        self.page_display.move(275, 500)
        self.page_count_display = self.page_display
        
        self.go_back = QtWidgets.QPushButton(self, objectName="turn_button")
        self.go_back.setText("<")
        self.go_back.setFlat(True)
        self.go_back.clicked.connect(lambda: self.changePage("back"))
        self.go_back.resize(50, 50)
        self.go_back.move(225, 500)
        
        self.go_next = QtWidgets.QPushButton(self, objectName="turn_button")
        self.go_next.setText(">")
        self.go_next.setFlat(True)
        self.go_next.clicked.connect(lambda: self.change_page("next"))
        self.go_next.resize(50, 50)
        self.go_next.move(475, 500)
        
        # Page set up
        self.page_title = QtWidgets.QLabel(self, objectName="section_title")
        self.page_title.setAlignment(QtCore.Qt.AlignCenter)
        self.page_title.resize(175, 50)
        self.page_title.move(5, 100)
        
        self.page_desc = QtWidgets.QLabel(self, objectName="section_desc")
        self.page_desc.setWordWrap(True)
        self.page_desc.resize(700, 350)
        self.page_desc.move(25, 140)
        
        # Page tracking variables
        self.total_pages = 4
        self.current_page = 1
        
        # Change the UI to the respective UI on current page
        page_functions[self.current_page](self)

    def change_page(self, turn):
        # Change the current page
        if turn == "back":
            self.current_page =  max(1, self.current_page - 1)
        elif turn == "next":
            self.current_page = min(self.total_pages, self.current_page + 1)
        
        # Update text of the page display
        self.page_display.setText(f"{self.current_page} / {self.total_pages}")
        page_functions[self.current_page](self)