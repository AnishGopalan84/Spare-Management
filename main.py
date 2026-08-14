

import sys

from PySide6.QtWidgets import QApplication

from ui.login import LoginWindow

app=QApplication(sys.argv)

window=LoginWindow()

window.show()


sys.exit(app.exec())


'''
import sys
from PySide6.QtWidgets import QApplication
from ui.spare_master import SpareMaster

app = QApplication(sys.argv)

window = SpareMaster()
window.show()

sys.exit(app.exec())'''

'''
import sys
from PySide6.QtWidgets import QApplication
from ui.spare_list import SpareList


app = QApplication(sys.argv)

window = SpareList()

window.show()

sys.exit(app.exec())'''

''' 
import sys

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


app = QApplication(sys.argv)


# Temporary test user
'''

'''
class User:
    fullname = "Administrator"
    role = "Administrator"

user = User()


window = MainWindow(user)

window.show()


sys.exit(app.exec())'''