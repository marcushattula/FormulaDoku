import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QCompleter, QLineEdit, QPushButton, QFileDialog, QGridLayout, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QDialogButtonBox, QDialog, QLabel, QComboBox
from PyQt6.QtGui import QPixmap, QColor, QPainter, QImage, QPen, QFont
from PyQt6 import QtCore

from globals import *
from quizgame import QuizGame, DriverQuiz
from readArchive import ArchiveReader

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
        self.quizwindow = DriverQuizWindow(self, 1, 3, 3)
        self.quizwindow.show()


class QuizWindow(QMainWindow):

    def __init__(self, parent:MainWindow, ):
        super().__init__()
        self.parent = parent

        self.setFixedHeight(GUI_SCALE*200)
        self.setFixedWidth(GUI_SCALE*250)
        self.quiz:QuizGame = None

    def init2(self, difficulty:int, n_columns:int, n_rows:int):
        widget = QWidget()
        self.layout = QVBoxLayout()

        assert hasattr(self, "quiz") and isinstance(self.quiz, QuizGame), "Missing quiz field!"
        self.quiz.set_difficulty(difficulty)
        self.quiz.set_n_rows(n_rows)
        self.quiz.set_n_columns(n_columns)
        self.quiz.start_game()

        self.gridwidget = self.render_grid()
        self.layout.addWidget(self.gridwidget)
        
        self.bottomrow = self.bottom_row()
        self.layout.addWidget(self.bottomrow)

        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def info_widget(self) -> QWidget:
        info_widget = QWidget()
        info_layout = QVBoxLayout()

        lives_text = QLabel(f"Guesses remaining: {self.quiz.guesses}")
        info_layout.addWidget(lives_text)

        return info_widget

    def render_grid(self) -> QWidget:
        
        grid = QWidget()
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)
        for row in range(self.quiz.n_columns+1):
            for col in range(self.quiz.n_rows+1):
                if row == 0 and col == 0:
                    grid_widget = QLabel("FormulaDoku!")
                elif row == 0:
                    grid_widget = QLabel(f"{self.quiz.colnames[col-1]}: {str(self.quiz.col_questions[col-1])}")
                elif col == 0:
                    grid_widget = QLabel(f"{self.quiz.rownames[row-1]}: {str(self.quiz.row_questions[row-1])}")
                else:
                    grid_widget = QPushButton()
                    grid_widget.setFixedSize(50*GUI_SCALE, 50*GUI_SCALE)
                    grid_widget.clicked.connect(lambda _, c=col, r=row: self.box_clicked(c-1, r-1))
                    grid_widget.setStyleSheet('background-color : rgba(0, 0, 0, 100); border :1px solid rgba(0, 0, 0, 150)')
                    if (col-1, row-1) in self.quiz.solved_cells:
                        grid_widget.setStyleSheet("background-color: green")
                        grid_widget.setEnabled(False)
                        grid_widget.setText(str(self.quiz.given_answers[(col-1, row-1)]))
                    if (col-1, row-1) not in self.quiz.solved_cells and self.quiz.guesses == 0:
                        grid_widget.setStyleSheet("background-color: red")
                        grid_widget.setEnabled(False)
                grid_layout.addWidget(grid_widget, row, col)
        grid.setLayout(grid_layout)
        return grid

    def update_grid(self):
        self.layout.removeWidget(self.gridwidget)
        self.layout.removeWidget(self.bottomrow)
        self.gridwidget = self.render_grid()
        self.layout.addWidget(self.gridwidget, 0)
        self.layout.addWidget(self.bottomrow)

    def box_clicked(self, column:int, row:int):
        print(f"{column}, {row}")
        self.search_window = SearchBox(self, [x.fullname for x in self.quiz.validation_list], column, row)
        self.search_window.show()

    def answer_given(self, given_answer:str, column:int, row:int):
        dataclass:MyDataClass = self.quiz.string_to_dataclass(remove_accents(given_answer))
        if dataclass != None:
            self.quiz.answer_question(column, row, dataclass)
            self.update_grid()

    def bottom_row(self) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout()

        give_up_button = QPushButton("Give up")
        give_up_button.clicked.connect(self.give_up_button_clicked)
        layout.addWidget(give_up_button)

        exit_button = new_exit_button()
        layout.addWidget(exit_button)

        widget.setLayout(layout)
        return widget
    
    def give_up_button_clicked(self):
        self.quiz.forfeit = True
        

class DriverQuizWindow(QuizWindow):

    def __init__(self, parent:MainWindow, difficulty:int, n_columns:int, n_rows:int):
        super().__init__(parent)
        self.quiz = DriverQuiz(ArchiveReader(archive_path=ARCHIVE_FILE))
        self.init2(difficulty, n_columns, n_rows)


class SearchBox(QMainWindow):

    def __init__(self, parent, possible_answers_list, col:int, row:int):
        super().__init__()
        self.parent = parent
        self.col = col
        self.row = row
        widget = QWidget()
        layout = QVBoxLayout()
        
        label_text = self.parent.quiz.print_cell_question(col, row)
        label_widget = QLabel(label_text)
        layout.addWidget(label_widget)

        self.linewidget = QLineEdit()
        self.linewidget.returnPressed.connect(self.name_driver)
        completer = QCompleter(possible_answers_list)
        
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        self.linewidget.setCompleter(completer)

        layout.addWidget(self.linewidget)

        layout.addWidget(self.bottom_row())

        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def bottom_row(self):
        widget = QWidget()
        layout = QHBoxLayout()

        exit_button = QPushButton("Close")
        exit_button.clicked.connect(self.exit_window)
        layout.addWidget(exit_button)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.name_driver)
        layout.addWidget(submit_button)

        widget.setLayout(layout)
        return widget
    
    def name_driver(self):
        self.parent.answer_given(self.linewidget.text().lower(), self.col, self.row)
        self.exit_window()
    
    def exit_window(self):
        self.parent.search_window = None




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