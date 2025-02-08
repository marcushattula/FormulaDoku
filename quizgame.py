import random

from readArchive import ArchiveReader
from mydataclass import MyDataClass, find_single_object_by_field_value
from driver import Driver
from globals import *
from question import Question, new_question

class QuizGame():
    """
    Classs for storing status of the game.
    """
    colnames = ['A','B','C','D','E'] # Columns are labeled letters A-E
    rownames = ['1','2','3','4','5'] # Rows are labeled numbers 1-5

    def __init__(self, archive:ArchiveReader, setseed=None):
        """
        Initialize game with default settings. Default is three rows and three columns, easy difficulty.
        """
        self.validation_list: list[MyDataClass] = [] # List of objects to validate against, overridden during inheritance.
        self.solved_cells = [] # List of solved cells, tuple (col, row)
        self.given_answers = {} # List of given correct answers, same answer cannot be used multiple times
        self.n_columns = 3 # Number of columns
        self.n_rows = 3 # Number of rows
        self.difficulty = 1 # 1 = Easy, 2 = Medium, 3 = Hard
        self.forfeit = False # Flag if player has forfeited game
        self.archive = archive # ArchiveReader class, containing result data
        self.guesses = self.n_columns * self.n_rows # Number of guesses
        self.col_questions: list[Question] = [] # List of column questions
        self.row_questions: list[Question] = [] # List of row questions
        self.possible_answers = {} # List of possible answers to this quiz
        self.seed = setseed # Seed for generating "random" quiz questions

    def solved(self) -> bool:
        """
        Check if game is solved (=> number of solved cells == number of cells in quiz)
        Parameters:
            None
        Outputs:
            b: bool; True if game is solved, else False
        """
        return len(self.solved_cells) == self.n_columns*self.n_rows

    def game_ended(self) -> bool:
        """
        Check if game has ended (no lives or all cells solved or forfeited)
        Parameters:
            None
        Outputs:
            b: bool; True if game has ended, else false
        """
        return self.guesses == 0 or self.forfeit or self.solved()

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
    
    def set_guesses(self, guesses:int) -> None:
        """
        Set the number of guesses available during the game. Default = 9
        Parameters:
            guesses: int; how many guesses the user has
        Outputs:
            Sets self.guesses to given number
            Returns None
        """
        assert isinstance(guesses, int) and guesses > 0, "Number of guesses must be positive integer."
        self.guesses = guesses

    def set_col_question(self, question:Question) -> None:
        """
        Add a question to col questions
        Parameters:
            question: Question; question to be added
        Outputs:
            None
            Adds the question to self.col_questions
        """
        assert isinstance(question, Question), f"Added question must be Question object"
        self.col_questions.append(question)

    def set_row_question(self, question:Question) -> None:
        """
        Add a question to row questions
        Parameters:
            question: Question; question to be added
        Outputs:
            None
            Adds the question to self.row_questions
        """
        assert isinstance(question, Question), f"Added question must be Question object"
        self.row_questions.append(question)

    def start_game(self) -> None:
        """
        Starts the game with set settings. Generates questions.
        Parameters:
            None
        Outputs:
            Adds questions to self.col_questions and self.row_questions
            Returns None
        """
        reset = False
        self.guesses = self.n_columns * self.n_rows
        while len(self.col_questions) < self.n_columns:
            n_col = len(self.col_questions)
            question = new_question(min([self.difficulty, self.n_columns-n_col]), setseed=self.seed)
            self.seed = random.random()
            if question not in self.col_questions:
                self.set_col_question(question)
        while len(self.row_questions) < self.n_rows:
            i = 0
            n_row = len(self.row_questions)
            valid_question = False
            while not valid_question:
                question = new_question(min([self.difficulty, self.n_rows-n_row]), setseed=self.seed)
                self.seed = random.random()
                valid_question = True
                for col_question in self.col_questions:
                    if not question.validate_question(col_question, self.validation_list):
                        valid_question = False
                        i += 1
                        break
            if i > self.n_columns*10:
                reset = True
                break
            if question not in self.row_questions and question not in self.col_questions:
                self.set_row_question(question)
        if reset or not self.full_validation():
            self.col_questions = []
            self.row_questions = []
            self.start_game()

    def full_validation(self) -> bool:
        """
        Full validation of questions.
        Parameters:
            None
        Outputs:
            all_unique: bool; True if every question can have at least one unique answer, else False
        """
        def get_list_of_answers_list() -> list[list[MyDataClass]]:
            """
            Get answers for each quiz box as separate lists
            Parameters:
                None
            Outputs:
                answers: list[list[MyDataClass]]; list of list of answers to each question pair
            """
            x = []
            for i in range(len(self.col_questions)):
                col_question = self.col_questions[i]
                for j in range(len(self.row_questions)):
                    row_question = self.row_questions[j]
                    valid_answers = col_question.get_mutual_answers(row_question, self.validation_list)
                    x.append(valid_answers)
            return x
       
        def set_possible_answers(possible_answers: list[MyDataClass]) -> None:
            """
            Takes list of correct answers and stores it to dictionary for each question
            Parameters:
                possible_answers: list[MyDataClass]; validated llist of answers
            Outputs:
                None
                Stores the dictionary to self.possible_answers
            """
            for i in range(self.n_columns):
                for j in range(self.n_rows):
                    index = i*self.n_rows+j
                    if index < len(possible_answers):
                        self.possible_answers[(i, j)] = possible_answers[index]

        def constraints_search(ans_list: list[list[MyDataClass]], used_answers=[]) -> bool:
            """
            Recursively check that there is a unused answer for each question
            Parameters:
                ans_list: list[list[MyDataClass]]; list of list of answers to each question
            Outputs:
                b: bool; True if each question has a unique answer, else False
                Stores a found solution to self.possible_answers, if found
            """
            if len(ans_list) == 0:
                set_possible_answers(used_answers)
                return True
            for answer in ans_list[0]:
                if answer not in used_answers:
                    temp_arr = used_answers.copy()
                    temp_arr.append(answer)
                    if constraints_search(ans_list[1:], used_answers=temp_arr):
                        return True
            return False
        
        all_answers = get_list_of_answers_list()
        sorted_answers = all_answers#sorted(all_answers, key=len)
        return constraints_search(sorted_answers)
    
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
            if n < len(self.col_questions):
                question_str = str(self.col_questions[n])
            else:
                question_str = "BLANK QUESTION"
            print(self.colnames[n] + ": " + question_str)
        print("\n", end="")
        for n in range(self.n_rows):
            if n < len(self.row_questions):
                question_str = str(self.row_questions[n])
            else:
                question_str = "BLANK QUESTION"
            print(self.rownames[n] + ": " + question_str)
    
    def print_cell_question(self, col:int, row:int) -> str:
        """
        Get the question of a single cell, that is it's column and row questions
        Parameters:
            col: int; cell column id
            row: int; cell row id
        Output:
            Reutrns column and row quetion as string
        """
        col_question = self.col_questions[col]
        row_question = self.row_questions[row]
        return str(col_question) + " + " + str(row_question)

    def check_cell_pair_answer(self, col:int, row:int, answer:MyDataClass) -> bool:
        """
        Check if given object is a correct answer for question. Answer must satisfy both column and row questions.
        Parameters:
            col: int; column id
            row: int; row id
            answer: MyDataClass; given answer
        Outputs:
            b: bool; True if answer satisfies both questions, else False
        """
        col_question = self.col_questions[col]
        row_question = self.row_questions[row]
        return col_question.check_question(answer) and row_question.check_question(answer)

    def answer_question(self, col:int, row:int, answer:MyDataClass) -> bool:
        """
        User gives an answer. Check if correct, and process game
        Parameters:
            col: int; column id
            row: int; row id
            answer: MyDataClass; given answer.
        Outputs:
            b: bool; True if both questions are satisfied by answer, else False
        """
        assert answer not in self.given_answers.values(), f"{str(answer)} has already been given as an answer!"
        assert self.guesses > 0, "No guesses remaining!"
        self.guesses -= 1
        if self.check_cell_pair_answer(col, row, answer):
            self.solved_cells.append((col, row))
            self.given_answers[(col, row)] = answer
            return True
        else:
            return False

    def user_turn(self) -> None:
        """
        It is the user's turn. Print the questions and prompt user for cell and answer.
        Parameters:
            None
        Outputs:
            Questions are printed and answered in terminal.
            Increments guesses by -1 with every guess
            Returns None
        """
        self.print_questions()
        while not self.game_ended():
            # Get user input. May be cell or cell and answer.
            user_input1 = self.get_user_input(1)
            if user_input1 == None: # User gave invalid answer -> Start over
                continue
            elif len(user_input1) == 2 and isinstance(user_input1, str): # User gave cell name -> prompt for answer
                selected_cell = user_input1
                (selected_col, selected_row) = self.select_cell(user_input1)
                print(self.print_cell_question(selected_col, selected_row))
                user_guess = self.get_user_input(2)
                if user_guess == None: # Start over
                    continue
            elif isinstance(user_input1, tuple): # User gave cell and answer -> continue to check answer
                (selected_cell, user_guess) = user_input1
                (selected_col, selected_row) = self.select_cell(selected_cell)
            else:
                raise Exception("Error in receiving answer.")
            assert isinstance(user_guess, MyDataClass), "Invalid guess class type!"
            if user_guess in self.given_answers.values():
                print(f"{str(user_guess)} has already been used as an answer! Try again!")
            elif self.answer_question(selected_col, selected_row, user_guess):
                print("Correct!\n")
                break
            else:
                print("Incorrect!\n")
                break

    def play_game(self) -> None:
        """
        Play the game in terminal.
        Parameters:
            None
        Outputs:
            Plays the game in the terminal. Outputs and receives data in terminal.
            Returns None
        """
        while not self.game_ended():
            self.user_turn()
        print(f"Game over! You answered {len(self.solved_cells)} questions correctly!")

    def string_to_dataclass(self) -> MyDataClass:
        """
        Turn string into driver Dataclass.
        Parameters:
            inp: str; string of driver surname or full name to match with MyDataClass object.
        Outputs:
            answer: MyDataClass; Driver object with matching name
        """
        raise AttributeError("Missing inherited override function.")

    def cell_to_tuple(self, cellname:str) -> tuple[int,int]:
        """
        Makes cell name into tuple = (col_id, row_id)
        Parameters:
            cellname: str; cell name, e.g. A1 or C2
        Outputs:
            col_row_tuple: tuple[int,int]; tuple of (col_id, row_id) of cell
        """
        assert len(cellname) == 2 and cellname[0] in self.colnames and cellname[1] in self.rownames, f'"{cellname}" is not a valid cell name'
        col_id = self.colnames.index(cellname[0])
        row_id = self.rownames.index(cellname[1])
        return (col_id, row_id)
    
    def tuple_to_cell(self, celltuple:tuple[int,int]) -> str:
        """
        Constucts cell name based on tuple of col and row id.
        Parameters:
            celltuple: tuple[int,int]; tuple of type (col_id, row_id)
        Outputs:
            cellname: str; name of cell, e.g. A1 or C3
        """
        assert len(celltuple) == 2, "Invalid cell tuple"
        colname = self.colnames(celltuple[0])
        rowname = self.rownames(celltuple[1])
        return colname + rowname


class DriverQuiz(QuizGame):
    """
    Quizgame where the player must answer different drivers.
    """

    def __init__(self, archive:ArchiveReader, setseed=None):
        super().__init__(archive, setseed=setseed) # Init parent class
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
        while True:
            if input_type == 1:
                input_string = "Please input the coordinates of the question you want to answer (e.g. B1). "
            elif input_type == 2:
                input_string = "Please input the name of the driver you want to guess (surname). "
            else:
                raise AssertionError("Invalid input_type value")
            input_string += "Type 'cancel' to cancel or 'quit' to exit program.\n"
            inp = input(input_string).strip().lower()
            
            if inp.lower() == "quit" or inp.lower() == 'q' or inp.lower() == "exit" or inp.lower() == "e":
                exit()
            elif inp.lower() == "give up" or inp.lower() == "forfeit" or inp.lower() == "f":
                self.forfeit = True
                return None
            elif len(inp) < 2 or inp.lower() == "cancel" or inp.lower() == "c":
                return None
            elif input_type == 1: # User should input grid coordinates
                if len(inp) == 2 and inp[0].upper() in self.colnames and inp[1] in self.rownames:
                    if self.cell_to_tuple(inp.upper()) in self.solved_cells:
                        print(f"Cell {inp} has already been solved!")
                    else:
                        return inp.upper()
                elif inp[0].upper() in self.colnames and inp[1] in self.rownames and " " in inp:
                    # User input both cell and answer simultaneously
                    inps = inp.split(" ", 1)
                    assert len(inps) == 2, "Invalid input, try again."
                    selected_cell = inps[0]
                    if self.cell_to_tuple(selected_cell.upper()) in self.solved_cells:
                        print(f"Cell {inp} has already been solved!")
                        continue
                    answer = self.string_to_dataclass(inps[1])
                    if isinstance(answer, Driver):
                        return (selected_cell.upper(), answer)
                else:
                    print("Invalid input. Please try again.")
            elif input_type == 2: # User should input driver name
                answer = self.string_to_dataclass(inp)
                if isinstance(answer, Driver):
                    return answer

    def string_to_dataclass(self, inp:str) -> MyDataClass:
        """
        Turn string into driver Dataclass.
        Parameters:
            inp: str; string of driver surname or full name to match with MyDataClass object.
        Outputs:
            answer: MyDataClass; Driver object with matching name
        """
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


def play_driver_game(cols:int=3, rows:int=3, difficulty:int=3, guesses:int=9):
    """
    Play driver quiz. This method is used for debugging.
    """
    new_quiz = DriverQuiz(ArchiveReader(archive_path=ARCHIVE_FILE))
    new_quiz.set_n_columns(cols)
    new_quiz.set_n_rows(rows)
    new_quiz.set_difficulty(difficulty)
    new_quiz.set_guesses(guesses)
    new_quiz.start_game()
    new_quiz.play_game()



if __name__ == "__main__":
    play_driver_game()
