from PySide6.QtWidgets import *
from database import get_session
from models import Unit        
from permissions import Permissions

class UnitMaster(QWidget):

    def __init__(self, user):
        super().__init__()

        self.user = user
        self.selected_id = None

        self.setWindowTitle("Unit Master")
        self.resize(600, 400)

        layout = QVBoxLayout()

        # Unit Name
        self.unit_name = QLineEdit()
        self.unit_name.setPlaceholderText(
            "Enter Unit Name"
        )

        layout.addWidget(
            self.unit_name
        )


        # Buttons
        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("Save")
        self.update_btn = QPushButton("Update")
        self.delete_btn = QPushButton("Delete")
        self.clear_btn = QPushButton("Clear")


        self.add_btn.clicked.connect(
            self.save_unit
        )

        self.update_btn.clicked.connect(
            self.update_unit
        )

        self.delete_btn.clicked.connect(
            self.delete_unit       
        )

        self.clear_btn.clicked.connect(
            self.clear_form
        )


        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.clear_btn)

        layout.addLayout(btn_layout)


        # Table
        self.table = QTableWidget()

        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Unit Name"
            ]
        )

        self.table.cellClicked.connect(
            self.select_unit                                       
        )


        layout.addWidget(
            self.table
        )


        self.setLayout(layout)


        self.load_units()


        # Permission
        if not Permissions.is_admin(self.user):

            self.add_btn.setEnabled(False)
            self.update_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)



    def load_units(self):

        session = get_session()

        units = session.query(
            Unit
        ).all()


        self.table.setRowCount(
            len(units)
        )


        for row, unit in enumerate(units):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(unit.id)
                )
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    unit.name
                )
            )


        session.close()



    def save_unit(self):

        name = self.unit_name.text().strip()


        if not name:

            QMessageBox.warning(
                self,
                "Error",
                "Enter unit name"
            )
            return
        session = get_session()
        existing = session.query(Unit).filter_by(
            name=self.unit_name.text().upper()
        ).first()

        if existing:
            QMessageBox.warning(
                self,
                "Duplicate",
                "Unit already exists."
            )
            return


        session = get_session()


        unit = Unit(
            name=name.upper()
        )


        session.add(unit)

        session.commit()

        session.close()


        QMessageBox.information(
            self,
            "Success",
            "Unit saved"
        )


        self.clear_form()

        self.load_units()



    def select_unit(self, row, column):

        self.selected_id = int(
            self.table.item(row,0).text()
        )


        self.unit_name.setText(
            self.table.item(row,1).text()
        )



    def update_unit(self):

        if not self.selected_id:
            return


        session = get_session()


        unit = session.query(
            Unit       
        ).filter_by(
            id=self.selected_id
        ).first()


        unit.name = (
            self.unit_name.text()
            .upper()
        )


        session.commit()

        session.close()


        self.load_units()

        self.clear_form()



    def delete_unit(self):

        if not self.selected_id:
            return
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this record?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return


        session = get_session()


        unit = session.query(
            Unit   
        ).filter_by(
            id=self.selected_id
        ).first()


        session.delete(unit)

        session.commit()

        session.close()


        self.load_units()

        self.clear_form()



    def clear_form(self):

        self.unit_name.clear()

        self.selected_id = None