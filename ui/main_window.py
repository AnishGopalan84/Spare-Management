from models import MaterialIssue
from ui.spare_master import SpareMaster
#from ui.category_master import CategoryMaster
from ui.customer_master import CustomerMaster
from ui.supplier_master import SupplierMaster
from ui.purchase_entry import PurchaseEntry
from ui.material_issue import MaterialIssueEntry
from ui.invoice_entry import InvoiceEntry
from ui.master_setup import MasterSetup
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget
)


class MainWindow(QMainWindow):

    def __init__(self, user):
        super().__init__()

        self.user = user
        #tempory code
        #print("Logged User:", self.user.fullname)
        #print("Role:", self.user.role)
        #tempory code
        self.setWindowTitle(
            "Spare Management System"
        )

        self.resize(1200, 700)
        self.master_page = MasterSetup(self.user)

        # Main Widget
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout()
        central.setLayout(main_layout)

        self.master_page = MasterSetup(self.user)
        #self.pages.addWidget(self.master_page)
        


        # Left Menu
        menu_layout = QVBoxLayout()
        self.dashboard_btn = QPushButton("Dashboard")
        self.spare_btn = QPushButton("Spare Master")
        self.customer_btn = QPushButton("Customer Master")
        self.supplier_btn = QPushButton("Supplier Master")
        self.master_btn = QPushButton("Master Setup")
        self.purchase_btn = QPushButton("Purchase Entry")
        self.material_issue_btn = QPushButton("Material Issue")
        self.invoice_btn = QPushButton("Invoice")



        '''menu_layout.addWidget(
            self.category_btn
        )'''
        
        self.logout_btn = QPushButton("Logout")


        menu_layout.addWidget(self.dashboard_btn)
        menu_layout.addWidget(self.spare_btn)
        menu_layout.addWidget(self.customer_btn)
       # menu_layout.addWidget(self.category_btn)
        menu_layout.addWidget(self.supplier_btn)
        menu_layout.addWidget(self.master_btn)
        menu_layout.addWidget(self.purchase_btn)
        menu_layout.addWidget(self.material_issue_btn)
        menu_layout.addWidget(self.invoice_btn)
        menu_layout.addStretch()

        menu_layout.addWidget(self.logout_btn)


        # Content Area

        self.pages = QStackedWidget()


        dashboard = QLabel(
            f"""
            Welcome : {self.user.fullname}

            Role : {self.user.role}

            Spare Management System
            """
        )

        dashboard.setStyleSheet(
            "font-size:20px;padding:20px;"
        )


        # Add pages

        self.dashboard_page = dashboard

        self.spare_page = SpareMaster(self.user)
        #self.category_page = CategoryMaster(self.user)
        self.customer_page = CustomerMaster(self.user)
        self.master_page = MasterSetup(self.user)
        self.supplier_page = SupplierMaster(self.user)
        self.purchase_page = PurchaseEntry(self.user)
        self.material_issue_page = MaterialIssueEntry(self.user)
        self.invoice_page = InvoiceEntry(self.user)
        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.spare_page)       
        self.pages.addWidget(self.customer_page)
        self.pages.addWidget(self.master_page)
        self.pages.addWidget(self.supplier_page)
        self.pages.addWidget(self.purchase_page)
        self.pages.addWidget(self.material_issue_page)
        self.pages.addWidget(self.invoice_page)



        # Button actions

        self.dashboard_btn.clicked.connect(
            lambda: self.pages.setCurrentIndex(0)
        )


        self.spare_btn.clicked.connect(
            self.open_spare_master
        )   
       
        self.customer_btn.clicked.connect(
            lambda: self.pages.setCurrentIndex(2)
        )
        self.master_btn.clicked.connect(
            lambda: self.pages.setCurrentIndex(3)
                )
        self.supplier_btn.clicked.connect(
            lambda: self.pages.setCurrentIndex(4)
        )

        self.purchase_btn.clicked.connect(
            self.open_purchase
            )
        self.material_issue_btn.clicked.connect(
            self.open_material_issue
        )
        self.invoice_btn.clicked.connect(
            lambda: self.pages.setCurrentIndex(7)
        )
        main_layout.addLayout(menu_layout, 1)
        main_layout.addWidget(self.pages, 4)

    def open_purchase(self):

        if self.purchase_page.table.rowCount() > 0:
            reply = QMessageBox.question(
                self,
                "New Purchase",
                "Current purchase will be cleared.\nContinue?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
        self.purchase_page.refresh_page()
        self.pages.setCurrentIndex(5)

    def open_material_issue(self):

        if self.material_issue_page.table.rowCount() > 0:
            reply = QMessageBox.question(
                self,
                "New Material Issue",
                "Current material issue will be cleared.\nContinue?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                    return
        self.material_issue_page.refresh_page()
        self.pages.setCurrentIndex(6)



    def open_spare_master(self):
    
       self.spare_page.refresh_page()
       self.pages.setCurrentWidget(self.spare_page)