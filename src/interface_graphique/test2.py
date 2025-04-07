from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFrame, QGraphicsDropShadowEffect
from PyQt6.QtGui import QFont, QPixmap, QColor, QFontDatabase
from PyQt6.QtCore import Qt, QTimer
import sys
import random as rd

# Chargement de la police undertale 
#font_name = "Press Start 2P"

class WelcomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    """"
    def animate_neon(self):
        Effet pulsation douce pour le néon
        self.brightness += self.brightness_direction
        if self.brightness <= 180 or self.brightness >= 255:
            self.brightness_direction *= -1  # Inverse la direction de la pulsation

        self.shadow.setColor(QColor(self.brightness, 0, 0))  # Change l’intensité du rouge
    """
        
    def animate_neon(self):
        """ Fait varier la luminosité de façon aléatoire pour un effet de panne néon """
        if rd.random() < 0.2:  # 20% de chances d'une pause plus longue (extinction temporaire)
            self.brightness = rd.choice([0, 50, 80])
        else:
            self.brightness = rd.randint(150, 255)  # Variation normale de luminosité

        self.shadow.setColor(QColor(self.brightness, self.brightness, self.brightness))  # Applique la couleur blanche
        self.start_random_blinking()  # Relance avec un nouveau temps aléatoire

    def start_random_blinking(self):
        """ Lance l'animation avec un intervalle aléatoire """
        self.timer.start(rd.randint(50, 400))  # Changement aléatoire entre 50ms et 400ms

    def initUI(self):
        self.setWindowTitle("Bienvenue")
        self.setGeometry(100, 100, 800, 600)

        # Image de fond
        self.background = QLabel(self)
        pixmap = QPixmap("/Users/maelebedel/Desktop/INSA/Cours/4A/S2_BiM/Developpement_logiciel/projet-4bim/image_de_fond.png")  # Mets le bon chemin ici
        self.background.setPixmap(pixmap)
        self.background.setScaledContents(True)
        self.background.setGeometry(0, 0, self.width(), self.height())

        # Création du layout principal
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Texte "Bienvenue!" avec l'effet néon
        self.label = QLabel("BIENVENUE !", self)
        self.label.setFont(QFont("Press Start 2P", 45, QFont.Weight.Bold))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color : white;")
        self.label.setFixedHeight(50)  # Réduit la hauteur de la zone de texte

        # Effet néon
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(70) # Pour la largeur de l'effet néon
        self.shadow.setColor(QColor(255, 255, 255)) # Néon blanc
        self.shadow.setOffset(0,0) # Pas de décalage, juste la lueur autour

        self.label.setGraphicsEffect(self.shadow) # application de l'effet
        layout.addWidget(self.label)

        # Animation du néon pour qu'il clignote
        self.brightness = 0 
        self.brightness_direction = -10 # Diminue puis remonte pour faire genre ça clignote
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_neon)
        self.start_random_blinking()

        """
        self.brightness = 0
        self.brightness_direction = -10 # Diminue puis remonte pour faire genre ça clignote
        self.timer =QTimer(self)
        self.timer.timeout.connect(self.animate_neon)
        self.timer.start(100) # Change l'intensité toutes les 100ms
        """

        self.setLayout(layout)


        # Style CSS des boutons
        button_style = """
            QPushButton {
                color: white;
                font-size: 17px;
                border: 2px solid red;  /* Contour rouge */
                border-radius: 20px;
                padding: 5px 20px;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 0.2); /* Rouge translucide au survol */
            }
        """

        layout.addSpacing(5)  # Ajuste la distance entre "Bienvenue !" et les boutons

        for text in ["Commencer", "Tutoriel", "Quitter"]:
            button = QPushButton(text, self)
            button.setStyleSheet(button_style)
            button.setFixedSize(200, 50)
            button.setFont(QFont("8_bit_1_6", 28))  # Mets ici le nom exact de la police 8-bit Fortress 8_bit_1_6 8BIT WONDER 8-bit pusab Eight-Bit Madness (bien pour le texte mais pas pour des titres) Pixel Operator 8 Pixel Operator Mono
            layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

            if text == "Quitter":
                button.clicked.connect(self.close)
            
            elif text == "Tutoriel":
                button.clicked.connect(self.show_tutorial)

        layout.addSpacing(5)  # Ajuste la distance entre "Bienvenue !" et les boutons




        # Appliquer le layout
        self.setLayout(layout)

    def resizeEvent(self, event):
        """ Redimensionner l'image de fond automatiquement """
        self.background.setGeometry(0, 0, self.width(), self.height())
    
    def show_tutorial(self):
            self.tutorial_popup = TutorialPopup(self)
            self.tutorial_popup.show()
    
class TutorialPopup(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 0, parent.width(), parent.height())  # Prend toute la fenêtre principale
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.6);")  # Fond semi-transparent

        # Contenu du pop-up
        popup_frame = QFrame(self)
        popup_frame.setStyleSheet("background-color: white; border-radius: 15px; padding: 20px;")
        popup_frame.setGeometry(parent.width() // 4, parent.height() // 4, parent.width() // 2, parent.height() // 2)

        layout = QVBoxLayout(popup_frame)
        layout.setContentsMargins(20, 20, 20, 20)  # Réduit les marges autour des widgets

        # Texte du tutoriel
        label = QLabel("Bienvenue dans le tutoriel !\n\nVoici comment utiliser cette application :\n- Étape 1\n- Étape 2\n- Étape 3", popup_frame)
        label.setFont(QFont("Arial", 14))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Bouton Fermer en haut à droite
        close_button = QPushButton("X", popup_frame)
        close_button.setStyleSheet("background-color: red; color: white; font-size: 14px; border-radius: 10px; border: none; padding: 5px;")
        close_button.setFixedSize(30, 30)
        close_button.clicked.connect(self.close_popup)
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)

    def close_popup(self):
        self.setParent(None)  # Enlève le pop-up de la fenêtre principale


app = QApplication(sys.argv)
window = WelcomeScreen()
window.show()
sys.exit(app.exec())
