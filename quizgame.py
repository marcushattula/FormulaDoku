import random

from readArchive import ArchiveReader
from mydataclass import MyDataClass, find_single_object_by_field_value
from driver import Driver
from globals import *
from question import Question, new_question, all_questions

RECURSION_LIMIT = 100

class QuizGame():
    """
    Classs for storing status of the game.
    """
    colnames = ['A','B','C','D','E'] # Columns are labeled letters A-E
    rownames = ['1','2','3','4','5'] # Rows are labeled numbers 1-5

    def __init__(self, archive:ArchiveReader, setseed=None, n_columns:int=3, n_rows:int=3, difficulty=3):
        """
        Initialize game with default settings. Default is three rows and three columns, easy difficulty.
        """
        self.validation_list: list[MyDataClass] = [] # List of objects to validate against, overridden during inheritance.
        self.solved_cells = [] # List of solved cells, tuple (col, row)
        self.given_answers = {} # List of given correct answers, same answer cannot be used multiple times
        self.difficulty = difficulty # 1 = Easy, 2 = Medium, 3 = Hard
        self.forfeit = False # Flag if player has forfeited game
        self.archive = archive # ArchiveReader class, containing result data
        self.possible_answers = {} # List of possible answers to this quiz
        self.seed = setseed # Seed for generating "random" quiz questions
        self.set_n_columns(n_columns)
        self.set_n_rows(n_rows)
        self.guesses = self.n_columns * self.n_rows # Number of guesses

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
        self.col_questions = [None for _ in range(n)]
    
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
        self.row_questions = [None for _ in range(n)]
    
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

    def set_col_question(self, i:int, question:Question) -> None:
        """
        Add a question to col questions
        Parameters:
            question: Question; question to be added
        Outputs:
            None
            Adds the question to self.col_questions
        """
        assert isinstance(question, Question), f"Added question must be Question object"
        assert isinstance(i, int) and 0 <= i < self.n_columns, f"Index must be in range of number of columns!"
        self.col_questions[i] = question

    def set_row_question(self, i:int, question:Question) -> None:
        """
        Add a question to row questions
        Parameters:
            question: Question; question to be added
        Outputs:
            None
            Adds the question to self.row_questions
        """
        assert isinstance(question, Question), f"Added question must be Question object"
        assert isinstance(i, int) and 0 <= i < self.n_rows, f"Index must be in range of number of columns!"
        self.row_questions[i] = question

    def start_game(self) -> None:
        """
        Starts the game with set settings. Generates questions.
        Parameters:
            None
        Outputs:
            Adds questions to self.col_questions and self.row_questions
            Returns None
        """
        raise DeprecationWarning("This function should no longer be used. Please use quizconstructor to generate quizzes.")
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
       
        def set_possible_answers(possible_answers: list[MyDataClass], answer_order:list[int]) -> None:
            """
            Takes list of correct answers and stores it to dictionary for each question
            Parameters:
                possible_answers: list[MyDataClass]; validated llist of answers
                answer_order: list[int]; indexes of questions before sorting for performance
            Outputs:
                None
                Stores the dictionary to self.possible_answers
            """
            possible_answers_sorted = [x for _, x in sorted(zip(answer_order, possible_answers))]
            for i in range(self.n_columns):
                for j in range(self.n_rows):
                    index = i*self.n_rows+j
                    if index < len(possible_answers_sorted):
                        self.possible_answers[(i, j)] = possible_answers_sorted[index]

        def constraints_search(ans_list: list[list[MyDataClass]], answer_order:list[int], used_answers=[]) -> bool:
            """
            Recursively check that there is a unused answer for each question
            Parameters:
                ans_list: list[list[MyDataClass]]; list of list of answers to each question
            Outputs:
                b: bool; True if each question has a unique answer, else False
                Stores a found solution to self.possible_answers, if found
            """
            if len(ans_list) == 0:
                set_possible_answers(used_answers, answer_order)
                return True
            for answer in ans_list[0]:
                if answer not in used_answers:
                    temp_arr = used_answers.copy()
                    temp_arr.append(answer)
                    if constraints_search(ans_list[1:], answer_order, used_answers=temp_arr):
                        return True
            return False
        
        # If any pair of questions has no mutual answers, it is automatically void
        for col_q in self.col_questions:
            for row_q in self.row_questions:
                if len(col_q.get_mutual_answers(row_q, self.validation_list)) == 0:
                    return False

        all_answers = get_list_of_answers_list()
        sorted_answers = sorted(all_answers, key=len)
        index_order = [all_answers.index(ans_list) for ans_list in sorted_answers]
        return constraints_search(sorted_answers, index_order)
    
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


class QuizConstructor():

    def __init__(self, archive:ArchiveReader, n_cols:int=3, n_rows:int=3, 
            difficulty:int=3, quiztype:int=0, guesses:int=0, seed=None):
        random.seed(seed)
        self.archive = archive
        self.set_n_cols(n_cols)
        self.set_n_rows(n_rows)
        self.set_difficulty(difficulty)
        self.set_quiztype(quiztype)
        self.set_n_guesses(guesses)
        self.all_questions:list[Question] = None
        self.quiz:QuizGame = None
    
    def validate_all(self):
        for question in self.all_questions:
            for other_question in self.all_questions:
                question.get_mutual_answers(other_question, self.archive.drivers)
        
    def set_n_cols(self, n_cols:int):
        assert isinstance(n_cols, int) and n_cols > 0, f"Number of columns must be positive integer! Currently {n_cols}"
        self.n_cols = n_cols
        self.col_question_id_set = [-1 for _ in range(n_cols)]
    
    def set_n_rows(self, n_rows:int):
        assert isinstance(n_rows, int) and n_rows > 0, f"Number of rows must be positive integer! Currently {n_rows}"
        self.n_rows = n_rows
        self.row_question_id_set = [-1 for _ in range(n_rows)]
    
    def set_difficulty(self, difficulty:int):
        assert isinstance(difficulty, int) and difficulty > 0, f"Difficulty must be positive integer! Currently {difficulty}"
        self.difficulty = difficulty
    
    def set_quiztype(self, quiztype:int):
        assert isinstance(quiztype, int) and quiztype in [0], f"Quiztype must be integer corresponding to type! Currently {quiztype}"
        self.quiztype = quiztype
    
    def set_n_guesses(self, guesses:int):
        assert isinstance(guesses, int) and guesses >= 0, f"Number of guesses must be non-negative integer! Currently {guesses}"
        self.guesses = guesses
    
    def select_question(self, id:int) -> Question:
        assert isinstance(id, int), f"Question index must be integer! Currently {id}"
        for q in self.all_questions:
            if q.question_id == id:
                return q
        raise ValueError(f"No question with id: {id}!")
    
    def random_question(self) -> Question:
        return random.choice(self.all_questions)

    def set_col_question_id(self, ids):
        assert all([x == None or isinstance(x, int) for x in ids]), "Ids must be None or integers!"
        self.col_question_id_set = ids
    
    def set_row_question_id(self, ids):
        assert all([x == None or isinstance(x, int) for x in ids]), "Ids must be None or integers!"
        self.row_question_id_set = ids

    def update_col_questions(self):
        """
        
        """
        assert len(self.col_question_id_set) == self.n_cols, f"Array length must match number of columns! ({len(self.col_question_id_set)} != {self.n_cols})"
        new_id_set = []
        for i in range(self.n_cols):
            i_question_id = self.col_question_id_set[i]
            if i_question_id == None:
                i_question = self.random_question()
                i_question_id = i_question.question_id
            else:
                assert isinstance(i_question_id, int), f"Question ID must be integer!"
                i_question = self.select_question(i_question_id)
            new_id_set.append(i_question_id)
            self.quiz.set_col_question(i, i_question)
        return new_id_set
    
    def update_row_questions(self):
        """
        
        """
        assert len(self.row_question_id_set) == self.n_rows, f"Array length must match number of rows! ({len(self.row_question_id_set)} != {self.n_rows})"
        new_id_set = []
        for i in range(self.n_rows):
            i_question_id = self.row_question_id_set[i]
            if i_question_id == None:
                i_question = self.random_question()
                i_question_id = i_question.question_id
            else:
                assert isinstance(i_question_id, int), f"Question ID must be integer!"
                i_question = self.select_question(i_question_id)
            new_id_set.append(i_question_id)
            self.quiz.set_row_question(i, i_question)
        return new_id_set

    def update_questions(self):
        """
        
        """
        new_questions_set = ([], [])
        for i in range(max(self.n_cols, self.n_rows)):
            if i < self.n_cols:
                i_col_question_id = self.col_question_id_set[i]
                while True:
                    if i_col_question_id == None:
                        i_col_question = self.random_question()
                    elif isinstance(i_col_question_id, int) and i_col_question_id < 0:
                        temp_seed = random.random()
                        i_col_question = new_question(max(min(self.n_cols-i, self.difficulty), 1), setseed=temp_seed)
                    else:
                        i_col_question = self.select_question(i_col_question_id)
                    temp_id = i_col_question.question_id
                    question_predetermined = isinstance(i_col_question_id, int) and i_col_question_id >= 0
                    random_or_logic = (i_col_question_id == None or i_col_question_id < 0)
                    not_in_cols_or_rows = not (any([temp_id == x.question_id for x in new_questions_set[0]]) or
                        any([temp_id == x.question_id for x in new_questions_set[1]]))
                    question_compatible = True#all([i_col_question.validate_question(other_question, self.quiz.validation_list) for other_question in new_questions_set[1]])
                    if question_predetermined or (random_or_logic and not_in_cols_or_rows and question_compatible):
                        new_questions_set[0].append(i_col_question)# Append question to set of columns
                        break
            if i < self.n_rows:
                i_row_question_id = self.row_question_id_set[i]
                while True:
                    if i_row_question_id == None:
                        i_row_question = self.random_question()
                    elif isinstance(i_row_question_id, int) and i_row_question_id < 0:
                        temp_seed = random.random()
                        i_row_question = new_question(max(min(self.n_rows-i, self.difficulty), 1), setseed=temp_seed)
                    else:
                        i_row_question = self.select_question(i_row_question_id)
                    temp_id = i_row_question.question_id
                    question_predetermined = isinstance(i_row_question_id, int) and i_row_question_id >= 0
                    random_or_logic = (i_row_question_id == None or i_row_question_id < 0)
                    not_in_cols_or_rows = not (any([temp_id == x.question_id for x in new_questions_set[0]]) or
                        any([temp_id == x.question_id for x in new_questions_set[1]]))
                    question_compatible = True#all([i_row_question.validate_question(other_question, self.quiz.validation_list) for other_question in new_questions_set[0]])
                    if question_predetermined or (random_or_logic and not_in_cols_or_rows and question_compatible):
                        new_questions_set[1].append(i_row_question)# Append question to set of columns
                        break
        for i in range(self.n_cols):
            self.quiz.set_col_question(i, new_questions_set[0][i])
        for i in range(self.n_rows):
            self.quiz.set_row_question(i, new_questions_set[1][i])
        return new_questions_set
        #return (col_q, row_q)

    def create_quiz(self):
        """
        
        """
        if self.quiztype == 0:
            self.quiz = DriverQuiz(self.archive)
        else:
            raise NotImplementedError("Other quizclasses not implemented yet!")
        self.quiz.set_n_columns(self.n_cols)
        self.quiz.set_n_rows(self.n_rows)
        self.quiz.set_difficulty(self.difficulty)
        self.all_questions = all_questions(self.quiztype)
        self.validate_all()
    
    def start_quiz(self, force:bool=False) -> QuizGame:
        """
        
        """

        def compare_sets(set1:tuple[list[int], list[int]], set_of_sets:list[tuple[list[int], list[int]]]) -> bool:
            """
            Helper function for checking if set1 exists in set_of_sets, regardless of order of internal lists
            """
            if set1 in set_of_sets:
                return True
            new_col_set = set1[0]
            new_row_set = set1[1]
            for set2 in set_of_sets:
                col_set = set2[0]
                row_set = set2[1]
                if (all([int1 in col_set for int1 in new_col_set]) and all([int2 in new_col_set for int2 in col_set]) and
                    all([int3 in row_set for int3 in new_row_set]) and all([int4 in new_row_set for int4 in row_set])):
                    return True
            return False

        if force:
            self.update_questions()
            return self.quiz
        validated = False
        incompatible_sets = []
        i = 0
        while not validated:
            new_question_set = self.update_questions()
            i += 1
            if i > RECURSION_LIMIT:
                raise RecursionError("Unable to find compatible set! Please change questions.")
            elif compare_sets(new_question_set, incompatible_sets):
                continue
            validated = self.quiz.full_validation()
            if not validated:
                incompatible_sets.append(new_question_set)
        return self.quiz


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
    archive = ArchiveReader(archive_path=ARCHIVE_FILE)
    qc = QuizConstructor(archive, n_cols=3, n_rows=3, seed=7)
    qc.create_quiz()
    qg = qc.start_quiz()
    breakpoint()
    #play_driver_game()
