from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRectF, QLineF
from ui.ui import ApplicationUI
from ui.items.algorithm import ActionItem, ConditionItem, EllipseItem, IOItem
from ui.items.connect import ConnectLineItem
import settings


class Application:
    def __init__(self, title):
        # Application
        self.application: QApplication = QApplication([])

        # UI
        self.ui: ApplicationUI = ApplicationUI(title)

        self.ui.editor_tab_elements_buttons["start"].clicked.connect(
            lambda: self.add_item(EllipseItem, QRectF(*settings.DELAULT_RECT))
        )
        self.ui.editor_tab_elements_buttons["io"].clicked.connect(
            lambda: self.add_item(IOItem, QRectF(*settings.DELAULT_RECT))
        )
        self.ui.editor_tab_elements_buttons["action"].clicked.connect(
            lambda: self.add_item(ActionItem, QRectF(*settings.DELAULT_RECT))
        )
        self.ui.editor_tab_elements_buttons["condition"].clicked.connect(
            lambda: self.add_item(ConditionItem, QRectF(*settings.DELAULT_RECT))
        )
        self.ui.editor_tab_elements_buttons["end"].clicked.connect(
            lambda: self.add_item(EllipseItem, QRectF(*settings.DELAULT_RECT))
        )
        self.ui.editor_tab_elements_buttons["line"].clicked.connect(
            lambda: self.add_item(ConnectLineItem, QLineF(*settings.DELAULT_LINE))
        )

    def add_item(self, Item, init):
        item = Item(init)
        self.ui.scene.addItem(item)
        for selected_item in self.ui.scene.selectedItems():
            selected_item.setSelected(False)
        item.setSelected(True)

    def execute(self):
        self.ui.show()
        self.application.exec()
