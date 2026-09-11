# tests/test_evaluator.py

from model.evaluator import score

def test_score_all_correct():
    guess  = ["R","G","B","Y","O"]
    secret = ["R","G","B","Y","O"]
    assert score(guess, secret) == (5, 0)

def test_score_none_correct():
    guess  = ["R","G","B","Y","O"]
    secret = ["P","P","P","P","P"]
    assert score(guess, secret) == (0, 0)

def test_score_all_misplaced():
    guess  = ["R","G","B","Y","O"]
    secret = ["G","B","Y","O","R"]
    assert score(guess, secret) == (0, 5)

def test_score_mix_black_white():
    guess  = ["R","G","B","Y","O"]
    secret = ["R","B","G","Y","P"]
    # R bien placé → 1 noir
    # G/B/Y mal placés → 3 blancs
    assert score(guess, secret) == (2, 2)

def test_score_with_duplicates_in_guess():
    guess  = ["R","R","R","G","G"]
    secret = ["R","G","B","Y","O"]
    # 1 noir (R)
    # 1 blanc (G)
    assert score(guess, secret) == (1, 1)

def test_score_with_duplicates_in_secret():
    guess  = ["R","G","B","Y","O"]
    secret = ["R","R","R","G","G"]
    # R noir → 1
    # G blanc → 1
    assert score(guess, secret) == (1, 1)
