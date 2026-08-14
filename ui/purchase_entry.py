from PySide6.QtWidgets import *
from database import get_session
from PySide6.QtCore import Qt
from models import Purchase, PurchaseItem, Supplier, SparePart 
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QSpinBox, QDoubleSpinBox 
from PySide6.QtWidgets import QMessageBox
from datetime import date


class PurchaseEntry(QWidget):

    def __init__(self, user):
        super().__init__()

        self.user = user

        self.setWindowTitle(
            "Purchase Entry"
        )

        self.resize(900,600)

        self.build_ui()
        self.load_suppliers()
        self.load_spares()
        self.generate_purchase_no()



    def build_ui(self):

        layout = QVBoxLayout()
        # Purchase No
        self.purchase_no = QLabel(
            "PUR0001"
        )

        layout.addWidget(
            QLabel("Purchase No")
        )

        layout.addWidget(
            self.purchase_no
        )


        # Supplier

        layout.addWidget(
            QLabel("Supplier")
        )

        self.supplier = QComboBox()
        self.supplier.setEditable(True) 
        self.supplier.setInsertPolicy(QComboBox.NoInsert)       
        self.supplier.setPlaceholderText(
            "Select Supplier"
        )
        completer = self.supplier.completer()
        completer.setFilterMode(Qt.MatchContains)
        completer.setCompletionMode(QCompleter.PopupCompletion)

        layout.addWidget(
            self.supplier
        )


        # Remarks

        self.remarks = QTextEdit()

        self.remarks.setPlaceholderText(
            "Remarks"
        )

        layout.addWidget(
            self.remarks
        )


        # Item section
        item_layout = QHBoxLayout()
        self.spare = QComboBox()
        self.lbl_part_no = QLabel("-")
        #self.lbl_part_no.setReadOnly(True)
        self.lbl_part_name = QLabel("-")
        self.lbl_category = QLabel("-")
        self.lbl_brand = QLabel("-")
        self.lbl_model = QLabel("-")
        self.lbl_unit = QLabel("-")
        self.lbl_stock = QLabel("-")

        self.qty = QSpinBox()
        self.qty.setValue(1)
        self.qty.setMinimum(1)
        self.qty.setMaximum(999999)


        self.price = QDoubleSpinBox()    
        self.price.setDecimals(3)
        self.price.setMinimum(0.001)
        self.price.setMaximum(999999.999)   
        self.price.setSingleStep(0.100)
        self.price.suffix = " OMR"
        


        item_layout.addWidget(
            self.spare
        )

        self.spare.currentIndexChanged.connect(
        self.load_spare_details
        )

        item_layout.addWidget(
            self.qty
        )

        item_layout.addWidget(
            self.price
        )


        self.add_item_btn = QPushButton(
            "Add Item"
        )
        self.remove_item_btn = QPushButton(
                    "Remove Item"
                )

        item_layout.addWidget(
            self.add_item_btn
        )
        item_layout.addWidget(
            self.remove_item_btn
        )

        layout.addLayout(
            item_layout
        )


        # Table

        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels(
            [
                 "ID",
                 "Part No",
                "Part Name",
                "Qty",
                "Price",
                "Total"
            ]
        )
        self.table.setColumnHidden(0, True)

        layout.addWidget(
            self.table
        )


        # Total

        self.total_label = QLabel(
            "Grand Total : 0.000"
        )

        layout.addWidget(
            self.total_label

        )

        ''' layout.addWidget(QLabel("Part Number"))
        layout.addWidget(self.part_no)

        layout.addWidget(QLabel("Category"))
        layout.addWidget(self.lbl_category)

        layout.addWidget(QLabel("Brand"))
        layout.addWidget(self.lbl_brand)

        layout.addWidget(QLabel("Model"))
        layout.addWidget(self.lbl_model)

        layout.addWidget(QLabel("Unit"))
        layout.addWidget(self.lbl_unit)

        layout.addWidget(QLabel("Current Stock"))
        layout.addWidget(self.lbl_stock)'''
        #new code for details layout
        details_layout = QFormLayout()
        details_layout.addRow("Part No :", self.lbl_part_no)
        details_layout.addRow("Part Name :", self.lbl_part_name)
        details_layout.addRow("Category :", self.lbl_category)
        details_layout.addRow("Brand :", self.lbl_brand)
        details_layout.addRow("Model :", self.lbl_model)
        details_layout.addRow("Unit :", self.lbl_unit)
        details_layout.addRow("Current Stock :", self.lbl_stock)
        layout.addLayout(details_layout)
        #end of new code for details layout

        self.spare.currentIndexChanged.connect(
        self.load_spare_details
        )

        # Buttons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton(
            "Save"
        )
        self.clear_btn = QPushButton(
            "Clear"
        )
        btn_layout.addWidget(
            self.save_btn
        )
        btn_layout.addWidget(
            self.clear_btn
        )
        layout.addLayout(
            btn_layout
        )
        self.setLayout(
            layout
        )

        self.table.setAlternatingRowColors(True)

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.setSelectionMode(
            QTableWidget.SingleSelection
        )

        self.table.horizontalHeader().setStretchLastSection(True)

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.add_item_btn.clicked.connect(
        self.add_item
        )
        self.remove_item_btn.clicked.connect(
            self.remove_item
        )
        self.save_btn.clicked.connect(
            self.save_purchase  
        )

    def load_suppliers(self):

        session = get_session()

        suppliers = session.query(Supplier).order_by(
            Supplier.company_name
        ).all()
       
        self.supplier.clear()

        self.supplier.addItem(
            "-- Select Supplier --",
            None
        )
        
        for supplier in suppliers:

            self.supplier.addItem(
                supplier.company_name,
                supplier.id
            )

        session.close()

    def load_spares(self):

        session = get_session()

        spares = session.query(SparePart).order_by(
            SparePart.part_name
        ).all()

        self.spare.clear()

        self.spare.addItem(
            "-- Select Spare --",
            None        
        )

        for spare in spares:

            self.spare.addItem(
                spare.part_name,
                spare.id
            )
    
        session.close()

    def load_spare_details(self):

        spare_id = self.spare.currentData()
         
        if spare_id is None:
            return

        session = get_session()

        spare = session.query(SparePart).filter_by(
            id=spare_id
        ).first()

        if spare:

            self.lbl_part_no.setText(
                spare.part_number
            )

            self.lbl_part_name.setText(
                spare.part_name
            )

            self.lbl_category.setText(
                spare.category.name
            )

            self.lbl_brand.setText(
                spare.brand.name
            )

            self.lbl_model.setText(
                spare.model.name
            )

            self.lbl_unit.setText(
                spare.unit.name
            )

            self.lbl_stock.setText(
                str(spare.stock_qty)
            )

            self.price.setValue(spare.purchase_price)
            self.qty.setValue(1)
            self.qty.setFocus()

        session.close()


    def add_item(self):

        spare_id = self.spare.currentData()

        if spare_id is None:
            QMessageBox.warning(
                self,
                "Error",
                "Select a spare part."
            )
            return

        if self.qty.value() == 0:
            QMessageBox.warning(
                self,
                "Error",
                "Enter quantity."
            )
            return

        if self.price.value() == 0:
            QMessageBox.warning(
                self,
                "Error",
                "Enter purchase price."
            )
            return

        for row in range(self.table.rowCount()):

            if self.table.item(row, 0).text() == str(self.spare.currentData()): 

                reply = QMessageBox.question(
                    self,
                    "Duplicate Spare",
                    f"{self.spare.currentText()} is already added.\n\n"
                    "Do you want to merge the quantity?",
                    QMessageBox.Yes | QMessageBox.Cancel
                )

                if reply == QMessageBox.Yes:

                    '''old_qty = float(self.table.item(row, 2).text())
                    new_qty = old_qty + self.qty.value()
                    price = self.price.value()
                    total = new_qty * price
                    self.table.item(row, 2).setText(f"{new_qty:.0f}")
                    self.table.item(row, 3).setText(f"{price:.3f}")
                    self.table.item(row, 4).setText(f"{total:.3f}")'''
                    old_qty = float(self.table.item(row, 3).text())
                    new_qty = old_qty + self.qty.value()
                    price = self.price.value()
                    total = new_qty * price
                    self.table.item(row, 3).setText(f"{new_qty:.0f}")
                    self.table.item(row, 4).setText(f"{price:.3f}")
                    self.table.item(row, 5).setText(f"{total:.3f}")

                    self.calculate_total()

                    self.qty.setValue(1)

                    self.qty.setFocus()

                    return

                else:

                    return

        qty = float(self.qty.value())
        price = float(self.price.value())

        total = qty * price

        row = self.table.rowCount()

        self.table.insertRow(row)

        self.table.setItem(row,0,QTableWidgetItem(str(self.spare.currentData())))
        self.table.setItem(row,1,QTableWidgetItem(self.lbl_part_no.text()))
        self.table.setItem(row,2,QTableWidgetItem(self.spare.currentText()))
        self.table.setItem(row,3,QTableWidgetItem(str(f"{qty:.0f}")))  
        self.table.setItem(row,4,QTableWidgetItem(f"{price:.3f}"))
        self.table.setItem(row,5,QTableWidgetItem(f"{total:.3f}"))
                

        self.calculate_total()

        self.qty.setValue(1)
        self.price.setValue(0.001)
        self.qty.setFocus() 
        self.spare.setCurrentIndex(0)
        self.reset_spare_details()



    def calculate_total(self):

        grand_total = 0

        for row in range(self.table.rowCount()):

            grand_total += float(
                self.table.item(row, 5).text()
            )
        self.grand_total = grand_total

        self.total_label.setText(
            f"Grand Total : {grand_total:.3f} OMR"
        )
    def remove_item(self):

        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self,
                "Remove Item",
                "Please select an item first."
            )
            return

        item_name = self.table.item(row, 1).text()

        reply = QMessageBox.question(
            self,
            "Remove Item",
            f"Remove {item_name} from purchase?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:

            self.table.removeRow(row)

            self.calculate_total()


    def save_purchase(self):

        session = get_session()

        try:
            self.save_btn.setEnabled(False)
            if self.supplier.currentData() is None:
                    QMessageBox.warning(
                        self,
                        "Purchase",
                        "Please select a supplier."
                    )
                    return

            if self.table.rowCount() == 0:
                    QMessageBox.warning(
                        self,
                        "Purchase",
                        "Please add at least one spare."
                    )
                    return
            purchase = Purchase(

                purchase_no=self.purchase_no.text(),

                purchase_date=date.today(),

                supplier_id=self.supplier.currentData(),

                remarks=self.remarks.toPlainText(),

                grand_total=float(self.grand_total),

                created_by=self.user.username
            )
            session.add(purchase)
            session.flush()  # Flush to get the purchase ID
            for row in range(self.table.rowCount()):

            

                spare_id = int(self.table.item(row, 0).text())

                qty = int(float(self.table.item(row, 3).text()))

                price = float(self.table.item(row, 4).text())

                total = float(self.table.item(row, 5).text())

                item = PurchaseItem(
                    purchase_id=purchase.id,
                    spare_id=spare_id,
                    quantity=qty,
                    purchase_price=price,
                    total=total
                )

                session.add(item)
                spare = session.get(
                SparePart,
                spare_id
                )
                spare.stock_qty += qty
                spare.purchase_price = price
            purchase_no = purchase.purchase_no
            item_count = self.table.rowCount()
            grand_total = self.grand_total
            session.commit()
        except Exception as e: 
            session.rollback()
            QMessageBox.critical(
                self,
                "Error",
                f"An error occurred while saving the purchase: {str(e)}"
            )
            return
        finally:
            session.close()
            self.save_btn.setEnabled(True)
            
        QMessageBox.information(
            self,
            "Purchase Saved",
            f"Purchase No : {purchase_no}\n\n"
            f"Items : {item_count}\n"
            f"Total : {grand_total:.3f} OMR\n\n"
            "Purchase saved successfully."
        )
        self.generate_purchase_no()
        self.table.setRowCount(0)
        self.calculate_total()
        self.remarks.clear()
        self.qty.setValue(1)
        self.price.setValue(0.001)
        self.supplier.setCurrentIndex(0)
        self.spare.setCurrentIndex(0)
        self.reset_spare_details()


    def generate_purchase_no(self):

        session = get_session()

        last_purchase = (
            session.query(Purchase)
            .order_by(Purchase.id.desc())
            .first()
        )

        if last_purchase is None:

            self.purchase_no.setText("PUR0001")

        else:

            last_no = last_purchase.purchase_no

            try:
                number = int(last_no.replace("PUR", ""))
            except ValueError:
                number = 0

            number += 1

            self.purchase_no.setText(
                f"PUR{number:04d}"
            )

        session.close()


    def reset_spare_details(self):
        self.lbl_part_no.setText("-")
        self.lbl_part_name.setText("-")
        self.lbl_category.setText("-")
        self.lbl_brand.setText("-")
        self.lbl_model.setText("-")
        self.lbl_unit.setText("-")
        self.lbl_stock.setText("-")


    def refresh_master_data(self):
        self.load_suppliers()
        self.load_spares()        
    def refresh_page(self):

        self.load_suppliers()
        self.load_spares()
        self.generate_purchase_no()
        self.supplier.setCurrentIndex(-1)
        self.supplier.lineEdit().clear()
        self.supplier.lineEdit().setPlaceholderText("Select Supplier")
        self.spare.setCurrentIndex(0)
        self.remarks.clear()
        self.table.setRowCount(0)
        self.calculate_total()
        self.qty.setValue(1)
        self.price.setValue(0.001)
        self.reset_spare_details()