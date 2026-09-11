# model/game_state.py

class GameState:
    """
    État du jeu Mastermind : mode, code secret, progression et historique.
    """

    def __init__(self, colors, allow_duplicates=False, mode="player"):
        self.mode = mode
        self.colors = colors[:]          # copie défensive
        self.allow_duplicates = allow_duplicates

        self.current_row = 0
        self.secret_code = None
        self.guesses = []
        self.feedbacks = []
        self.game_over = False

    # ----------------------------------------------------------------------
    # Code secret
    # ----------------------------------------------------------------------

    def set_secret_code(self, code):
        """Définit le code secret."""
        self.secret_code = code

    def has_secret_code(self):
        """Retourne True si le code secret est défini."""
        return self.secret_code is not None

    # ----------------------------------------------------------------------
    # Historique
    # ----------------------------------------------------------------------

    def add_guess(self, guess):
        """Ajoute une proposition à l'historique."""
        self.guesses.append(guess)

    def add_feedback(self, feedback):
        """Ajoute un feedback à l'historique."""
        self.feedbacks.append(feedback)

    # ----------------------------------------------------------------------
    # Progression
    # ----------------------------------------------------------------------

    def next_row(self):
        """Passe à la ligne suivante et détecte la fin de partie."""
        self.current_row += 1
        if self.current_row >= 12:
            self.game_over = True

    def is_game_over(self):
        """Retourne True si les 12 lignes ont été utilisées."""
        return self.game_over

    # ----------------------------------------------------------------------
    # Réinitialisation
    # ----------------------------------------------------------------------

    def reset(self):
        """Réinitialise l'état du jeu."""
        self.current_row = 0
        self.secret_code = None
        self.guesses.clear()
        self.feedbacks.clear()
        self.game_over = False



    