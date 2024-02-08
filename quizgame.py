from globals import *
from readArchive import ArchiveReader

class QuizGame():
    colnames = ['A','B','C','D','E']
    rownames = ['1','2','3','4','5']

    def __init__(self, archive:ArchiveReader):
        """
        Initialize game with default settings. Default is three rows and three columns, easy difficulty.
        """
        self.solved = False
        self.solved_cells = []
        self.n_columns = 3
        self.n_rows = 3
        self.difficulty = 1 # 1 = Easy, 2 = Medium, 3 = Hard
        self.archive = archive

    def set_n_columns(self, n:int):
        assert isinstance(n, int), "Number of columns must be integer!"
        assert 1 <= n <= 5, "Number of columns must be 1-5!"
        self.n_columns = n
    
    def set_n_rows(self, n:int):
        assert isinstance(n, int), "Number of rows must be integer!"
        assert 1 <= n <= 5, "Number of rows must be 1-5!"
        self.n_rows = n
    
    def set_difficulty(self, difficulty:int):
        assert isinstance(difficulty, int) and 1 <= difficulty <= 3, "Number of columns must be integer 1-3!"
        self.difficulty = difficulty
    
    def start_game(self):
        self.col_questions = []
        self.row_questions = []
        for n in range(self.n_columns):
            question = new_question(min([self.difficulty, n+1]), 1)
            self.col_questions.append(question)
        for n in range(self.n_rows):
            valid_question = False
            while not valid_question:
                question = new_question(min([self.difficulty, n+1]), 2)
                valid_question = True
                for col_question in self.col_questions:
                    if not question.validate_question(col_question, self.validation_list):
                        valid_question = False
                        break
            self.row_questions.append(question)

    def select_cell(self, cellname:str) -> tuple[int,int]:
        assert len(cellname) == 2, "Name of cell must be two characters!"
        col = self.colnames.index(cellname[0])
        row = self.rownames.index(cellname[1])
        return (col, row)

    def print_questions(self):
        for n in range(self.n_columns):
            question = self.col_questions[n].question
            print(self.colnames[n] + ": " + question[0] + ": " + str(question[1]))
        print("\n")
        for n in range(self.n_rows):
            question = self.row_questions[n].question
            print(self.rownames[n] + ": " + question[0] + ": " + str(question[1]))
    
    def print_cell_question(self, col:int, row:int) -> None:
        """"""
        col_question = self.col_questions[col].question
        row_question = self.row_questions[row].question
        printstr1 = col_question[0] + ": " + str(col_question[1])
        printstr2 = row_question[0] + ": " + str(row_question[1])
        print(printstr1 + " + " + printstr2)

    def answer_question(self, col:int, row:int, answer:MyDataClass) -> bool:
        """"""
        col_question = self.col_questions[col]
        row_question = self.row_questions[row]
        return col_question.check_question(answer) and row_question.check_question(answer)

    def user_turn(self):
        """"""
        self.print_questions()
        while True:
            selected_cell = self.get_user_input(1)
            if selected_cell == None: # Start over
                continue
            (selected_col, selected_row) = self.select_cell(selected_cell)
            self.print_cell_question(selected_col, selected_row)
            user_guess = self.get_user_input(2)
            if user_guess == None: # Start over
                continue
            assert isinstance(user_guess, MyDataClass), "Invalid guess class type!"
            if self.answer_question(selected_col, selected_row, user_guess):
                self.solved_cells.append(selected_cell)
                print("Correct!\n")
            else:
                print("Incorrect!\n")
            break




class DriverQuiz(QuizGame):

    def __init__(self, archive:ArchiveReader):
        super().__init__(archive)
        self.validation_list = self.archive.drivers

    def get_user_input(self, input_type:int):
        """
        Get user input depending on expected type.
        Parameters:
            input_type: int; Expected input type. See chart below:
                1: Grid coordinates.
                2: Driver name
        Outputs:
            user_input: ?; User's input. Must be valid answer depending on input type. None means cancel.
        """
        while True:
            if input_type == 1:
                input_string = "Please input the coordinates of the question you want to answer (e.g. B1). "
            elif input_type == 2:
                input_string = "Please input the name of the driver you want to guess (surname). "
            else:
                raise AssertionError("Invalid input_type value")
            input_string += "Type 'cancel' to cancel or 'quit' to exit program.\n"
            inp = input(input_string).strip().lower()
            if inp.lower() == "cancel":
                return None
            elif inp.lower() == "quit" or inp.lower() == 'q':
                exit()
            elif input_type == 1: # User should grid coordinates
                if len(inp) == 2 and inp[0].upper() in self.colnames[:self.n_columns] and inp[1] in self.rownames[:self.n_rows]:
                    if inp.upper() in self.solved_cells:
                        print(f"Cell {inp} has already been solved!")
                    else:
                        return inp.upper()
                else:
                    print("Invalid input. Please try again.")
            elif input_type == 2: # User should input driver name
                if inp in [remove_accents(driver_name).lower() for driver_name in self.archive.get_category("drivers", "fullname")]:
                    return find_single_object_by_field_value(self.archive.drivers, "fullname", inp, strict=False)
                elif inp in [remove_accents(driver_name).lower() for driver_name in self.archive.get_category("drivers", "surname")]:
                    try:
                        answer = find_single_object_by_field_value(self.archive.drivers, "surname", inp, strict=False)
                        return answer
                    except AssertionError:
                        print("Multiple possible drivers for given criteria. Use full name.")
                    except Exception as e:
                        raise e
                else:
                    print("Invalid input. Try again.")

class ConstructorQuiz(QuizGame):

    def __init__(self):
        pass

class RaceQuiz(QuizGame):

    def __init__(self):
        pass

def play_game(cols:int=3, rows:int=3, difficulty:int=1):
    new_quiz = DriverQuiz(ArchiveReader(archive_path=ARCHIVE_FILE))
    new_quiz.set_difficulty(1)
    new_quiz.start_game()
    guesses = 9
    
    while not (new_quiz.solved or guesses == 0):
        new_quiz.user_turn()
        guesses -= 1
    print(f"Game over! You answered {len(new_quiz.solved_cells)} questions correctly!")


if __name__ == "__main__":
    play_game()