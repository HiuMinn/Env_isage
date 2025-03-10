from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
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

        layout = QVBoxLayout()
        layout.setSpacing(5)  # Espacement réduit entre les widgets (5 pixels)

        # Texte "Bienvenue !"
        label = QLabel("Bienvenue !")
        label.setFont(QFont("Helvetica", 34, QFont.Weight.Bold))  # Police Helvetica en gras
        label.setStyleSheet("color: white;")  # Texte blanc
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Style commun aux boutons
        button_style = """
            QPushButton {
                color: white;
                font-size: 17px;
                font-family: Helvetica;
                border: 2px solid #00AEEF;  /* Bleu clair */
                border-radius: 20px;
                padding: 10px 20px;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: rgba(0, 174, 239, 0.2); /* Effet au survol */
            }
        """

        # Bouton "Commencer"
        start_button = QPushButton("Commencer")
        start_button.setFont(QFont("Helvetica", 17))
        start_button.setStyleSheet(button_style)
        start_button.setFixedSize(200, 50)
        layout.addWidget(start_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Bouton "Tutoriel"
        tutorial_button = QPushButton("Tutoriel")
        tutorial_button.setFont(QFont("Helvetica", 17))
        tutorial_button.setStyleSheet(button_style)
        tutorial_button.setFixedSize(200, 50)
        layout.addWidget(tutorial_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Bouton "Quitter"
        quit_button = QPushButton("Quitter")
        quit_button.setFont(QFont("Helvetica", 17))
        quit_button.setStyleSheet(button_style)
        quit_button.setFixedSize(200, 50)
        quit_button.clicked.connect(self.close)  # Ferme la fenêtre quand on clique dessus
        layout.addWidget(quit_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

app = QApplication([])
window = WelcomeScreen()
window.show()
app.exec()
