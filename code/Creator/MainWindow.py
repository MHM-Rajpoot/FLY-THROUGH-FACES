from common import *
from utilities import Uilities
from VideoColumn import VideoColumn
from InfoColumn import InfoColumn
from ImageProcessing import ImageProcessing
from model import ModelA

class MyWindow(QMainWindow):
    
    def __init__(self):
        """
        Initialize the main window.
        """
        super().__init__()

        # Setup the GUI
        self.gui_setup()

        # Initialize ImageProcessing instance
        self.img_pro = ImageProcessing()

        # Initialize Utilities instance
        self.util = Uilities()

        # Initialize ModelA instance
        self.modelA = ModelA()
        
        # OpenCV Video Capture
        self.video_capture = self.img_pro.get_video_capture()
        self.detector = self.img_pro.get_detector()

        # Setup the timer for updating frames
        self.setup_timer()

        # Initialize variables for time tracking and detection/capture control
        self.timer_start = bool(1)
        self.start_time = time.time()
        self.detect = bool(0)
        self.capture = bool(1)
        self.save = bool(0)

    def gui_setup(self):
        """
        Set up the GUI layout.
        """
        # Set window properties
        self.setWindowFlag(Qt.FramelessWindowHint)  # Remove the title bar

        # Get the screen dimensions using QGuiApplication
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width, screen_height = screen_geometry.width(), screen_geometry.height()

        # Set the window size to fill the whole screen
        self.setGeometry(0, 0, screen_width, screen_height)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)

        # Create the first column (75% width) for video display
        self.column1 = VideoColumn()
        layout.addWidget(self.column1, 3)

        # Create the second column (25% width) for information display
        self.column2 = InfoColumn()
        layout.addWidget(self.column2, 1)

    def setup_timer(self):
        """
        Set up a timer to update frames at 120 FPS.
        """
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1000 // 120)  # Update at 120 FPS
    
    def update_frame(self):
        """
        Update frames function.
        """

        ret, frame = self.video_capture.read()
        self.detect = self.column2.get_capture_image()
        
        if ret and self.capture:

            detection_result,frame = self.img_pro.preprocess(frame)

            if detection_result.detections and self.detect:
                if detection_result.detections[0].categories[0].score > 0.75:

                    if self.timer_start:
                        self.start_time = time.time()
                        self.timer_start = False
                    
                    frame = self.img_pro.add_circle(frame,1)
                    
                    # Calculate the elapsed time
                    elapsed_time = time.time() - self.start_time
                    current_digit = str(3 - int(elapsed_time))  # Start from 5 and decrement

                    frame = self.img_pro.timer_on_image(frame,current_digit)

                    if(int(current_digit)==int(0)):
                        self.save = True
                        self.capture = False

            else:
                frame = self.img_pro.add_circle(frame,0)
                self.timer_start = True

            self.column1.update_frame(frame)
            print('\r Annotated ',frame.shape,end='')

        elif self.save:

            if(self.img_pro.image_cpaturing()):
                self.column2.set_cap_image(False)
                self.util.train_test_split()
                out =self.modelA.train_n_save_a(self.column2.get_textbox())
                if(out):
                    self.column2.set_textbox()
                self.util.usb_passport(self.column2.get_textbox())
            else:
                self.column2.set_cap_image(True)
            
            self.capture = True
            self.save = False
            self.timer_start = True
