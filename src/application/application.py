from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRectF
from ui.ui import ApplicationUI
from ui.items.algorithm import ActionItem, ConditionItem, EllipseItem, IOItem
import settings


class Application:
    def __init__(self, title):
        # Application
        self.application: QApplication = QApplication([])

        # UI
        self.ui: ApplicationUI = ApplicationUI(title)

        self.ui.editor_tab_elements_buttons["start"].clicked.connect(
            lambda: self.add_item(EllipseItem)
        )
        self.ui.editor_tab_elements_buttons["io"].clicked.connect(
            lambda: self.add_item(IOItem)
        )
        self.ui.editor_tab_elements_buttons["action"].clicked.connect(
            lambda: self.add_item(ActionItem)
        )
        self.ui.editor_tab_elements_buttons["condition"].clicked.connect(
            lambda: self.add_item(ConditionItem)
        )
        self.ui.editor_tab_elements_buttons["end"].clicked.connect(
            lambda: self.add_item(EllipseItem)
        )

    def add_item(self, Item):
        item = Item(QRectF(*settings.DELAULT_RECT))
        self.ui.scene.addItem(item)
        for selected_item in self.ui.scene.selectedItems():
            selected_item.setSelected(False)
        item.setSelected(True)

    def execute(self):
        self.ui.show()
        self.application.exec()
