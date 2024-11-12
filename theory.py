# theory.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class Theory(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create layout and widget for Theory Tab
        layout = QVBoxLayout()
        self.label = QLabel("This is the Theory tab.")
        layout.addWidget(self.label)
        self.setLayout(layout)
