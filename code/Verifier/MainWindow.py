from common import *
from model import ModelA
from VideoColumn import VideoColumn
from InfoColumn import InfoColumn
from ImageProcessing import ImageProcessing

class MyWindow(QMainWindow):
    """
    Class representing the main application window.
    """

    def __init__(self):
        """
        Initialize the main application window.
        """
        super().__init__()

        # Call the method to set up the GUI
        self.gui_setup()

        # Initialize ImageProcessing instance
        self.img_pro = ImageProcessing()

        # Initialize ModelA instance
        self.modela = ModelA()

        # Initialize a variable to keep track of the insertion of the passport
        self.pinsert = int(0)
        
        # OpenCV Video Capture
        self.video_capture = self.img_pro.get_video_capture()
        self.detector = self.img_pro.get_detector()

        # Set up the timer for updating frames
        self.setup_timer()

        # Initialize variables for time tracking and detection/capture control
        self.timer_start = bool(1)
        self.start_time = time.time()
        self.detect = bool(1)
        self.capture = bool(0)

    def gui_setup(self):
        """
        Set up the graphical user interface.
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
        
        # Call set_content to update the image and text in the second column
        self.column2.set_content("...", "Cnic Here", " \n Default \n Default ")
  
    def setup_timer(self):
        """
        Set up a timer for updating frames at 120 FPS.
        """
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1000 // 120)
    
    def update_frame(self):
        """
        Update frames and information display.
        """
        # Check if the passport is not inserted yet
        if not(self.pinsert):
            try:
                with open('...', 'r') as file:
                    self.cnic = file.readlines()[0]
                self.column2.set_content("...", str(self.cnic), "Dummy")
                self.detect = 1
                self.pinsert = 1
            except:
                self.column2.set_content("...", "Cnic Here", " \n Default \n Default ")
                self.detect = 0
            
        ret, frame = self.video_capture.read()
        
        if ret and not self.capture:
            
            # Preprocess the frame to detect faces
            detection_result, frame = self.img_pro.preprocess(frame)

            if detection_result.detections and self.detect:
                if (detection_result.detections[0].categories[0].score > 0.75) :
                    if self.timer_start:
                        self.start_time = time.time()
                        self.timer_start = False
                    
                    frame = self.img_pro.add_circle(frame,1)
                    
                    # Calculate the elapsed time
                    elapsed_time = time.time() - self.start_time
                    current_digit = str(5 - int(elapsed_time))  

                    frame = self.img_pro.timer_on_image(frame,current_digit)

                    if(int(current_digit)<int(2)):
                        self.capture = True

            else:
                frame = self.img_pro.add_circle(frame,0)
                self.timer_start = True

            # Update the video column with the new frame
            self.column1.update_frame(frame)
            print('\r Annoted ',frame.shape,end='')

        else:
            if(self.img_pro.image_cpaturing()):
                pp,np = self.modela.model_a_verification(self.cnic)
                self.column2.set_result(str(pp))
                self.detect =  False
            else:  
                self.detect = True
            

            self.capture = False
            self.timer_start = True
