import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QDialogButtonBox, QDialog, QLabel, QComboBox
from PyQt6.QtGui import QPixmap, QColor
from PyQt6 import QtCore

from globals import *

GUI_SCALE = 3

class MainWindow(QMainWindow):
    """
    Main window that opens when running the program.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle(PROJECT_NAME)
        self.setFixedHeight(GUI_SCALE*200)
        self.setFixedWidth(GUI_SCALE*200)

        widget = QWidget()
        layout = QVBoxLayout()

        self.quiztype_box = QComboBox()
        self.quiztype_box.addItem("Driver Quiz")
        layout.addWidget(self.quiztype_box)

        self.difficulty_box = QComboBox()
        self.difficulty_box.addItems(["Easy","Medium","Hard"])
        layout.addWidget(self.difficulty_box)

        self.rows_box = QComboBox()
        self.rows_box.addItems("1,2,3,4,5".split(","))
        self.rows_box.setCurrentIndex(2)
        layout.addWidget(self.rows_box)

        self.columns_box = QComboBox()
        self.columns_box.addItems("1,2,3,4,5".split(","))
        self.columns_box.setCurrentIndex(2)
        layout.addWidget(self.columns_box)

        start_button = QPushButton("Start")
        start_button.clicked.connect(self.start_game)
        layout.addWidget(start_button)

        exit_button = new_exit_button()
        layout.addWidget(exit_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def start_game(self):
        """
        Start button clicked -> Init new quiz with settings from main form.
        Parameters:
            None
            Accesses settings in main form
        Outputs:
            Opens a new window with quiz
        """
        pass

class QuizWindow(QMainWindow):

    def __init__(self, parent:MainWindow):
        super().__init__()
        self.parent = parent


def new_exit_button() -> QPushButton:
    """
    Create an exit button and connect it to the exit method
    Parameters:
        None
    Outputs:
        exit_button: QPushButton; button that runs the exit command when clicked
    """
    exit_button = QPushButton("Exit")
    exit_button.clicked.connect(exit_button_clicked)
    return exit_button

def exit_button_clicked():
    """
    When an exit button is clicked, runs this method. Exits program.
    Parameters:
        None
    Outputs:
        Exits program
    """
    exit()
    

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())