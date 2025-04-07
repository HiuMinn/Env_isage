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
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout, QSpacerItem, QSizePolicy, QScrollArea
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt, QSize
import sys

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
        self.image_labels = []  
        self.selected_images = []  
        self.selection_mode = "combine"  
        self.load_images()

        layout.addWidget(self.label)
        layout.addLayout(self.grid_layout)

        spacer_item = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addSpacerItem(spacer_item)

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
                image_label.setStyleSheet("border: 2px solid white;")
            else:
                self.selected_images.append(image_label)
                image_label.setStyleSheet("border: 2px solid red;")
        elif self.selection_mode == "generate":
            if image_label not in self.selected_images and len(self.selected_images) < 1:
                self.selected_images.append(image_label)
                image_label.setStyleSheet("border: 2px solid red;")
            elif image_label in self.selected_images:
                self.selected_images.remove(image_label)
                image_label.setStyleSheet("border: 2px solid white;")

        self.update_buttons_state()

    def update_buttons_state(self):
        """Met à jour l'état des boutons en fonction des images sélectionnées"""
        if len(self.selected_images) > 1:
            self.generate_button.setEnabled(False)  
            self.combine_button.setEnabled(True)   
        elif len(self.selected_images) == 1:
            self.generate_button.setEnabled(True)  
            self.combine_button.setEnabled(False)  
        else:
            self.generate_button.setEnabled(False)
            self.combine_button.setEnabled(False)

    def on_generate_button_click(self):
        """ Ouvre la fenêtre GenerateScreen avec les images sélectionnées """
        if self.selected_images:
            self.generate_screen = GenerateScreen(self.selected_images)
            self.generate_screen.show()

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

        button_layout = QHBoxLayout()

        button_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.combine_button = QPushButton("COMBINATE", self)
        self.combine_button.setStyleSheet(button_style)
        self.combine_button.setFixedSize(200, 50)
        self.combine_button.setFont(QFont("8_bit_1_6", 28))
        self.combine_button.setEnabled(False)  
        button_layout.addWidget(self.combine_button)

        self.generate_button = QPushButton("GENERATE", self)
        self.generate_button.setStyleSheet(button_style)
        self.generate_button.setFixedSize(200, 50)
        self.generate_button.setFont(QFont("8_bit_1_6", 28))
        self.generate_button.setEnabled(False)  
        button_layout.addWidget(self.generate_button)

        self.generate_button.clicked.connect(self.on_generate_button_click)  

        finish_button = QPushButton("FINISH", self)
        finish_button.setStyleSheet(button_style)
        finish_button.setFixedSize(200, 50)
        finish_button.setFont(QFont("8_bit_1_6", 28))
        finish_button.clicked.connect(lambda: None)
        button_layout.addWidget(finish_button)

        button_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        layout.addLayout(button_layout)

##### GENERATE SCREEN ######
class GenerateScreen(QWidget):
    def __init__(self, selected_images):
        super().__init__()
        self.selected_images = selected_images  # Stocke les images sélectionnées
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Générer les portraits")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: black;")

        main_layout = QHBoxLayout(self)

        grid_layout = QGridLayout()

        # 🔹 Affichage des images sélectionnées
        for i, image_label in enumerate(self.selected_images[:4]):  
            pixmap = image_label.pixmap()
            btn = QPushButton()
            btn.setFixedSize(150, 150)
            btn.setIcon(QIcon(pixmap))
            btn.setIconSize(btn.size())
            btn.setStyleSheet("border: 2px solid white; background-color: black;")
            grid_layout.addWidget(btn, i // 2, i % 2)

        main_layout.addLayout(grid_layout, 2)
        self.setLayout(main_layout)

        # 🔹 HISTORIQUE DES SÉLECTIONS
        self.history_layout = QGridLayout()
        self.history_label = QLabel("Historique de sélection")
        self.history_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none; background-color: black;")

        self.history_widget = QWidget()
        self.history_widget.setLayout(self.history_layout)
        self.scroll_area.setWidget(self.history_widget)

        history_container = QVBoxLayout()
        history_container.addWidget(self.history_label, alignment=Qt.AlignmentFlag.AlignCenter)
        history_container.addWidget(self.scroll_area)

        main_layout.addLayout(history_container, 1)

        # 🔹 GRILLE DES PORTRAITS
        grid_layout = QGridLayout()
        self.portrait_buttons = []
        self.selected_portraits = {}

        for row in range(2):
            for col in range(2):
                index = row * 2 + col
                btn = QPushButton()
                btn.setFixedSize(150, 150)
                pixmap = QPixmap(150, 150)
                pixmap.fill(Qt.GlobalColor.gray)
                btn.setIcon(QIcon(pixmap))
                btn.setIconSize(btn.size())
                btn.setStyleSheet("border: 2px solid white; background-color: black;")
                btn.clicked.connect(lambda checked=False, idx=index: self.toggle_selection(idx))

                self.portrait_buttons.append(btn)
                grid_layout.addWidget(btn, row, col)

        main_layout.addLayout(grid_layout, 2)

        # ✅ Boutons d'action
        btn_layout = QVBoxLayout()
        self.btn_combine = QPushButton("Combiner")
        self.btn_generate = QPushButton("Générer")
        self.btn_terminate = QPushButton("Terminer")

        for btn in [self.btn_combine, self.btn_generate, self.btn_terminate]:
            btn.setStyleSheet("background-color: white; color: black; border-radius: 5px; padding: 10px;")
            btn_layout.addWidget(btn)

        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

    def toggle_selection(self, index):
        """ Gère la sélection/désélection des portraits et met à jour l'historique """
        btn = self.portrait_buttons[index]
        icon = btn.icon()

        if index in self.selected_portraits:
            del self.selected_portraits[index]
            btn.setStyleSheet("border: 2px solid white; background-color: black;")
            btn.setIcon(QIcon())

            if icon in self.history_buttons:
                self.remove_from_history(icon)
        else:
            self.selected_portraits[index] = icon
            btn.setStyleSheet("border: 2px solid cyan; background-color: black;")
            self.add_to_history(icon)

    def add_to_history(self, icon):
        """ Ajoute une image à l'historique seulement si elle n'y est pas déjà """
        if icon not in self.history_buttons:
            btn = QPushButton()
            btn.setIcon(icon)
            btn.setIconSize(QSize(60, 60))
            btn.setFixedSize(70, 70)
            btn.setStyleSheet("border: 2px solid white; background-color: black;")
            btn.clicked.connect(lambda checked=False, ic=icon: self.select_from_history(ic))

            self.history_buttons[icon] = btn
            row, col = divmod(len(self.history_buttons) - 1, 2)
            self.history_layout.addWidget(btn, row, col)

    def remove_from_history(self, icon):
        """ Supprime une image de l'historique si elle est désélectionnée """
        if icon in self.history_buttons:
            hist_btn = self.history_buttons.pop(icon)
            hist_btn.setParent(None)

    def select_from_history(self, icon):
        """ Sélectionne une image depuis l'historique sans la déplacer """
        for btn in self.portrait_buttons:
            if btn.icon().isNull():
                btn.setIcon(icon)
                btn.setIconSize(QSize(150, 150))
                break


app = QApplication(sys.argv)
window = WelcomeScreen()
window.show()
sys.exit(app.exec())