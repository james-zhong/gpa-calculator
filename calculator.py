import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit
from PyQt5.QtCore import Qt

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("NCEA GPA Calculator")
window.setGeometry(100, 100, 1250, 750)

style = """
    QWidget {
        background-color: #333;
    }
    QLabel {
        color: #fff;
        font-size: 16px;
        padding: 10px;
        background-color: #272822;
        border-radius: 10px;
        text-align: center;
    }
    QLineEdit {
        background-color: #444;
        color: #fff;
        font-size: 16px;
        border: 2px solid #555;
        border-radius: 10px;
        padding: 8px;
        width: 25px;
    }
"""

window.setStyleSheet(style)

layout = QGridLayout()

title = QLabel("NCEA GPA Calculator")
title.setStyleSheet(
    "text-align: center;"+
    "padding: 0;"
)
layout.addWidget(title, 0, 0, 1, 8)

grades = [
    "Low Not Achieved", "Not Achieved", "High Not Achieved",
    "Low Achieved", "Achieved", "High Achieved",
    "Low Merit", "Merit", "High Merit",
    "Low Excellence", "Excellence", "High Excellence"
]

for row in range(3):
    for col in range(4):
        index = row * 4 + col
        grade = grades[index]
        label = QLabel(grade)
        input_box = QLineEdit()

        layout.addWidget(label, row + 1, col * 2)
        layout.addWidget(input_box, row + 1, col * 2 + 1)

window.setLayout(layout)
window.show()

sys.exit(app.exec_())