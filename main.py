from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from employees import Employees
from specialties import Specialties
from norms import Norms
from ranks import Ranks
from training import Training
from roles_changes import do_for_admin, do_for_empl
import sys
from connection import ConnectionManager

class MainForm(QMainWindow):
    def __init__(self, conn: ConnectionManager):
        self.conn : ConnectionManager = conn
        super().__init__()
        self.setWindowTitle("Main Form")
        self.setGeometry(100, 100, 600, 400)
        self.showMaximized()

        # Создаем вертикальный макет для кнопок
        button_layout = QVBoxLayout()

        self.button1 = QPushButton("Сотрудники")
        self.button1.setGeometry(50, 50, 100, 30)
        self.button1.clicked.connect(self.open_form1)
        button_layout.addWidget(self.button1)

        self.button2 = QPushButton("Специальности")
        self.button2.setGeometry(200, 50, 100, 30)
        self.button2.clicked.connect(self.open_form2)
        button_layout.addWidget(self.button2)

        self.button3 = QPushButton("Нормы")
        self.button3.setGeometry(350, 50, 100, 30)
        self.button3.clicked.connect(self.open_form3)
        button_layout.addWidget(self.button3)
        
        self.button4 = QPushButton("Разряды")
        self.button4.setGeometry(350, 50, 100, 30)
        self.button4.clicked.connect(self.open_form4)
        button_layout.addWidget(self.button4)
        
        
        self.button5 = QPushButton("Обучение")
        self.button5.setGeometry(350, 50, 100, 30)
        self.button5.clicked.connect(self.open_form5)
        button_layout.addWidget(self.button5)

        # Устанавливаем макет кнопок в качестве центрального виджета
        central_widget = QWidget()
        central_widget.setLayout(button_layout)
        self.setCentralWidget(central_widget)

    def open_form1(self):
        self.form1 = Employees(self.conn)
        self.form1.show()
        self.close()

    def open_form2(self):
        self.form2 = Specialties(self.conn)
        self.form2.show()
        self.close()

    def open_form3(self):
        self.form3 = Norms(self.conn)
        self.form3.show()
        self.close()
        
    def open_form4(self):
        self.form4 = Ranks(self.conn)
        self.form4.show()
        self.close()
        
    def open_form5(self):
        self.form5 = Training(self.conn)
        self.form5.show()
        self.close()
        
class AuthorizationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Авторизация")
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        self.roleLabel = QLabel("Выберите роль:")
        layout.addWidget(self.roleLabel)

        self.adminButton = QPushButton("Администратор")
        self.adminButton.clicked.connect(self.handleAdminClick)
        layout.addWidget(self.adminButton)

        self.employeeButton = QPushButton("Сотрудник")
        self.employeeButton.clicked.connect(self.handleEmployeeClick)
        layout.addWidget(self.employeeButton)

        self.setLayout(layout)

    def handleAdminClick(self):
        conn = ConnectionManager("admin_role")
        do_for_admin()
        self.form1 = MainForm(conn)
        self.form1.show()
        self.close()


    def handleEmployeeClick(self):
        conn = ConnectionManager("employee_role")
        do_for_empl()
        self.form1 = MainForm(conn)
        self.form1.show()
        self.close()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_form = AuthorizationWindow()
    main_form.show()
    sys.exit(app.exec_())
