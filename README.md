# Mastermind (PyQt6)

Version du jeu Mastermind en Python, avec interface graphique PyQt6, moteur de résolution Knuth, et suite de tests automatisés.  
Ce projet est conçu pour être propre, modulaire, maintenable et facilement distribuable via Poetry.

---

## 🎮 Fonctionnalités

- Interface graphique complète (PyQt6)
- Mode Joueur (l’utilisateur propose des codes)
- Mode Ordinateur (résolution automatique via Knuth)
- Palette de couleurs dynamique
- Historique des coups
- Feedback noir/blanc conforme aux règles Mastermind
- Architecture MVC claire (model / view / controller)
- Tests PyQt6 (pytest + pytest-qt)
- Code entièrement uniformisé et finalisé

---

## 📦 Installation (Poetry)

Assurez-vous d’avoir Poetry installé :

```bash
pip install poetry
Installer les dépendances :

bash
poetry install
🚀 Lancement de l’application
bash
poetry run mastermind
ou directement :

bash
poetry run python app.py
🧪 Lancer les tests
bash
poetry run pytest
Les tests utilisent pytest-qt pour simuler l’interface PyQt6.

📁 Structure du projet
Code
mastermind/
│
├── app.py
│
├── controller/
│   └── game_controller.py
│
├── model/
│   ├── game_state.py
│   ├── evaluator.py
│   └── solver_knuth.py
│
├── view/
│   ├── main_window.py
│   ├── board_widget.py
│   └── palette_dialog.py
│
├── tests/
│   └── conftest.py
│
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
🛠️ Dépendances principales
Python ≥ 3.10

PyQt6

NumPy

pytest

pytest-qt

Toutes les dépendances sont gérées automatiquement via Poetry.