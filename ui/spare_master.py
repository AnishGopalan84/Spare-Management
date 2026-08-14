from PySide6.QtWidgets import *
from database import get_session
from models import SparePart, Category, Brand, Model, Unit
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem,QLineEdit
from permissions import Permissions

class SpareMaster(QWidget):
    #clear fields and reset selected_spare_id when creating a new spare
    def new_spare(self):

        self.selected_spare_id = None
        self.clear_fields()

#update spare details in the database based on the selected spare id
    def update_spare(self):

        if not self.selected_spare_id:
            QMessageBox.warning(
                self,
                "Warning",
                "Please select a spare first"
            )
            return
        
        session = get_session()

        spare = session.query(SparePart).filter_by(
            id=self.selected_spare_id
        ).first()

        if spare:

            spare.part_number = self.part_number.text().upper()
            spare.part_name = self.part_name.text().upper() 
            spare.category_id = self.category.currentData()
            spare.brand_id = self.brand.currentData()
            spare.model_id = self.model.currentData()
            spare.unit_id = self.unit.currentData()

            spare.purchase_price = float(
                self.purchase_price.text() or 0
            )

            spare.selling_price = float(
                self.selling_price.text() or 0
            )

            spare.minimum_stock = int(
                self.minimum_stock.text() or 0
            )

            spare.location = self.location.text().upper()
            spare.remarks = self.remarks.text().upper()


            session.commit()


            QMessageBox.information(
                self,
                "Success",
                "Spare updated successfully"
            )
            self.load_spares()
            self.clear_fields()
            self.selected_spare_id = None
        session.close()     

  
#delete the selected spare from the database based on the selected spare id
    def delete_spare(self):

        if not self.selected_spare_id:
            QMessageBox.warning(
                self,
                "Warning",
                "Please select a spare first"
            )
            return


        reply = QMessageBox.question(
            self,
            "Confirm",
            "Delete this spare?"
        )
        if reply == QMessageBox.Yes:

            session = get_session()
            spare = session.query(SparePart).filter_by(
                id=self.selected_spare_id
            ).first()

            if spare:
                session.delete(spare)
                session.commit()
            session.close()
            QMessageBox.information(
                self,
                "Success",
                "Spare deleted"
            )
            self.load_spares()
            self.clear_fields()

#select a spare from the table and populate the input fields with its details
    def select_spare(self, item):

        row = item.row()

        session = get_session()

        part_number = self.table.item(
            row,0
        ).text()


        spare = session.query(SparePart).filter_by(
            part_number=part_number
        ).first()


        if spare:

            self.selected_spare_id = spare.id


            self.part_number.setText(
                spare.part_number
            )

            self.part_name.setText(
                spare.part_name
            )


            # Category

            index = self.category.findData(
                spare.category_id
            )

            self.category.setCurrentIndex(index)


            # Brand

            index = self.brand.findData(
                spare.brand_id
            )

            self.brand.setCurrentIndex(index)


            # Model

            index = self.model.findData(
                spare.model_id
            )

            self.model.setCurrentIndex(index)


            # Unit

            index = self.unit.findData(
                spare.unit_id
            )

            self.unit.setCurrentIndex(index)


            self.purchase_price.setText(
                str(spare.purchase_price)
            )

            self.selling_price.setText(
                str(spare.selling_price)
            )

            self.stock_qty.setText(
                str(spare.stock_qty)
            )

            self.minimum_stock.setText(
                str(spare.minimum_stock)
            )

            self.location.setText(
                spare.location or ""
            )

            self.remarks.setText(
                spare.remarks or ""
            )


        session.close()
#load all spares from the database and display them in the table
    def load_spares(self):

        session = get_session()
        spares = session.query(SparePart).all()
        self.table.setRowCount(len(spares))
        for row, spare in enumerate(spares):

            self.table.setItem(
                row,0,
                QTableWidgetItem(spare.part_number)
            )

            self.table.setItem(
                row,1,
                QTableWidgetItem(spare.part_name)
            )

            self.table.setItem(
                row,2,
                QTableWidgetItem(spare.category.name)
            )

            self.table.setItem(
                row,3,
                QTableWidgetItem(spare.brand.name)
            )

            self.table.setItem(
                row,4,
                QTableWidgetItem(spare.model.name)
            )

            self.table.setItem(
                row,5,
                QTableWidgetItem(spare.unit.name)
            )

            self.table.setItem(
                row,6,
                QTableWidgetItem(str(spare.stock_qty))
            )

            self.table.setItem(
                row,7,
                QTableWidgetItem(
                    str(spare.selling_price)
                )
            )


        session.close()
    def search_spares(self, text):

        session = get_session()

        spares = session.query(SparePart).join(
            Brand
        ).join(
            Model
        ).filter(
            (SparePart.part_number.contains(text)) |
            (SparePart.part_name.contains(text)) |
            (Brand.name.contains(text)) |
            (Model.name.contains(text))
        ).all()


        self.table.setRowCount(len(spares))


        for row, spare in enumerate(spares):

            self.table.setItem(
                row,0,
                QTableWidgetItem(spare.part_number)
            )

            self.table.setItem(
                row,1,
                QTableWidgetItem(spare.part_name)
            )

            self.table.setItem(
                row,2,
                QTableWidgetItem(spare.category.name)
            )

            self.table.setItem(
                row,3,
                QTableWidgetItem(spare.brand.name)
            )

            self.table.setItem(
                row,4,
                QTableWidgetItem(spare.model.name)
            )

            self.table.setItem(
                row,5,
                QTableWidgetItem(spare.unit.name)
            )

            self.table.setItem(
                row,6,
                QTableWidgetItem(str(spare.stock_qty))
            )

            self.table.setItem(
                row,7,
                QTableWidgetItem(str(spare.selling_price))
            )


        session.close()

    def __init__(self,user):
        self.user = user
        super().__init__()
        self.setWindowTitle("Spare Master")
        self.resize(700,500)
        ''' new line added to initialize selected_spare_id to None '''
        self.selected_spare_id = None
        self.unit = QComboBox()        
        layout = QVBoxLayout()
        # Input fields
        self.part_number = QLineEdit()
        self.part_name = QLineEdit()
        self.category = QComboBox()
        self.brand = QComboBox()
        self.model = QComboBox()
        self.unit = QComboBox()
        
        self.purchase_price = QLineEdit()
        self.selling_price = QLineEdit()
        self.stock_qty = QLineEdit()
        self.minimum_stock = QLineEdit()
        self.location = QLineEdit()
        self.remarks = QLineEdit()
        self.brand.currentIndexChanged.connect(
            self.load_models
            )
        self.load_dropdowns()
        fields = [
            ("Part Number", self.part_number),
            ("Part Name", self.part_name),
            ("Category", self.category),
            ("Brand", self.brand),
            ("Model", self.model),
            ("Unit", self.unit),
            ("Purchase Price", self.purchase_price),
            ("Selling Price", self.selling_price),
            ("Stock Qty", self.stock_qty),
            ("Minimum Stock", self.minimum_stock),
            ("Location", self.location),
            ("Remarks", self.remarks)
        ]
        
        form = QFormLayout()

        for name, widget in fields:
            form.addRow(name, widget)
        layout.addLayout(form)
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(
             "Search Part Number / Name / Brand / Model"
            )

        self.search_box.textChanged.connect(
                self.search_spares
        )

        layout.addWidget(self.search_box)

        #  Save New Update Delete Clear Button

        button_layout = QHBoxLayout()
        self.new_btn = QPushButton("New")
        self.save_btn = QPushButton("Save")
        self.update_btn = QPushButton("Update")
        self.delete_btn = QPushButton("Delete")
        self.clear_btn = QPushButton("Clear")


        self.new_btn.clicked.connect(
            self.new_spare
        )

        self.save_btn.clicked.connect(
            self.save_spare
        )

        self.update_btn.clicked.connect(
            self.update_spare
        )

        self.delete_btn.clicked.connect(
            self.delete_spare
        )

        self.clear_btn.clicked.connect(
            self.clear_fields
        )


        button_layout.addWidget(self.new_btn)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.update_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.clear_btn)


        layout.addLayout(button_layout)
        
        self.table = QTableWidget()
        
        self.table.setColumnCount(8)
        
        self.table.setHorizontalHeaderLabels([
                    "Part No",
                    "Part Name",
                    "Category",
                    "Brand",
                    "Model",
                    "Unit",
                    "Stock",
                    "Selling Price"
                ])        
        
        layout.addWidget(self.table)
        self.table.itemClicked.connect(
                            self.select_spare
                            )

        

        self.setLayout(layout)
        self.load_spares()
        #role = self.user.role.lower().strip()

        if Permissions.is_store(self.user):

            self.new_btn.setEnabled(False)
            self.save_btn.setEnabled(False)
            self.update_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)

        elif Permissions.is_inventory(self.user):

            self.delete_btn.setEnabled(False)

        elif Permissions.is_admin(self.user):

            pass

    def load_dropdowns(self):

        session = get_session()

        # Category
        self.category.clear()

        categories = session.query(Category).all()
        self.category.addItem("", None)
        for item in categories:
            self.category.addItem(item.name, item.id)


        # Brand
        self.brand.clear()

        brands = session.query(Brand).all()
        self.brand.addItem("", None)
        for item in brands:
            self.brand.addItem(item.name, item.id)


        # Unit
        self.unit.clear()

        units = session.query(Unit).all()
        self.unit.addItem("", None)
        for item in units:
            self.unit.addItem(item.name, item.id)


        session.close()

        self.load_models()

    def load_models(self):

        session = get_session()

        self.model.clear()


        brand_id = self.brand.currentData()


        if brand_id:

            models = session.query(Model).filter(
                Model.brand_id == brand_id
            ).all()

            self.model.addItem("", None)
            for item in models:
                self.model.addItem(
                    item.name,
                    item.id
                )


        session.close()


    def save_spare(self):

        

        if not self.part_number.text().strip():

            QMessageBox.warning(
                self,
                "Validation Error",
                "Please enter Part Number"
            )
            return


        if not self.part_name.text().strip():

            QMessageBox.warning(
                self,
                "Validation Error",
                "Please enter Part Name"
            )
            return


        if self.category.currentData() is None:

            QMessageBox.warning(
                self,
                "Validation Error",
                "Please select Category"
            )
            return


        if self.brand.currentData() is None:

            QMessageBox.warning(
                self,
                "Validation Error",
                "Please select Brand"
            )
            return
        

        try:
            session = get_session()

            spare = SparePart(

                part_number=self.part_number.text().upper(),

                part_name=self.part_name.text().upper(),

                category_id=self.category.currentData(),

                brand_id=self.brand.currentData(),

                model_id=self.model.currentData(),

                unit_id=self.unit.currentData(),

                purchase_price=float(self.purchase_price.text() or 0),

                selling_price=float(self.selling_price.text() or 0),

                stock_qty=int(self.stock_qty.text() or 0),

                minimum_stock=int(self.minimum_stock.text() or 0),

                location=self.location.text().upper(),

                remarks=self.remarks.text().upper()
            )

            existing = session.query(SparePart).filter_by(
                part_number=self.part_number.text()
            ).first()


            if existing:

                QMessageBox.warning(
                    self,
                    "Duplicate",
                    "Part Number already exists"
                )

                session.close()
                return
            session.add(spare)
            session.commit()
            self.load_spares()

            QMessageBox.information(
                self,
                "Success",
                "Spare saved successfully"
            )

            self.clear_fields()


        except Exception as e:

            QMessageBox.warning(
                self,
                "Error",
                str(e)
            )



    def clear_fields(self):

        self.part_number.clear()
        self.part_name.clear()

        self.category.setCurrentIndex(0)
        self.brand.setCurrentIndex(0)
        self.model.setCurrentIndex(0)
        self.unit.setCurrentIndex(0)

        self.purchase_price.clear()
        self.selling_price.clear()
        self.stock_qty.clear()
        self.minimum_stock.clear()
        self.location.clear()
        self.remarks.clear()
        self.selected_spare_id = None

    def refresh_page(self):

        self.clear_fields()
        self.load_spares()
    
            