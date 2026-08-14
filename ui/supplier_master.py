from PySide6.QtWidgets import *
from database import get_session
from models import Supplier
from permissions import Permissions
from PySide6.QtWidgets import QHeaderView




class SupplierMaster(QWidget):

    def __init__(self, user):
        super().__init__()

        self.user = user
        self.selected_id = None

        self.setWindowTitle("Supplier Master")
        self.resize(1000, 600)

        main_layout = QHBoxLayout()

        # LEFT FORM
        form_layout = QFormLayout()

        self.supplier_code = QLineEdit()
        self.supplier_code.setReadOnly(True)

        self.supplier_name = QLineEdit()
        self.company_name = QLineEdit()
        self.contact_person = QLineEdit()
        self.mobile = QLineEdit()
        self.email = QLineEdit()
        self.address = QLineEdit()
        self.city = QLineEdit()
        self.country = QLineEdit()
        self.vat_number = QLineEdit()
        self.remarks = QLineEdit()

        form_layout.addRow("Supplier Code", self.supplier_code)
        form_layout.addRow("Supplier Name", self.supplier_name)
        form_layout.addRow("Company Name", self.company_name)
        form_layout.addRow("Contact Person", self.contact_person)
        form_layout.addRow("Mobile", self.mobile)
        form_layout.addRow("Email", self.email)
        form_layout.addRow("Address", self.address)
        form_layout.addRow("City", self.city)
        form_layout.addRow("Country", self.country)
        form_layout.addRow("VAT Number", self.vat_number)
        form_layout.addRow("Remarks", self.remarks)


        # BUTTONS

        self.save_btn = QPushButton("Save")
        self.update_btn = QPushButton("Update")
        self.delete_btn = QPushButton("Delete")
        self.clear_btn = QPushButton("Clear")
        
        self.save_btn.clicked.connect(
            self.save_supplier
        )

        self.update_btn.clicked.connect(
            self.update_supplier
        )

        self.delete_btn.clicked.connect(
            self.delete_supplier
        )

        self.clear_btn.clicked.connect(
            self.clear_form
        )

        self.delete_btn.setVisible(False)
        btn_layout = QHBoxLayout()

        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.clear_btn)


        left_layout = QVBoxLayout()

        left_layout.addLayout(form_layout)
        left_layout.addLayout(btn_layout)


        # RIGHT TABLE

        self.table = QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Code",
                "Supplier Name",
                "Company",
                "Mobile"
            ]
        )

        self.table.cellClicked.connect(
            self.select_supplier
        )


        main_layout.addLayout(left_layout, 1)
        main_layout.addWidget(self.table, 2)


       

#table improvement
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)   # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)   # Code
        header.setSectionResizeMode(2, QHeaderView.Stretch)            # Supplier Name
        header.setSectionResizeMode(3, QHeaderView.Stretch)            # Company
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)   # Mobile
        #table improvementcls
        self.setLayout(main_layout)

        self.load_suppliers()

        self.supplier_code.setText(
        self.generate_code()
            )


        if not Permissions.is_admin(self.user):

            self.save_btn.setEnabled(False)
            self.update_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)



    def generate_code(self):

        session = get_session()

        last = session.query(Supplier)\
            .order_by(Supplier.id.desc())\
            .first()

        session.close()


        if not last:
            return "SUP0001"


        number = int(
            last.supplier_code.replace(
                "SUP", ""
                ""
            )
        )

        return f"SUP{number+1:04d}"



    def load_suppliers(self):

        session = get_session()

        suppliers = session.query(Supplier).all()


        self.table.setRowCount(
            len(suppliers)
        )


        for row, supplier in enumerate(suppliers):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(supplier.id)
                )
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    supplier.supplier_code
                )
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    supplier.supplier_name
                )
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    supplier.company_name or ""
                )
            )

            self.table.setItem(
                row,
                4,
                QTableWidgetItem(
                    supplier.mobile or ""
                )
            )


        session.close()



    def save_supplier(self):
        #print("SAVE BUTTON CLICKED")

        
        reply = QMessageBox.question(
        self,
        "Confirm Save",
        "Do you want to save this supplier?",
        QMessageBox.Yes | QMessageBox.No
    )

        if reply != QMessageBox.Yes:
            return

        name = self.supplier_name.text().strip().upper()
        mobile = self.mobile.text().strip()


        if not name or not mobile:

            QMessageBox.warning(
                self,
                "Error",
                "Supplier Name and Mobile required"
            )
            return


        session = get_session()


        existing = session.query(Supplier).filter_by(
            supplier_name=name,
            mobile=mobile
        ).first()


        if existing:

            QMessageBox.warning(
                self,
                "Duplicate",
                "Supplier already exists"
            )

            session.close()
            return



        supplier = Supplier(

            supplier_code=self.generate_code(),

            supplier_name=name,

            company_name=self.company_name.text().upper(),

            contact_person=self.contact_person.text().upper(),

            mobile=mobile,

            email=self.email.text().upper(),

            address=self.address.text().upper(),

            city=self.city.text().upper(),

            country=self.country.text().upper(),

            vat_number=self.vat_number.text().upper(),

            remarks=self.remarks.text().upper()
        )


        session.add(supplier)

        session.commit()

        session.close()


        '''QMessageBox.information(
            self,
            "Success",
            "Supplier saved"
        )'''
        QMessageBox.information(
            self,
            "Saved",
            f"{name} has been saved successfully."
        )

        self.load_suppliers()

        self.clear_form()



    def select_supplier(self, row, column):

        self.selected_id = int(
            self.table.item(row, 0).text()
        )

        session = get_session()

        supplier = session.query(Supplier)\
            .filter_by(id=self.selected_id)\
            .first()

        if supplier:

            self.supplier_code.setText(
                supplier.supplier_code
            )

            self.supplier_name.setText(
                supplier.supplier_name or ""
            )

            self.company_name.setText(
                supplier.company_name or ""
            )

            self.contact_person.setText(
                supplier.contact_person or ""
            )

            self.mobile.setText(
                supplier.mobile or ""
            )

            self.email.setText(
                supplier.email or ""
            )

            self.address.setText(
                supplier.address or ""
            )

            self.city.setText(
                supplier.city or ""
            )

            self.country.setText(
                supplier.country or ""
            )

            self.vat_number.setText(
                supplier.vat_number or ""
            )

            self.remarks.setText(
                supplier.remarks or ""
            )

        session.close()


    def update_supplier(self):
        reply = QMessageBox.question(
        self,
        "Confirm Update",
        "Do you want to update this supplier?",
        QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        if not self.selected_id:
            return


        session = get_session()


        supplier = session.query(Supplier)\
            .filter_by(id=self.selected_id)\
            .first()


        supplier.supplier_name = self.supplier_name.text().upper()

        supplier.company_name = self.company_name.text().upper()

        supplier.contact_person = self.contact_person.text().upper()

        supplier.email = self.email.text().upper()

        supplier.address = self.address.text().upper()

        supplier.city = self.city.text().upper()

        supplier.country = self.country.text().upper()

        supplier.vat_number = self.vat_number.text().upper()

        supplier.remarks = self.remarks.text().upper()

        supplier.mobile = self.mobile.text()


        session.commit()

        session.close()


        self.load_suppliers()

        self.clear_form()
        


    def delete_supplier(self):

        if not self.selected_id:
            return


        session = get_session()


        supplier = session.query(Supplier)\
            .filter_by(id=self.selected_id)\
            .first()


        session.delete(supplier)

        session.commit()

        session.close()


        self.load_suppliers()

        self.clear_form()



    def clear_form(self):

        self.supplier_code.clear()

        self.supplier_name.clear()

        self.company_name.clear()

        self.contact_person.clear()

        self.mobile.clear()

        self.email.clear()

        self.address.clear()

        self.city.clear()

        self.country.clear()

        self.vat_number.clear()

        self.remarks.clear()

        self.selected_id = None

        self.supplier_code.setText(
            self.generate_code()
        )
        self.supplier_name.setFocus()