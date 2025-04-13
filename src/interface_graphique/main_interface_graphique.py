#Import des librairies PyQt6
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFrame, QGraphicsDropShadowEffect, QGridLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect, QMessageBox, QScrollArea, QFileDialog
from PyQt6.QtGui import QFont, QPixmap, QColor, QFontDatabase, QIcon, QPalette, QFont
from PyQt6.QtCore import Qt, QTimer, QSize, QPropertyAnimation, QEasingCurve, pyqtSignal
import sys
import random as rd
import os
import sys
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import share


#######  WELCOME SCREEN ###########
class WelcomeScreen(QWidget):
    """
    Application home screen.

    This class displays a home screen with an animated neon text effect.
    It can be used to trigger the tutorial display, switch to the application's main screen or quit the application.
    """

    def __init__(self):
        """ Initializes home screen components. """
        super().__init__()
        self.initUI()

    def animate_neon(self):
        """ 
        Animates the neon text effect by randomly varying the brightness.
        This effect simulates a neon light that flickers or flickers irregularly. 
        """
        if rd.random() < 0.2:  # 20% chance of a longer pause (temporary extinction) for a flashing effect
            self.brightness = rd.choice([0, 50, 80])
        else:
            self.brightness = rd.randint(150, 255)  # Luminosity variation

        self.shadow.setColor(QColor(self.brightness, self.brightness, self.brightness))  # Apply the white color
        self.start_random_blinking()  # Relaunch with a new random time

    def start_random_blinking(self):
        """ Starts a new animation with a random delay. The delay is between 50 and 400 ms. """
        self.timer.start(rd.randint(50, 400))  # Random change between 50ms and 400ms

    def start_main_screen(self):
        """ Switches to the application's main screen. 
            Creates an instance of MainScreen, displays it and closes the home screen. """
        self.main_screen = MainScreen()
        self.main_screen.show()
        self.close()
    
    def start_zoom_animation(self):
        """ Launches a looping zoom-in/zoom-out animation on the text 'WELCOME!
            The `label` label is enlarged up to 1.2x, then reduced, with a fluid effect. """
        self.zoom_animation = QPropertyAnimation(self.label, b"scale")
        self.zoom_animation.setDuration(1000)  # Zoom animation duration
        self.zoom_animation.setStartValue(1)  # Initial size (normal)
        self.zoom_animation.setEndValue(1.2)  # Increased size (zoom)
        self.zoom_animation.setLoopCount(-1)  # Repeats animation indefinitely
        self.zoom_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)  
        self.zoom_animation.start()

    def initUI(self):
        """ Initializes the graphical interface of the home screen.

            Configures window, background image, ‘WELCOME!’ animated text with neon effect, buttons (‘Start’, ‘Tutorial’, ‘Exit’) and launches animations. """
        self.setWindowTitle("Welcome")
        self.setGeometry(100, 100, 800, 600)

        # Background image
        self.background = QLabel(self)
        pixmap = QPixmap(os.path.join(os.path.dirname(os.path.abspath(__file__)),"image_de_fond.png"))  
        self.background.setPixmap(pixmap)
        self.background.setScaledContents(True)
        self.background.setGeometry(0, 0, self.width(), self.height())

        # Creating the main layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 'Welcome' text with neon effect
        self.label = QLabel("WELCOME !", self)
        self.label.setFont(QFont("Press Start 2P", 45, QFont.Weight.Bold))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color : white;")
        self.label.setFixedHeight(50)  

        # Neon effet
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(70) 
        self.shadow.setColor(QColor(255, 255, 255)) 
        self.shadow.setOffset(0,0) 

        self.label.setGraphicsEffect(self.shadow)
        layout.addWidget(self.label)

        # 'Welcome' text with neon effectFlashing neon animation
        self.brightness = 0
        self.brightness_direction = -10 
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_neon)
        self.start_random_blinking()

        self.setLayout(layout)

        # Button CSS styling
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

        layout.addSpacing(5) 

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
                button.clicked.connect(self.show_tutorial)  # Adding the connection to display the tutorial

        layout.addSpacing(5)  

        self.setLayout(layout)

        self.start_zoom_animation()

    def resizeEvent(self, event):
        """ Automatically resizes the background image when the window is resized. """
        self.background.setGeometry(0, 0, self.width(), self.height())
    
    def show_tutorial(self):
        """ Open the tutorial """
        self.tutorial_popup = UndertaleDialog()
        self.tutorial_popup.show()


####### TUTORIAL ###########    
class UndertaleDialog(QWidget):
    """
    Undertale-style tutorial window.

    Displays a series of messages guiding the user through the interface, with a progressive text effect, a blinking cursor, an "OK" button to move on to the next message, and a progressive appearance animation.
    """
    
    def __init__(self):
        """ Initializes the tutorial window.
            Prepares dialogs to be displayed, initializes text variables, configures the user interface and launches the pop-up animation. """
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
        """ Configures the tutorial's graphical interface.
            Initializes title, dialog frame, animated text, "OK" button, and timers for progressive text display and cursor blinking. """
        self.setWindowTitle("Tutorial")
        self.setGeometry(300, 200, 650, 250)  
        self.setStyleSheet("background-color: black;")  

        # Add title "TUTORIAL
        self.title_label = QLabel("TUTORIAL", self)
        self.title_label.setFont(QFont("Eight-Bit Madness", 24))  
        self.title_label.setStyleSheet("color: white; border: none;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setGeometry(50, 20, 550, 30)  

        # Framework for dialogue
        self.dialog_frame = QFrame(self)
        self.dialog_frame.setStyleSheet("background-color: black; border: 2px solid white;")
        self.dialog_frame.setGeometry(50, 60, 550, 100)

        # Text to be displayed in the frame
        self.text_label = QLabel(self.dialog_frame)
        self.text_label.setStyleSheet("color: white; border: none;")  
        self.text_label.setFont(QFont("Eight-Bit Madness", 20))
        self.text_label.setWordWrap(True)
        self.text_label.setGeometry(20, 20, 500, 50)  

        # 'OK' button
        self.ok_button = QPushButton("OK", self.dialog_frame)
        self.ok_button.setStyleSheet(
            "color: white; background-color: transparent; border: 2px solid white; padding: 2px;"
        )
        self.ok_button.setFont(QFont("Eight-Bit Madness", 12))
        self.ok_button.setGeometry(460, 70, 60, 25)  
        self.ok_button.clicked.connect(self.next_dialog)
        self.ok_button.hide()  

        self.text_timer = QTimer(self)
        self.text_timer.timeout.connect(self.update_text)
        self.text_timer.start(50)

        self.cursor_timer = QTimer(self)
        self.cursor_timer.timeout.connect(self.blink_cursor)

    def start_fade_in_animation(self):
        """ Starts a progressive window animation.
             Gradually increases opacity until the window is fully visible. """
        self.opacity = 0
        self.fade_timer = QTimer(self)
        self.fade_timer.timeout.connect(self.increase_opacity)
        self.fade_timer.start(30)

    def increase_opacity(self):
        """ Gradually increases window opacity.
            Increments opacity until it reaches 1, then stops the animation timer. """
        if self.opacity < 1:
            self.opacity += 0.1
            self.setWindowOpacity(self.opacity)
        else:
            self.fade_timer.stop()

    def update_text(self):
        """ Gradually displays text letter by letter in the dialog box.
            Once the complete text is displayed, the cursor starts flashing and the "OK" button becomes visible."""
        if self.text_index < len(self.full_text):
            self.current_text += self.full_text[self.text_index]
            self.text_label.setText(self.current_text)
            self.text_index += 1
        else:
            self.text_timer.stop()
            self.cursor_timer.start(500)  
            self.ok_button.show()  

    def blink_cursor(self):
        """ Flashes a “_” cursor at the end of the displayed text.
            Toggles between display with or without cursor every 500 ms. """
        if self.show_cursor:
            self.text_label.setText(self.current_text + "_")
        else:
            self.text_label.setText(self.current_text)
        self.show_cursor = not self.show_cursor

    def next_dialog(self):
        """ Goes to the next message in the tutorial, or closes the window if there are none left.
            Resets text display and restarts letter-by-letter animation. """
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
    """
    Class representing the start screen of the application.

    This window allows the user to:
    - View 20 random images from a temporary folder.
    - Select one or more images.
    - Choose between two actions: 'GENERATE' (to generate a new image) or 'COMBINE' (to merge several images).
    - Launch a process based on the selected images.
    - Regenerate a new set of images.

    Attributes:
        open_windows (list): List of open secondary windows.
        tmp (str): Path to the 'tmp' folder containing the images.
        image_paths (list): List of file paths to the displayed images.
        selected_images (list): List of images selected by the user.
        selection_mode (str): Image selection mode ("combine" or "generate").
    """
     
    def __init__(self):
        """Initializes the main screen"""
        super().__init__()
        self.open_windows = []  # List to store opened secondary windows
        self.setWindowTitle("Selection of images")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: black;")
        self.tmp = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tmp"))

        layout = QVBoxLayout(self)

        # Title label at the top
        self.label = QLabel("   Please, select at least one image :   ", self)
        self.label.setFont(QFont("Press Start 2P", 18, QFont.Weight.Bold))
        self.label.setStyleSheet("color: white;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Grid layout to display image thumbnails
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(5)

        # Prepare placeholder paths for 20 images
        self.image_paths = [os.path.join(self.tmp,f"img{i}.png") for i in range(1, 21)]
        self.image_size = 150 # Size for displayed thumbnails
        self.row, self.col = 0, 0 # Grid coordinates
        self.image_labels = []  # List to keep track of QLabel widgets showing the images
        self.selected_images = []   # Currently selected images
        self.selection_mode = "combine"  # Default mode

        # Load and display images
        self.load_images()

        # Add title and grid to layout
        layout.addWidget(self.label)
        layout.addLayout(self.grid_layout)

        # Add spacing between the grid and buttons
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addSpacerItem(spacer_item)

        # Add action buttons (COMBINE, GENERATE, EXIT, etc.)
        self.add_buttons(layout)

        # Set final layout for the widget
        self.setLayout(layout)

    def load_images(self):
        """Loads 20 random images into the 'grid_layout' from the 'tmp' folder."""
        img_folder = self.tmp

        # Check that the folder exists
        if not os.path.exists(img_folder):
            print(f"The file {img_folder} doesn't exist.")
            return
        
        # Get all image files from the folder
        all_images = [f for f in os.listdir(img_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        # Check if there are at least 20 images available
        if len(all_images) < 20:
            print("Not enough images in the folder.")
            return

        # Select the 20 images in the tmp folder 
        #self.image_paths = rd.sample(all_images, 20)
        self.image_paths = all_images
        
        # Clear previous images from the layout
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().deleteLater()

        self.image_labels = []  # Reset image labels list
        self.selected_images = []  # Reset selected images
        self.row, self.col = 0, 0  # Reset grid position

        # Display selected images in the grid
        for image_file in self.image_paths:
            image_path = os.path.join(img_folder, image_file)

            image_label = QLabel(self)
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(self.image_size, self.image_size, Qt.AspectRatioMode.KeepAspectRatio)
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            image_label.setStyleSheet("border: 2px solid white;")

            # Assign a mouse click handler to allow image selection
            image_label.mousePressEvent = self.create_image_click_handler(image_label)

            # Add image to the grid layout
            self.grid_layout.addWidget(image_label, self.row, self.col)
            self.image_labels.append(image_label)

            # Update grid position
            self.col += 1
            if self.col >= 5:
                self.col = 0
                self.row += 1

    def create_image_click_handler(self, image_label):
        """Returns a click handler function for a given image"""
        
        def on_image_click(event):
            # Toggle selection state when the image is clicked
            self.toggle_image_selection(image_label)
            
        return on_image_click

    def toggle_image_selection(self, image_label):
        """
        Selects or deselects an image based on its current state.
        The image's state is visually changed by modifying its border color.
        """
        if self.selection_mode == "combine":
            # In "combine" mode: allow multiple images to be selected
            if image_label in self.selected_images:
                self.selected_images.remove(image_label)
                image_label.setStyleSheet("border: 2px solid white;")  # Deselect: revert to white border
            else:
                self.selected_images.append(image_label)
                image_label.setStyleSheet("border: 2px solid red;")    # Select: apply red border

        elif self.selection_mode == "generate":
            # In "generate" mode: only allow one image to be selected at a time
            if image_label not in self.selected_images and len(self.selected_images) < 1:
                self.selected_images.append(image_label)
                image_label.setStyleSheet("border: 2px solid red;")    # Select: apply red border
            elif image_label in self.selected_images:
                self.selected_images.remove(image_label)
                image_label.setStyleSheet("border: 2px solid white;")  # Deselect: revert to white border

        # Update the state of the action buttons based on the current selection
        self.update_buttons_state()

    def update_buttons_state(self):
        """
        Enables or disables the buttons based on the number of selected images.
        """
        if len(self.selected_images) > 1:
            # If more than one image is selected, allow the 'combine' action
            # but disable the 'generate' button
            self.generate_button.setEnabled(False)
            self.combine_button.setEnabled(True)
        elif len(self.selected_images) == 1:
            # If exactly one image is selected, allow the 'generate' action
            # but disable the 'combine' button
            self.generate_button.setEnabled(True)
            self.combine_button.setEnabled(False)
        else:
            # If no images are selected, disable both the 'generate' and 'combine' buttons
            self.generate_button.setEnabled(False)
            self.combine_button.setEnabled(False)


    def get_image_path_from_qlabel(self, image_label):
        """
        Returns the absolute path of the image associated with a QLabel.
        """
        # Search in the list of labels to find the associated path
        image_index = self.image_labels.index(image_label)
        image_path = self.image_paths[image_index]
        
        # Return the absolute path by joining with the base directory
        return os.path.join(self.tmp, image_path)

    def on_generate_button_click(self):
        """
        Starts the process of generating a new image.
        """
        if self.selected_images:
            # Get the absolute paths of the selected images
            selected_paths = [self.get_image_path_from_qlabel(label) for label in self.selected_images]

            # Call the function with the image paths
            share.generate_img(selected_paths)

            # Open a new workspace window with the selected images and temporary directory
            self.window = PortraitWorkspace(self.selected_images, self.tmp)
            self.window.show()

    def on_combine_button_click(self):
        """
        Starts the process of combining images.
        """
        if self.selected_images:
            # Get the absolute paths of the selected images
            selected_paths = [self.get_image_path_from_qlabel(label) for label in self.selected_images]
            
            # Call the function with the image paths
            share.combine_img(selected_paths)
            
            # Open a new workspace window with the selected images and temporary directory
            self.window = PortraitWorkspace(self.selected_images, self.tmp)
            self.window.show()

    def add_buttons(self, layout):
        """Ajoute les boutons d'action (COMBINE, GENERATE, EXIT, REGENERATE) """
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
        self.combine_button.setFixedSize(250, 50)
        self.combine_button.setFont(QFont("8_bit_1_6", 28))
        self.combine_button.setEnabled(False)  
        button_layout.addWidget(self.combine_button)

        self.generate_button = QPushButton("GENERATE", self)
        self.generate_button.setStyleSheet(button_style)
        self.generate_button.setFixedSize(250, 50)
        self.generate_button.setFont(QFont("8_bit_1_6", 28))
        self.generate_button.setEnabled(False)  
        button_layout.addWidget(self.generate_button)


        self.generate_button.clicked.connect(self.on_generate_button_click)  
        self.combine_button.clicked.connect(self.on_combine_button_click)  

        exit_button = QPushButton("BACK TO START", self)
        exit_button.setStyleSheet(button_style)
        exit_button.setFixedSize(250, 50)
        exit_button.setFont(QFont("8_bit_1_6", 28))
        exit_button.clicked.connect(self.on_exit_button_click)
        button_layout.addWidget(exit_button)

        # Add the "Regenerate" icon in the same horizontal layout
        self.regenerate_button = QPushButton(self)
        self.regenerate_button.setIcon(
            QIcon(os.path.join(os.path.dirname(os.path.abspath(__file__)),"icone1.png")))
        self.regenerate_button.setIconSize(QSize(40, 40))  # Taille de l'icône
        self.regenerate_button.setStyleSheet("border: none; background-color: transparent;")
        self.regenerate_button.setFixedSize(50, 50)
        self.regenerate_button.clicked.connect(self.regenerate_images)
        button_layout.addWidget(self.regenerate_button)

        # Spacer after the buttons to center them
        button_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Add the buttons to the main window
        layout.addLayout(button_layout)

    def regenerate_images(self):
        """Regenerates a new selection of 20 random images from the 'data' folder and resets the selection."""
        print("Regenerating images...")

        # Clear the list of selected images
        self.selected_images.clear()

        # Remove all current images from the grid_layout
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  # Remove the widget (image label) from the layout

        #clear the tmp folder and upload 20 new images from the data folder
        share.clear_tmp()
        share.replace_20_first_img_in_directory()

        # Reload 20 new random images
        self.load_images()

        # Update the state of the buttons based on the new selection
        self.update_buttons_state()
        
    def on_exit_button_click(self):
        """Closes the current window and returns to the welcome screen (WelcomeScreen)."""

        #clear tmp and add 20 new images from data 
        share.clear_tmp()
        share.replace_20_first_img_in_directory()
        self.welcome_screen = WelcomeScreen()  # Create a new instance of WelcomeScreen
        self.welcome_screen.show() # Show the welcome screen
        self.close() # Close the current window



##### PORTRAIT WORKSPACE ######
class PortraitWorkspace(QWidget):
    """
    A workspace for displaying and interacting with generated portraits.

    This class allows the user to interact with a set of generated portraits by selecting them, generating new images, combining images, and viewing the result on the final screen.
    The screen shows the generated portraits of the genetic algorithm and the whole history of previous selected images.

    Attributes:
        tmp (str): The path to the directory containing the images.
        genetic_portraits (dict): A dictionary storing the last 4 generated portraits with their respective QIcons and QPushButtons.
        history_buttons (dict): A dictionary of previously selected portrait buttons for quick access.
        generated_buttons (list): A list of QPushButtons created for the portraits.
        selected_images (list): A list of selected portraits as QPushButtons.
        selected_buttons (list): A list of selected portrait buttons for quick access.
    """
    def __init__(self, selected_images, tmp):
        super().__init__()
        self.tmp = tmp  # Path to the tmp folder where images are stored

        self.genetic_portraits = self.get_last_images(tmp)  # Dict to get the last 4 portraits generated by the genetic algorithm
        self.history_buttons = {}  # Selective history; if an image isn't already in the history, add it.
        self.generated_buttons = []  # Holds all the buttons generated from selected images
        
        # List of images selected by the user
        self.selected_images = list(selected_images)  # A global history of selected images, storing all selected images
        self.selected_buttons = []  # List to store buttons associated with selected images
        
        # Initialize the user interface
        self.initUI()

    
    def get_last_images(self, tmp):
        """Fetches the last 4 images from the 'tmp' folder in the form of a dictionary {QIcon: QPushButton}."""

        def extract_index(filename):
            match = re.search(r'img(\d+)\.jpg', filename)
            return int(match.group(1)) if match else -1
        if not os.path.exists(tmp):
            raise ValueError("Image introuvable")

        valid_ext = ('.png', '.jpg', '.jpeg')
        images = [f for f in os.listdir(tmp) if f.lower().endswith(valid_ext) and f.startswith('img')]
        images = sorted(images,key = extract_index,reverse=True)[:4]  # Select the last 4 elements of the list 

        genetic_portraits = {} # Create a dictionary with QIcon as the key and QPushButton as the value
        for file_name in images: 
            path = os.path.join(tmp, file_name) 
            pixmap = QPixmap(path) # Create a QPixmap object from the image file
            icon = QIcon(pixmap) # Create a QIcon object from the QPixmap
            btn = self.create_image_button(icon) # Create a QPushButton with the QIcon
            btn.image_path = path # Store the image path in the button
            genetic_portraits[btn] = icon  # Add the button to the dictionary, with QIcon as the value

        return genetic_portraits # Return the dictionary containing the 4 most recent images

    def initUI(self):
        # Set window title and geometry
        self.setWindowTitle("Portrait Workspace")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: black;")

        # Create the main layout and sub-layouts
        self.global_layout = QVBoxLayout(self)
        main_layout = QHBoxLayout()
        self.generated_layout = QGridLayout()

        # History selection layout
        self.history_layout = QGridLayout()
        self.history_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.history_layout.setHorizontalSpacing(2)
        self.history_layout.setVerticalSpacing(2)

        # History label
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
        self.scroll_area.setStyleSheet("""
        QScrollArea {
            border: none;
            background-color: black;
        }
        QScrollBar:vertical {
            background: black;
            width: 14px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background: rgba(255, 255, 255, 120);  /* blanc semi-transparent */
            min-height: 20px;
            border-radius: 7px;
        }
        QScrollBar::handle:vertical:hover {
            background: rgba(255, 255, 255, 180);  /* plus lumineux au survol */
        }
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0px;
            background: none;
        }
        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {
            background: none;
        }
        """)

        self.history_widget = QWidget()  # Create a new QWidget to hold the history section

        # Create a layout for the history container
        history_container_layout = QVBoxLayout()  # Vertical layout to arrange history section widgets
        history_container_layout.setContentsMargins(0, 0, 0, 0)  # Remove any margins around the layout
        history_container_layout.addLayout(self.history_layout)  # Add the history layout (the grid) to the container layout
        history_container_layout.addStretch(1)  

        self.history_widget.setLayout(history_container_layout)  # Assign the layout to the history widget
        self.scroll_area.setWidget(self.history_widget)  # Add the history widget to the scroll area

        # Wrapper to better manage the history section size
        self.left_container = QWidget()  # Create a QWidget to contain the history section
        left_container_layout = QVBoxLayout(self.left_container)  # Vertical layout for the left container
        left_container_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins around the layout

        # Add the history label and scroll area to the layout
        left_container_layout.addWidget(self.history_label, alignment=Qt.AlignmentFlag.AlignCenter)  # Center align the history label
        left_container_layout.addWidget(self.scroll_area)  # Add the scroll area that will hold the history widget
        self.left_container.setMaximumWidth(int(self.width() * 0.28))  # Control the size of the left container based on window width

        main_layout.addWidget(self.left_container, stretch=1)  # Add the left container to the main layout with stretch factor 1
        main_layout.addLayout(self.generated_layout, stretch=2)  # Add the generated layout to the main layout with stretch factor 2

       # Center area
        self.global_layout.addLayout(main_layout)  # Add the main layout to the global layout of the window
        self.add_buttons() 
        self.load_buttons_into_grid(self.genetic_portraits.values())  # Add the genetic portraits (from algorithm) to the grid

        # Add selected images to the history section
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

        self.btn_finish = QPushButton("END")
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
        """
        This method creates a new QPushButton, sets its fixed size, assigns the provided
        icon to the button, and applies a style sheet to customize its appearance. 
        The button's click event is connected to a function that handles the selection toggling.
        """
        btn = QPushButton()  # Create a new QPushButton widget
        btn.setFixedSize(150, 150)  # Set the fixed size of the button (150x150 pixels)
        btn.setIcon(icon)  # Set the button icon (QIcon passed as a parameter)
        btn.setIconSize(btn.size())  # Set the icon size to fit the button's size
        btn.setStyleSheet("border: 2px solid white; background-color: black;")  # Style the button with a white border and black background
        btn.clicked.connect(lambda: self.toggle_selection(icon, btn))  # Connect the button click event to toggle selection (using a lambda for simplicity)
        return btn  # Return the created button

    def create_selection_handler(self, icon, btn):
        """
        Returns a lambda function that toggles the selection of the button when checked or unchecked.
        """
        # Returns a lambda function that toggles the selection of the button when checked or unchecked
        return lambda checked=False: self.toggle_selection(icon, btn)

    def load_buttons_into_grid(self, buttons):
        """
        Loads the buttons into the grid layout, removing any previous widgets.

        This function clears the existing widgets from the grid layout, and then loads 
        the buttons from the `genetic_portraits` dictionary into the layout in a 
        2-column format. After adding the buttons, it updates the state of the buttons 
        based on the current selection.
        """
        # Remove any existing widgets from the layout
        for i in reversed(range(self.generated_layout.count())):  
            widget = self.generated_layout.itemAt(i).widget()  # Get the widget at position i
            if widget:
                widget.setParent(None)  # Remove the widget from the layout (detaching it)

        self.generated_buttons.clear()  # Clear the list of generated buttons
        
        # Load the buttons from the genetic_portraits dictionary
        for i, (btn, icon) in enumerate(self.genetic_portraits.items()):  
            self.generated_buttons.append(btn)  # Add the button to the list of generated buttons
            self.generated_layout.addWidget(btn, i // 2, i % 2)  # Add the button to the grid layout, in 2-column format

        self.update_buttons_state()  # Update the state of the buttons (enable/disable based on the selection)

    def toggle_selection(self, icon, btn):
        """
        Toggles the selection state of a button (icon) and updates its appearance.

        If the button is already selected, it will be deselected and the border color will be reset.
        If the button is not selected, it will be added to the selected list, and the border color will change to red.
        """
        if btn in self.selected_buttons:
            # Deselect the button if it is already selected
            self.selected_buttons.remove(btn)  # Remove the button from the list of selected buttons
            btn.setStyleSheet("border: 2px solid white; background-color: black;")  # Reset the button's border color

        else:
            # Select the button if it is not selected
            self.selected_buttons.append(btn)  # Add the button to the list of selected buttons
            btn.setStyleSheet("border: 2px solid red; background-color: black;")  # Change the button's border color to red
            self.selected_images.append(btn)  # Add the button to the list of selected images

        self.update_buttons_state()  # Update the state of the buttons (enable/disable based on the selection)

    def update_buttons_state(self):
        """
        This method checks the number of buttons currently selected and enables or disables
        the "Generate" and "Combine" buttons accordingly:
        - The "Generate" button is enabled only if exactly one button is selected.
        - The "Combine" button is enabled only if more than one button is selected.
        """
        count = len(self.selected_buttons)  # Get the number of selected buttons

        # Enable the "Generate" button only if exactly one button is selected
        self.btn_generate.setEnabled(count == 1)

        # Enable the "Combine" button only if more than one button is selected
        self.btn_combine.setEnabled(count > 1)

    def add_to_history(self, icon):
        """
        Adds an icon to the selection history if it is not already present.
        
        Compares the new icon with the existing icons in the history to avoid duplicates.
        If the icon is unique, a new button is created for it and added to the history layout.
        
        Args:
            icon (QIcon): The icon representing an image to add to the history.
        """
        # Check if the icon is already in the history by comparing its pixmap (scaled to 60x60)
        for existing_icon in self.history_buttons.keys():
            if existing_icon.pixmap(QSize(60, 60)).toImage() == icon.pixmap(QSize(60, 60)).toImage():
                return  # If the icon is already in history, do nothing

        # Create a new button for the icon if it's not already in history
        btn = QPushButton()
        btn.setIcon(icon)  # Set the icon for the button
        btn.setIconSize(QSize(60, 60))  # Set the icon size to 60x60
        btn.setFixedSize(70, 70)  # Set the button size to 70x70
        btn.setStyleSheet("border: 2px solid white; background-color: black;")  # Style the button

        # Connect the button's click event to the toggle_selection function
        btn.clicked.connect(lambda: self.toggle_selection(icon, btn))
        self.history_buttons[icon] = btn
        row, col = divmod(len(self.history_buttons) - 1, 2) # Calculate the row and column for placing the button in the history layout
        self.history_layout.addWidget(btn, row, col) # Add the button to the history layout

    def reset_selection_styles(self):
        """
         Deselects all selected buttons and resets their style to the default.
        """
        # Deselect all the generated buttons and reset their styles to default
        for btn in self.generated_buttons:
            btn.setStyleSheet("border: 2px solid white; background-color: black;")
        self.selected_buttons.clear()
        # Deselect all the history buttons and reset their styles to default
        for btn in self.history_buttons.values():
            btn.setStyleSheet("border: 2px solid white; background-color: black;")
    
    def get_selected_image_paths(self):
        """
        This method goes through the list of selected buttons and extracts the 
        associated image paths. If the button has an 'image_path' attribute, 
        it appends the path to the list.
        """
        paths = [] # List to store the paths of the selected images
        for btn in self.selected_buttons:
            if hasattr(btn, 'image_path'):
                paths.append(btn.image_path)
        return paths

    def on_generate_clicked(self):
        """
        Handles the click event of the "Generate" button.

        This method checks if exactly one image button is selected. If so, it calls the `generate_img` function with the selected image's path, adds
        the image to the history, and resets the selection styles.
        """
        if len(self.selected_buttons) != 1: # If the number of selected buttons is not exactly 1, do nothing
            return
        
        # Call the generate_img function with the image paths
        image_paths = self.get_selected_image_paths()
        if image_paths:
            share.generate_img(image_paths)

        selected_btn = self.selected_buttons[0] # Get the selected button
        icon = self.genetic_portraits.get(selected_btn)  # Get the icon associated with the selected button
        if icon:
            self.add_to_history(icon)  # Add the selected image to the history

        self.genetic_portraits = self.get_last_images(self.tmp)
        self.load_buttons_into_grid(self.genetic_portraits.items())
        self.reset_selection_styles() # Reset the selection styles (deselect the images)

    def on_combine_clicked(self):
        """
        Handles the click event of the "Combine" button.

        This method checks if at least two image buttons are selected. If so, it  calls the `combine_img` function with the paths of the selected images,
        adds each selected image to the history, and resets the selection styles.
        """
        if len(self.selected_buttons) < 2: # If less than 2 buttons are selected, do nothing
            return
        
        # Get the paths of the selected images
        image_paths = self.get_selected_image_paths()
        if image_paths:
            share.combine_img(image_paths)

        # Add each selected image to the history
        for btn in self.selected_buttons:
            icon = self.genetic_portraits.get(btn)
            if icon:
                self.add_to_history(icon)

        self.genetic_portraits = self.get_last_images(self.tmp)
        self.load_buttons_into_grid(self.genetic_portraits.items())
        self.reset_selection_styles() # Reset the selection styles (deselect the images)

    def on_finish_button_click(self):
        """
        Handles the click event of the "Finish" button.

        This method converts each selected QPushButton from the `selected_images` list into a QLabel containing the corresponding image. Then, it passes
        these labels to the `FinalScreen` to display them.
        """
        selected_images_2 = []  # New list to hold QLabel objects

        # Convert each QPushButton into a QLabel
        for button in self.selected_images:  # self.selected_images contains QPushButton objects
            if isinstance(button, QPushButton):  # Check if the item is a QPushButton
                pixmap = button.icon().pixmap(button.size())  # Get the QPixmap of the button's icon
                if pixmap:
                    # Create a QLabel with the image
                    label = QLabel()
                    label.setPixmap(pixmap)  # Set the image to the QLabel
                    selected_images_2.append(label)  # Add the QLabel to the new list

        # Now pass the selected_images_2 (containing QLabels) to FinalScreen
        self.final_screen = FinalScreen(selected_images_2, self.history_buttons)
        self.final_screen.show()  


##### FINAL SCREEN ##### 
class FinalScreen(QWidget):
    """
    A screen displayed after completing the portrait generation process.

    This class shows a "Well Done!" message, the last selected portrait image, and buttons for downloading the image, downloading the history, and showing the history.

    Attributes:
        selected_images (list): List of selected images (QLabel objects) to be displayed.
        history_buttons (dict): Dictionary of historical buttons (QPushButton objects).
    """

    def __init__(self, selected_images_2, history_buttons):
        """
        Initializes the FinalScreen with the selected images and history buttons.
        """
        super().__init__()
        self.selected_images = selected_images_2  # List of selected images (QLabel objects)
        self.history_buttons = history_buttons  # Dictionary of historical buttons
        self.setWindowTitle("Well Done")
        self.setGeometry(100, 100, 800, 600)  # Set the window size and position
        self.setStyleSheet("background-color: black;")  # Set the background to black
    
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

        # Image: Retrieve the last selected image (the last in the list)
        last_image_label = self.selected_images[-1]  # Last QLabel in the list
        pixmap = last_image_label.pixmap()  # Get the pixmap from the QLabel

        # If the pixmap is valid (not null), resize it
        if pixmap:
            # Resize the image to make it larger
            scaled_pixmap = pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio)  # Scale the image to 300x300 while keeping the aspect ratio
            self.image_label = QLabel(self)  # Create a QLabel to display the image
            self.image_label.setPixmap(scaled_pixmap)  # Apply the scaled image to the label
            self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the image within the label
            layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)  # Add the image to the layout

            # Create a neon flashing frame around the image
            self.create_neon_frame(self.image_label)
           
        else:
            print("Erreur")  
        
        # Add buttons to the interface with the same style as the other screens
        self.add_buttons(layout)
    
    def create_neon_frame(self, image_label):
        """
        Creates a neon flashing frame around the image.
        """        
        self.neon_effect = QGraphicsDropShadowEffect()
        self.neon_effect.setColor(QColor(255, 0, 0))  # Red color
        self.neon_effect.setBlurRadius(100) # Blur radius for the frame
        self.neon_effect.setOffset(0, 0)  

        # Apply the effect to the label containing the image
        image_label.setGraphicsEffect(self.neon_effect)

        # Create a timer to make the frame flash
        self.neon_timer = QTimer(self)
        self.neon_timer.timeout.connect(self.toggle_neon_effect)  
        self.neon_timer.start(500)  # The frame flashes every 500 ms (0.5 second)

    def toggle_neon_effect(self):
        """
        Toggles the visibility of the neon frame to make it flash.
        """        
        if self.neon_effect.isEnabled():
            self.neon_effect.setEnabled(False)  # Disable the frame effect
        else:
            self.neon_effect.setEnabled(True)  # Enable the frame effect

    def add_buttons(self, layout):
        """
        Adds the buttons for downloading the image, downloading the history, 
        and showing the history to the layout.
        """
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

        # "Download this image" button
        self.download_image_button = QPushButton("Download image", self)
        self.download_image_button.setStyleSheet(button_style)
        self.download_image_button.setFixedSize(250, 50)
        self.download_image_button.setFont(QFont("8_bit_1_6", 14))
        self.download_image_button.setEnabled(True)  # Active le bouton selon ton besoin
        button_layout.addWidget(self.download_image_button)

        # "Download the whole history" button
        self.download_history_button = QPushButton("Download history", self)
        self.download_history_button.setStyleSheet(button_style)
        self.download_history_button.setFixedSize(250, 50)
        self.download_history_button.setFont(QFont("8_bit_1_6", 14))
        self.download_history_button.setEnabled(True)  # Active le bouton selon ton besoin
        button_layout.addWidget(self.download_history_button)

        # "Show the whole history" button
        self.show_history_button = QPushButton("Show history", self)
        self.show_history_button.setStyleSheet(button_style)
        self.show_history_button.setFixedSize(250, 50)
        self.show_history_button.setFont(QFont("8_bit_1_6", 14))
        self.show_history_button.setEnabled(True)  # Active le bouton selon ton besoin
        button_layout.addWidget(self.show_history_button)

        # Connect the buttons to their respective actions
        self.download_image_button.clicked.connect(self.download_image)
        self.download_history_button.clicked.connect(self.download_history)
        self.show_history_button.clicked.connect(self.show_history)

        # Spacer after the buttons to center them
        button_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Add the buttons to the main window
        layout.addLayout(button_layout)

    def download_history(self):
        """
        Downloads all images from the history into a folder named 'history'.
        Opens a file dialog for the user to select the download directory.
        """
        # Open a dialog to choose the folder
        folder_path = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        if not folder_path:
            print("No folder selected.")
            return "Download canceled."

        # Create a "history" subfolder in the selected directory
        history_folder = os.path.join(folder_path, "history")
        os.makedirs(history_folder, exist_ok=True)

        # Loop through all history buttons
        for index, button in enumerate(self.history_buttons.values(), start=1):
            pixmap = button.icon().pixmap(300, 300)  # Get the pixmap of the button's icon

            if pixmap and not pixmap.isNull():
                file_name = f"image_{index}.png"
                file_path = os.path.join(history_folder, file_name)

                if pixmap.save(file_path):
                    print(f"Image saved: {file_path}")
                else:
                    print(f"Error saving {file_path}")
            else:
                print(f"No valid pixmap for button {index}")

        return f"Images saved in: {history_folder}"

    def show_history(self):
        """
        Displays the history of portraits as a grid of buttons.
        Creates a grid layout to display all the historical buttons.
        """
       # Create a grid layout for the history
        history_layout = QVBoxLayout()  # Main layout to contain the title + grid
        history_layout.setSpacing(15)

        # "History" title
        history_label = QLabel("History", self)
        history_label.setFont(QFont("Press Start 2P", 20, QFont.Weight.Bold))
        history_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        history_label.setStyleSheet("color: white; background: transparent;")
        history_layout.addWidget(history_label)

        # Grid of buttons
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)  # Space between buttons
        columns = 8  # Number of columns in the grid
        row, col = 0, 0

        for index, btn in enumerate(self.history_buttons.values()):
            grid_layout.addWidget(btn, row, col)
            col += 1
            if col >= columns:
                col = 0
                row += 1

        history_layout.addLayout(grid_layout)  # Add the grid to the main layout
        self.layout().addLayout(history_layout)  # Add everything to the window
        self.show_history_button.setEnabled(False)  # Disable the button to avoid duplicates

    def download_image(self):
        """
        Downloads the last selected image as 'selected portrait'.

        Opens a file dialog to allow the user to choose where to save the image.
        """
        # Open a file dialog to allow the user to choose where to save the image
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)  # Allow selecting any file
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg)")  # Filter for image files
        file_dialog.setViewMode(QFileDialog.ViewMode.List)  # List view for file selection

        # Default file name for the save
        default_file_name = "selected portrait.png"
        file_dialog.selectFile(default_file_name)  # Set the default file name in the dialog

        if file_dialog.exec():  # If the user has selected a file
            file_path = file_dialog.selectedFiles()[0]  # Get the selected file path
            print(f"Selected path: {file_path}")  # Debugging message showing the selected path
            
            last_image_label = self.selected_images[-1]  # Get the last selected image
            pixmap = last_image_label.pixmap()  # Get the pixmap of the last image

            if pixmap:  # If the pixmap is valid
                # Check the file format
                if not file_path.endswith(('.png', '.xpm', '.jpg')):  # If the file format is incorrect
                    file_path += '.png'  # Add .png extension if not specified

                print(f"Trying to save the image at {file_path}")  # Debugging message before saving
                
                saved = pixmap.save(file_path)  # Save the image to the chosen location
                
                if saved:
                    print(f"Image saved at {file_path}")  # Success message
                    return "Image saved successfully!"  # Return a success message
                else:
                    print(f"Error saving the image: {file_path}")  # Error message
                    return "Error saving the image."  # Return an error message
            else:
                print("No image to save!")  # Error message if no image is available
                return "No image to save!"  # Return an error message



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WelcomeScreen()
    window.show()
    sys.exit(app.exec())