from common import *

class InfoColumn(QWidget):
    """
    Class representing the information column in the GUI.
    """

    def __init__(self):
        """
        Initialize the InfoColumn widget.
        """
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface for the InfoColumn.
        """
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(231, 76, 60))  # Red color
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
        layout = QVBoxLayout(self)  # Use a vertical layout for the second column

        # Create a label for the image
        self.image_label = QLabel(self)
        self.image_label.setStyleSheet("background-color: lightgreen;")
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        # Create labels for the rows
        self.row1_label = QLabel(self)
        self.row2_label = QLabel(self)
        self.status = QLabel(self)

        # Increase the font size for row content
        font = QFont()
        font.setPointSize(16)  # Adjust the font size as needed

        self.row1_label.setFont(font)
        self.row2_label.setFont(font)
        self.status.setFont(font)

        # Set background colors for the labels
        self.row1_label.setStyleSheet("background-color: lightgreen;")  # Change color as desired
        self.row2_label.setStyleSheet("background-color: lightgreen;")  # Change color as desired
        self.status.setStyleSheet("background-color: lightgreen;")

        layout.addWidget(self.row1_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.row2_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.status, alignment=Qt.AlignCenter)

        # Add some spacing between the rows and image (optional)
        layout.addSpacing(20)

        # Set layout for the second column
        self.setLayout(layout)

    def set_content(self, image_path, text1, text2):
        """
        Set the content of the InfoColumn.

        Args:
            image_path (str): Path to the image to be displayed.
            text1 (str): Text for the first row.
            text2 (str): Text for the second row.
        """
        # Set the image
        pixmap = QPixmap(image_path)
        # Resize the image to fit within the column width
        pixmap = pixmap.scaledToWidth(200)  # Adjust the width as needed
        self.image_label.setPixmap(pixmap)

        # Set the text for row 1 and row 2
        self.row1_label.setText(text1)
        self.row2_label.setText(text2)
        self.status.setText('Detetion Result')
    
    def set_result(self,txt:str):
        """
        Set the detection result text.

        Args:
            txt (str): Text to be set as the detection result.
        """
        self.status.setText(txt)
    
    def get_cnic(self):
        """
        Get the CNIC text from the InfoColumn.

        Returns:
            str: The CNIC text.
        """
        return self.status.text()
