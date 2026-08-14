invoice_group = QGroupBox("Invoice Details")
        invoice_layout = QFormLayout()

        # Invoice No
        self.invoice_no = QLineEdit()
        self.invoice_no.setReadOnly(True)
        self.invoice_no.setPlaceholderText("Invoice No.")
        invoice_layout.addRow(
            "Invoice No.:",
            self.invoice_no
        )

        # Invoice Date
        self.invoice_date = QDateEdit()
        self.invoice_date.setCalendarPopup(True)
        self.invoice_date.setDate(QDate.currentDate())

        invoice_layout.addRow(
            "Invoice Date:",
            self.invoice_date
        )

        # Invoice Type
        self.invoice_type = QComboBox()
        self.invoice_type.addItem("Direct Invoice", "DIRECT")
        self.invoice_type.addItem(
            "Material Issue Invoice",
            "MATERIAL_ISSUE"
        )

        invoice_layout.addRow(
            "Invoice Type:",
            self.invoice_type
        )

        invoice_group.setLayout(invoice_layout)
        main_layout.addWidget(invoice_group)

        # ==========================================================
        # CUSTOMER DETAILS
        # ==========================================================

        customer_group = QGroupBox("Customer Details")
        customer_layout = QFormLayout()

        # Customer
        self.customer = QComboBox()
        self.customer.setEditable(True)
        self.customer.setInsertPolicy(
            QComboBox.NoInsert
        )
        self.customer.setEditable(True)
        self.customer.setInsertPolicy(QComboBox.NoInsert)

        completer = self.customer.completer()
        completer.setFilterMode(Qt.MatchContains)
        completer.setCompletionMode(
            QCompleter.PopupCompletion
        )

        customer_layout.addRow(
            "Customer:",
            self.customer
        )
        self.refresh_customers()

        # Walk-in Customer Name
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText(
            "Walk-in customer name"
        )

        customer_layout.addRow(
            "Customer Name:",
            self.customer_name
        )

        # Company
        self.company_name = QLineEdit()
        self.company_name.setPlaceholderText(
            "Company name"
        )

        customer_layout.addRow(
            "Company:",
            self.company_name
        )

        # Phone
        self.phone = QLineEdit()
        self.phone.setPlaceholderText(
            "Phone number"
        )

        customer_layout.addRow(
            "Phone:",
            self.phone
        )

        # Address
        self.address = QTextEdit()
        self.address.setPlaceholderText(
            "Customer address"
        )
        self.address.setFixedHeight(60)

        customer_layout.addRow(
            "Address:",
            self.address
        )

        customer_group.setLayout(customer_layout)
        main_layout.addWidget(customer_group)

        # ==========================================================
        # PO DETAILS
        # ==========================================================

        po_group = QGroupBox("Purchase Order Details")
        po_layout = QFormLayout()

        # PO Number
        self.po_number = QLineEdit()
        self.po_number.setPlaceholderText(
            "PO Number"
        )

        po_layout.addRow(
            "PO Number:",
            self.po_number
        )

        # PO Date
        self.po_date = QDateEdit()
        self.po_date.setCalendarPopup(True)
        self.po_date.setSpecialValueText(" ")
        self.po_date.setDate(
            self.po_date.minimumDate()
        )

        po_layout.addRow(
            "PO Date:",
            self.po_date
        )

        po_group.setLayout(po_layout)
        main_layout.addWidget(po_group)







if hasattr(self, "editing_row") and self.editing_row >= 0:
            self.update_item()
            return
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(
                self,
                "Invoice",
                "Please select an item to edit."
            )
            return
        spare_id = int(
            self.table.item(row, 0).text()
        )
        qty = int(
            float(
                self.table.item(row, 3).text()
            )
        )
        price = float(
            self.table.item(row, 4).text()
        )
        # Load values into entry controls
        self.spare.setCurrentIndex(
            self.spare.findData(spare_id)
        )
        self.qty.setValue(qty)
        self.price.setValue(price)
        # Remember which row is being edited


        def edit_item(self):
                if hasattr(self, "editing_row") and self.editing_row >= 0:
                    self.update_item()
                    return
            
                    row = self.table.currentRow()
                    if row < 0:
                        QMessageBox.warning(
                                self,
                                "Invoice",
                                "Please select an item to edit."
                            )
                        return
                    spare_id = int(
                        self.table.item(row, 0).text()
                        )
                    qty = int(
                            float(
                                self.table.item(row, 3).text()
                            )
                        )
                    price = float(
                            self.table.item(row, 4).text()
                        )
                        # Load values into entry controls
                    self.spare.setCurrentIndex(
                            self.spare.findData(spare_id)
                        )
                    self.qty.setValue(qty)
                    self.price.setValue(price)
                    # Remember which row is being edited
                    #self.editing_row = row
            def update_item(self):
        
                # Only update Qty, Price and Total
        
                self.table.setItem(
                    row,
                    3,
                    QTableWidgetItem(str(new_qty))
                )
        
                self.table.setItem(
                    row,
                    4,
                    QTableWidgetItem(
                        f"{new_price:.3f}"
                    )
                )
        
                self.table.setItem(
                    row,
                    5,
                    QTableWidgetItem(
                        f"{new_qty * new_price:.3f}"
                    )
                )
        
                row = self.editing_row
                spare_id = self.editing_spare_id
                if spare_id is None:
                    return
                new_qty = self.qty.value()
                new_price = self.price.value()
                session = get_session()
                try:
                    spare = session.get(
                        SparePart,
                        spare_id
                    )
                    if spare is None:
                        return
                    available_stock = (
                        spare.stock_qty or 0
                    )
                    # Calculate quantity used by OTHER rows
                    other_qty = 0
                    for r in range(
                        self.table.rowCount()
                    ):
                        if r == row:
                            continue
                        row_spare_id = int(
                            self.table.item(
                                r,
                                0
                            ).text()
                        )
                        if row_spare_id == spare_id:
        
                            other_qty += int(
                                float(
                                    self.table.item(
                                        r,
                                        3
                                    ).text()
                                )
                            )
                    requested_total = (
                        other_qty + new_qty
                    )
                    if requested_total > available_stock:
                        QMessageBox.warning(
                            self,
                            "Insufficient Stock",
                            f"Available stock: {available_stock}\n"
                            f"Already used in other lines: {other_qty}\n"
                            f"Requested quantity: {new_qty}\n\n"
                            f"Total requested: {requested_total}"
                        )
                        return
                    # Update row
                    total = new_qty * new_price
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
                            f"{new_price:.3f}"
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
                    # Clear edit mode
                    self.editing_row = -1
                    self.qty.setValue(1)
                    self.price.setValue(0)
                    self.spare.setCurrentIndex(0)
                finally:
                    session.close()