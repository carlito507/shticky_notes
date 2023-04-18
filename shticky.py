import sys
import re
import pickle
import logging
import os

from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget,
                             QSplitter, QPushButton, QHBoxLayout, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtWebEngineWidgets import QWebEngineView
import markdown

NOTE_FILE_NAME = "note.pickle"
DEFAULT_WINDOW_SIZE = (800, 800)
DEFAULT_SPLITTER_SIZE = [400, 400]


def load_style_sheet(file_name):
    try:
        with open(file_name, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error loading style sheet: {e}")
        return ""


# Load the style sheet from an external file
style_sheet = load_style_sheet("style.qss")


class MarkdownStickyNote(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set up the UI
        self.init_ui()
        try:
            with open(NOTE_FILE_NAME, "rb") as f:
                notes = pickle.load(f)
                self.text_edit.setText(notes)
        except Exception as e:
            print(f"Error loading note from file: {e}")

    def init_ui(self):
        # Set the window title
        self.setWindowTitle('Markdown Sticky Note')

        # Set the default window size
        self.setGeometry(100, 100, DEFAULT_WINDOW_SIZE)

        # Apply the dark high contrast theme
        self.apply_dark_theme()

        # Set the main layout
        layout = QVBoxLayout()

        self.setStyleSheet(style_sheet)

        # Create and configure the markdown text editor
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont('Neue Plak', 12))

        # Create the QWebEngineView to display the rendered markdown
        self.web_view = QWebEngineView()

        # Add the text editor and web view to a splitter
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.text_edit)
        self.splitter.addWidget(self.web_view)

        # Set the initial sizes of the text editor and the web view
        self.splitter.setSizes(DEFAULT_SPLITTER_SIZE)

        # Create a button to toggle between single and dual views
        self.toggle_view_button1 = QPushButton("Toggle Raw View")
        self.toggle_view_button1.clicked.connect(self.toggle_view1)

        self.toggle_view_button2 = QPushButton("Toggle Markdown View")
        self.toggle_view_button2.clicked.connect(self.toggle_view2)

        # Add the buttons to a horizontal layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.toggle_view_button1)
        button_layout.addWidget(self.toggle_view_button2)

        # Add the splitter and buttons to the layout
        layout.addLayout(button_layout)
        layout.addWidget(self.splitter)

        # Create a widget to hold the layout and set it as the central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connect textChanged signal to the markdown rendering function
        self.text_edit.textChanged.connect(self.render_markdown)
        self.text_edit.textChanged.connect(self.to_pickle)

        # Initialize view state and mode
        self.single_view1 = False
        self.single_view2 = False
        self.render_markdown()

    def to_pickle(self):
        try:
            with open(NOTE_FILE_NAME, "wb") as f:
                pickle.dump(self.text_edit.toPlainText(), f)
        except Exception as e:
            print(f"Error saving note to file: {e}")

    def render_markdown(self):
        # Get the current text from the text editor
        text = self.text_edit.toPlainText()

        # Convert the text to HTML using the markdown library with the "breaks" extension
        html = markdown.markdown(text, extensions=['extra'])

        # Set the HTML in the QWebEngineView widget
        self.web_view.setHtml(html)

    def toggle_view1(self):
        if self.single_view2:
            return
        if self.single_view1:
            self.text_edit.show()
            self.single_view1 = False
            self.toggle_view_button2.setEnabled(True)
        else:
            self.text_edit.hide()
            self.single_view1 = True
            self.toggle_view_button2.setEnabled(False)

    def toggle_view2(self):
        if self.single_view1:
            return
        if self.single_view2:
            self.web_view.show()
            self.single_view2 = False
            self.toggle_view_button1.setEnabled(True)
        else:
            self.web_view.hide()
            self.single_view2 = True
            self.toggle_view_button1.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MarkdownStickyNote()
    window.show()
    sys.exit(app.exec_())




