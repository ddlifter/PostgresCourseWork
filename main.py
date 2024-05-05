from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from employees import Employees
from specialties import Specialties
from norms import Norms
from ranks import Ranks

import sys

class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Form")
        self.setGeometry(100, 100, 600, 400)
        self.showMaximized()

        # Создаем вертикальный макет для кнопок
        button_layout = QVBoxLayout()

        self.button1 = QPushButton("Open Form 1")
        self.button1.setGeometry(50, 50, 100, 30)
        self.button1.clicked.connect(self.open_form1)
        button_layout.addWidget(self.button1)

        self.button2 = QPushButton("Open Form 2")
        self.button2.setGeometry(200, 50, 100, 30)
        self.button2.clicked.connect(self.open_form2)
        button_layout.addWidget(self.button2)

        self.button3 = QPushButton("Open Form 3")
        self.button3.setGeometry(350, 50, 100, 30)
        self.button3.clicked.connect(self.open_form3)
        button_layout.addWidget(self.button3)
        
        self.button4 = QPushButton("Open Form 4")
        self.button4.setGeometry(350, 50, 100, 30)
        self.button4.clicked.connect(self.open_form4)
        button_layout.addWidget(self.button4)

        # Устанавливаем макет кнопок в качестве центрального виджета
        central_widget = QWidget()
        central_widget.setLayout(button_layout)
        self.setCentralWidget(central_widget)

    def open_form1(self):
        self.form1 = Employees()
        self.form1.show()
        self.close()

    def open_form2(self):
        self.form2 = Specialties()
        self.form2.show()
        self.close()

    def open_form3(self):
        self.form3 = Norms()
        self.form3.show()
        self.close()
        
    def open_form4(self):
        self.form4 = Ranks()
        self.form4.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_form = MainForm()
    main_form.show()
    sys.exit(app.exec_())
