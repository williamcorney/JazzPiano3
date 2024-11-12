import pickle
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QListWidget, \
    QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QAbstractItemView
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap, QFont
from note_handler import note_handler  # Importing the note_handler function


class Practical(QWidget):
    # Define custom signals for note on/off
    note_on_signal = pyqtSignal(int, str)
    note_off_signal = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap_item = {}

        # Initialize Theory from pickle file
        try:
            with open('theory.pkl', 'rb') as file:
                self.Theory = pickle.load(file)
            print("Theory loaded from file")
        except FileNotFoundError:
            self.Theory = {}  # Default empty dictionary if file is not found
            print("Theory file not found. Using default.")

        # Create layout and widget for Practical Tab
        self.layout = QVBoxLayout(self)
        self.label = QLabel("This is the Practical tab.")
        self.layout.addWidget(self.label)

        # Button to print shared data (from Oralia)
        self.print_data_button = QPushButton("Print Shared Data")
        self.print_data_button.clicked.connect(self.print_shared_data)
        self.layout.addWidget(self.print_data_button)

        # Set up the list widgets for theory display
        self.horizontal = QHBoxLayout()
        self.layout.addLayout(self.horizontal)

        # Creating QListWidgets for different theories
        self.theory1, self.theory2, self.theory3 = QListWidget(), QListWidget(), QListWidget()
        for theory in [self.theory1, self.theory2, self.theory3]:
            self.horizontal.addWidget(theory, stretch=1)

        self.theory1.addItems(["Notes", "Scales", "Triads", "Sevenths", "Modes", "Shells"])
        self.theory2.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        # Set up QGraphicsScene for displaying piano keys
        self.Scene = QGraphicsScene()
        self.BackgroundPixmap = QPixmap(
            "/Users/williamcorney/PycharmProjects/JazzPiano2/Practical/Images/Piano/keys.png")
        self.BackgroundItem = QGraphicsPixmapItem(self.BackgroundPixmap)
        self.Scene.addItem(self.BackgroundItem)

        self.View = QGraphicsView(self.Scene)
        self.View.setFixedSize(self.BackgroundPixmap.size())
        self.View.setSceneRect(0, 0, self.BackgroundPixmap.width(), self.BackgroundPixmap.height())
        self.View.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.View.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.layout.addWidget(self.View)

        # Connect signals to methods
        self.note_on_signal.connect(self.insert_note)
        self.note_off_signal.connect(self.delete_note)

        # Set up the additional labels in the layout
        self.horizontal_vertical = QVBoxLayout()
        self.horizontal.addLayout(self.horizontal_vertical, 2)

        # Create the labels with relevant text
        self.labels = {}
        for key, text in [('key_label', 'Key: C Major'),
                          ('inversion_label', 'Inversion: Root'),
                          ('fingering_label', 'Fingering: 1-2-3-4-5'),
                          ('score_value', 'Score: 100')]:
            label = QLabel(text)
            if key == 'key_label':
                label.setFont(QFont("Arial", 32))  # Set the font for 'key_label'
            self.labels[key] = label
            self.horizontal_vertical.addWidget(label)

    def handle_midi_message(self, message):

        """
        This method will be passed as a callback to mido, which will in turn
        call note_handler with the Practical instance and the message.
        """
        note_handler(self, message)  # Pass self (Practical instance) and the MIDI message

    def get_shared_data(self):
        """
        Returns the shared data as a dictionary from the main window (Oralia).
        """
        main_window = self.window()  # Access Oralia window to get shared data
        return main_window.shared_data  # Access shared data from Oralia

    def print_shared_data(self):
        """
        Calls get_shared_data and prints the result to the console.
        """
        shared_data = self.get_shared_data()
        print("Shared Data:", shared_data)  # Print shared data to the console

    def insert_note(self, note, color):
        """
        Insert a note (visual representation) on the piano keyboard at the given position.
        """
        self.xcord = self.Theory["NoteCoordinates"][note % 12] + ((note // 12) - 4) * 239
        self.pixmap_item[note] = QGraphicsPixmapItem(
            QPixmap("/Users/williamcorney/PycharmProjects/JazzPiano2/Practical/Images/Piano/key_" + color + self.Theory["NoteFilenames"][note % 12]))
        self.pixmap_item[note].setPos(self.xcord, 0)
        current_scene = self.pixmap_item[note].scene()
        if current_scene:
            current_scene.removeItem(self.pixmap_item[note])
        self.Scene.addItem(self.pixmap_item[note])

    def delete_note(self, note):
        if note in self.pixmap_item:
            if self.pixmap_item[note].scene():
                self.pixmap_item[note].scene().removeItem(self.pixmap_item[note])
            del self.pixmap_item[note]
