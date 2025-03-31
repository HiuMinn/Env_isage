#Import des librairies PyQt6
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFrame, QGraphicsDropShadowEffect, QGridLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect, QMessageBox, QScrollArea
from PyQt6.QtGui import QFont, QPixmap, QColor, QFontDatabase, QIcon, QPalette, QFont
from PyQt6.QtCore import Qt, QTimer, QSize, QPropertyAnimation, QEasingCurve, pyqtSignal
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
    
    def start_zoom_animation(self):
        """ Anime le texte 'WELCOME !' avec un effet de zoom/dézoom """
        self.zoom_animation = QPropertyAnimation(self.label, b"scale")
        self.zoom_animation.setDuration(1000)  # Durée de l'animation de zoom/dézoom
        self.zoom_animation.setStartValue(1)  # Taille initiale (normal)
        self.zoom_animation.setEndValue(1.2)  # Taille augmentée (zoom)
        self.zoom_animation.setLoopCount(-1)  # Répète l'animation indéfiniment
        self.zoom_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)  # Courbe fluide pour l'animation
        self.zoom_animation.start()

    def initUI(self):
        self.setWindowTitle("Welcome")
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

        self.start_zoom_animation()

    def resizeEvent(self, event):
        """ Redimensionner l'image de fond automatiquement """
        self.background.setGeometry(0, 0, self.width(), self.height())
    
    def show_tutorial(self):
        """ Ouvre le tutoriel """
        self.tutorial_popup = UndertaleDialog()
        self.tutorial_popup.show()
    
    from PyQt6.QtCore import QPropertyAnimation, QRect

def start_welcome_animation(self):
    """ Anime le texte 'WELCOME !' avec un effet de saut """
    self.animation = QPropertyAnimation(self.label, b"geometry")
    self.animation.setDuration(500)  # Durée totale du saut en millisecondes
    self.animation.setStartValue(QRect(self.label.x(), self.label.y(), self.label.width(), self.label.height()))
    self.animation.setEndValue(QRect(self.label.x(), self.label.y() - 20, self.label.width(), self.label.height()))  # Monte légèrement
    self.animation.setLoopCount(-1)  # Répète l'animation en boucle
    self.animation.setEasingCurve(QEasingCurve.Type.OutBounce)  # Effet rebondissant
    self.animation.start()

    self.zoom_animation = QPropertyAnimation(self.label, b"font")
    self.zoom_animation.setDuration(500)
    self.zoom_animation.setStartValue(QFont("Press Start 2P", 45, QFont.Weight.Bold))
    self.zoom_animation.setEndValue(QFont("Press Start 2P", 50, QFont.Weight.Bold))  # Grossit légèrement
    self.zoom_animation.setLoopCount(-1)
    self.zoom_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)  # Animation fluide
    self.zoom_animation.start()


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
        self.open_windows = []  # Liste pour stocker les fenêtres ouvertes
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

        self.image_paths = [f"/Users/maelebedel/Desktop/INSA/Cours/4A/S2_BiM/Developpement_logiciel/projet-4bim/images/img{i}.jpeg" for i in range(1, 21)]
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
            self.window = PortraitWorkspace(self.selected_images, mode="generate")
            self.window.show()

    def on_combine_button_click(self):
        """ Ouvre la fenêtre CombineScreen avec les images sélectionnées """
        if self.selected_images:
            self.window = PortraitWorkspace(self.selected_images, mode="combine")
            self.window.show()


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

        self.combine_button = QPushButton("COMBINE", self)
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
        self.combine_button.clicked.connect(self.on_combine_button_click)  

        finish_button = QPushButton("FINISH", self)
        finish_button.setStyleSheet(button_style)
        finish_button.setFixedSize(200, 50)
        finish_button.setFont(QFont("8_bit_1_6", 28))
        finish_button.clicked.connect(lambda: None)
        button_layout.addWidget(finish_button)

        # Spacer après les boutons pour centrer
        button_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Ajouter les boutons à la fenêtre principale
        layout.addLayout(button_layout)

    def regenerate_images(self):
        """Fonction qui régénère les images"""
        print("Régénération des images...")

class PortraitWorkspace(QWidget):
    def __init__(self, selected_images, mode="generate"):
        super().__init__()
        self.selected_images = selected_images
        self.mode = mode
        self.history_buttons = {}
        self.selected_portraits = {}
        self.generated_buttons = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Générer les portraits" if self.mode == "generate" else "Combiner les portraits")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: black;")

        self.global_layout = QVBoxLayout(self)
        main_layout = QHBoxLayout()

        # Historique
        self.history_layout = QGridLayout()
        self.history_label = QLabel("Historique de sélection")
        self.history_label.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
            font-family: 'Pixel Operator Mono';
        """)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none; background-color: black;")

        self.history_widget = QWidget()
        self.history_widget.setLayout(self.history_layout)
        self.scroll_area.setWidget(self.history_widget)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.history_label, alignment=Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.scroll_area)
        main_layout.addLayout(left_layout, 1)

        # Zone centrale
        self.generated_layout = QGridLayout()
        main_layout.addLayout(self.generated_layout, 2)
        self.global_layout.addLayout(main_layout)

        self.add_buttons()

        # Charge les images de départ
        self.load_buttons_from_labels(self.selected_images)

        for label in self.selected_images:
            self.add_to_history(QIcon(label.pixmap()))

    def add_buttons(self):
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
        layout = QHBoxLayout()
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.btn_combine = QPushButton("COMBINE")
        self.btn_combine.setStyleSheet(button_style)
        self.btn_combine.setFixedSize(200, 50)
        self.btn_combine.setFont(QFont("8_bit_1_6", 28))
        self.btn_combine.setEnabled(False)
        self.btn_combine.clicked.connect(self.on_combine_clicked)
        layout.addWidget(self.btn_combine)

        self.btn_generate = QPushButton("GENERATE")
        self.btn_generate.setStyleSheet(button_style)
        self.btn_generate.setFixedSize(200, 50)
        self.btn_generate.setFont(QFont("8_bit_1_6", 28))
        self.btn_generate.setEnabled(False)
        self.btn_generate.clicked.connect(self.on_generate_clicked)
        layout.addWidget(self.btn_generate)

        self.btn_finish = QPushButton("FINISH")
        self.btn_finish.setStyleSheet(button_style)
        self.btn_finish.setFixedSize(200, 50)
        self.btn_finish.setFont(QFont("8_bit_1_6", 28))
        self.btn_finish.clicked.connect(self.close)
        layout.addWidget(self.btn_finish)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.global_layout.addSpacing(10)
        self.global_layout.addLayout(layout)

    def load_buttons_from_labels(self, labels):
        buttons = []
        for label in labels[:4]:
            pixmap = label.pixmap()
            icon = QIcon(pixmap)
            btn = self.create_image_button(icon)
            buttons.append(btn)
        self.load_buttons_into_grid(buttons)

    def create_image_button(self, icon):
        btn = QPushButton()
        btn.setFixedSize(150, 150)
        btn.setIcon(icon)
        btn.setIconSize(btn.size())
        btn.setStyleSheet("border: 2px solid white; background-color: black;")
        btn.clicked.connect(self.create_selection_handler(icon, btn))
        return btn

    def create_selection_handler(self, icon, btn):
        return lambda checked=False: self.toggle_selection(icon, btn)

    def load_buttons_into_grid(self, buttons):
        for i in reversed(range(self.generated_layout.count())):
            widget = self.generated_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.generated_buttons.clear()
        self.selected_portraits.clear()

        for i, btn in enumerate(buttons):
            self.generated_buttons.append(btn)
            self.generated_layout.addWidget(btn, i // 2, i % 2)

        self.update_buttons_state()

    def toggle_selection(self, icon, btn):
        if icon in self.selected_portraits:
            del self.selected_portraits[icon]
            btn.setStyleSheet("border: 2px solid white; background-color: black;")
        else:
            self.selected_portraits[icon] = btn
            btn.setStyleSheet("border: 2px solid red; background-color: black;")
        self.update_buttons_state()

    def update_buttons_state(self):
        count = len(self.selected_portraits)
        self.btn_generate.setEnabled(count == 1)
        self.btn_combine.setEnabled(count > 1)

    def add_to_history(self, icon):
        for existing_icon in self.history_buttons:
            if existing_icon.pixmap(QSize(60, 60)).toImage() == icon.pixmap(QSize(60, 60)).toImage():
                return
        btn = QPushButton()
        btn.setIcon(icon)
        btn.setIconSize(QSize(60, 60))
        btn.setFixedSize(70, 70)
        btn.setStyleSheet("border: 2px solid white; background-color: black;")
        btn.clicked.connect(self.create_selection_handler(icon, btn))

        self.history_buttons[icon] = btn
        row, col = divmod(len(self.history_buttons) - 1, 2)
        self.history_layout.addWidget(btn, row, col)

    def on_generate_clicked(self):
        if self.mode != "generate":
            return
        selected_icons = list(self.selected_portraits.keys())
        if not selected_icons:
            return

        for icon in selected_icons:
            self.add_to_history(icon)

        new_buttons = []
        for i in range(4):
            pix = QPixmap(150, 150)
            pix.fill(Qt.GlobalColor.green if i % 2 == 0 else Qt.GlobalColor.yellow)
            icon = QIcon(pix)
            new_buttons.append(self.create_image_button(icon))

        self.load_buttons_into_grid(new_buttons)

    def on_combine_clicked(self):
        if self.mode != "combine":
            return
        selected_icons = list(self.selected_portraits.keys())
        if not selected_icons:
            return

        for icon in selected_icons:
            self.add_to_history(icon)

        new_buttons = []
        for i in range(4):
            pix = QPixmap(150, 150)
            pix.fill(Qt.GlobalColor.red if i % 2 == 0 else Qt.GlobalColor.blue)
            icon = QIcon(pix)
            new_buttons.append(self.create_image_button(icon))

        self.load_buttons_into_grid(new_buttons)


app = QApplication(sys.argv)
window = WelcomeScreen()
window.show()
sys.exit(app.exec())