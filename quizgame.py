from globals import *
from readArchive import ArchiveReader

class QuizGame():
    """
    Classs for storing status of the game.
    """
    colnames = ['A','B','C','D','E'] # Columns are labeled letters A-E
    rownames = ['1','2','3','4','5'] # Rows are labeled numbers 1-5

    def __init__(self, archive:ArchiveReader):
        """
        Initialize game with default settings. Default is three rows and three columns, easy difficulty.
        """
        self.solved = False # Flag for if game is solved, i.e. all cells have been answered
        self.solved_cells = [] # List of solved cells
        self.n_columns = 3 # Number of columns
        self.n_rows = 3 # Number of rows
        self.difficulty = 1 # 1 = Easy, 2 = Medium, 3 = Hard
        self.archive = archive # ArchiveReader class, containing result data

    def set_n_columns(self, n:int) -> None:
        """
        Set number of columns, minimum of 1, maximum of 5
        Parameters:
            n: int; number of columns in this quiz.
        Outputs:
            Sets self.n_columns to n.
            Returns None
        """
        assert isinstance(n, int), "Number of columns must be integer!"
        assert 1 <= n <= 5, "Number of columns must be 1-5!"
        self.n_columns = n
    
    def set_n_rows(self, n:int) -> None:
        """
        Set number of rows, minimum of 1, maximum of 5
        Parameters:
            n: int; number of rows in this quiz.
        Outputs:
            Sets self.n_rows to n.
            Returns None
        """
        assert isinstance(n, int), "Number of rows must be integer!"
        assert 1 <= n <= 5, "Number of rows must be 1-5!"
        self.n_rows = n
    
    def set_difficulty(self, difficulty:int) -> None:
        """
        Sets the difficulty of the game.
        Parameters:
            difficulty: int; difficulty of quiz. 1 = Easy, 2 = Medium, 3 = Hard
        Outputs:
            Sets self.difficulty to given number
            Returns None
        """
        assert isinstance(difficulty, int) and 1 <= difficulty <= 3, "Number of columns must be integer 1-3!"
        self.difficulty = difficulty
    
    def start_game(self) -> None:
        """
        Starts the game with set settings. Generates questions.
        Parameters:
            None
        Outputs:
            Adds questions to self.col_questions and self.row_questions
            Returns None
        """
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
        """
        Return the coordinates of a cell based on its name.
        Parameters:
            cellname: str; name of cell, e.g. C2
        Outputs:
            t: tuple[int, int]; tuple of cell coordinates, [column_id, row_id]
        """
        assert len(cellname) == 2, "Name of cell must be two characters!"
        col = self.colnames.index(cellname[0])
        row = self.rownames.index(cellname[1])
        return (col, row)

    def print_questions(self) -> None:
        """
        Print all the columns and rows along with corresponding questions.
        Parameters:
            None
        Outputs:
            Questions are printed to terminal
            Returns None
        """
        for n in range(self.n_columns):
            print(self.colnames[n] + ": " + str(self.col_questions[n]))
        print("\n")
        for n in range(self.n_rows):
            print(self.rownames[n] + ": " + str(self.row_questions[n]))
    
    def print_cell_question(self, col:int, row:int) -> None:
        """
        Print the question of a single cell, that is it's column and row questions
        Parameters:
            col: int; cell column id
            row: int; cell row id
        Output:
            Prints column and row quetion to terminal
            Returns None
        """
        col_question = self.col_questions[col]
        row_question = self.row_questions[row]
        print(str(col_question) + " + " + str(row_question))

    def answer_question(self, col:int, row:int, answer:MyDataClass) -> bool:
        """
        Check if given object is a correct answer for question. Answer must satisfy both column and row questions.
        Parameters:
            col: int; column id
            row: int; row id
            answer: MyDataClass; given answer.
        Outputs:
            b: bool; True if both questions are satisfied by answer, else False
        """
        col_question = self.col_questions[col]
        row_question = self.row_questions[row]
        return col_question.check_question(answer) and row_question.check_question(answer)

    def user_turn(self) -> None:
        """
        It is the user's turn. Print the questions and prompt user for cell and answer.
        Parameters:
            None
        Outputs:
            Questions are printed and answered in terminal.
            If user answers question correctly, add it to self.solved_cells
            Returns None
        """
        self.print_questions()
        while True:
            # Get user input. May be cell or cell and answer.
            user_input1 = self.get_user_input(1)
            if user_input1 == None: # User gave invalid answer -> Start over
                continue
            elif len(user_input1) == 2 and isinstance(user_input1, str): # User gave cell name -> prompt for answer
                selected_cell = user_input1
                (selected_col, selected_row) = self.select_cell(user_input1)
                self.print_cell_question(selected_col, selected_row)
                user_guess = self.get_user_input(2)
                if user_guess == None: # Start over
                    continue
            elif isinstance(user_input1, tuple): # User gave cell and answer -> continue to check answer
                (selected_cell, user_guess) = user_input1
                (selected_col, selected_row) = self.select_cell(selected_cell)
            else:
                raise Exception("Error in receiving answer.")
            assert isinstance(user_guess, MyDataClass), "Invalid guess class type!"
            if self.answer_question(selected_col, selected_row, user_guess):
                self.solved_cells.append(selected_cell)
                print("Correct!\n")
            else:
                print("Incorrect!\n")
            break


class DriverQuiz(QuizGame):
    """
    Quizgame where the player must answer different drivers.
    """

    def __init__(self, archive:ArchiveReader):
        super().__init__(archive) # Init parent class
        self.validation_list = self.archive.drivers # Use drivers when validating answers.

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

        def driver_answer(inp:str) -> MyDataClass:
            if inp in [remove_accents(driver_name).lower() for driver_name in self.archive.get_category("drivers", "fullname")]:
                return find_single_object_by_field_value(self.archive.drivers, "fullname", inp, strict=False)
            elif inp in [remove_accents(driver_name).lower() for driver_name in self.archive.get_category("drivers", "surname")]:
                try:
                    answer = find_single_object_by_field_value(self.archive.drivers, "surname", inp, strict=False)
                    return answer
                except AssertionError:
                    print("Multiple possible drivers for given criteria. Use full name.")
                    return None
                except Exception as e:
                    raise e
            else:
                print("Invalid input. Try again.")
                return None

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
            elif input_type == 1: # User should input grid coordinates
                if len(inp) == 2 and inp[0].upper() in self.colnames[:self.n_columns] and inp[1] in self.rownames[:self.n_rows]:
                    if inp.upper() in self.solved_cells:
                        print(f"Cell {inp} has already been solved!")
                    else:
                        return inp.upper()
                elif inp[0].upper() in self.colnames[:self.n_columns] and inp[1] in self.rownames[:self.n_rows] and " " in inp:
                    # User input both cell and answer simultaneously
                    inps = inp.split(" ", 1)
                    assert len(inps) == 2, "Invalid input, try again."
                    selected_cell = inps[0]
                    answer = driver_answer(inps[1])
                    if isinstance(answer, Driver):
                        return (selected_cell.upper(), answer)
                else:
                    print("Invalid input. Please try again.")
            elif input_type == 2: # User should input driver name
                answer = driver_answer(inp)
                if isinstance(answer, Driver):
                    return answer
                


class ConstructorQuiz(QuizGame):
    """
    Quizgame where the player must answer different constructors (NOT IMPLEMENTED).
    """

    def __init__(self):
        pass


class RaceQuiz(QuizGame):
    """
    Quizgame where the player must answer different races (NOT IMPLEMENTED).
    """

    def __init__(self):
        pass


def play_game(cols:int=3, rows:int=3, difficulty:int=1):
    """
    Play driver quiz. This method is used for debugging.
    """
    new_quiz = DriverQuiz(ArchiveReader(archive_path=ARCHIVE_FILE))
    new_quiz.set_n_columns(cols)
    new_quiz.set_n_rows(rows)
    new_quiz.set_difficulty(difficulty)
    new_quiz.start_game()
    guesses = 9
    
    while not (new_quiz.solved or guesses == 0):
        new_quiz.user_turn()
        guesses -= 1
    print(f"Game over! You answered {len(new_quiz.solved_cells)} questions correctly!")


if __name__ == "__main__":
    play_game()