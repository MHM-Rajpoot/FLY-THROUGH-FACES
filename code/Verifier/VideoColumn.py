from common import *

class VideoColumn(QWidget):
    
    def __init__(self):
        """
        Initialize the VideoColumn widget.
        """
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface for the VideoColumn widget.
        """
        # Set the background color of the widget to blue
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(52, 152, 219))  # Blue color
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
        # Create a horizontal layout for the widget
        layout = QHBoxLayout(self)
        
        # Create a QLabel to display the video frame, centered within the widget
        self.label = QLabel(self)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)

    def update_frame(self, frame):
        """
        Update the displayed video frame.

        Args:
            frame: The frame to be displayed, represented as a numpy array.
        """
        # Get the dimensions of the frame
        height, width, channel = frame.shape
        
        # Calculate the number of bytes per line in the frame
        bytes_per_line = 3 * width
        
        # Convert the frame to a QImage
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        
        # Swap the R and B channels of the QImage
        q_image = q_image.rgbSwapped()
        
        # Convert the QImage to a QPixmap
        pixmap = QPixmap.fromImage(q_image)
        
        # Set the QPixmap as the pixmap of the QLabel, displaying the frame
        self.label.setPixmap(pixmap)
