# MASTERMIND_final/tests/test_controller_player.py

from PyQt6.QtWidgets import QToolBar
from PyQt6.QtCore import Qt

def test_player_mode_initial(setup_app):
    window, controller, qtbot = setup_app
    controller.set_mode("player")
    assert controller.state.current_row == 0


def test_player_validates_first_row(setup_app):
    window, controller, qtbot = setup_app

    controller.set_mode("player")
    controller.state.set_secret_code(["R", "G", "B", "Y", "O"])

    for col, color in enumerate(["R", "G", "B", "Y", "O"]):
        window.board.pion_widgets[(0, col)].set_color(color)

    toolbar = window.findChild(QToolBar)
    validate_btn = toolbar.widgetForAction(window.action_validate)

    qtbot.mouseClick(validate_btn, Qt.LeftButton)

    assert controller.state.current_row == 0


def test_player_wins(setup_app):
    window, controller, qtbot = setup_app

    controller.set_mode("player")
    controller.state.set_secret_code(["R", "G", "B", "Y", "O"])

    for col, color in enumerate(["R", "G", "B", "Y", "O"]):
        window.board.pion_widgets[(0, col)].set_color(color)

    toolbar = window.findChild(QToolBar)
    validate_btn = toolbar.widgetForAction(window.action_validate)

    qtbot.mouseClick(validate_btn, Qt.LeftButton)

    assert controller.state.current_row == 0

