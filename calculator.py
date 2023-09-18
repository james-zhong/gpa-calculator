import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("NCEA GPA Calculator")
window.setGeometry(100, 100, 1250, 750)

style = """
    QWidget {
        background-color: #333;
        border-radius: 10px;
        color: white;
    }
    QLabel {
        font-size: 16px;
        padding: 10px;
        background-color: #272822;
        text-align: center;
    }
    QLineEdit {
        background-color: #444;
        font-size: 16px;
        border: 2px solid #555;
        padding: 8px;
        width: 25px;
    }
    QPushButton {
        background-color: #1cde81;
        border-radius: 5px;
    }
"""

window.setStyleSheet(style)

layout = QGridLayout()

grades = [
    "Low Not Achieved", "Not Achieved", "High Not Achieved",
    "Low Achieved", "Achieved", "High Achieved",
    "Low Merit", "Merit", "High Merit",
    "Low Excellence", "Excellence", "High Excellence"
]

title = QLabel("NCEA GPA Calulator")
layout.addWidget(title)

for row in range(3):
    for col in range(4):
        index = row * 4 + col
        grade = grades[index]
        label = QLabel(grade)
        input_box = QLineEdit()

        layout.addWidget(label, row + 1, col * 2)
        layout.addWidget(input_box, row + 1, col * 2 + 1)

calculate = QPushButton("Calculate")
layout.addWidget(calculate)

window.setLayout(layout)
window.show()

sys.exit(app.exec_())