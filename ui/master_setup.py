from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTabWidget
)

from ui.category_master import CategoryMaster
from ui.brand_master import BrandMaster
from ui.model_master import ModelMaster
from ui.unit_master import UnitMaster


class MasterSetup(QWidget):

    def __init__(self, user):
        super().__init__()

        self.user = user

        self.setWindowTitle("Master Setup")

        layout = QVBoxLayout()

        self.tabs = QTabWidget()

        self.tabs.addTab(CategoryMaster(user), "Category")
        self.tabs.addTab(BrandMaster(user), "Brand")
        self.tabs.addTab(ModelMaster(user), "Model")
        self.tabs.addTab(UnitMaster(user), "Unit")

        layout.addWidget(self.tabs)

        self.setLayout(layout)