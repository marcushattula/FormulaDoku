import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QCompleter, QLineEdit, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QScrollArea, QDialog, QDialogButtonBox
from PyQt6 import QtCore, QtGui

from quizgame import *

GUI_SCALE = 3

class MainWindow(QMainWindow):
    """
    Main window that opens when running the program.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle(PROJECT_NAME)

        self.archive = ArchiveReader(archive_path=ARCHIVE_FILE)

        widget = QWidget()
        layout = QVBoxLayout()

        self.quiztype_box = QComboBox()
        self.quiztype_box.addItem("Driver Quiz")
        layout.addWidget(self.quiztype_box)

        self.difficulty_box = QComboBox()
        self.difficulty_box.addItems(["Easy","Medium","Hard"])
        self.difficulty_box.setCurrentIndex(2)
        layout.addWidget(self.difficulty_box)

        self.rows_box = QComboBox()
        self.rows_box.addItems("1,2,3,4,5".split(","))
        self.rows_box.setCurrentIndex(2)
        self.rows_box
        layout.addWidget(self.rows_box)

        self.columns_box = QComboBox()
        self.columns_box.addItems("1,2,3,4,5".split(","))
        self.columns_box.setCurrentIndex(2)
        layout.addWidget(self.columns_box)

        start_button = QPushButton("Start")
        start_button.clicked.connect(self.start_game)
        layout.addWidget(start_button)

        custom_game_button = QPushButton("Custom Game")
        custom_game_button.clicked.connect(self.custom_game)
        layout.addWidget(custom_game_button)

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
        difficulty = int(self.difficulty_box.currentIndex()) + 1
        n_cols = int(self.columns_box.currentText())
        n_rows = int(self.rows_box.currentText())
        constructor = QuizConstructor(self.archive, n_cols, n_rows, difficulty)
        constructor.set_quiztype(int(self.quiztype_box.currentIndex()))
        constructor.create_quiz()
        quiz = constructor.start_quiz()
        self.quizwindow = QuizWindow(self, quiz)
        self.quizwindow.show()
    
    def custom_game(self):
        """
        
        """
        difficulty = int(self.difficulty_box.currentIndex()) + 1
        n_cols = int(self.columns_box.currentText())
        n_rows = int(self.rows_box.currentText())
        constructor = QuizConstructor(self.archive, n_cols, n_rows, difficulty)
        constructor.set_quiztype(int(self.quiztype_box.currentIndex()))
        constructor.create_quiz()
        self.constructorwindow = CreatorWindow(self, constructor)
        self.constructorwindow.show()


class CreatorWindow(QMainWindow):

    def __init__(self, parent:MainWindow, constructor:QuizConstructor):
        super().__init__(parent)
        self.parent = parent
        self.constructor = constructor

        widget = QWidget()
        layout = QVBoxLayout()

        self.grid_widget = self.render_grid()
        layout.addWidget(self.grid_widget)

        self.bottomrow = self.bottom_row()
        layout.addWidget(self.bottomrow)

        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def bottom_row(self) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout()

        give_up_button = QPushButton("Start")
        give_up_button.clicked.connect(self.start_button_clicked)
        layout.addWidget(give_up_button)

        close_button = QPushButton("Cancel")
        close_button.clicked.connect(self.exit_window)
        layout.addWidget(close_button)

        exit_button = new_exit_button()
        layout.addWidget(exit_button)

        widget.setLayout(layout)
        return widget
    
    def start_button_clicked(self):

        def reverse_displaytext(q):
            if isinstance(q, Question):
                return q.question_id
            elif q == None or q == -1:
                return q
            raise ValueError(f"Unsupported value for reverse displaytext(): {q}")
        col_q_ids = [reverse_displaytext(self.question_options[col_q_box.currentIndex()]) for col_q_box in self.col_question_boxes]
        row_q_ids = [reverse_displaytext(self.question_options[row_q_box.currentIndex()]) for row_q_box in self.row_question_boxes]
        self.constructor.set_col_question_id(col_q_ids)
        self.constructor.set_row_question_id(row_q_ids)
        try:
            quiz = self.constructor.start_quiz()
        except RecursionError:
            # Quiz could not be verified => prompt to force start
            if show_confirm_window("Unsolveable quiz!", "You are about to create an unsolveable quiz.\nAre you sure you want to continue?"):
                quiz = self.constructor.start_quiz(force=True)
        except Exception as e:
            raise e
        self.parent.quizwindow = QuizWindow(self.parent, quiz)
        self.parent.quizwindow.show()
        self.exit_window()

    def exit_window(self):
        self.parent.constructorwindow = None
        self.close()

    def render_grid(self) -> QWidget:
        """
        
        """

        class CustomComboBox(QComboBox):
            def __init__(self):
                super().__init__()
                self.setFixedWidth(50*GUI_SCALE)

            def calculate_max_width(self):
                font_metrics = QtGui.QFontMetrics(self.font())
                max_width = round(max([font_metrics.horizontalAdvance(item) for item in self.items()])*1.2)
                return max_width

            def items(self):
                return [self.itemText(i) for i in range(self.count())]

            def showPopup(self):
                self.view().setMinimumWidth(self.calculate_max_width())
                super().showPopup()



        def displaytext(q) -> str:
            """
            Create text to display in combobox from Question or -1 or None
            """
            if isinstance(q, Question) and q.question_id >= 0:
                return str(q)
            elif q == -1:
                return "Default Question"
            elif q == None:
                return "Random Question"
            raise ValueError(f"Unsupported question: {q}!")
        
        self.col_question_boxes:list[CustomComboBox] = []
        self.row_question_boxes:list[CustomComboBox] = []
        grid = QWidget()
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)
        self.question_options = [-1, None]
        self.question_options.extend(self.constructor.all_questions)
        for row in range(self.constructor.n_rows+1):
            for col in range(self.constructor.n_cols+1):
                if row == 0 and col == 0:
                    grid_widget = QLabel("FormulaDoku!")
                elif row == 0 or col == 0:
                    grid_widget = CustomComboBox()
                    grid_widget.addItems([displaytext(x) for x in self.question_options])
                    if row == 0:
                        self.col_question_boxes.append(grid_widget)
                    elif col == 0:
                        self.row_question_boxes.append(grid_widget)
                else:
                    grid_widget = QPushButton()
                    grid_widget.setFixedSize(50*GUI_SCALE, 50*GUI_SCALE)
                    grid_widget.setStyleSheet('background-color : rgba(0, 0, 0, 100); border :1px solid rgba(0, 0, 0, 150)')
                    grid_widget.setEnabled(False)
                grid_layout.addWidget(grid_widget, row, col)
        grid.setLayout(grid_layout)
        return grid


class QuizWindow(QMainWindow):

    def __init__(self, parent:MainWindow, quiz:QuizGame):
        super().__init__()
        self.parent = parent
        self.quiz=quiz

        widget = QWidget()
        self.layout = QVBoxLayout()

        assert hasattr(self, "quiz") and isinstance(self.quiz, QuizGame), "Missing quiz field!"

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
        for row in range(self.quiz.n_rows+1):
            for col in range(self.quiz.n_columns+1):
                if row == 0 and col == 0:
                    grid_widget = QLabel("FormulaDoku!")
                elif row == 0:
                    grid_widget = QLabel(f"{self.quiz.colnames[col-1]}:\n{self.quiz.col_questions[col-1].quiz_format_str()}")
                elif col == 0:
                    grid_widget = QLabel(f"{self.quiz.rownames[row-1]}:\n{self.quiz.row_questions[row-1].quiz_format_str()}")
                else:
                    grid_widget = QPushButton()
                    grid_widget.setFixedSize(50*GUI_SCALE, 50*GUI_SCALE)
                    grid_widget.setStyleSheet('background-color : rgba(0, 0, 0, 100); border :1px solid rgba(0, 0, 0, 150)')
                    if (col-1, row-1) in self.quiz.solved_cells: # Cell has been solved => box is green, add given answer and diable
                        grid_widget.setStyleSheet("background-color: green")
                        grid_widget.setEnabled(False)
                        grid_widget.setText(str(self.quiz.given_answers[(col-1, row-1)]))
                    if self.quiz.game_ended():
                        if (col-1, row-1) not in self.quiz.solved_cells:
                            grid_widget.setStyleSheet("background-color: red")
                        grid_widget.setEnabled(True)
                        grid_widget.clicked.connect(lambda _, c=col, r=row: self.answer_box_clicked(c-1, r-1))
                    else:
                        grid_widget.clicked.connect(lambda _, c=col, r=row: self.box_clicked(c-1, r-1))
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
        self.search_window = SearchBox(self, [x.fullname for x in self.quiz.validation_list], column, row)
        self.search_window.show()

    def answer_box_clicked(self, column:int, row:int):
        if (column, row) in self.quiz.given_answers:
            given_answer = self.quiz.given_answers[(column, row)]
        else:
            given_answer = None
        self.answer_window = AnswerBox(self, given_answer, column, row)
        self.answer_window.show()

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

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.exit_window)
        layout.addWidget(cancel_button)

        exit_button = new_exit_button()
        layout.addWidget(exit_button)

        widget.setLayout(layout)
        return widget
    
    def give_up_button_clicked(self):
        self.quiz.forfeit = True
        self.update_grid()

    def exit_window(self):
        self.parent.quizwindow = None
        self.close()


class SearchBox(QMainWindow):

    def __init__(self, parent, possible_answers_list, col:int, row:int):
        super().__init__()
        self.parent = parent
        self.col = col
        self.row = row
        widget = QWidget()
        self.layout = QVBoxLayout()
        
        label_text = self.parent.quiz.print_cell_question(col, row)
        label_widget = QLabel(label_text)
        self.layout.addWidget(label_widget)

        self.linewidget = QLineEdit()
        self.linewidget.returnPressed.connect(self.name_driver)
        completer = QCompleter(possible_answers_list)
        
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        self.linewidget.setCompleter(completer)

        self.layout.addWidget(self.linewidget)

        self.layout.addWidget(self.bottom_row())

        widget.setLayout(self.layout)
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
        text_input = self.linewidget.text().lower()
        dataclass:MyDataClass = self.parent.quiz.string_to_dataclass(remove_accents(text_input))
        if dataclass != None and dataclass not in self.parent.quiz.given_answers.values():
            self.parent.answer_given(text_input, self.col, self.row)
            self.exit_window()
        else:
            if hasattr(self, "label"):
                self.layout.removeWidget(self.label)
            if dataclass == None:
                self.label = QLabel(f"Unknown input: {str(text_input)}")
            elif dataclass in self.parent.quiz.given_answers.values():
                self.label = QLabel(f"{str(dataclass)} has already been used as an answer!")
            self.layout.addWidget(self.label)       
    
    def exit_window(self):
        self.parent.search_window = None


class AnswerBox(QMainWindow):

    def __init__(self, parent:QuizWindow, given_answer, column, row):
        super().__init__()
        layout = QVBoxLayout()
        widget = QWidget()
        self.parent = parent
        
        scrollwidget = self.scrollwidget(column, row, given_answer)
        layout.addWidget(scrollwidget)

        bottom_row = self.bottom_row()
        layout.addWidget(bottom_row)

        widget.setLayout(layout)

        self.setCentralWidget(widget)
    
    def scrollwidget(self, column:int, row:int, given_answer) -> QScrollArea:
        scroll = QScrollArea()
        layout = QGridLayout()
        widget = QWidget()

        col_question = self.parent.quiz.col_questions[column]
        row_question = self.parent.quiz.row_questions[row]

        i = 0
        self.top_row(col_question, row_question, layout, i)
        for obj in col_question.get_mutual_answers(row_question, self.parent.quiz.validation_list):
            i += 1
            self.obj_line(obj, col_question, row_question, layout, i)
        
        widget.setLayout(layout)

        # scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        # scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # scroll.setWidgetResizable(True)
        scroll.setWidget(widget)

        return scroll

    def top_row(self, question1:Question, question2:Question, layout:QGridLayout, layout_row:int) -> QWidget:
        label1 = QLabel("Valid answer")
        label2 = QLabel(str(question1.base))
        label3 = QLabel(str(question2.base))

        layout.addWidget(label1, layout_row, 0)
        layout.addWidget(label2, layout_row, 1)
        if not question1.base == question2.base:
            layout.addWidget(label3, layout_row, 2)

    def obj_line(self, object:MyDataClass, question1:Question, question2:Question, layout:QGridLayout, layout_row:int) -> QWidget:
        label1 = QLabel(str(object))
        label2 = QLabel(str(object.map_to_string(question1.bonus_fields)))
        label3 = QLabel(str(object.map_to_string(question2.bonus_fields)))

        layout.addWidget(label1, layout_row, 0)
        layout.addWidget(label2, layout_row, 1)
        if not question1.base == question2.base:
            layout.addWidget(label3, layout_row, 2)
  
    def bottom_row(self):
        widget = QWidget()
        layout = QHBoxLayout()

        exit_button = QPushButton("Close")
        exit_button.clicked.connect(self.exit_window)

        layout.addWidget(exit_button)
        widget.setLayout(layout)
        return widget

    def exit_window(self):
        self.parent.answer_window = None


class ConfirmDialog(QDialog):
    """
    Single window which asks user to confirm their selection. Call this object through show_confirm_window() method.
    """

    def __init__(self, title:str, text:str):
        super().__init__()

        self.setWindowTitle(title)

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(text)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


def show_confirm_window(title:str, text:str) -> bool:
    """
    Show a window which prompts user to confirm their selection.
    Parameters:
        title: str; String for the window title
        text: str; String for the window text
    Outputs:
        Opens ConfirmDialog window with buttons yes and no.
        Returns True if user presses yes button, else False
    """
    confirm_window = ConfirmDialog(title, text)
    return confirm_window.exec()

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