from PySide6.QtWidgets import *
from database import get_session
from models import Brand
from permissions import Permissions

class BrandMaster(QWidget):

    def __init__(self, user):
        super().__init__()

        self.user = user
        self.selected_id = None

        self.setWindowTitle("Brand Master")
        self.resize(600, 400)

        layout = QVBoxLayout()

        # Brand Name
        self.brand_name = QLineEdit()
        self.brand_name.setPlaceholderText(
            "Enter Brand Name"
        )

        layout.addWidget(
            self.brand_name
        )


        # Buttons
        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("Save")
        self.update_btn = QPushButton("Update")
        self.delete_btn = QPushButton("Delete")
        self.clear_btn = QPushButton("Clear")


        self.add_btn.clicked.connect(
            self.save_brand
        )

        self.update_btn.clicked.connect(
            self.update_brand
        )

        self.delete_btn.clicked.connect(
            self.delete_brand       
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
                "Brand Name"
            ]
        )

        self.table.cellClicked.connect(
            self.select_brand                                       
        )


        layout.addWidget(
            self.table
        )


        self.setLayout(layout)


        self.load_brands()


        # Permission
        if not Permissions.is_admin(self.user):

            self.add_btn.setEnabled(False)
            self.update_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)



    def load_brands(self):

        session = get_session()

        brands = session.query(
            Brand
        ).all()


        self.table.setRowCount(
            len(brands)
        )


        for row, brand in enumerate(brands):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(brand.id)
                )
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    brand.name
                )
            )


        session.close()



    def save_brand(self):

        name = self.brand_name.text().strip()


        if not name:

            QMessageBox.warning(
                self,
                "Error",
                "Enter brand name"
            )
            return
        session = get_session()
        existing = session.query(Brand).filter_by(
            name=self.brand_name.text().upper()
        ).first()

        if existing:
            QMessageBox.warning(
                self,
                "Duplicate",
                "Brand already exists."
            )
            return


        session = get_session()


        brand = Brand(
            name=name.upper()
        )


        session.add(brand)

        session.commit()

        session.close()


        QMessageBox.information(
            self,
            "Success",
            "Brand saved"
        )


        self.clear_form()

        self.load_brands()



    def select_brand(self, row, column):

        self.selected_id = int(
            self.table.item(row,0).text()
        )


        self.brand_name.setText(
            self.table.item(row,1).text()
        )



    def update_brand(self):

        if not self.selected_id:
            return


        session = get_session()


        brand = session.query(
            Brand       
        ).filter_by(
            id=self.selected_id
        ).first()


        brand.name = (
            self.brand_name.text()
            .upper()
        )


        session.commit()

        session.close()


        self.load_brands()

        self.clear_form()



    def delete_brand(self):

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


        brand = session.query(
            Brand
        ).filter_by(
            id=self.selected_id
        ).first()


        session.delete(brand)

        session.commit()

        session.close()


        self.load_brands()

        self.clear_form()



    def clear_form(self):

        self.brand_name.clear()

        self.selected_id = None