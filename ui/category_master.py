from PySide6.QtWidgets import *
from database import get_session
from models import Category
from permissions import Permissions

class CategoryMaster(QWidget):

    def __init__(self, user):
        super().__init__()

        self.user = user
        self.selected_id = None

        self.setWindowTitle("Category Master")
        self.resize(600, 400)

        layout = QVBoxLayout()

        # Category Name
        self.category_name = QLineEdit()
        self.category_name.setPlaceholderText(
            "Enter Category Name"
        )

        layout.addWidget(
            self.category_name
        )


        # Buttons
        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("Save")
        self.update_btn = QPushButton("Update")
        self.delete_btn = QPushButton("Delete")
        self.clear_btn = QPushButton("Clear")


        self.add_btn.clicked.connect(
            self.save_category
        )

        self.update_btn.clicked.connect(
            self.update_category
        )

        self.delete_btn.clicked.connect(
            self.delete_category
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
                "Model Name"
            ]
        )

        self.table.cellClicked.connect(
            self.select_category
        )


        layout.addWidget(
            self.table
        )


        self.setLayout(layout)


        self.load_categories()


        # Permission
        if not Permissions.is_admin(self.user):

            self.add_btn.setEnabled(False)
            self.update_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)



    def load_categories(self):

        session = get_session()

        categories = session.query(
            Category
        ).all()


        self.table.setRowCount(
            len(categories)
        )


        for row, category in enumerate(categories):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(category.id)
                )
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    category.name
                )
            )


        session.close()



    def save_category(self):

        name = self.category_name.text().strip()


        if not name:

            QMessageBox.warning(
                self,
                "Error",
                "Enter category name"
            )

            return
        session = get_session()
        existing = session.query(Category).filter_by(
        name=self.category_name.text().upper()
        ).first()

        if existing:
            QMessageBox.warning(
            self,
            "Duplicate",
            "Category already exists."
            )
            return


        #session = get_session()


        category = Category(
            name=name.upper()
        )


        session.add(category)

        session.commit()

        session.close()


        QMessageBox.information(
            self,
            "Success",
            "Category saved"
        )


        self.clear_form()

        self.load_categories()



    def select_category(self, row, column):

        self.selected_id = int(
            self.table.item(row,0).text()
        )


        self.category_name.setText(
            self.table.item(row,1).text()
        )



    def update_category(self):

        if not self.selected_id:
            return


        session = get_session()


        category = session.query(
            Category    
        ).filter_by(
            id=self.selected_id
        ).first()


        category.name = (
            self.category_name.text()
            .upper()
        )


        session.commit()

        session.close()


        self.load_categories()

        self.clear_form()



    def delete_category(self):

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


        category = session.query(
            Category
        ).filter_by(
            id=self.selected_id
        ).first()


        session.delete(category)

        session.commit()

        session.close()


        self.load_categories()

        self.clear_form()



    def clear_form(self):

        self.category_name.clear()

        self.selected_id = None