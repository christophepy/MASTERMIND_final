# model/evaluator.py

# model/evaluator.py

def score(guess, secret):
    """
    Calcule les pions bien placés (well) et mal placés (mis)
    selon les règles Mastermind.
    """

    # Bien placés
    well = sum(g == s for g, s in zip(guess, secret))

    # Copies pour le calcul des mal placés
    secret_copy = secret[:]
    guess_copy = guess[:]

    # Neutralisation des bien placés
    for i in range(5):
        if guess_copy[i] == secret_copy[i]:
            secret_copy[i] = None
            guess_copy[i] = None

    # Mal placés
    mis = 0
    for g in guess_copy:
        if g and g in secret_copy:
            mis += 1
            secret_copy[secret_copy.index(g)] = None

    return well, mis


