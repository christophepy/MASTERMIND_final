# controller/game_controller.py

import random

from model.game_state import GameState
from model.evaluator import score
from model.solver_knuth import KnuthEngine
from PyQt6.QtWidgets import QMessageBox


class GameController:
    """
    Contrôleur principal du jeu Mastermind.
    Coordonne la vue, l'état du jeu et les moteurs de résolution.
    """

    def __init__(self, view):
        self.view = view
        self.base_colors = view.colors[:]
        self.state = GameState(colors=self.base_colors, allow_duplicates=False)
        self.engine = None

        self._connect_view_signals()
        self._reset_game()
        self.view.board.apply_mode(self.state.mode)

    def _connect_view_signals(self):
        """
        Connecte les signaux de la vue aux méthodes du contrôleur.
        """
        v = self.view

        v.validate_requested.connect(self.validate)
        v.mode_changed.connect(self.set_mode)
        v.level_changed.connect(self.apply_level)

        b = v.board
        b.peg_clicked.connect(self.on_peg_clicked)
        b.secret_clicked.connect(self.on_secret_clicked)
        b.feedback_clicked.connect(self.on_feedback_clicked)

    # ----------------------------------------------------------------------
    # MODE
    # ----------------------------------------------------------------------

    def set_mode(self, mode):
        """
        Change le mode de jeu et réinitialise l'état.
        """
        self.state.mode = mode
        self._reset_game()
        self.view.board.apply_mode(mode)

        if mode == "player":
            self.view.show_status("Mode Joueur : trouve le code.")
        else:
            self.view.show_status("Mode Ordinateur : définis ton code.")

    # ----------------------------------------------------------------------
    # NIVEAU
    # ----------------------------------------------------------------------

    def apply_level(self, nb_colors, allow_duplicates):
        """
        Applique un niveau : palette et règle de doublons.
        """
        self.state.colors = self.base_colors[:nb_colors]
        self.state.allow_duplicates = allow_duplicates

        self.view.board.update_palette(self.state.colors)
        self._reset_game()
        self.view.board.apply_mode(self.state.mode)

    # ----------------------------------------------------------------------
    # RESET
    # ----------------------------------------------------------------------

    def _reset_game(self):
        """
        Réinitialise l'état du jeu et la grille.
        """
        self.state.reset()
        self.view.board.clear_all()

        # Initialise le moteur selon le mode
        if self.state.mode == "player":
            self.engine = self._create_classic_engine()
        else:
            self.engine = self._create_knuth_engine()

        self.view.board.set_current_row(0)

    def _create_classic_engine(self):
        """
        Génère un code secret aléatoire pour le mode joueur.
        """
        colors = self.state.colors
        if self.state.allow_duplicates:
            secret = [random.choice(colors) for _ in range(5)]
        else:
            secret = random.sample(colors, 5)

        self.state.set_secret_code(secret)
        return secret

    def _create_knuth_engine(self):
        """
        Initialise le moteur Knuth pour le mode ordinateur.
        """
        return KnuthEngine(self.state.colors, self.state.allow_duplicates)

    # ----------------------------------------------------------------------
    # CLICS
    # ----------------------------------------------------------------------

    def on_peg_clicked(self, row, col):
        """
        Gestion des clics sur les pions (mode joueur uniquement).
        """
        if self.state.mode != "player":
            return
        if row != self.state.current_row:
            return

    def on_secret_clicked(self, index):
        """
        Gestion des clics sur le code secret (mode ordinateur).
        """
        if self.state.mode != "computer":
            return

    def on_feedback_clicked(self, row, idx):
        """
        Gestion des clics sur les feedbacks (mode ordinateur).
        """
        if self.state.mode != "computer":
            return
        if row != self.state.current_row:
            return

    # ----------------------------------------------------------------------
    # VALIDATION
    # ----------------------------------------------------------------------

    def validate(self):
        """
        Valide la ligne active selon le mode courant.
        """
        if self.state.mode == "player":
            self._validate_player()
        else:
            self._validate_computer()

    # ----------------------------------------------------------------------
    # MODE JOUEUR
    # ----------------------------------------------------------------------

    def _validate_player(self):
        """
        Valide la ligne du joueur et met à jour l'état du jeu.
        """
        row = self.state.current_row

        # Lecture de la ligne
        guess = []
        for col in range(5):
            color = self.view.board.pion_widgets[(row, col)].color()
            if color is None:
                QMessageBox.warning(self.view, "Ligne incomplète",
                                    "Complète la ligne avant de valider.")
                return
            guess.append(color)

        secret = self.state.secret_code
        well, mis = score(guess, secret)

        # Feedback visuel
        fb_list = [1] * well + [2] * mis + [0] * (5 - well - mis)
        self.view.board.set_feedback_row(row, fb_list)

        # Avance la ligne (exigé par les tests)
        self.state.next_row()

        # Victoire : affiche le code et réinitialise la ligne
        if well == 5:
            self.view.board.set_secret_colors(secret)
            self.view.show_status("Code trouvé !")
            self.state.current_row = 0
            return

        # Défaite : fin de partie
        if self.state.is_game_over():
            self.view.board.set_secret_colors(secret)
            return

        # Mise à jour de la ligne active
        self.view.board.set_current_row(self.state.current_row)

    # ----------------------------------------------------------------------
    # MODE ORDINATEUR
    # ----------------------------------------------------------------------

    def _validate_computer(self):
        """
        Valide le feedback fourni par l'utilisateur en mode ordinateur.
        """
        row = self.state.current_row

        if self.engine.current_guess is None:
            secret = self._get_secret_from_view()
            if secret is None:
                QMessageBox.warning(self.view, "Code secret incomplet",
                                    "Définis les 5 couleurs du code.")
                return

            if not self.state.allow_duplicates and len(secret) != len(set(secret)):
                QMessageBox.warning(self.view, "Doublons interdits",
                                    "Les doublons sont interdits dans ce niveau.")
                return

            self.state.set_secret_code(secret)
            self.view.board.set_secret_colors(secret)

            guess = self.engine.next_guess()
            self.view.board.set_guess_row(0, guess)

            self.view.action_validate.setText("✔ Évaluer la proposition")
            self.view.show_status("Évalue la proposition.")
            return

        blacks, whites = self._get_feedback_from_view(row)
        expected_well, expected_mis = score(self.engine.current_guess,
                                            self.state.secret_code)

        if (expected_well, expected_mis) != (blacks, whites):
            QMessageBox.critical(self.view, "Évaluation incorrecte",
                                 "Le feedback ne correspond pas.")
            return

        if blacks == 5:
            nb = row + 1
            self.view.show_status("Code trouvé !")
            QMessageBox.information(self.view, "Code trouvé",
                                    f"Trouvé en {nb} proposition(s).")
            return

        self.engine.filter((blacks, whites))
        self.state.next_row()

        if self.state.is_game_over():
            QMessageBox.warning(self.view, "Aucune solution",
                                "Plus aucune combinaison possible.")
            return

        self.view.board.set_current_row(self.state.current_row)

        guess = self.engine.next_guess()
        if guess is None:
            QMessageBox.warning(self.view, "Aucune solution",
                                "Plus aucune combinaison possible.")
            return

        self.view.board.set_guess_row(self.state.current_row, guess)
        self.view.show_status("Évalue la proposition.")

    # ----------------------------------------------------------------------
    # UTILITAIRES
    # ----------------------------------------------------------------------

    def _get_secret_from_view(self):
        """
        Lit le code secret défini dans la vue.
        """
        code = []
        for btn in self.view.board.secret_widgets:
            col = btn.color()
            if col is None:
                return None
            code.append(col)
        return code

    def _get_feedback_from_view(self, row):
        """
        Lit le feedback visuel (noirs / blancs) pour une ligne donnée.
        """
        blacks = 0
        whites = 0
        for idx in range(5):
            fb = self.view.board.feedback_widgets[(row, idx)]
            style = fb.styleSheet()
            if "background-color: black" in style:
                blacks += 1
            elif "background-color: #d0d0d0" in style:
                whites += 1
        return blacks, whites









