# tests/test_solver_knuth.py

import numpy as np
from model.solver_knuth import KnuthEngine
from model.evaluator import score


def test_knuth_initial_guess():
    colors = ["R", "G", "B", "Y", "O"]
    engine = KnuthEngine(colors, allow_duplicates=False)

    guess = engine.next_guess()
    assert isinstance(guess, list)
    assert len(guess) == 5
    assert all(c in colors for c in guess)


def test_knuth_filter_reduces_candidates():
    colors = ["R", "G", "B", "Y", "O"]
    engine = KnuthEngine(colors, allow_duplicates=False)

    initial_count = np.sum(engine.candidates_mask)

    guess = engine.next_guess()
    blacks, whites = score(guess, ["R", "G", "B", "Y", "O"])

    engine.filter((blacks, whites))
    new_count = np.sum(engine.candidates_mask)

    assert new_count <= initial_count
    assert new_count > 0


def test_knuth_converges_simple_secret():
    colors = ["R", "G", "B", "Y", "O"]
    secret = ["R", "G", "B", "Y", "O"]

    engine = KnuthEngine(colors, allow_duplicates=False)

    for _ in range(12):
        guess = engine.next_guess()
        blacks, whites = score(guess, secret)
        engine.filter((blacks, whites))
        if blacks == 5:
            return

    assert False, "Knuth n'a pas trouvé le code en 12 coups"


def test_knuth_allows_duplicates_when_enabled():
    colors = ["R", "G", "B"]
    engine = KnuthEngine(colors, allow_duplicates=True)

    guess = engine.next_guess()
    # Avec doublons autorisés, on doit pouvoir voir des répétitions
    assert len(guess) == 5
    assert any(guess.count(c) > 1 for c in colors)
