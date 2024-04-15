# Import necessary modules
from common import *
from MainWindow import MyWindow

# Check if this module is being run as the main program
if __name__ == "__main__":
    # Create a QApplication instance, required for GUI applications
    app = QApplication(sys.argv)
    
    # Create an instance of MyWindow class, which presumably is the main application window
    window = MyWindow()
    
    # Show the main window
    window.show()
    
    # Start the application event loop, sys.exit() ensures a clean exit
    sys.exit(app.exec())
