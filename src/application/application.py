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
            self.add_start_item
        )
        self.ui.editor_tab_elements_buttons["io"].clicked.connect(self.add_io_item)
        self.ui.editor_tab_elements_buttons["action"].clicked.connect(
            self.add_action_item
        )
        self.ui.editor_tab_elements_buttons["condition"].clicked.connect(
            self.add_condition_item
        )
        self.ui.editor_tab_elements_buttons["end"].clicked.connect(self.add_end_item)

    def add_start_item(self):
        self.ui.scene.addItem(EllipseItem(QRectF(*settings.DELAULT_RECT)))

    def add_io_item(self):
        self.ui.scene.addItem(IOItem(QRectF(*settings.DELAULT_RECT)))

    def add_action_item(self):
        self.ui.scene.addItem(ActionItem(QRectF(*settings.DELAULT_RECT)))

    def add_condition_item(self):
        self.ui.scene.addItem(ConditionItem(QRectF(*settings.DELAULT_RECT)))

    def add_end_item(self):
        self.ui.scene.addItem(EllipseItem(QRectF(*settings.DELAULT_RECT)))

    def execute(self):
        self.ui.show()
        self.application.exec()
