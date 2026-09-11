# view/palette_dialog.py

from PyQt6.QtWidgets import QDialog, QHBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal


class PaletteDialog(QDialog):
    """
    Boîte de dialogue affichant une palette de couleurs.
    Émet la couleur sélectionnée puis se ferme.
    """

    color_selected = pyqtSignal(str)

    def __init__(self, colors, parent=None):
        super().__init__(parent)

        self.colors = colors
        self.setWindowTitle("Palette de couleurs")
        self.setModal(True)

        self._build_ui()

    def _build_ui(self):
        """
        Construit la palette de boutons colorés.
        """
        layout = QHBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        for color in self.colors:
            btn = QPushButton("")
            btn.setFixedSize(40, 40)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    border: 2px solid #5a4632;
                    border-radius: 20px;
                }}
            """)
            btn.clicked.connect(lambda _, c=color: self._on_color_selected(c))
            layout.addWidget(btn)

    def _on_color_selected(self, color):
        """
        Émet la couleur choisie et ferme la boîte.
        """
        self.color_selected.emit(color)
        self.accept()

