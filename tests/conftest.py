# tests/conftest.py

import pytest
from PyQt6.QtWidgets import QApplication, QMessageBox
from unittest.mock import patch

from view.main_window import MainWindow
from controller.game_controller import GameController


# ---------------------------------------------------------------------------
# FIXTURE Qt6 STABLE POUR CI (QApplication unique)
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def qapp_session():
    """
    QApplication unique pour toute la session de tests.
    Indispensable pour stabiliser PyQt6 + Qt6 en CI (évite les abort).
    """
    app = QApplication([])
    return app


# ---------------------------------------------------------------------------
# FIXTURE POUR LES TESTS GUI (MainWindow + GameController)
# ---------------------------------------------------------------------------
@pytest.fixture
def setup_app(qtbot, qapp_session):
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


# ---------------------------------------------------------------------------
# FIXTURE POUR DÉSACTIVER LES QMessageBox EN TEST
# ---------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def disable_message_boxes():
    """
    Empêche les QMessageBox de bloquer les tests.
    """
    with patch.object(QMessageBox, "information", return_value=None), \
         patch.object(QMessageBox, "warning", return_value=None), \
         patch.object(QMessageBox, "critical", return_value=None):
        yield

