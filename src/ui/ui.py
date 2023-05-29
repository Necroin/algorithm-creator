from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QGroupBox,
    QGraphicsView,
    QPushButton,
    QVBoxLayout,
    QTabWidget,
)
from PyQt6.QtCore import QPointF
from ui.widgets.scene import GridScene


class ApplicationUI(QMainWindow):
    def __init__(self, title):
        super().__init__()
        self.window = self
        self.window.setWindowTitle(title)
        self.central_widget = QWidget(self.window)
        self.central_widget_layout = QHBoxLayout(self.central_widget)
        self.central_widget.setLayout(self.central_widget_layout)
        self.window.setCentralWidget(self.central_widget)
        self.window.resize(600, 400)

        self.tab_widget = QTabWidget(self.central_widget)
        self.central_widget_layout.addWidget(self.tab_widget)

        self.add_editor_tab()
        self.add_simulation_tab()

    def add_editor_tab(self):
        self.editor_tab_widget = QWidget()
        self.editor_tab_layout = QHBoxLayout(self.editor_tab_widget)
        self.editor_tab_widget.setLayout(self.editor_tab_layout)

        self.scene = GridScene()
        self.scene.setSceneRect(-200, -200, 200, 200)
        self.view = QGraphicsView(self.scene, self.editor_tab_widget)
        self.view.centerOn(QPointF(0, 0))
        self.view.scale(1, 1)

        self.editor_tab_elements_widget = QGroupBox(self.editor_tab_widget)
        self.editor_tab_elements_layout = QVBoxLayout(self.editor_tab_elements_widget)
        self.editor_tab_elements_widget.setLayout(self.editor_tab_elements_layout)
        self.editor_tab_elements_widget.setTitle("Elements")

        self.editor_tab_elements_buttons = {
            "start": QPushButton(self.editor_tab_elements_widget),
            "io": QPushButton(self.editor_tab_elements_widget),
            "action": QPushButton(self.editor_tab_elements_widget),
            "condition": QPushButton(self.editor_tab_elements_widget),
            "end": QPushButton(self.editor_tab_elements_widget),
        }

        # self.elements_buttons["rect"].setMaximumSize(100,100)
        # self.elements_buttons["rect"].setMinimumSize(100,100)
        # self.elements_buttons["rect"].setFlat(True)

        # self.elements_buttons["rect"].setIcon(QIcon("assets/rectangle-outline.svg"))
        # self.elements_buttons["rect"].setIconSize(self.elements_buttons["rect"].size())

        for button_name, button in self.editor_tab_elements_buttons.items():
            button.setText(button_name)
            self.editor_tab_elements_layout.addWidget(button)

        self.editor_tab_elements_layout.addStretch()

        self.editor_tab_layout.addWidget(self.editor_tab_elements_widget)
        self.editor_tab_layout.addWidget(self.view)

        self.tab_widget.addTab(self.editor_tab_widget, "Editor")

    def add_simulation_tab(self):
        self.simulation_tab_widget = QWidget()
        self.simulation_tab_layout = QHBoxLayout(self.simulation_tab_widget)
        self.simulation_tab_widget.setLayout(self.simulation_tab_layout)

        self.tab_widget.addTab(self.simulation_tab_widget, "Simulation")
