from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QVBoxLayout, QPushButton, QTextEdit, QLabel, QWidget
)
from PyQt5.QtCore import QThread, pyqtSignal
from src.assistant import process_query
from src.voice_input import get_voice_input
from src.voice_output import speak
class AssistantThread(QThread):
    """Thread to run the assistant logic without blocking the GUI."""
    response_signal = pyqtSignal(str)

    def __init__(self, query):
        super().__init__()
        self.query = query

    def run(self):
        response = process_query(self.query)  # Call assistant logic
        self.response_signal.emit(response)   # Emit the response

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Adi - Voice Assistant")
        self.setGeometry(300, 300, 400, 300)

        # Layout and Widgets
        layout = QVBoxLayout()
        self.query_input = QTextEdit()
        layout.addWidget(QLabel("Enter Command or Speak:"))
        layout.addWidget(self.query_input)

        self.submit_button = QPushButton("Submit Text Command")
        self.voice_button = QPushButton("Speak Command")
        layout.addWidget(self.submit_button)
        layout.addWidget(self.voice_button)

        self.response_label = QLabel("Response will appear here.")
        layout.addWidget(self.response_label)

        # Set layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connect buttons to handlers
        self.submit_button.clicked.connect(self.handle_text_input)
        self.voice_button.clicked.connect(self.handle_voice_input)

    def handle_text_input(self):
        """Handle text input submission."""
        query = self.query_input.toPlainText().strip()
        if query:
            self.run_assistant(query)

    def handle_voice_input(self):
        """Capture and process voice input automatically."""
        query = get_voice_input()  # Capture voice input
        if query:
            self.query_input.setText(query)  # Display query in the text box
            self.run_assistant(query)  # Auto-submit the query
    # Auto-submit the query

    def run_assistant(self, query):
        """Run the assistant logic in a separate thread."""
        self.assistant_thread = AssistantThread(query)
        self.assistant_thread.response_signal.connect(self.display_response)
        self.assistant_thread.start()

    def display_response(self, response):
        """Display the response in the GUI and speak it once."""
        if response:  # Ensure response is valid
            self.response_label.setText(response)  # Update the response label
            speak(response)  # Speak the response only once



