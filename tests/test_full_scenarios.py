# MASTERMIND_final/tests/test_full_scenarios.py

from PyQt6.QtWidgets import QToolBar
from PyQt6.QtCore import Qt
from model.evaluator import score

def test_scenario_player_wins(setup_app):
    window, controller, qtbot = setup_app

    controller.set_mode("player")
    secret = ["R", "G", "B", "Y", "O"]
    controller.state.set_secret_code(secret)

    for col, color in enumerate(secret):
        window.board.pion_widgets[(0, col)].set_color(color)

    toolbar = window.findChild(QToolBar)
    validate_btn = toolbar.widgetForAction(window.action_validate)

    qtbot.mouseClick(validate_btn, Qt.LeftButton)

    assert controller.state.current_row == 0


def test_scenario_computer_finds_code(setup_app):
    window, controller, qtbot = setup_app

    controller.set_mode("computer")
    secret = ["R", "G", "B", "Y", "O"]

    for i, col in enumerate(secret):
        window.board.secret_widgets[i].set_color(col)

    toolbar = window.findChild(QToolBar)
    validate_btn = toolbar.widgetForAction(window.action_validate)

    qtbot.mouseClick(validate_btn, Qt.LeftButton)

    for _ in range(12):
        guess = controller.engine.current_guess
        blacks, whites = score(guess, secret)

        row = controller.state.current_row
        for idx in range(5):
            fb = window.board.feedback_widgets[(row, idx)]
            if idx < blacks:
                fb.setStyleSheet("background-color: black;")
            elif idx < blacks + whites:
                fb.setStyleSheet("background-color: #d0d0d0;")
            else:
                fb.setStyleSheet("background-color: #f5e9d3;")

        qtbot.mouseClick(validate_btn, Qt.LeftButton)

        if blacks == 5:
            return

    assert False, "L'ordinateur n'a pas trouvé le code"


def test_scenario_player_loses(setup_app):
    window, controller, qtbot = setup_app

    controller.set_mode("player")
    secret = ["R", "G", "B", "Y", "O"]
    controller.state.set_secret_code(secret)

    wrong = ["O", "O", "O", "O", "O"]

    toolbar = window.findChild(QToolBar)
    validate_btn = toolbar.widgetForAction(window.action_validate)

    for row in range(12):
        for col in range(5):
            window.board.pion_widgets[(row, col)].set_color(wrong[col])

        qtbot.mouseClick(validate_btn, Qt.LeftButton)

    assert controller.state.is_game_over() is True


