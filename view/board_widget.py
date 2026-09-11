# view/board_widget.py

from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt
from .peg_widget import PegWidget


class BoardWidget(QWidget):
    """
    Grille Mastermind : palette, code secret, pions, feedbacks.
    Gère l'affichage et les interactions utilisateur.
    """

    peg_clicked = pyqtSignal(int, int)
    secret_clicked = pyqtSignal(int)
    feedback_clicked = pyqtSignal(int, int)

    def __init__(self, colors, parent=None):
        super().__init__(parent)

        self.colors = colors
        self.current_row = 0
        self.selected_peg = None
        self.mode = "player"

        self.secret_widgets = []
        self.pion_widgets = {}
        self.feedback_widgets = {}
        self.palette_widgets = []

        self._build_ui()

    # ----------------------------------------------------------------------
    # MODE
    # ----------------------------------------------------------------------

    def apply_mode(self, mode):
        """
        Applique le mode joueur ou ordinateur.
        Active/désactive les zones correspondantes.
        """
        self.mode = mode

        if mode == "player":
            # Code secret masqué
            for btn in self.secret_widgets:
                btn.setEnabled(False)
                btn.set_color(None)
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #5a4632;
                        border: 2px solid #3e2d20;
                        border-radius: 16px;
                    }
                """)

            # Feedback désactivé
            for fb in self.feedback_widgets.values():
                fb.setEnabled(False)

            # Pions actifs sur la ligne courante
            for (row, col), peg in self.pion_widgets.items():
                peg.setEnabled(True)

        else:  # mode ordinateur
            # Code secret visible et cliquable
            for btn in self.secret_widgets:
                btn.setEnabled(True)
                btn.set_color(None)
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #f5e9d3;
                        border: 1px solid #5a4632;
                        border-radius: 16px;
                    }
                """)

            # Feedback activé
            for fb in self.feedback_widgets.values():
                fb.setEnabled(True)

            # Pions désactivés
            for peg in self.pion_widgets.values():
                peg.setEnabled(False)

        self._update_active_row()

    # ----------------------------------------------------------------------
    # UI
    # ----------------------------------------------------------------------

    def _build_ui(self):
        """
        Construit l'interface : palette, code secret, 12 lignes de jeu.
        """
        self.setStyleSheet("""
            QWidget { background-color: #e8d7b5; }
            #cadre {
                background-color: #d1b892;
                border: 6px solid #8b6f4e;
                border-radius: 12px;
            }
        """)

        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)

        # Palette
        self.palette_row = QWidget()
        palette_layout = QGridLayout(self.palette_row)
        palette_layout.setSpacing(6)
        palette_layout.setContentsMargins(10, 10, 10, 10)

        for i, color in enumerate(self.colors):
            btn = PegWidget(size=28)
            btn.set_color(color)
            btn.clicked_with_self.connect(
                lambda w, col=color: self._on_palette_color_clicked(col)
            )
            self.palette_widgets.append(btn)
            palette_layout.addWidget(btn, 0, i)

        main.addWidget(self.palette_row)

        # Cadre principal
        cadre = QWidget()
        cadre.setObjectName("cadre")
        grid = QGridLayout(cadre)
        grid.setSpacing(10)
        grid.setContentsMargins(20, 20, 20, 20)
        main.addWidget(cadre)

        # Code secret
        lbl = QLabel("Code secret")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #5a4632;
                min-width: 140px;
                max-width: 140px;
            }
        """)
        grid.addWidget(lbl, 0, 0)

        for i in range(5):
            btn = PegWidget(size=32)
            btn.clicked_with_self.connect(lambda w, idx=i: self._on_secret_clicked(idx))
            self.secret_widgets.append(btn)
            grid.addWidget(btn, 0, i + 1)

        # 12 lignes de jeu
        for row in range(12):

            sep = QLabel("")
            sep.setStyleSheet("background-color: #c9b28a;")
            sep.setFixedHeight(2)
            grid.addWidget(sep, row * 2 + 1, 0, 1, 12)

            lbl = QLabel(f"Proposition {row+1}")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("""
                QLabel {
                    font-weight: bold;
                    color: #5a4632;
                    min-width: 140px;
                    max-width: 140px;
                }
            """)
            grid.addWidget(lbl, row * 2 + 2, 0)

            # Pions
            for col in range(5):
                peg = PegWidget(size=32)
                peg.clicked_with_self.connect(
                    lambda w, r=row, c=col: self._on_peg_clicked(r, c)
                )
                self.pion_widgets[(row, col)] = peg
                grid.addWidget(peg, row * 2 + 2, col + 1)

            # Feedback
            for idx in range(5):
                fb = QPushButton("")
                fb.setFixedSize(18, 18)
                fb.setStyleSheet("""
                    QPushButton {
                        background-color: #f5e9d3;
                        border: 1px solid #5a4632;
                        border-radius: 9px;
                    }
                """)
                fb.clicked.connect(
                    lambda _, r=row, i=idx: self._on_feedback_clicked(r, i)
                )
                self.feedback_widgets[(row, idx)] = fb
                grid.addWidget(fb, row * 2 + 2, idx + 6)

        self._update_active_row()

    # ----------------------------------------------------------------------
    # CLICS
    # ----------------------------------------------------------------------

    def _on_peg_clicked(self, row, col):
        """
        Sélection d’un pion (ligne active uniquement).
        """
        if self.current_row != -1 and row != self.current_row:
            return

        self.selected_peg = ("peg", row, col)
        self._highlight_selected_peg()
        self.peg_clicked.emit(row, col)

    def _on_secret_clicked(self, index):
        """
        Sélection d’un élément du code secret (mode ordinateur).
        """
        if self.mode != "computer":
            return

        self.selected_peg = ("secret", index)
        self._highlight_selected_peg()
        self.secret_clicked.emit(index)

    def _on_palette_color_clicked(self, color):
        """
        Applique une couleur depuis la palette au pion sélectionné.
        """
        if self.selected_peg is None:
            return

        kind = self.selected_peg[0]

        if kind == "secret" and self.mode == "computer":
            _, idx = self.selected_peg
            self.secret_widgets[idx].set_color(color)

        elif kind == "peg" and self.mode == "player":
            _, row, col = self.selected_peg
            self.pion_widgets[(row, col)].set_color(color)

        self._highlight_selected_peg()

    def _on_feedback_clicked(self, row, idx):
        """
        Cycle visuel du feedback (vide → noir → blanc).
        """
        if self.mode != "computer":
            return
        if row != self.current_row:
            return

        fb = self.feedback_widgets[(row, idx)]
        style = fb.styleSheet()

        if "background-color: #f5e9d3" in style:
            fb.setStyleSheet("QPushButton { background-color: black; border-radius: 9px; }")
        elif "background-color: black" in style:
            fb.setStyleSheet("QPushButton { background-color: #d0d0d0; border-radius: 9px; }")
        else:
            fb.setStyleSheet("""
                QPushButton {
                    background-color: #f5e9d3;
                    border: 1px solid #5a4632;
                    border-radius: 9px;
                }
            """)

        self.feedback_clicked.emit(row, idx)

    # ----------------------------------------------------------------------
    # SURBRILLANCE
    # ----------------------------------------------------------------------

    def _highlight_selected_peg(self):
        """
        Met en surbrillance le pion ou élément secret sélectionné.
        """
        # Réinitialisation de la ligne active
        for col in range(5):
            peg = self.pion_widgets[(self.current_row, col)]
            peg.set_color(peg.color())

        if self.selected_peg is None:
            return

        kind = self.selected_peg[0]

        if kind == "peg":
            _, row, col = self.selected_peg
            if row == self.current_row:
                peg = self.pion_widgets[(row, col)]
                c = peg.color() or "#f5e9d3"
                peg.setStyleSheet(
                    f"background-color: {c}; border: 3px solid #ffaa33; border-radius: 16px;"
                )

        elif kind == "secret" and self.mode == "computer":
            _, idx = self.selected_peg
            col = self.secret_widgets[idx].color() or "#f5e9d3"
            self.secret_widgets[idx].setStyleSheet(
                f"background-color: {col}; border: 3px solid #ffaa33; border-radius: 16px;"
            )

    # ----------------------------------------------------------------------
    # PALETTE
    # ----------------------------------------------------------------------

    def update_palette(self, colors):
        """
        Met à jour la palette de couleurs affichée.
        """
        self.colors = colors

        for btn in self.palette_widgets:
            btn.setParent(None)

        self.palette_widgets = []
        layout = self.palette_row.layout()

        for i, color in enumerate(self.colors):
            btn = PegWidget(size=28)
            btn.set_color(color)
            btn.clicked_with_self.connect(
                lambda w, col=color: self._on_palette_color_clicked(col)
            )
            self.palette_widgets.append(btn)
            layout.addWidget(btn, 0, i)

        self.update()

    # ----------------------------------------------------------------------
    # LIGNE ACTIVE
    # ----------------------------------------------------------------------

    def _update_active_row(self):
        """
        Met en évidence la ligne active selon le mode.
        """
        for (row, col), peg in self.pion_widgets.items():

            if self.mode == "player":
                if row == self.current_row:
                    peg.setStyleSheet("""
                        QPushButton {
                            background-color: #fff2cc;
                            border: 3px solid #ffcc66;
                            border-radius: 16px;
                        }
                    """)
                else:
                    peg.set_color(peg.color())

            else:
                peg.set_color(peg.color())

    def set_current_row(self, row):
        """
        Définit la ligne active.
        """
        self.current_row = row
        self.selected_peg = None
        self._update_active_row()

    # ----------------------------------------------------------------------
    # RESET
    # ----------------------------------------------------------------------

    def clear_all(self):
        """
        Réinitialise la grille : code secret, pions, feedbacks.
        """
        for btn in self.secret_widgets:
            btn.set_color(None)

        for peg in self.pion_widgets.values():
            peg.set_color(None)

        for fb in self.feedback_widgets.values():
            fb.setStyleSheet("""
                QPushButton {
                    background-color: #f5e9d3;
                    border: 1px solid #5a4632;
                    border-radius: 9px;
                }
            """)

        self.selected_peg = None
        self.current_row = 0
        self._update_active_row()

    # ----------------------------------------------------------------------
    # MISE À JOUR PAR LE CONTRÔLEUR
    # ----------------------------------------------------------------------

    def set_guess_row(self, row, colors):
        """
        Applique une proposition sur une ligne donnée.
        """
        for col, color in enumerate(colors):
            self.pion_widgets[(row, col)].set_color(color)

    def set_feedback_row(self, row, feedback_states):
        """
        Applique les feedbacks visuels (vide / noir / blanc).
        """
        for idx, state in enumerate(feedback_states):
            fb = self.feedback_widgets[(row, idx)]

            if state == 0:
                fb.setStyleSheet("""
                    QPushButton {
                        background-color: #f5e9d3;
                        border: 1px solid #5a4632;
                        border-radius: 9px;
                    }
                """)
            elif state == 1:
                fb.setStyleSheet("QPushButton { background-color: black; border-radius: 9px; }")
            elif state == 2:
                fb.setStyleSheet("QPushButton { background-color: #d0d0d0; border-radius: 9px; }")

    def set_secret_colors(self, colors):
        """
        Applique les couleurs du code secret.
        """
        for i, col in enumerate(colors):
            self.secret_widgets[i].set_color(col)


















