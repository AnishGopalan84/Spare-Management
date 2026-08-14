from PySide6.QtWidgets import *
from database import get_session
from models import Customer
from permissions import Permissions
from PySide6.QtWidgets import QHeaderView




class CustomerMaster(QWidget):

    def __init__(self, user):
        super().__init__()

        self.user = user
        self.selected_id = None

        self.setWindowTitle("Customer Master")
        self.resize(1000, 600)

        main_layout = QHBoxLayout()

        # LEFT FORM
        form_layout = QFormLayout()

        self.customer_code = QLineEdit()
        self.customer_code.setReadOnly(True)

        self.customer_name = QLineEdit()
        self.company_name = QLineEdit()
        self.contact_person = QLineEdit()
        self.mobile = QLineEdit()
        self.email = QLineEdit()
        self.address = QLineEdit()
        self.city = QLineEdit()
        self.country = QLineEdit()
        self.vat_number = QLineEdit()
        self.remarks = QLineEdit()

        form_layout.addRow("Customer Code", self.customer_code)
        form_layout.addRow("Customer Name", self.customer_name)
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
            self.save_customer
        )

        self.update_btn.clicked.connect(
            self.update_customer
        )

        self.delete_btn.clicked.connect(
            self.delete_customer
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
                "Customer",
                "Company",
                "Mobile"
            ]
        )

        self.table.cellClicked.connect(
            self.select_customer
        )


        main_layout.addLayout(left_layout, 1)
        main_layout.addWidget(self.table, 2)


       

#table improvement
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)   # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)   # Code
        header.setSectionResizeMode(2, QHeaderView.Stretch)            # Customer Name
        header.setSectionResizeMode(3, QHeaderView.Stretch)            # Company
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)   # Mobile
        #table improvementcls
        self.setLayout(main_layout)

        self.load_customers()

        self.customer_code.setText(
        self.generate_code()
            )


        if not Permissions.is_admin(self.user):

            self.save_btn.setEnabled(False)
            self.update_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)



    def generate_code(self):

        session = get_session()

        last = session.query(Customer)\
            .order_by(Customer.id.desc())\
            .first()

        session.close()


        if not last:
            return "CUS0001"


        number = int(
            last.customer_code.replace(
                "CUS",
                ""
            )
        )

        return f"CUS{number+1:04d}"



    def load_customers(self):

        session = get_session()

        customers = session.query(Customer).all()


        self.table.setRowCount(
            len(customers)
        )


        for row, customer in enumerate(customers):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(customer.id)
                )
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    customer.customer_code
                )
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    customer.customer_name
                )
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    customer.company_name or ""
                )
            )

            self.table.setItem(
                row,
                4,
                QTableWidgetItem(
                    customer.mobile or ""
                )
            )


        session.close()



    def save_customer(self):
        reply = QMessageBox.question(
        self,
        "Confirm Save",
        "Do you want to save this customer?",
        QMessageBox.Yes | QMessageBox.No
    )

        if reply != QMessageBox.Yes:
            return

        name = self.customer_name.text().strip().upper()
        mobile = self.mobile.text().strip()


        if not name or not mobile:

            QMessageBox.warning(
                self,
                "Error",
                "Customer Name and Mobile required"
            )
            return


        session = get_session()


        existing = session.query(Customer).filter_by(
            customer_name=name,
            mobile=mobile
        ).first()


        if existing:

            QMessageBox.warning(
                self,
                "Duplicate",
                "Customer already exists"
            )

            session.close()
            return



        customer = Customer(

            customer_code=self.generate_code(),

            customer_name=name,

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


        session.add(customer)

        session.commit()

        session.close()


        '''QMessageBox.information(
            self,
            "Success",
            "Customer saved"
        )'''
        QMessageBox.information(
            self,
            "Saved",
            f"{name} has been saved successfully."
        )

        self.load_customers()

        self.clear_form()



    def select_customer(self, row, column):

        self.selected_id = int(
            self.table.item(row, 0).text()
        )

        session = get_session()

        customer = session.query(Customer)\
            .filter_by(id=self.selected_id)\
            .first()

        if customer:

            self.customer_code.setText(
                customer.customer_code
            )

            self.customer_name.setText(
                customer.customer_name or ""
            )

            self.company_name.setText(
                customer.company_name or ""
            )

            self.contact_person.setText(
                customer.contact_person or ""
            )

            self.mobile.setText(
                customer.mobile or ""
            )

            self.email.setText(
                customer.email or ""
            )

            self.address.setText(
                customer.address or ""
            )

            self.city.setText(
                customer.city or ""
            )

            self.country.setText(
                customer.country or ""
            )

            self.vat_number.setText(
                customer.vat_number or ""
            )

            self.remarks.setText(
                customer.remarks or ""
            )

        session.close()


    def update_customer(self):
        reply = QMessageBox.question(
        self,
        "Confirm Update",
        "Do you want to update this customer?",
        QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        if not self.selected_id:
            return


        session = get_session()


        customer = session.query(Customer)\
            .filter_by(id=self.selected_id)\
            .first()


        customer.customer_name = self.customer_name.text().upper()

        customer.company_name = self.company_name.text().upper()

        customer.contact_person = self.contact_person.text().upper()

        customer.email = self.email.text().upper()

        customer.address = self.address.text().upper()

        customer.city = self.city.text().upper()

        customer.country = self.country.text().upper()

        customer.vat_number = self.vat_number.text().upper()

        customer.remarks = self.remarks.text().upper()

        customer.mobile = self.mobile.text()


        session.commit()

        session.close()


        self.load_customers()

        self.clear_form()
        



    def delete_customer(self):

        if not self.selected_id:
            return


        session = get_session()


        customer = session.query(Customer)\
            .filter_by(id=self.selected_id)\
            .first()


        session.delete(customer)

        session.commit()

        session.close()


        self.load_customers()

        self.clear_form()



    def clear_form(self):

        self.customer_code.clear()

        self.customer_name.clear()

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

        self.customer_code.setText(
        self.generate_code()
        )
        self.customer_name.setFocus()