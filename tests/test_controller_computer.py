# tests/test_controller_computer.py

import pytest
from PyQt6.QtWidgets import QToolBar
from PyQt6.QtCore import Qt

from model.evaluator import score


def test_computer_mode_initial(setup_app):
    window, controller, qtbot = setup_app

    controller.set_mode("computer")

    assert controller.state.current_row == 0
    assert controller.engine.current_guess is None


def test_computer_first_guess(setup_app):
    window, controller, qtbot = setup_app

    controller.set_mode("computer")

    secret = ["R", "G", "B", "Y", "O"]
    for i, col in enumerate(secret):
        window.board.secret_widgets[i].set_color(col)

    toolbar = window.findChild(QToolBar)
    validate_btn = toolbar.widgetForAction(window.action_validate)

    qtbot.mouseClick(validate_btn, Qt.LeftButton)

    guess = controller.engine.current_guess
    assert guess is not None
    assert len(guess) == 5


def test_computer_feedback_and_next_guess(setup_app):
    window, controller, qtbot = setup_app

    controller.set_mode("computer")

    secret = ["R", "G", "B", "Y", "O"]
    for i, col in enumerate(secret):
        window.board.secret_widgets[i].set_color(col)

    toolbar = window.findChild(QToolBar)
    validate_btn = toolbar.widgetForAction(window.action_validate)

    qtbot.mouseClick(validate_btn, Qt.LeftButton)
    guess = controller.engine.current_guess

    blacks, whites = score(guess, secret)

    for idx in range(5):
        fb = window.board.feedback_widgets[(0, idx)]
        if idx < blacks:
            fb.setStyleSheet("background-color: black;")
        elif idx < blacks + whites:
            fb.setStyleSheet("background-color: #d0d0d0;")
        else:
            fb.setStyleSheet("background-color: #f5e9d3;")

    qtbot.mouseClick(validate_btn, Qt.LeftButton)

    assert controller.state.current_row == 1
    assert controller.engine.current_guess is not None


def test_computer_converges_simple_secret(setup_app):
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
            assert controller.state.current_row <= 11
            return

    assert False, "L'ordinateur n'a pas trouvé le code en 12 coups"


 
