from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

from database import get_session
from models import SparePart


class SpareList(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Spare List")
        self.resize(900,500)

        layout = QVBoxLayout()


        # Search box
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search Part Number / Name / Brand")

        self.search.textChanged.connect(self.load_data)

        layout.addWidget(self.search)


        # Table

        self.table = QTableWidget()

        self.table.setColumnCount(9)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Part Number",
            "Part Name",
            "Category",
            "Brand",
            "Model",
            "Unit",
            "Stock",
            "Selling Price"
        ])


        self.table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.table)


        # Refresh button

        btn = QPushButton("Refresh")

        btn.clicked.connect(self.load_data)

        layout.addWidget(btn)


        self.setLayout(layout)


        self.load_data()



    def load_data(self):

        session = get_session()


        keyword = self.search.text()


        query = session.query(SparePart)


        if keyword:

            query = query.filter(
                (SparePart.part_number.contains(keyword)) |
                (SparePart.part_name.contains(keyword)) |
                (SparePart.brand.contains(keyword))
            )


        data = query.all()


        self.table.setRowCount(len(data))


        for row, spare in enumerate(data):

            self.table.setItem(row,0,QTableWidgetItem(str(spare.id)))

            self.table.setItem(row,1,QTableWidgetItem(spare.part_number))

            self.table.setItem(row,2,QTableWidgetItem(spare.part_name))

            self.table.setItem(row,3,QTableWidgetItem(spare.category))

            self.table.setItem(row,4,QTableWidgetItem(spare.brand))

            self.table.setItem(row,5,QTableWidgetItem(spare.model))

            self.table.setItem(row,6,QTableWidgetItem(spare.unit))

            self.table.setItem(row,7,QTableWidgetItem(str(spare.stock_qty)))

            self.table.setItem(row,8,QTableWidgetItem(str(spare.selling_price)))


        session.close()