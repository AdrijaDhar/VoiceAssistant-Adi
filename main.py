from src.gui import MainWindow  # Import your GUI class
from PyQt5.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)  # Initialize the Qt application
    window = MainWindow()  # Create an instance of your main window
    window.show()  # Show the GUI window
    sys.exit(app.exec_())  # Start the application event loop

if __name__ == "__main__":
    main()
