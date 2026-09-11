# view/main_window.py

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QToolBar
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from .board_widget import BoardWidget


class MainWindow(QMainWindow):
    """
    Fenêtre principale du jeu Mastermind.
    Gère la barre d’outils, le menu, le bandeau de niveau et la grille.
    """

    validate_requested = pyqtSignal()
    mode_changed = pyqtSignal(str)
    level_changed = pyqtSignal(int, bool)

    def __init__(self, colors, parent=None):
        super().__init__(parent)

        self.colors = colors

        self.setWindowTitle("Mastermind Premium")
        self.resize(400, 700)

        # Grille principale
        self.board = BoardWidget(colors)

        # Bandeau de niveau
        self.level_label = QLabel("Niveau : non défini")
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.level_label.setStyleSheet("""
            QLabel {
                background-color: #f0e6d2;
                color: #5a4632;
                font-weight: bold;
                padding: 6px;
                border-bottom: 2px solid #8b6f4e;
            }
        """)

        # Conteneur principal
        container = QWidget()
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        vbox.addWidget(self.level_label)
        vbox.addWidget(self.board)
        self.setCentralWidget(container)

        # Barre de statut
        self.status = self.statusBar()
        self.status.setStyleSheet("""
            QStatusBar {
                background-color: #f0e6d2;
                color: #5a4632;
                font-weight: bold;
                padding: 4px;
            }
        """)

        # Toolbar et menu
        self._build_toolbar()
        self._build_menu()

        self.update_banner("Mode Joueur", "Débutant", 7, False)

    # ----------------------------------------------------------------------
    # Toolbar
    # ----------------------------------------------------------------------

    def _build_toolbar(self):
        """
        Construit la barre d’outils (validation).
        """
        toolbar = QToolBar("Outils")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        self.action_validate = QAction("✔ Valider proposition", self)
        self.action_validate.triggered.connect(self.validate_requested.emit)
        toolbar.addAction(self.action_validate)

    # ----------------------------------------------------------------------
    # Menu
    # ----------------------------------------------------------------------

    def _build_menu(self):
        """
        Construit le menu : mode et niveaux.
        """
        menubar = self.menuBar()

        # Mode
        menu_mode = menubar.addMenu("Mode")

        act_player = QAction("Joueur cherche", self)
        act_player.triggered.connect(lambda: self._on_mode_selected("player"))
        menu_mode.addAction(act_player)

        act_computer = QAction("Ordinateur cherche", self)
        act_computer.triggered.connect(lambda: self._on_mode_selected("computer"))
        menu_mode.addAction(act_computer)

        # Niveau
        menu_level = menubar.addMenu("Niveau")

        # Débutant
        lvl_deb = menu_level.addMenu("Débutant")

        deb_sans = lvl_deb.addMenu("Sans doublons")
        for c in [6, 7]:
            act = QAction(f"{c} couleurs", self)
            act.triggered.connect(lambda _, n=c: self._on_level_selected(n, False))
            deb_sans.addAction(act)

        deb_avec = lvl_deb.addMenu("Avec doublons")
        for c in [4, 5]:
            act = QAction(f"{c} couleurs", self)
            act.triggered.connect(lambda _, n=c: self._on_level_selected(n, True))
            deb_avec.addAction(act)

        # Intermédiaire
        lvl_int = menu_level.addMenu("Intermédiaire")

        int_sans = lvl_int.addMenu("Sans doublons")
        for c in [8, 9]:
            act = QAction(f"{c} couleurs", self)
            act.triggered.connect(lambda _, n=c: self._on_level_selected(n, False))
            int_sans.addAction(act)

        int_avec = lvl_int.addMenu("Avec doublons")
        for c in [6, 7]:
            act = QAction(f"{c} couleurs", self)
            act.triggered.connect(lambda _, n=c: self._on_level_selected(n, True))
            int_avec.addAction(act)

        # Expert
        lvl_exp = menu_level.addMenu("Expert")

        exp_avec = lvl_exp.addMenu("Avec doublons")
        for c in [8, 9]:
            act = QAction(f"{c} couleurs", self)
            act.triggered.connect(lambda _, n=c: self._on_level_selected(n, True))
            exp_avec.addAction(act)

    # ----------------------------------------------------------------------
    # Actions du menu
    # ----------------------------------------------------------------------

    def _on_mode_selected(self, mode):
        """
        Émet le changement de mode et met à jour le texte de validation.
        """
        self.mode_changed.emit(mode)

        if mode == "player":
            self.action_validate.setText("✔ Valider proposition")
            self.show_status("Mode Joueur : trouve le code.")
        else:
            self.action_validate.setText("✔ Valider le code secret")
            self.show_status("Mode Ordinateur : définis ton code.")

    def _on_level_selected(self, nb_colors, allow_duplicates):
        """
        Émet le changement de niveau.
        """
        self.level_changed.emit(nb_colors, allow_duplicates)

    # ----------------------------------------------------------------------
    # Bandeau
    # ----------------------------------------------------------------------

    def update_banner(self, mode_name, level_name, nb_colors, allow_duplicates):
        """
        Met à jour le bandeau d'information du niveau.
        """
        dup = "avec doublons" if allow_duplicates else "sans doublons"
        self.level_label.setText(
            f"{mode_name} – {level_name} – {nb_colors} couleurs, {dup}"
        )

    # ----------------------------------------------------------------------
    # Status bar
    # ----------------------------------------------------------------------

    def show_status(self, message):
        """
        Affiche un message dans la barre de statut.
        """
        self.status.showMessage(message)



