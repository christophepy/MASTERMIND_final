# tests/test_controller_player.py

import pytest
from PyQt6.QtWidgets import QToolBar
from PyQt6.QtCore import Qt


@pytest.mark.gui
def test_player_validates_first_row(setup_app):
    window, controller, qtbot = setup_app

    controller.set_mode("player")
    controller.state.set_secret_code(["R", "G", "B", "Y", "O"])

    for col, color in enumerate(["R", "G", "B", "Y", "O"]):
        window.board.pion_widgets[(0, col)].set_color(color)

    toolbar = window.findChild(QToolBar)
    validate_btn = toolbar.widgetForAction(window.action_validate)

    qtbot.mouseClick(validate_btn, Qt.MouseButton.LeftButton)

    assert controller.state.current_row == 1


@pytest.mark.gui
def test_player_wins(setup_app):
    window, controller, qtbot = setup_app

    controller.set_mode("player")
    controller.state.set_secret_code(["R", "G", "B", "Y", "O"])

    for col, color in enumerate(["R", "G", "B", "Y", "O"]):
        window.board.pion_widgets[(0, col)].set_color(color)

    toolbar = window.findChild(QToolBar)
    validate_btn = toolbar.widgetForAction(window.action_validate)

    qtbot.mouseClick(validate_btn, Qt.MouseButton.LeftButton)

    assert controller.state.game_over is True
    assert controller.state.player_won is True


