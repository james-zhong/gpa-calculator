import sys, ctypes, time, help_text
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QScrollArea
from PyQt5.QtGui import QCursor

# Track the pages of user manual
current_page = 1

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
        self.initUI()
        
    def initUI(self):
        # Title
        self.header = QtWidgets.QLabel(self, objectName="header")
        self.header.setText("User Manual")
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.resize(750, 100)
        
        # Page navigation
        self.page_display = QtWidgets.QLabel(self, objectName="page_display")
        self.page_display.setText("0 / 10")
        self.page_display.setAlignment(QtCore.Qt.AlignCenter)
        self.page_display.resize(200, 50)
        self.page_display.move(275, 500)
        
        self.go_back = QtWidgets.QPushButton(self, objectName="turn_button")
        self.go_back.setText("<")
        self.go_back.setFlat(True)
        self.go_back.resize(50, 50)
        self.go_back.move(225, 500)
        
        self.go_next = QtWidgets.QPushButton(self, objectName="turn_button")
        self.go_next.setText(">")
        self.go_next.setFlat(True)
        self.go_next.resize(50, 50)
        self.go_next.move(475, 500)
        
        # Different pages
        def page1(self):
            # Description of the app
            self.overview_title = QtWidgets.QLabel(self, objectName="section_title")
            self.overview_title.setText("<u>Overview</u>")
            self.overview_title.setAlignment(QtCore.Qt.AlignCenter)
            self.overview_title.resize(175, 50)
            self.overview_title.move(5, 100)
            
            self.overview_desc = QtWidgets.QLabel(self, objectName="section_desc")
            self.overview_desc.setText(help_text.overview_desc)
            self.overview_desc.setWordWrap(True)
            self.overview_desc.resize(700, 350)
            self.overview_desc.move(25, 140)
            
        page1() # Temp
"""
Temporary so I can test out this window quicker
"""

if __name__ == "__main__":
    def window():
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        win = Manual()
        win.show() # Show all the widgets applied to the window
        sys.exit(app.exec_()) # Close application when the X is pressed
        
    window()