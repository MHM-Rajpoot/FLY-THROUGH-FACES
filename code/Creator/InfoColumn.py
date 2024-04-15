from common import *
from utilities import Uilities

class InfoColumn(QWidget):
    
    def __init__(self):
        """
        Initialize the InfoColumn widget.
        """
        super().__init__()
        self.setup_ui()

        # Initialize Utilities instance
        self.util = Uilities()

    def setup_ui(self):
        """
        Set up the UI components of the InfoColumn widget.
        """
        self.detect = False

        # Set background color
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(231, 76, 60))  # Red color
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Use a vertical layout for the second column
        layout = QVBoxLayout(self)

        # Increase the font size for row content
        font = QFont()
        font.setPointSize(16)  # Adjust the font size as needed

        # Add some spacing between the rows and image (optional)
        layout.addSpacing(20)

        # Create a button for capturing
        self.capture_button = QPushButton("Detect")
        self.capture_button.clicked.connect(self.set_capture_image)
        layout.addWidget(self.capture_button, alignment=Qt.AlignCenter)
        self.capture_button.setEnabled(False)  # Initially disable the button

        # Create a text box
        self.textbox = QLineEdit(self)
        layout.addWidget(self.textbox, alignment=Qt.AlignCenter)
        self.textbox.textChanged.connect(self.check_textbox)  # Connect the signal to the slot

        # Create a save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_text)
        layout.addWidget(self.save_button, alignment=Qt.AlignCenter)

        # Create a status label
        self.status = QLabel(self)
        self.status.setFont(font)
        self.status.setStyleSheet("background-color: lightgreen;")
        layout.addWidget(self.status, alignment=Qt.AlignCenter)
        self.status.setText('Enter Valid CNIC !')

        # Add some spacing between the rows and image (optional)
        layout.addSpacing(20)

        # Set layout for the second column
        self.setLayout(layout)

    def set_status(self, status, color):
        """
        Set the status text and background color of the status label.
        """
        self.status.setText(status)
        if color:
            self.status.setStyleSheet("background-color: green;")
        else:
            self.status.setStyleSheet("background-color: red;")

    def set_capture_image(self):
        """
        Set the capture image flag to True.
        """
        self.detect = True

    def set_cap_image(self, state):
        """
        Set the capture image flag based on the given state.
        """
        self.detect = state

    def get_capture_image(self):
        """
        Get the current state of the capture image flag.
        """
        return self.detect
        
    def save_text(self):
        """
        Handle the save button click event.
        """
        text = self.textbox.text()
        print("Save Pressed ", end='')

    def check_textbox(self):
        """
        Check the validity of the CNIC entered in the text box.
        """
        text = self.textbox.text()
        check = self.util.check_cnic(text)
        if check:
            self.capture_button.setEnabled(True)
            self.set_status('Successful CNIC', 1)
        else:
            self.capture_button.setEnabled(False)
            self.set_status('Unsuccessful CNIC', 0)

    def set_textbox(self, value='') -> None:
        """
        Set the text box value.
        """
        self.textbox.setPlaceholderText('')

    def get_textbox(self) -> str:
        """
        Get the text from the text box.
        """
        return self.textbox.text()

    def set_save_button(self, state):
        """
        Enable or disable the save button based on the given state.
        """
        self.save_button.setEnabled(state)
        print('State : ', state, end='')

    def get_text(self):
        """
        Get the text from the text box (not implemented).
        """
        text = self.textbox.text()
        print("Text to save:", text)
        # You can add code here to save the text to a file or perform any other necessary action
