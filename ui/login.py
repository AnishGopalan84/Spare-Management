from PySide6.QtWidgets import *

from auth import login

class LoginWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Spare Management Login")

        self.resize(350,220)

        layout=QVBoxLayout()

        self.user=QLineEdit()

        self.user.setPlaceholderText("Username")

        self.password=QLineEdit()

        self.password.setEchoMode(QLineEdit.Password)

        self.password.setPlaceholderText("Password")

        btn=QPushButton("Login")

        btn.clicked.connect(self.do_login)

        layout.addWidget(self.user)

        layout.addWidget(self.password)

        self.password.returnPressed.connect(
        self.do_login
)

        layout.addWidget(btn)

        self.setLayout(layout)

    def do_login(self):

        user=login(
            self.user.text(),
            self.password.text()
        )

        if user:

            QMessageBox.information(
                self,
                "Success",
                f"Welcome {user.fullname}\nRole : {user.role}"
            )
            from ui.main_window import MainWindow

            self.main_window = MainWindow(user)
            self.main_window.show()

            self.close()

            

        else:

            QMessageBox.warning(
                self,
                "Error",
                "Invalid Username or Password"
            )