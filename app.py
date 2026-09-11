# app.py

import sys

from PyQt6.QtWidgets import QApplication
from view.main_window import MainWindow
from controller.game_controller import GameController


def main():
    """
    Point d'entrée de l'application Mastermind.
    Initialise l'interface et lance l'application.
    """

    app = QApplication(sys.argv)

    # Palette de couleurs (modifiable ici)
    colors = [
        "#ff0000", "#00ff00", "#0000ff",
        "#ffff00", "#ff00ff", "#00ffff",
        "#ff8800", "#8844ff", "#00aa55"
    ]

    window = MainWindow(colors)
    controller = GameController(window)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

