# Import des librairies PyQt6
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFrame, QGraphicsDropShadowEffect, \
    QGridLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect, QMessageBox, QScrollArea, QFileDialog
from PyQt6.QtGui import QFont, QPixmap, QColor, QFontDatabase, QIcon, QPalette, QFont
from PyQt6.QtCore import Qt, QTimer, QSize, QPropertyAnimation, QEasingCurve, pyqtSignal, QRect
import sys
import random as rd
import os

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import share

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
        pixmap = QPixmap(
            os.path.join(os.path.dirname(os.path.abspath(__file__)),"image_de_fond.png"))  # Mets le bon chemin ici
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
        self.shadow.setBlurRadius(70)  # Pour la largeur de l'effet néon
        self.shadow.setColor(QColor(255, 255, 255))  # Néon blanc
        self.shadow.setOffset(0, 0)  # Pas de décalage, juste la lueur autour

        self.label.setGraphicsEffect(self.shadow)  # application de l'effet
        layout.addWidget(self.label)

        # Animation du néon pour qu'il clignote
        self.brightness = 0
        self.brightness_direction = -10  # Diminue puis remonte pour faire genre ça clignote
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
    self.animation.setEndValue(
        QRect(self.label.x(), self.label.y() - 20, self.label.width(), self.label.height()))  # Monte légèrement
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


####### TUTORIEL ###########
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

        #######  START SCREEN ###########


class MainScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.open_windows = []  # Liste pour stocker les fenêtres ouvertes
        self.setWindowTitle("Sélection d'images")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: black;")
        self.tmp = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tmp"))

        layout = QVBoxLayout(self)

        self.label = QLabel("   Please, select at least one image :   ", self)
        self.label.setFont(QFont("Press Start 2P", 18, QFont.Weight.Bold))
        self.label.setStyleSheet("color: white;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(5)

        self.image_paths = [os.path.join(self.tmp,f"img{i}.png") for i in range(1, 21)]
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
        """Charge 20 images aléatoires dans le grid_layout depuis le dossier tmp"""
        img_folder = self.tmp

        # Vérifier que le dossier existe
        if not os.path.exists(img_folder):
            print(f"Le dossier {img_folder} n'existe pas.")
            return

        # Récupérer tous les fichiers d'image du dossier
        all_images = [f for f in os.listdir(img_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

        # Vérifier qu'il y a au moins 20 images disponibles
        if len(all_images) < 20:
            print("Pas assez d'images dans le dossier !")
            return

        # Sélectionner 20 images aléatoires
        self.image_paths = rd.sample(all_images, 20)

        # Vider le layout précédent
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().deleteLater()

        self.image_labels = []
        self.selected_images = []
        self.row, self.col = 0, 0

        # Ajouter les nouvelles images au layout
        for image_file in self.image_paths:
            image_path = os.path.join(img_folder, image_file)

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
            share.generate_img(self.selected_images) #appel de la fonction generate_img (algo génétique)
            self.window = PortraitWorkspace(self.selected_images, self.tmp)
            self.window.show()

    def on_combine_button_click(self):
        """ Ouvre la fenêtre CombineScreen avec les images sélectionnées """
        share.combine_img(self.selected_images) #appel de la fonction combine_img (plusieurs images)
        if self.selected_images:
            self.window = PortraitWorkspace(self.selected_images, self.tmp)
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
        finish_button.clicked.connect(self.on_finish_button_click)
        button_layout.addWidget(finish_button)

        # Ajouter le bouton "Régénérer" dans le même layout horizontal
        self.regenerate_button = QPushButton(self)
        self.regenerate_button.setIcon(
            QIcon(os.path.join(os.path.dirname(os.path.abspath(__file__)),"icone1.png")))
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
        """Régénère 20 images aléatoires depuis le dossier img_align_celeba"""
        print("Régénération des images...")

        # Vider la liste des images sélectionnées
        self.selected_images.clear()

        # Supprimer toutes les images actuelles du grid_layout
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Recharger 20 nouvelles images
        self.load_images()

        # Mettre à jour l'état des boutons
        self.update_buttons_state()

    def on_finish_button_click(self):
        """Affiche la fenêtre FinalScreen"""
        self.final_screen = FinalScreen(self.selected_images)
        self.final_screen.show()


##### PORTRAIT WORKSPACE ######
class PortraitWorkspace(QWidget):
    def __init__(self, selected_images, tmp):
        super().__init__()
        self.tmp = tmp
        self.genetic_portraits = self.get_last_images(
            tmp)  # DICT récupérer les 4 portraits générés par l'algo génétique, avant = selected_portraits, doit être ajté a selected_portraits
        self.history_buttons = {}  # DICT historique séléctif, ssi une image n'est pas déjà dans l'historique = dictionnaire de Maele
        self.generated_buttons = []  # LISTE
        self.selected_images = list(
            selected_images)  # LISTE, historique global, ajout de toutes les images dès leur séléction
        self.selected_buttons = []
        self.initUI()

    def get_last_images(self, tmp):
        """Récupère les 4 dernières images du dossier tmp sous forme de dictionnaire {QIcon: QPushButton}"""
        if not os.path.exists(tmp):
            raise ValueError("Image introuvable")

        images = [os.path.join(tmp, f) for f in os.listdir(tmp) if f.endswith(('.png', '.jpg', '.jpeg'))]
        images.sort(key=os.path.getmtime,
                    reverse=True)  # Trier par date de modification (du plus récent au plus ancien)

        # Créer le dictionnaire avec des QIcon et QPushButton
        genetic_portraits = {}
        for path in images[:4]:
            pixmap = QPixmap(path)
            icon = QIcon(pixmap)
            btn = self.create_image_button(icon)
            genetic_portraits[btn] = icon  # Inverse : clé=QPushButton, valeur=QIcon

        return genetic_portraits  # Retour des 4 dernières images du dossier

    def initUI(self):
        self.setWindowTitle("Portrait Workspace")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: black;")

        self.global_layout = QVBoxLayout(self)
        main_layout = QHBoxLayout()
        self.generated_layout = QGridLayout()

        # HISTORIQUE
        self.history_layout = QGridLayout()
        self.history_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.history_layout.setHorizontalSpacing(2)
        self.history_layout.setVerticalSpacing(2)
        # self.history_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.history_label = QLabel("  Selection history  ")
        self.history_label.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
            font-family: 'Pixel Operator Mono';
        """)

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none; background-color: black;")

        self.history_widget = QWidget()
        history_container_layout = QVBoxLayout()
        history_container_layout.setContentsMargins(0, 0, 0, 0)
        history_container_layout.addLayout(self.history_layout)
        history_container_layout.addStretch(1)
        self.history_widget.setLayout(history_container_layout)
        self.scroll_area.setWidget(self.history_widget)

        # WRAPPER pour mieux gÃ©rer la taille de l'historique
        self.left_container = QWidget()
        left_container_layout = QVBoxLayout(self.left_container)
        left_container_layout.setContentsMargins(0, 0, 0, 0)
        left_container_layout.addWidget(self.history_label, alignment=Qt.AlignmentFlag.AlignCenter)
        left_container_layout.addWidget(self.scroll_area)

        self.left_container.setMaximumWidth(int(self.width() * 0.28))  # Fixer Ã  ~1/3 de lâ€™Ã©cran
        # left_container.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        # Ajouter les layouts dans la disposition principale
        main_layout.addWidget(self.left_container, stretch=1)
        main_layout.addLayout(self.generated_layout, stretch=2)

        # Zone centrale
        self.global_layout.addLayout(main_layout)

        self.add_buttons()

        # Charge les images de départ
        self.load_buttons_into_grid(self.genetic_portraits.values())

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
        self.btn_finish.clicked.connect(self.on_finish_button_click)
        layout.addWidget(self.btn_finish)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.global_layout.addSpacing(10)
        self.global_layout.addLayout(layout)

    def create_image_button(self, icon):
        btn = QPushButton()
        btn.setFixedSize(150, 150)
        btn.setIcon(icon)
        btn.setIconSize(btn.size())
        btn.setStyleSheet("border: 2px solid white; background-color: black;")
        btn.clicked.connect(lambda: self.toggle_selection(icon, btn))  # Simple lambda
        return btn

    def create_selection_handler(self, icon, btn):
        return lambda checked=False: self.toggle_selection(icon, btn)

    def load_buttons_into_grid(self, buttons):
        for i in reversed(range(self.generated_layout.count())):
            widget = self.generated_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.generated_buttons.clear()

        # Charge les boutons du dictionnaire genetic_portraits
        for i, (btn, icon) in enumerate(self.genetic_portraits.items()):
            self.generated_buttons.append(btn)
            self.generated_layout.addWidget(btn, i // 2, i % 2)

        self.update_buttons_state()

    def toggle_selection(self, icon, btn):
        if btn in self.selected_buttons:
            # Déselection
            self.selected_buttons.remove(btn)
            btn.setStyleSheet("border: 2px solid white; background-color: black;")
        else:
            # Sélection
            self.selected_buttons.append(btn)
            btn.setStyleSheet("border: 2px solid red; background-color: black;")
            self.selected_images.append(btn)

        self.update_buttons_state()

    def update_buttons_state(self):
        count = len(self.selected_buttons)
        self.btn_generate.setEnabled(count == 1)
        self.btn_combine.setEnabled(count > 1)

    def add_to_history(self, icon):
        for existing_icon in self.history_buttons.keys():
            if existing_icon.pixmap(QSize(60, 60)).toImage() == icon.pixmap(QSize(60, 60)).toImage():
                return

        btn = QPushButton()
        btn.setIcon(icon)
        btn.setIconSize(QSize(60, 60))
        btn.setFixedSize(70, 70)
        btn.setStyleSheet("border: 2px solid white; background-color: black;")
        btn.clicked.connect(lambda: self.toggle_selection(icon, btn))

        self.history_buttons[icon] = btn
        row, col = divmod(len(self.history_buttons) - 1, 2)
        self.history_layout.addWidget(btn, row, col)

    def reset_selection_styles(self):
        # Déselectionne les boutons générés
        for btn in self.generated_buttons:
            btn.setStyleSheet("border: 2px solid white; background-color: black;")
        self.selected_buttons.clear()

        # Déselectionne les boutons de l'historique
        for btn in self.history_buttons.values():
            btn.setStyleSheet("border: 2px solid white; background-color: black;")

    def on_generate_clicked(self):
        if len(self.selected_buttons) != 1:
            return
        selected_btn = self.selected_buttons[0]
        icon = self.genetic_portraits.get(selected_btn)
        if icon:
            self.add_to_history(icon)
        self.reset_selection_styles()

    def on_combine_clicked(self):
        if len(self.selected_buttons) < 2:
            return
        for btn in self.selected_buttons:
            icon = self.genetic_portraits.get(btn)
            if icon:
                self.add_to_history(icon)
        self.reset_selection_styles()

    def on_finish_button_click(self):
        selected_images_2 = []  # Nouvelle liste qui contiendra des QLabel

        # Convertir chaque QPushButton en QLabel
        for button in self.selected_images:  # self.selected_images contient des QPushButton
            if isinstance(button, QPushButton):
                pixmap = button.icon().pixmap(button.size())  # Récupérer le QPixmap de l'icône du bouton
                if pixmap:
                    # Créer un QLabel avec l'image
                    label = QLabel()
                    label.setPixmap(pixmap)  # Appliquer l'image au QLabel
                    selected_images_2.append(label)  # Ajouter le QLabel à la nouvelle liste

        # Maintenant, passer selected_images_2 (contenant des QLabel) à FinalScreen
        self.final_screen = FinalScreen(selected_images_2, self.history_buttons)
        self.final_screen.show()


##### FINAL SCREEN #####
class FinalScreen(QWidget):
    def __init__(self, selected_images_2, history_buttons):
        super().__init__()
        self.selected_images = selected_images_2  # Liste des images sélectionnées
        self.history_buttons = history_buttons  # Dictionnaire des boutons d'historique
        self.setWindowTitle("Well Done")
        self.setGeometry(100, 100, 800, 600)  # Taille et position de la fenêtre
        self.setStyleSheet("background-color: black;")  # Style de fond noir

        layout = QVBoxLayout(self)

        # "Well Done!" Title with Neon Effect
        self.label = QLabel("Well Done!", self)
        self.label.setFont(QFont("Press Start 2P", 45, QFont.Weight.Bold))  # Font and size
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: white; background: transparent; border: none;")  # White text color
        self.label.setFixedHeight(50)  # Reduced height for the label area

        # Neon effect using QGraphicsDropShadowEffect
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(70)  # Width of the neon effect
        self.shadow.setColor(QColor(255, 255, 255))  # White neon color
        self.shadow.setOffset(0, 0)  # No offset, just the glow around

        self.label.setGraphicsEffect(self.shadow)  # Apply the shadow effect
        layout.addWidget(self.label)

        # Image : Récupérer la dernière image sélectionnée (la dernière de la liste)
        last_image_label = self.selected_images[-1]  # Dernier QLabel dans la liste
        pixmap = last_image_label.pixmap()  # Récupérer le pixmap de ce QLabel

        # Si le pixmap est valide (non nul), on le redimensionne
        if pixmap:
            # Redimensionner l'image pour la rendre plus grande
            scaled_pixmap = pixmap.scaled(300, 300,
                                          Qt.AspectRatioMode.KeepAspectRatio)  # Agrandir l'image à 400x400 tout en gardant le ratio
            self.image_label = QLabel(self)  # Créer un QLabel pour afficher l'image
            self.image_label.setPixmap(scaled_pixmap)  # Appliquer l'image redimensionnée au label
            self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrer l'image dans le label
            layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)  # Ajouter l'image au layout

            # Créer un cadre néon clignotant autour de l'image
            self.create_neon_frame(self.image_label)

        else:
            print("Erreur")  # Si le pixmap est nul, afficher un message d'erreur

        # Ajouter les boutons de l'interface avec le même style que les autres écrans
        self.add_buttons(layout)

    def create_neon_frame(self, image_label):
        """Création d'un cadre néon clignotant autour de l'image"""
        self.neon_effect = QGraphicsDropShadowEffect()
        self.neon_effect.setColor(QColor(255, 0, 0))  # Couleur rouge néon
        self.neon_effect.setBlurRadius(100)  # Rayon de flou du cadre
        self.neon_effect.setOffset(0, 0)  # Pas de décalage, juste autour de l'image

        # Appliquer l'effet au label contenant l'image
        image_label.setGraphicsEffect(self.neon_effect)

        # Créer un timer pour faire clignoter le cadre
        self.neon_timer = QTimer(self)
        self.neon_timer.timeout.connect(self.toggle_neon_effect)  # Changer la visibilité du cadre
        self.neon_timer.start(500)  # Le cadre clignote toutes les 500 ms (0.5 seconde)

    def toggle_neon_effect(self):
        """Alterner la visibilité du cadre néon pour le faire clignoter"""
        if self.neon_effect.isEnabled():
            self.neon_effect.setEnabled(False)  # Désactiver l'effet de cadre
        else:
            self.neon_effect.setEnabled(True)  # Activer l'effet de cadre

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

        # Bouton "Download this image"
        self.download_image_button = QPushButton("Download image", self)
        self.download_image_button.setStyleSheet(button_style)
        self.download_image_button.setFixedSize(250, 50)
        self.download_image_button.setFont(QFont("8_bit_1_6", 14))
        self.download_image_button.setEnabled(True)  # Active le bouton selon ton besoin
        button_layout.addWidget(self.download_image_button)

        # Bouton "Download the whole history"
        self.download_history_button = QPushButton("Download history", self)
        self.download_history_button.setStyleSheet(button_style)
        self.download_history_button.setFixedSize(250, 50)
        self.download_history_button.setFont(QFont("8_bit_1_6", 14))
        self.download_history_button.setEnabled(True)  # Active le bouton selon ton besoin
        button_layout.addWidget(self.download_history_button)

        # Bouton "Show the whole history"
        self.show_history_button = QPushButton("Show history", self)
        self.show_history_button.setStyleSheet(button_style)
        self.show_history_button.setFixedSize(250, 50)
        self.show_history_button.setFont(QFont("8_bit_1_6", 14))
        self.show_history_button.setEnabled(True)  # Active le bouton selon ton besoin
        button_layout.addWidget(self.show_history_button)

        # Connecter les boutons à leurs actions respectives
        self.download_image_button.clicked.connect(self.download_image)
        self.download_history_button.clicked.connect(self.download_history)
        self.show_history_button.clicked.connect(self.show_history)

        # Spacer après les boutons pour centrer
        button_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Ajouter les boutons à la fenêtre principale
        layout.addLayout(button_layout)

    def download_history(self):
        return "history downloaded"

    def show_history(self):
        """Afficher l'historique sous forme de boutons"""
        # Créer un layout pour l'historique
        history_layout = QVBoxLayout()  # Nouveau layout pour l'historique
        history_layout.setSpacing(5)

        # Créer un label pour l'historique
        history_label = QLabel("History", self)
        history_label.setFont(QFont("Press Start 2P", 20, QFont.Weight.Bold))
        history_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        history_label.setStyleSheet("color: white; background: transparent;")
        history_layout.addWidget(history_label)

        # Ajouter les boutons d'historique
        for btn in self.history_buttons.values():
            history_layout.addWidget(btn)

        # Ajouter le layout de l'historique à la fenêtre
        self.layout().addLayout(history_layout)  # Ajouter à la fenêtre principale

        # Désactiver le bouton "Show history" après affichage pour éviter de l'ajouter plusieurs fois
        self.show_history_button.setEnabled(
            False)  # Optionnel, tu peux aussi choisir de cacher ce bouton après l'action

    def download_image(self):
        """Télécharger la dernière image sélectionnée sous le nom 'selected portrait'"""
        # Ouvrir une boîte de dialogue pour permettre à l'utilisateur de choisir où enregistrer l'image
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)  # Permet de sélectionner un fichier
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg)")  # Filtrer les fichiers d'images
        file_dialog.setViewMode(QFileDialog.ViewMode.List)  # Affichage sous forme de liste

        # Définir le nom par défaut du fichier
        default_file_name = "selected portrait.png"
        file_dialog.selectFile(default_file_name)  # Définir le nom par défaut dans la boîte de dialogue

        if file_dialog.exec():  # Si l'utilisateur a sélectionné un fichier
            file_path = file_dialog.selectedFiles()[0]  # Récupérer le chemin du fichier sélectionné
            print(f"Chemin sélectionné : {file_path}")  # Afficher le chemin sélectionné pour le débugage

            last_image_label = self.selected_images[-1]  # Récupérer la dernière image sélectionnée
            pixmap = last_image_label.pixmap()  # Obtenir le pixmap (image) de cette dernière image

            if pixmap:  # Si le pixmap est valide
                # Vérification du format de fichier
                if not file_path.endswith(('.png', '.xpm', '.jpg')):  # Si le format du fichier n'est pas correct
                    file_path += '.png'  # Par défaut, on ajoute .png si aucun format n'est spécifié

                print(f"Essayer d'enregistrer l'image à {file_path}")  # Message de débogage avant l'enregistrement

                saved = pixmap.save(file_path)  # Sauvegarder l'image à l'emplacement choisi

                if saved:
                    print(f"L'image a été enregistrée à {file_path}")  # Afficher un message de succès
                    return "Image enregistrée avec succès !"  # Retourner un message de succès
                else:
                    print(f"Erreur lors de l'enregistrement de l'image : {file_path}")  # Afficher un message d'erreur
                    return "Erreur lors de l'enregistrement de l'image."  # Retourner un message d'erreur
            else:
                print("Aucune image à enregistrer !")  # Afficher un message d'erreur si aucune image n'est disponible
                return "Aucune image à enregistrer !"  # Retourner un message d'erreur

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WelcomeScreen()
    window.show()
    sys.exit(app.exec())