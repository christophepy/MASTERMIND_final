# model/solver_knuth.py

import numpy as np
from itertools import product, permutations


class KnuthEngine:
    """
    Moteur de résolution Mastermind basé sur l'heuristique de Knuth.
    Utilise une représentation indexée et un filtrage vectorisé NumPy.
    """

    def __init__(self, colors, allow_duplicates):
        self.colors = colors
        self.allow_duplicates = allow_duplicates
        self.nb_colors = len(colors)

        # Mappage couleur ↔ indice
        self.color_to_idx = {c: i for i, c in enumerate(colors)}
        self.idx_to_color = {i: c for i, c in enumerate(colors)}

        self._generate_space()

        # Masque des candidats encore possibles
        self.candidates_mask = np.ones(len(self.codes), dtype=bool)

        # Dernière proposition effectuée
        self.current_guess = None

    # ------------------------------------------------------------------ #
    # Génération de l’espace de recherche
    # ------------------------------------------------------------------ #

    def _generate_space(self):
        """
        Génère l'ensemble des codes possibles selon les règles de doublons.
        """
        if self.allow_duplicates:
            all_codes = list(product(range(self.nb_colors), repeat=5))
        else:
            all_codes = list(permutations(range(self.nb_colors), 5))

        self.codes = np.array(all_codes, dtype=np.int8)

    # ------------------------------------------------------------------ #
    # Score vectorisé (noirs / blancs)
    # ------------------------------------------------------------------ #

    @staticmethod
    def _score_vectorized(guess, codes):
        """
        Calcule les scores (noirs, blancs) pour un ensemble de codes.
        guess : (5,) int
        codes : (N,5) int
        """
        # Bien placés
        blacks = np.sum(codes == guess, axis=1)

        # Comptage des couleurs
        counts_guess = np.zeros((codes.shape[0], 10), dtype=np.int8)
        counts_code = np.zeros((codes.shape[0], 10), dtype=np.int8)

        for pos in range(5):
            g = guess[pos]
            c = codes[:, pos]
            counts_guess[np.arange(codes.shape[0]), g] += 1
            counts_code[np.arange(codes.shape[0]), c] += 1

        common = np.minimum(counts_guess, counts_code).sum(axis=1)
        whites = common - blacks

        return blacks, whites

    # ------------------------------------------------------------------ #
    # Choix de la prochaine proposition
    # ------------------------------------------------------------------ #

    def next_guess(self):
        """
        Sélectionne la prochaine proposition selon une heuristique simplifiée.
        """
        if not np.any(self.candidates_mask):
            self.current_guess = None
            return None

        candidate_indices = np.where(self.candidates_mask)[0]
        candidate_codes = self.codes[candidate_indices]

        # Cas simple : peu de candidats
        if candidate_codes.shape[0] <= 200:
            best_idx = candidate_indices[0]

        else:
            # Échantillonnage pour limiter le coût
            sample_size = min(50, candidate_codes.shape[0])
            sample_indices = np.random.choice(candidate_indices, size=sample_size, replace=False)
            sample_codes = self.codes[sample_indices]

            worst_scores = []

            for gi, gcode in zip(sample_indices, sample_codes):
                blacks, whites = self._score_vectorized(gcode, candidate_codes)
                pairs = np.stack((blacks, whites), axis=1)
                _, counts = np.unique(pairs, axis=0, return_counts=True)
                worst_scores.append(counts.max())

            best_sample_idx = sample_indices[int(np.argmin(worst_scores))]
            best_idx = best_sample_idx

        guess_code = self.codes[best_idx]
        self.current_guess = [self.idx_to_color[i] for i in guess_code]
        return self.current_guess

    # ------------------------------------------------------------------ #
    # Filtrage des candidats
    # ------------------------------------------------------------------ #

    def filter(self, feedback):
        """
        Filtre les candidats selon le feedback (noirs, blancs).
        """
        if self.current_guess is None:
            return

        guess_idx = np.array([self.color_to_idx[c] for c in self.current_guess], dtype=np.int8)
        blacks, whites = self._score_vectorized(guess_idx, self.codes)

        b_exp, w_exp = feedback
        mask = (blacks == b_exp) & (whites == w_exp)

        self.candidates_mask &= mask



