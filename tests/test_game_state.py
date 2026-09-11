# tests/test_game_state.py

from model.game_state import GameState

def test_initial_state():
    gs = GameState(colors=["R","G","B"], allow_duplicates=False, mode="player")
    assert gs.mode == "player"
    assert gs.colors == ["R","G","B"]
    assert gs.allow_duplicates is False
    assert gs.current_row == 0
    assert gs.secret_code is None
    assert gs.guesses == []
    assert gs.feedbacks == []

def test_set_secret_code():
    gs = GameState(["R","G","B"])
    gs.set_secret_code(["R","B","G"])
    assert gs.secret_code == ["R","B","G"]
    assert gs.has_secret_code() is True

def test_add_guess_and_feedback():
    gs = GameState(["R","G","B"])
    gs.add_guess(["R","G","B"])
    gs.add_feedback((1, 2))
    assert gs.guesses == [["R","G","B"]]
    assert gs.feedbacks == [(1, 2)]

def test_next_row():
    gs = GameState(["R","G","B"])
    assert gs.current_row == 0
    gs.next_row()
    assert gs.current_row == 1
    gs.next_row()
    assert gs.current_row == 2

def test_is_game_over():
    gs = GameState(["R","G","B"])
    for _ in range(12):
        gs.next_row()
    assert gs.is_game_over() is True

def test_reset():
    gs = GameState(["R","G","B"])
    gs.set_secret_code(["R","G","B"])
    gs.add_guess(["R","G","B"])
    gs.add_feedback((1, 2))
    gs.next_row()

    gs.reset()

    assert gs.current_row == 0
    assert gs.secret_code is None
    assert gs.guesses == []
    assert gs.feedbacks == []
