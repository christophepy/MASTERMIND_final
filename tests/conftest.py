# tests/conftest.py

import pytest
from PyQt6.QtWidgets import QApplication
from view.main_window import MainWindow
from controller.game_controller import GameController

@pytest.fixture
def setup_app(qtbot):
    """
    Crée une fenêtre MainWindow + un GameController
    et les retourne pour les tests GUI.
    """

    # Couleurs standard Mastermind
    colors = ["R", "G", "B", "Y", "O", "P", "C", "M", "W"]

    # Créer la fenêtre
    window = MainWindow(colors)
    qtbot.addWidget(window)
    window.show()

    # Créer le contrôleur (ATTENTION : GameController attend la vue)
    controller = GameController(window)

    return window, controller, qtbot

import pytest
from unittest.mock import patch
from PyQt6.QtWidgets import QMessageBox

@pytest.fixture(autouse=True)
def disable_message_boxes():
    """Empêche les QMessageBox de bloquer les tests."""
    with patch.object(QMessageBox, "information", return_value=None), \
         patch.object(QMessageBox, "warning", return_value=None), \
         patch.object(QMessageBox, "critical", return_value=None):
        yield
