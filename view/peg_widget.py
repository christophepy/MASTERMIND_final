# view/peg_widget.py

from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import pyqtSignal


class PegWidget(QPushButton):
    """
    Bouton représentant un pion Mastermind.
    Gère sa couleur et émet un signal lors du clic.
    """

    clicked_with_self = pyqtSignal(object)

    def __init__(self, size=32, parent=None):
        super().__init__(parent)

        self._color = None
        self.setFixedSize(size, size)

        # Style de base sans couleur
        self._base_style = """
            QPushButton {
                border: 2px solid #5a4632;
                border-radius: 16px;
            }
        """

        self.setStyleSheet(self._base_style)
        self.clicked.connect(self._on_clicked)

    def set_color(self, color):
        """
        Applique la couleur visuelle du pion.
        """
        self._color = color

        bg = (
            "background-color: #f5e9d3;"
            if color is None
            else f"background-color: {color};"
        )

        self.setStyleSheet(f"""
            QPushButton {{
                {bg}
                border: 2px solid #5a4632;
                border-radius: 16px;
            }}
        """)

    def color(self):
        """
        Retourne la couleur actuelle du pion.
        """
        return self._color

    def _on_clicked(self):
        """
        Émet le signal avec le widget lui-même.
        """
        self.clicked_with_self.emit(self)



