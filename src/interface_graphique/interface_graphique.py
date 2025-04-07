from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class WelcomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Bienvenue")
        self.setGeometry(100, 100, 800, 600)  # Taille de la fenêtre
        self.setStyleSheet("background-color: #001F3F;")  # Fond bleu marine

        # Texte "Bienvenue !" (Positionnement absolu)
        label = QLabel("Bienvenue !", self)
        label.setFont(QFont("Raleway", 34, QFont.Weight.Bold))  # Police en gras
        label.setStyleSheet("color: white;")  # Texte blanc
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setGeometry(300, 150, 200, 50)  # (x, y, largeur, hauteur)

        # Style CSS commun pour les boutons
        button_style = """
            QPushButton {
                color: white;
                font-size: 17px;
                border: 2px solid #00AEEF;  /* Bleu clair */
                border-radius: 20px;
                padding: 5px 20px;  /* Réduire le padding interne */
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: rgba(0, 174, 239, 0.2); /* Effet au survol */
            }
        """

        # Bouton "Commencer" (Positionnement absolu)
        button_start = QPushButton("Commencer", self)
        button_start.setStyleSheet(button_style)
        button_start.setFixedSize(200, 50)
        button_start.move(300, 250)  # (x, y)

        # Bouton "Tutoriel" (Positionnement absolu juste en dessous)
        button_tutorial = QPushButton("Tutoriel", self)
        button_tutorial.setStyleSheet(button_style)
        button_tutorial.setFixedSize(200, 50)
        button_tutorial.move(300, 310)  # (x, y)


        # Bouton "Quitter"
        quit_button = QPushButton("Quitter", self)
        quit_button.setStyleSheet(button_style)
        quit_button.setFixedSize(200, 50)
        quit_button.clicked.connect(self.close)  # Ferme la fenêtre quand on clique dessus
        quit_button.move(300, 370)  # (x, y)

app = QApplication([])
window = WelcomeScreen()
window.show()
app.exec()
