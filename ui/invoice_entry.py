from datetime import date
from database import get_session
from models import Customer,SparePart,Invoice,InvoiceItem
from PySide6.QtWidgets import *
from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QTextEdit,
    QGroupBox,
    QTableWidget,   
    QTableWidgetItem,
    QPushButton,
    QSpinBox,
    QDoubleSpinBox,
)


class InvoiceEntry(QWidget):

    def __init__(self, user):
        
        super().__init__()

        self.user = user

        main_layout = QVBoxLayout(self)

        # ==========================================================
        # INVOICE DETAILS
        # ==========================================================

        # ==========================================================
        # TOP SECTION - TWO COLUMNS
        # ==========================================================

        top_layout = QHBoxLayout()

        # ==========================================================
        # LEFT COLUMN
        # ==========================================================

        left_layout = QVBoxLayout()

        # ----------------------------------------------------------
        # Invoice Type
        # ----------------------------------------------------------

        invoice_type_group = QGroupBox("Invoice Type")
        invoice_type_layout = QFormLayout()

        self.invoice_type = QComboBox()
        self.invoice_type.addItem(
            "Direct Invoice",
            "DIRECT"
        )
        self.invoice_type.addItem(
            "Material Issue Invoice",
            "MATERIAL_ISSUE"
        )

        invoice_type_layout.addRow(
            "Invoice Type:",
            self.invoice_type
        )

        invoice_type_group.setLayout(
            invoice_type_layout
        )

        left_layout.addWidget(
            invoice_type_group
        )

        # ----------------------------------------------------------
        # Customer Details
        # ----------------------------------------------------------

        customer_group = QGroupBox(
            "Customer Details"
        )

        customer_layout = QFormLayout()

        self.customer = QComboBox()
        self.customer.setEditable(True)
        self.customer.setInsertPolicy(
            QComboBox.NoInsert
        )

        completer = self.customer.completer()
        completer.setFilterMode(
            Qt.MatchContains
        )
        completer.setCompletionMode(
            QCompleter.PopupCompletion
        )

        customer_layout.addRow(
            "Customer:",
            self.customer
        )

        self.refresh_customers()

        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText(
            "customer name"
        )
        self.customer_name.setReadOnly(True)

        customer_layout.addRow(
            "Customer Name:",
            self.customer_name
        )

        self.company_name = QLineEdit()
        self.company_name.setPlaceholderText(
            "Company name"
        )
        self.company_name.setReadOnly(True)

        customer_layout.addRow(
            "Company:",
            self.company_name
        )

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText(
            "Mobile number"
        )
        self.mobile.setReadOnly(True)
        customer_layout.addRow(
            "Mobile:",
            self.mobile
        )

        self.address = QTextEdit()
        self.address.setPlaceholderText(
            "Customer address"
        )
        self.address.setFixedHeight(60)
        self.address.setReadOnly(True)

        customer_layout.addRow(
            "Address:",
            self.address
        )

        self.vat_number = QLineEdit()
        self.vat_number.setPlaceholderText(
            "VAT Number"
        )
        self.vat_number.setReadOnly(True)

        customer_layout.addRow(
            "VAT Number:",
            self.vat_number
        )

        self.customer.currentIndexChanged.connect(
            self.customer_changed)

        customer_group.setLayout(
            customer_layout
        )

        left_layout.addWidget(
            customer_group
        )

        # ==========================================================
        # RIGHT COLUMN
        # ==========================================================

        right_layout = QVBoxLayout()

        # ----------------------------------------------------------
        # Invoice Details
        # ----------------------------------------------------------

        invoice_group = QGroupBox(
            "Invoice Details"
        )

        invoice_layout = QFormLayout()

        self.invoice_no = QLineEdit()
        self.invoice_no.setReadOnly(True)
        self.invoice_no.setPlaceholderText(
            "Invoice No."
        )

        invoice_layout.addRow(
            "Invoice No.:",
            self.invoice_no
        )

        self.invoice_date = QDateEdit()
        self.invoice_date.setCalendarPopup(True)
        self.invoice_date.setDate(
            QDate.currentDate()
        )

        invoice_layout.addRow(
            "Invoice Date:",
            self.invoice_date
        )

        invoice_group.setLayout(
            invoice_layout
        )

        right_layout.addWidget(
            invoice_group
        )

        # ----------------------------------------------------------
        # PO Details
        # ----------------------------------------------------------

        po_group = QGroupBox(
            "Purchase Order Details"
        )

        po_layout = QFormLayout()

        self.po_number = QLineEdit()
        self.po_number.setPlaceholderText(
            "PO Number"
        )

        po_layout.addRow(
            "PO Number:",
            self.po_number
        )

        self.po_date = QDateEdit()
        self.po_date.setCalendarPopup(True)
        self.po_date.setSpecialValueText(" ")

        po_layout.addRow(
            "PO Date:",
            self.po_date
        )

        po_group.setLayout(
            po_layout
        )

        right_layout.addWidget(
            po_group
        )

        # ==========================================================
        # ADD COLUMNS TO TOP LAYOUT
        # ==========================================================

        top_layout.addLayout(
            left_layout,
            1
        )

        top_layout.addLayout(
            right_layout,
            1
        )

        main_layout.addLayout(
            top_layout
        )

        # ==========================================================
        # REMARKS
        # ==========================================================

        remarks_group = QGroupBox("Remarks")

        remarks_layout = QVBoxLayout()

        self.remarks = QTextEdit()
        self.remarks.setPlaceholderText(
            "Remarks"
        )
        self.remarks.setFixedHeight(70)

        remarks_layout.addWidget(
            self.remarks
        )

        remarks_group.setLayout(
            remarks_layout
        )

        main_layout.addWidget(
            remarks_group
        )
        # ==========================================================
        # INVOICE ITEMS
        # ==========================================================

        items_group = QGroupBox("Invoice Items")
        items_layout = QVBoxLayout()

        # ----------------------------------------------------------
        # Spare selection row
        # ----------------------------------------------------------

        entry_layout = QHBoxLayout()

        self.spare = QComboBox()
        self.spare.setEditable(True)
        self.spare.setInsertPolicy(QComboBox.NoInsert)
        self.spare.lineEdit().setPlaceholderText("Select Spare")
        completer = self.spare.completer()
        completer.setFilterMode(Qt.MatchContains)   
        completer.setCompletionMode(QCompleter.PopupCompletion)

        entry_layout.addWidget(
            QLabel("Spare:")
        )

        entry_layout.addWidget(
            self.spare
        )
        self.spare.currentIndexChanged.connect(
            self.spare_changed
                )

        # Quantity
        self.qty = QSpinBox()
        self.qty.setMinimum(1)
        self.qty.setMaximum(999999)
        self.qty.setValue(1)

        entry_layout.addWidget(
            QLabel("Qty:")
        )

        entry_layout.addWidget(
            self.qty
        )

        # Price
        self.price = QDoubleSpinBox()
        self.price.setDecimals(3)
        self.price.setMinimum(0)
        self.price.setMaximum(999999999)
        self.price.setValue(0)

        entry_layout.addWidget(
            QLabel("Price:")
        )

        entry_layout.addWidget(
            self.price
        )

        # Add button
        self.add_item_btn = QPushButton(
            "Add Item"
        )

        self.add_item_btn.clicked.connect(
            self.add_item
        )

        entry_layout.addWidget(
            self.add_item_btn
        )

        items_layout.addLayout(
            entry_layout
        )

        # ----------------------------------------------------------
        # Invoice item table
        # ----------------------------------------------------------

        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([
            "Spare ID",
            "Part No.",
            "Description",
            "Qty",
            "Price",
            "Total"
        ])

        self.table.setColumnHidden(0, True)

        self.table.setEditTriggers(
            QTableWidget.DoubleClicked
        )

        items_layout.addWidget(
            self.table
        )

        # ==========================================================
        # SERVICE CHARGE
        # ==========================================================

        service_layout = QHBoxLayout()

        self.service_charge_check = QCheckBox(
            "Service Charge"
        )

        self.service_charge = QDoubleSpinBox()
        self.service_charge.setDecimals(3)
        self.service_charge.setMaximum(999999999)
        self.service_charge.setValue(0)
        self.service_charge.setEnabled(False)

        self.service_charge_check.toggled.connect(
            self.service_charge_toggled
        )

        self.service_charge.valueChanged.connect(
            self.calculate_total
        )

        service_layout.addWidget(
            self.service_charge_check
        )

        service_layout.addWidget(
            self.service_charge
        )

        service_layout.addStretch()

        items_layout.addLayout(
            service_layout
        )

#..................service charges ...............

        # ----------------------------------------------------------
        # Grand Total
        # ----------------------------------------------------------

        total_layout = QHBoxLayout()

        total_layout.addStretch()

        total_layout.addWidget(
            QLabel("Grand Total:")
        )

        self.grand_total_label = QLabel(
            "0.000"
        )

        total_layout.addWidget(
            self.grand_total_label
        )
        items_layout.addLayout(
            total_layout
        )
        items_group.setLayout(
            items_layout
        )
        main_layout.addWidget(
            items_group
        )

        # Item action buttons
        #---------------------------------------------------------
        #---------------------------------------------------------
        button_layout = QHBoxLayout()

        self.remove_item_btn = QPushButton(
            "Remove Selected Item"
        )
        self.save_invoice_btn = QPushButton(
            "Save Invoice"
        )
        self.remove_item_btn.clicked.connect(
            self.remove_item
        )
        self.save_invoice_btn.clicked.connect(
            self.save_invoice
        )
        button_layout.addWidget(
            self.remove_item_btn
        )
        button_layout.addWidget(
            self.save_invoice_btn
        )
        
        button_layout.addStretch()
        items_layout.addLayout(button_layout)


        #.............................................................
        main_layout.addStretch()
        self.refresh_spares()
    def refresh_customers(self):

        session = get_session()

        try:
            self.customer.blockSignals(True)
            self.customer.clear()
            # First option
            #self.customer.addItem("Select Customer",None)
            #test code customer 
            self.customer.setCurrentIndex(-1)
            self.customer.lineEdit().clear()
            self.customer.lineEdit().setPlaceholderText("Select Customer")
            #test code customer 
            customers = (
                session.query(Customer)
                .order_by(Customer.customer_name)
                .all()
            )

            for customer in customers:
                company = (
                    customer.company_name.strip()
                    if customer.company_name
                    else ""
                )

                if company:
                    display_text = (
                        f"{customer.customer_code} - "
                        f"{customer.customer_name} - "
                        f"{company}"
                    )
                else:
                    display_text = (
                        f"{customer.customer_code} - "
                        f"{customer.customer_name}"
                    )

                self.customer.addItem(
                    display_text,
                    customer.id
                )

        finally:

            self.customer.blockSignals(False)
            session.close()

        self.customer.setCurrentIndex(-1)


    def refresh_spares(self):

        session = get_session()

        try:
            self.spare.blockSignals(True)
            self.spare.setCurrentIndex(-1)
            self.spare.lineEdit().clear()
            self.spare.lineEdit().setPlaceholderText("Select Spare")
            self.spare.clear()


            spares = (
                session.query(SparePart)
                .order_by(SparePart.part_number)
                .all()
            )
            for spare in spares:

                display_text = (
                    f"{spare.part_number} - "
                    f"{spare.part_name}"
                )
                self.spare.addItem(
                    display_text,
                    spare.id
                )
        finally:
            self.spare.blockSignals(False)
            session.close()
        self.spare.setCurrentIndex(-1)
    def spare_changed(self):

        spare_id = self.spare.currentData()
        if spare_id is None:
            self.price.setValue(0)
            return
        session = get_session()
        try:
            spare = session.get(
                SparePart,
                spare_id
            )
            if spare:
                self.price.setValue(
                    float(spare.selling_price or 0)
                )
        finally:
            session.close()

    def add_item(self):

        spare_id = self.spare.currentData()
        if spare_id is None:
            QMessageBox.warning(
                self,
                "Invoice",
                "Please select a spare."
            )
            return
        qty = self.qty.value()
        price = self.price.value()
        session = get_session()
        try:
            spare = session.get(
                SparePart,
                spare_id
            )
            if spare is None:
                QMessageBox.warning(
                    self,
                    "Invoice",
                    "Selected spare was not found."
                )
                return
            available_stock = (
                spare.stock_qty or 0
            )
            # ------------------------------------------
            # Check quantity already added
            # ------------------------------------------
            existing_qty = 0
            for row in range(
                self.table.rowCount()
            ):
                existing_spare_id = int(
                    self.table.item(row, 0).text()
                )
                if existing_spare_id == spare_id:
                    existing_qty += int(
                        float(
                            self.table.item(
                                row,
                                3
                            ).text()
                        )
                    )
            requested_total = (
                existing_qty + qty
            )
            # ------------------------------------------
            # Stock validation
            # ------------------------------------------
            if requested_total > available_stock:
                QMessageBox.warning(
                    self,
                    "Insufficient Stock",
                    f"Available stock: {available_stock}\n"
                    f"Already added: {existing_qty}\n"
                    f"Requested quantity: {qty}\n\n"
                    f"Total requested: {requested_total}"
                )
                return
            # ------------------------------------------
            # If same spare already exists
            # ------------------------------------------
            for row in range(
                self.table.rowCount()
            ):
                existing_spare_id = int(
                    self.table.item(row, 0).text()
                )
                if existing_spare_id == spare_id:
                    new_qty = (
                        existing_qty + qty
                    )
                    new_total = (
                        new_qty * price
                    )
                    self.table.setItem(
                        row,
                        3,
                        QTableWidgetItem(
                            str(new_qty)
                        )
                    )
                    self.table.setItem(
                        row,
                        4,
                        QTableWidgetItem(
                            f"{price:.3f}"
                        )
                    )
                    self.table.setItem(
                        row,
                        5,
                        QTableWidgetItem(
                            f"{new_total:.3f}"
                        )
                    )
                    self.calculate_total()
                    self.qty.setValue(1)
                    self.spare.setCurrentIndex(-1)
                    self.spare.lineEdit().clear()
                    return
            # ------------------------------------------
            # New item
            # ------------------------------------------
            total = qty * price
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(spare.id)
                )
            )
            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    spare.part_number
                )
            )
            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    spare.part_name
                )
            )
            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    str(qty)
                )
            )
            self.table.setItem(
                row,
                4,
                QTableWidgetItem(
                    f"{price:.3f}"
                )
            )
            self.table.setItem(
                row,
                5,
                QTableWidgetItem(
                    f"{total:.3f}"
                )
            )
            self.calculate_total()
            # Reset entry fields
            self.qty.setValue(1)
            self.spare.setCurrentIndex(-1)
            self.spare.lineEdit().clear()   
        finally:
            session.close()

    def calculate_total(self):
        grand_total = 0
        for row in range(
            self.table.rowCount()
        ):
            total_item = self.table.item(
                row,
                5
            )
            if total_item:
                grand_total += float(
                    total_item.text()
                )
          # Add service charge
        if self.service_charge_check.isChecked():
            grand_total += self.service_charge.value()
        self.grand_total = grand_total
        self.grand_total_label.setText(
            f"{grand_total:.3f}"
        )

    def customer_changed(self):

        customer_id = self.customer.currentData()

        if customer_id is None:
            self.clear_customer_details()
            return

        session = get_session()

        try:

            customer = session.get(
                Customer,
                customer_id
            )

            if customer is None:
                self.clear_customer_details()
                return

            # CASH CUSTOMER
            if customer.customer_code == "CASH":

                self.customer_name.setReadOnly(False)
                self.company_name.setReadOnly(False)
                self.mobile.setReadOnly(False)
                self.address.setReadOnly(False)
                self.vat_number.setReadOnly(False)

                self.customer_name.clear()
                self.company_name.clear()
                self.mobile.clear()
                self.address.clear()
                self.vat_number.clear()

            # NORMAL CUSTOMER
            else:

                self.customer_name.setReadOnly(True)
                self.company_name.setReadOnly(True)
                self.mobile.setReadOnly(True)
                self.address.setReadOnly(True)
                self.vat_number.setReadOnly(True)

                self.customer_name.setText(
                    customer.customer_name or ""
                )

                self.company_name.setText(
                    customer.company_name or ""
                )

                self.mobile.setText(
                    customer.mobile or ""
                )

                self.address.setPlainText(
                    customer.address or ""
                )

                self.vat_number.setText(
                    customer.vat_number or ""
                )

        finally:
            session.close()

    def clear_customer_details(self):

        self.customer_name.clear()
        self.company_name.clear()
        self.mobile.clear()
        self.address.clear()
        self.vat_number.clear()

        self.customer_name.setReadOnly(True)
        self.company_name.setReadOnly(True)
        self.mobile.setReadOnly(True)
        self.address.setReadOnly(True)
        self.vat_number.setReadOnly(True)
    def remove_item(self):

        row = self.table.currentRow()

        if row < 0:

            QMessageBox.warning(
                self,
                "Invoice",
                "Please select an item to remove."
            )

            return

        self.table.removeRow(row)

        self.calculate_total()

    def generate_invoice_no(self, session):
        last_invoice = (
            session.query(Invoice)
            .order_by(Invoice.id.desc())
            .first()
        )

        if last_invoice:
            try:
                last_no = int(
                    last_invoice.invoice_no.replace(
                        "INV", ""
                    )
                )
                next_no = last_no + 1
            except ValueError:
                next_no = 1
        else:
            next_no = 1

        return f"INV{next_no:05d}"

    def save_invoice(self):

        # --------------------------------------------------
        # VALIDATION
        # --------------------------------------------------

        if self.table.rowCount() == 0:
            QMessageBox.warning(
                self,
                "Invoice",
                "Please add at least one item."
            )
            return

        customer_id = self.customer.currentData()

        if customer_id is None:
            QMessageBox.warning(
                self,
                "Invoice",
                "Please select a customer."
            )
            return

        session = get_session()

        try:

            # --------------------------------------------------
            # INVOICE NUMBER
            # --------------------------------------------------

            invoice_no = self.generate_invoice_no(
                session
            )

            # --------------------------------------------------
            # CUSTOMER
            # --------------------------------------------------

            customer = session.get(
                Customer,
                customer_id
            )

            if customer is None:
                QMessageBox.warning(
                    self,
                    "Invoice",
                    "Selected customer was not found."
                )
                return

            # --------------------------------------------------
            # CREATE INVOICE
            # --------------------------------------------------

            invoice = Invoice(
                invoice_no=invoice_no,
                invoice_date=self.invoice_date.date().toPython(),
                invoice_type=self.invoice_type.currentData(),
                status="COMPLETED",
                customer_id=customer_id,

                customer_name=self.customer_name.text().strip(),
                company_name=self.company_name.text().strip(),
                phone=self.mobile.text().strip()
                    if hasattr(self, "mobile")
                    else "",

                address=self.address.toPlainText().strip(),

                po_number=self.po_number.text().strip(),

                po_date=(
                    self.po_date.date().toPython()
                    if not self.po_date.date()
                        == self.po_date.minimumDate()
                    else None
                ),

                remarks=self.remarks.toPlainText().strip(),

                grand_total=self.grand_total,

                created_by=self.user.username
            )

            session.add(invoice)
            session.flush()

            # --------------------------------------------------
            # SAVE ITEMS
            # --------------------------------------------------

            for row in range(
                self.table.rowCount()
            ):

                spare_id = int(
                    self.table.item(
                        row, 0
                    ).text()
                )

                description = self.table.item(
                    row, 2
                ).text()

                quantity = float(
                    self.table.item(
                        row, 3
                    ).text()
                )

                unit_price = float(
                    self.table.item(
                        row, 4
                    ).text()
                )

                total = float(
                    self.table.item(
                        row, 5
                    ).text()
                )

                item = InvoiceItem(
                    invoice_id=invoice.id,
                    item_type="SPARE",
                    spare_id=spare_id,
                    description=description,
                    quantity=quantity,
                    unit_price=unit_price,
                    total=total
                )

                session.add(item)

            # --------------------------------------------------
            # SERVICE CHARGE
            # --------------------------------------------------

            service_charge_check = getattr(
                self,
                "service_charge_check",
                None
            )

            if (
                service_charge_check is not None
                and service_charge_check.isChecked()
                and self.service_charge.value() > 0
            ):

                service_amount = (
                    self.service_charge.value()
                )

                service_item = InvoiceItem(
                    invoice_id=invoice.id,
                    item_type="SERVICE",
                    spare_id=None,
                    description="SERVICE CHARGE",
                    quantity=1,
                    unit_price=service_amount,
                    total=service_amount
                )

                session.add(service_item)

            # --------------------------------------------------
            # SAVE
            # --------------------------------------------------

            session.commit()

            self.invoice_no.setText(
                invoice_no
            )

            QMessageBox.information(
                self,
                "Invoice Saved",
                f"Invoice {invoice_no} saved successfully."
            )

        except Exception as e:

            session.rollback()

            QMessageBox.critical(
                self,
                "Save Error",
                str(e)
            )

        finally:

            session.close()

        

    def service_charge_toggled(self, checked):
        self.service_charge.setEnabled(checked)
        self.calculate_total()