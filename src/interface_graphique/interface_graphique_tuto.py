from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

# La classe WelcomeScreen reste la même
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
        label.setFont(QFont("Helvetica", 34, QFont.Weight.Bold))  # Police en gras
        label.setStyleSheet("color: white;")  # Texte blanc
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setGeometry(300, 150, 200, 50)  # (x, y, largeur, hauteur)

        # Style CSS commun pour les boutons
        button_style = """
            QPushButton {
                color: white;
                font-family: Helvetica, Arial, sans-serif;  /* Définir la police */
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
        button_tutorial.clicked.connect(self.openTutorial)  # Connecte le bouton à la méthode

        # Bouton "Quitter"
        quit_button = QPushButton("Quitter", self)
        quit_button.setStyleSheet(button_style)
        quit_button.setFixedSize(200, 50)
        quit_button.clicked.connect(self.close)  # Ferme la fenêtre quand on clique dessus
        quit_button.move(300, 370)  # (x, y)

    def openTutorial(self):
        self.tutorial_window = TutorialScreen()  # Créer une nouvelle fenêtre de tutoriel
        self.tutorial_window.show()  # Afficher la fenêtre du tutoriel
        self.close()  # Ferme la fenêtre actuelle

# La classe TutorialScreen est la nouvelle page qui s'affiche
class TutorialScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Tutoriel")
        self.setGeometry(100, 100, 800, 600)  # Taille de la fenêtre
        self.setStyleSheet("background-color: #001F3F;")  # Fond bleu marine

        # Texte "Bienvenue dans le Tutoriel" (Positionnement absolu)
        label = QLabel("Bienvenue dans le Tutoriel !", self)
        label.setFont(QFont("Helvetica", 24, QFont.Weight.Bold))  # Police en gras
        label.setStyleSheet("color: white;")  # Texte blanc
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setGeometry(200, 150, 400, 50)  # (x, y, largeur, hauteur)

        # Ajouter d'autres éléments de tutoriel ici
        tutorial_text = QLabel("Voici les instructions du tutoriel...\n\nAppuyez sur le bouton pour revenir.", self)
        tutorial_text.setFont(QFont("Helvetica", 16))
        tutorial_text.setStyleSheet("color: white;")
        tutorial_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tutorial_text.setGeometry(150, 250, 500, 150)

        # Bouton "Retour" (Ferme la fenêtre de tutoriel et revient à l'écran précédent)
        back_button = QPushButton("Retour", self)
        back_button.setStyleSheet("""
            QPushButton {
                color: white;
                font-family: Helvetica, Arial, sans-serif;
                font-size: 17px;
                border: 2px solid #00AEEF;
                border-radius: 20px;
                padding: 5px 20px;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: rgba(0, 174, 239, 0.2);
            }
        """)
        back_button.setFixedSize(200, 50)
        back_button.clicked.connect(self.goBack)  # Connecte le bouton à la méthode pour revenir
        back_button.move(300, 450)  # (x, y)

    def goBack(self):
        self.close()  # Ferme la fenêtre actuelle (le tutoriel)

app = QApplication([])
window = WelcomeScreen()
window.show()
app.exec()
