from pyexpat import model

from PySide6.QtWidgets import *
from database import get_session
from models import Model,Brand        
from permissions import Permissions

class ModelMaster(QWidget):

    def __init__(self, user):
        super().__init__()

        self.user = user
        self.selected_id = None

        self.setWindowTitle("Model Master")
        self.resize(600, 400)

        layout = QVBoxLayout()
        # Brand
        self.brand = QComboBox()
        layout.addWidget(QLabel("Brand"))
        
        layout.addWidget(self.brand)

        #layout.addWidget(QLabel("Brand"))

        #layout.addWidget(self.brand)
        # Model Name
        layout.addWidget(QLabel("Model Name"))
        self.model_name = QLineEdit()
        self.model_name.setPlaceholderText(
            "Enter Model Name"
        )

        layout.addWidget(
            self.model_name
        )
        # Brand
        #self.brand = QComboBox()

        

        # Buttons
        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("Save")
        self.update_btn = QPushButton("Update")
        self.delete_btn = QPushButton("Delete")
        self.clear_btn = QPushButton("Clear")


        self.add_btn.clicked.connect(
            self.save_model
        )

        self.update_btn.clicked.connect(
            self.update_model
        )

        self.delete_btn.clicked.connect(
            self.delete_model       
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

        self.table.setColumnCount(3)

        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Brand",
                "Model"
            ]
        )
            

        self.table.cellClicked.connect(
            self.select_model                                       
        )


        layout.addWidget(
            self.table
        )


        self.setLayout(layout)
        
        self.load_brands()
        self.load_models()

        # Permission
        if not Permissions.is_admin(self.user):

            self.add_btn.setEnabled(False)
            self.update_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)



    def load_models(self):

        session = get_session()

        models = session.query(Model).join(Brand).all()


        self.table.setRowCount(
            len(models)
        )


        for row, model in enumerate(models):

            '''self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(model.id)
                )
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    model.name
                )
            )'''
            self.table.setItem(
            row,
            0,
            QTableWidgetItem(str(model.id))
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(model.brand.name)
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(model.name)
            )


        session.close()



    def save_model(self):

        name = self.model_name.text().strip()


        if not name:

            QMessageBox.warning(
                self,
                "Error",
                "Enter model name"
            )
            return
        
        session = get_session()
        brand_id = self.brand.currentData()
        existing = session.query(Model).filter_by(
            brand_id=brand_id,
            name=name.upper()
        ).first()

        if existing:
            QMessageBox.warning(
                self,
                "Duplicate",
                "Model already exists."
            )
            session.close()
            return
        '''
        session = get_session()
        brand_id = self.brand.currentData()
        if brand_id is None:
            QMessageBox.warning(
                self,
                "Error",
                "Select Brand"
            )
            return
'''

        model = Model(
            brand_id=brand_id,
            name=name.upper()
            )


        session.add(model)

        session.commit()

        session.close()


        QMessageBox.information(
            self,
            "Success",
            "Model saved"
        )


        self.clear_form()

        self.load_models()



    def select_model(self, row, column):

        self.selected_id = int(
            self.table.item(row,0).text()
        )


        brand_name = self.table.item(row,1).text()

        index = self.brand.findText(brand_name)

        if index >= 0:
            self.brand.setCurrentIndex(index)

        self.model_name.setText(
            self.table.item(row,2).text()
        )



    def update_model(self):

        if not self.selected_id:
            return


        session = get_session()


        model = session.query(
            Model       
        ).filter_by(
            id=self.selected_id
        ).first()

        model.brand_id = self.brand.currentData()
        model.name = (
            self.model_name.text()
            .upper()
            .strip()
        )


        session.commit()

        session.close()


        self.load_models()

        self.clear_form()



    def delete_model(self):

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


        model = session.query(
            Model   
        ).filter_by(
            id=self.selected_id
        ).first()


        session.delete(model)

        session.commit()

        session.close()


        self.load_models()

        self.clear_form()



    def clear_form(self):

        self.model_name.clear()
        self.brand.setCurrentIndex(0)

        self.selected_id = None

    def load_brands(self):

        session = get_session()

        brands = session.query(Brand).order_by(Brand.name).all()

        self.brand.clear()


        self.brand.addItem("", None)

        for brand in brands:
            self.brand.addItem(
                brand.name,
                brand.id
            )

        session.close()