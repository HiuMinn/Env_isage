#Import des librairies PyQt6
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFrame, QGraphicsDropShadowEffect, QGridLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect, QMessageBox
from PyQt6.QtGui import QFont, QPixmap, QColor, QFontDatabase, QIcon, QPalette, QFont
from PyQt6.QtCore import Qt, QTimer, QSize
import sys
import random as rd
import os


#######  ECRAN D'ACCUEIL ###########
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

    def start_main_screen(self):
        self.main_screen = MainScreen()
        self.main_screen.show()
        self.close()

    def initUI(self):
        self.setWindowTitle("Welcome")
        self.setGeometry(100, 100, 800, 600)

        # Image de fond
        self.background = QLabel(self)
        pixmap = QPixmap("/Users/laura.forestier/Documents/4BIM_S2/Développement Logiciel/Projet-4BIM/image_de_fond.png")  # Mets le bon chemin ici
        self.background.setPixmap(pixmap)
        self.background.setScaledContents(True)
        self.background.setGeometry(0, 0, self.width(), self.height())

        # Création du layout principal
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Texte "Bienvenue!" avec l'effet néon
        self.label = QLabel("WELCOME !", self)
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

        for text in ["Start", "Tutorial", "Exit"]:
            button = QPushButton(text, self)
            button.setStyleSheet(button_style)
            button.setFixedSize(200, 50)
            button.setFont(QFont("8_bit_1_6", 28))
            layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

            if text == "Exit":
                button.clicked.connect(self.close)

            elif text == "Start":
                button.clicked.connect(self.start_main_screen)

            elif text == "Tutorial":
                button.clicked.connect(self.show_tutorial)  # Ajout de la connexion pour afficher le tutoriel

        layout.addSpacing(5)  # Ajuste la distance entre "Bienvenue !" et les boutons


        # Appliquer le layout
        self.setLayout(layout)

    def resizeEvent(self, event):
        """ Redimensionner l'image de fond automatiquement """
        self.background.setGeometry(0, 0, self.width(), self.height())
    
    def show_tutorial(self):
        """ Ouvre le tutoriel """
        self.tutorial_popup = UndertaleDialog()
        self.tutorial_popup.show()

####### TUTORIEL(TUTORIAL) ###########    
class UndertaleDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.dialogs = [
            "* Welcome to the tutorial!\nLearn how to use this interface step by step.",
            "* First, click on images to select them.",
            "* Now you have to make a choice",
            "* Press 'Combine' to mix them!",
            "* Or press “Generate” if you wish to create a variant.",
            "* Once you're satisfied with the portraits presented, click 'Finish' to validate.",
            "* Now, you're ready to start! Good luck!"
        ]
        self.dialog_index = 0  
        self.full_text = self.dialogs[self.dialog_index]  
        self.current_text = ""  
        self.text_index = 0  
        self.show_cursor = False  

        self.initUI()
        self.setWindowOpacity(0)  
        self.start_fade_in_animation()  

    def initUI(self):
        self.setWindowTitle("Tutorial")
        self.setGeometry(300, 200, 650, 250)  # 🔹 Augmentation de la hauteur pour le titre
        self.setStyleSheet("background-color: black;")  

        # ✅ Ajout du Titre "TUTORIAL"
        self.title_label = QLabel("TUTORIAL", self)
        self.title_label.setFont(QFont("Eight-Bit Madness", 24))  # 🔹 Police pixel
        self.title_label.setStyleSheet("color: white; border: none;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setGeometry(50, 20, 550, 30)  # 🔹 Position au-dessus du cadre

        # ✅ Un SEUL cadre pour le dialogue
        self.dialog_frame = QFrame(self)
        self.dialog_frame.setStyleSheet("background-color: black; border: 2px solid white;")
        self.dialog_frame.setGeometry(50, 60, 550, 100)

        # ✅ Texte sans cadre supplémentaire
        self.text_label = QLabel(self.dialog_frame)
        self.text_label.setStyleSheet("color: white; border: none;")  
        self.text_label.setFont(QFont("Eight-Bit Madness", 20))
        self.text_label.setWordWrap(True)
        self.text_label.setGeometry(20, 20, 500, 50)  

        # ✅ Bouton OK bien intégré dans le cadre
        self.ok_button = QPushButton("OK", self.dialog_frame)
        self.ok_button.setStyleSheet(
            "color: white; background-color: transparent; border: 2px solid white; padding: 2px;"
        )
        self.ok_button.setFont(QFont("Eight-Bit Madness", 12))
        self.ok_button.setGeometry(460, 70, 60, 25)  # 🔹 Position correcte en bas à droite
        self.ok_button.clicked.connect(self.next_dialog)
        self.ok_button.hide()  

        self.text_timer = QTimer(self)
        self.text_timer.timeout.connect(self.update_text)
        self.text_timer.start(50)

        self.cursor_timer = QTimer(self)
        self.cursor_timer.timeout.connect(self.blink_cursor)

    def start_fade_in_animation(self):
        self.opacity = 0
        self.fade_timer = QTimer(self)
        self.fade_timer.timeout.connect(self.increase_opacity)
        self.fade_timer.start(30)

    def increase_opacity(self):
        if self.opacity < 1:
            self.opacity += 0.1
            self.setWindowOpacity(self.opacity)
        else:
            self.fade_timer.stop()

    def update_text(self):
        if self.text_index < len(self.full_text):
            self.current_text += self.full_text[self.text_index]
            self.text_label.setText(self.current_text)
            self.text_index += 1
        else:
            self.text_timer.stop()
            self.cursor_timer.start(500)  
            self.ok_button.show()  

    def blink_cursor(self):
        if self.show_cursor:
            self.text_label.setText(self.current_text + "_")
        else:
            self.text_label.setText(self.current_text)
        self.show_cursor = not self.show_cursor

    def next_dialog(self):
        self.cursor_timer.stop()  
        self.ok_button.hide()  

        if self.dialog_index < len(self.dialogs) - 1:
            self.dialog_index += 1
            self.full_text = self.dialogs[self.dialog_index]
            self.current_text = ""
            self.text_index = 0

            self.text_label.setText("")  
            self.text_timer.start(50)  
        else:
            self.close()    

#######  MAIN SCREEN (START) ###########
class MainScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sélection d'images")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout(self)

        self.label = QLabel("   Veuillez sélectionner au moins une image :   ", self)
        self.label.setFont(QFont("Press Start 2P", 18, QFont.Weight.Bold))
        self.label.setStyleSheet("color: white;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(5)

        self.image_paths = [f"/Users/laura.forestier/Documents/4BIM_S2/Développement Logiciel/Projet-4BIM/img{i}.jpeg" for i in range(1, 21)]
        self.image_size = 150
        self.row, self.col = 0, 0
        self.image_labels = []  # Liste pour garder une trace des labels des images
        self.selected_images = []  # Liste des images sélectionnées
        self.selection_mode = "combine"  # Mode de sélection : "combine" ou "generate"
        self.load_images()

        layout.addWidget(self.label)
        layout.addLayout(self.grid_layout)

        # Ajouter un spacer pour séparer les images du bouton de régénération
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addSpacerItem(spacer_item)

        # Ajouter les boutons d'action et le bouton "Régénérer" sur la même ligne
        self.add_buttons(layout)

        self.setLayout(layout)

    def load_images(self):
        """Charge les images dans le grid_layout"""
        for image_path in self.image_paths:
            image_label = QLabel(self)
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(self.image_size, self.image_size, Qt.AspectRatioMode.KeepAspectRatio)
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            image_label.setStyleSheet("border: 2px solid white;")
            
            # Connecter l'événement de clic
            image_label.mousePressEvent = self.create_image_click_handler(image_label)

            self.grid_layout.addWidget(image_label, self.row, self.col)
            self.image_labels.append(image_label)

            self.col += 1
            if self.col >= 5:
                self.col = 0
                self.row += 1

    def create_image_click_handler(self, image_label):
        """Retourne une fonction de gestion du clic pour chaque image"""
        def on_image_click(event):
            self.toggle_image_selection(image_label)
        return on_image_click

    def toggle_image_selection(self, image_label):
        """Sélectionne ou désélectionne une image en fonction de son état actuel"""
        if self.selection_mode == "combine":
            if image_label in self.selected_images:
                self.selected_images.remove(image_label)
                image_label.setStyleSheet("border: 2px solid white;")  # Retirer l'effet néon
            else:
                self.selected_images.append(image_label)
                image_label.setStyleSheet("border: 2px solid red;")  # Appliquer l'effet néon

        elif self.selection_mode == "generate":
            if image_label not in self.selected_images and len(self.selected_images) < 1:
                self.selected_images.append(image_label)
                image_label.setStyleSheet("border: 2px solid red;")  # Appliquer l'effet néon
            elif image_label in self.selected_images:
                self.selected_images.remove(image_label)
                image_label.setStyleSheet("border: 2px solid white;")  # Retirer l'effet néon

        # Mise à jour de l'état des boutons en fonction du nombre d'images sélectionnées
        self.update_buttons_state()

    def update_buttons_state(self):
        """Met à jour l'état des boutons en fonction des images sélectionnées"""
        # Si plus d'une image est sélectionnée, grise le bouton "GENERATE" et dégrise le bouton "COMBINATE"
        if len(self.selected_images) > 1:
            self.generate_button.setEnabled(False)  # Griser le bouton "GENERATE"
            self.combine_button.setEnabled(True)   # Dégriser le bouton "COMBINATE"
        # Si une seule image est sélectionnée, dégrise "GENERATE" et grise "COMBINATE"
        elif len(self.selected_images) == 1:
            self.generate_button.setEnabled(True)  # Dégriser le bouton "GENERATE"
            self.combine_button.setEnabled(False)  # Griser le bouton "COMBINATE"
        else:
            # Si aucune image n'est sélectionnée, griser les deux boutons
            self.generate_button.setEnabled(False)
            self.combine_button.setEnabled(False)

    def add_buttons(self, layout):
        button_style = """
            QPushButton {
                color: white;
                font-size: 17px;
                border: 2px solid red;
                border-radius: 20px;
                padding: 5px 20px;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 0.2);
            }
            QPushButton:disabled {
                color: grey;
                border-color: grey;
                background-color: #333;
            }
        """

        button_layout = QHBoxLayout()  # Utilisation de QHBoxLayout pour aligner horizontalement les boutons

        # Spacer avant les boutons pour centrer
        button_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Ajouter les boutons dans le layout
        self.combine_button = QPushButton("COMBINATE", self)
        self.combine_button.setStyleSheet(button_style)
        self.combine_button.setFixedSize(200, 50)
        self.combine_button.setFont(QFont("8_bit_1_6", 28))
        self.combine_button.setEnabled(False)  # Griser le bouton
        button_layout.addWidget(self.combine_button)

        self.generate_button = QPushButton("GENERATE", self)
        self.generate_button.setStyleSheet(button_style)
        self.generate_button.setFixedSize(200, 50)
        self.generate_button.setFont(QFont("8_bit_1_6", 28))
        self.generate_button.setEnabled(False)  # Griser le bouton
        button_layout.addWidget(self.generate_button)

        finish_button = QPushButton("FINISH", self)
        finish_button.setStyleSheet(button_style)
        finish_button.setFixedSize(200, 50)
        finish_button.setFont(QFont("8_bit_1_6", 28))
        finish_button.clicked.connect(lambda: None)
        button_layout.addWidget(finish_button)

        # Ajouter le bouton "Régénérer" dans le même layout horizontal
        self.regenerate_button = QPushButton(self)
        self.regenerate_button.setIcon(QIcon("/Users/laura.forestier/Documents/4BIM_S2/Développement Logiciel/Projet-4BIM/icone1.png"))
        self.regenerate_button.setIconSize(QSize(40, 40))  # Taille de l'icône
        self.regenerate_button.setStyleSheet("border: none; background-color: transparent;")
        self.regenerate_button.setFixedSize(50, 50)
        self.regenerate_button.clicked.connect(self.regenerate_images)
        button_layout.addWidget(self.regenerate_button)

        # Spacer après les boutons pour centrer
        button_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Ajouter les boutons à la fenêtre principale
        layout.addLayout(button_layout)

    def regenerate_images(self):
        """Fonction qui régénère les images"""
        print("Régénération des images...")

    def return_to_welcome(self):
        self.welcome_screen = WelcomeScreen()
        self.welcome_screen.show()
        self.close()

app = QApplication(sys.argv)
window = WelcomeScreen()
window.show()
sys.exit(app.exec())