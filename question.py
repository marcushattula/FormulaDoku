import random
from mydataclass import MyDataClass

def numberWins(n:int, answer:MyDataClass) -> bool:
    """
    Determine if given answer meets criteria
    Parameters:
        n: int; limit

    """
    return answer.wins >= n

def numberChampionships(n:int, answer:MyDataClass) -> bool:
    """
    Determine if given answer meets criteria
    Parameters:
        n: int; limit

    """
    return answer.championships >= n

def numberEntries(n:int, answer:MyDataClass) -> bool:
    """
    Determine if given answer meets criteria
    Parameters:
        n: int; limit

    """
    return answer.entries >= n

def numberPoles(n:int, answer:MyDataClass) -> bool:
    return answer.poles >= n

def numberPodiums(n:int, answer:MyDataClass) -> bool:
    return answer.podiums >= n

def numberPoints(n:int, answer:MyDataClass) -> bool:
    return answer.career_points >= n

def numberSprintWins(n:int, answer:MyDataClass) -> bool:
    return answer.sprint_wins >= n

def driverNationality(nationality:str, answer:MyDataClass) -> bool:
    """"""
    return nationality == answer.nationality

def driverTeam(team:str, answer:MyDataClass) -> bool:
    """"""
    return any(constructor.name == team for constructor in answer.teams)

def numberSeasonPoints(n:int, answer:MyDataClass) -> bool:
    for year in answer.season_data:
        season = answer.season_data[year]
        if season["points"] >= n:
            return True
    return False

def numberSeasonPoles(n:int, answer:MyDataClass) -> bool:
    for year in answer.season_data:
        season = answer.season_data[year]
        if season["poles"] >= n:
            return True
    return False

def numberSeasonPodiums(n:int, answer:MyDataClass) -> bool:
    for year in answer.season_data:
        season = answer.season_data[year]
        if season["podiums"] >= n:
            return True
    return False

def numberSeasonWins(n:int, answer:MyDataClass) -> bool:
    for year in answer.season_data:
        season = answer.season_data[year]
        if season["wins"] >= n:
            return True
    return False


class Question():
    """
    Parent class for inheritance of question methods.
    """
    # Each question is a tuple (Question base, Question limit/target, function to check validity)
    questions1 = [] # Easy questions
    questions2 = [] # Medium questions
    questions3 = [] # Hard questions

    def __init__(self):
        """
        Parent init does nothing.
        """
        pass
    
    def __str__(self) -> str:
        """
        Overwrite string method to return string consisting of question base and limit/target
        """
        return self.question[0] + ": " + str(self.question[1])

    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, other_question):
        return str(self) == str(other_question)

    def choose_question(self, difficulty:int, setseed=None):
        """
        Choose a question depending on difficulty. One question cannot be selected multiple times.
        Parameters:
            difficulty: int; difficulty of question, 1 = Easy, 2 = Medium, 3 = Hard
            (Optional) setseed: int; use predetermined seed for question selection. Default = None = Random
        """
        if setseed and isinstance(setseed, int) or setseed == None:
            random.seed(setseed)
        if difficulty == 1:
            self.question = random.choice(self.questions1)
        elif difficulty == 2:
            self.question = random.choice(self.questions2)
        elif difficulty == 3:
            self.question = random.choice(self.questions3)
        
    def check_question(self, answer:MyDataClass) -> bool:
        """
        Check if question was answered correctly
        Parameters:
            answer: MyDataClass; The object given as an answer.
        Outputs:
            correct: bool; True if correct, False if incorrect
        """
        if hasattr(self, "__all_answers"):
            return answer in self.__all_answers
        else:
            return self.question[2](self.question[1], answer)

    def validate_question(self, otherQuestion, candidates:list[MyDataClass]) -> bool:
        """
        Validate that this question and another question have at least one valid answer from candidate list.
        Parameters:
            otherQuestion: Question; the other question to validate
            candidates: list[MyDataClass]; list of objects that are potential answers to the question
        Returns:
            valid: bool; boolean for if at least one valid answer exists for both questions. True = true
        """
        for candidate in candidates:
            ans1 = self.check_question(candidate)
            ans2 = otherQuestion.check_question(candidate)
            if ans1 and ans2:
                return True
        return False

    def get_all_answers(self, candidates:list[MyDataClass]) -> list[MyDataClass]:
        """
        Get all valid answers to this question from candidate list.
        Parameters:
            candidates: list[MyDataClass]; list of MyDataClass objects that are possible answers to question
        Outputs:
            filtered_list: list[MyDataClass]; filtered list of candidates that are correct answers
        """
        if hasattr(self, "_all_answers"):
            return self._all_answers
        else:
            self._all_answers = []
            for candidate in candidates:
                if self.check_question(candidate):
                    self._all_answers.append(candidate)
            return self.get_all_answers(candidates)
    
    def get_mutual_answers(self, other_question, candidates:list[MyDataClass]) -> list[MyDataClass]:
        """
        Get all correct answers to two mutual questions form list of candidate answers.
        Parameters:
            other_question: Question; the other question to be filtered for
            candidates: list[MyDataClass]; list of candidate answers
        Outputs:
            Sets self._mutual_answers[other_question] to list of valid answers
            Sets other_question._mutual_answers[self] to list of valid answers
            Returns list of valid answers
        """
        if (hasattr(self, "_mutual_answers") and other_question in self._mutual_answers):
            other_question._mutual_answers[self] = self._mutual_answers[other_question]
            return self._mutual_answers[other_question]
        elif (hasattr(other_question, "_mutual_answers") and self in other_question._mutual_answers):
            other_question._mutual_answers[self] = self._mutual_answers[other_question]
            return other_question._mutual_answers[self]
        else:
            self._mutual_answers = {}
            self._mutual_answers[other_question] = []
            other_question._mutual_answers = {}
            other_question._mutual_answers[self] = []
            for candidate in candidates:
                if self.check_question(candidate) and other_question.check_question(candidate):
                    self._mutual_answers[other_question].append(candidate)
                    other_question._mutual_answers[self].append(candidate)
            return self._mutual_answers[other_question]

class DriverAchievmentQuestion(Question):
    questions1 = [ # Easy questions
        ("Race wins", 5, numberWins, "wins"),
        ("World championships", 1, numberChampionships, "championships"),
        ("Race entries", 20, numberEntries, "entries"),
        ("Pole positions", 5, numberPoles, "poles"),
        ]
    questions2 = [ # Medium questions
        ("Number of podiums in a season", 6, numberSeasonPodiums, "season_data", "wins"),
        ("Number of points during career", 300, numberPoints, "points"),
        ("Number of wins in a season", 3, numberSeasonWins, "season_data", "wins"),
        ("Podiums", 10, numberPodiums, "season_data", "podiums"),
    ]
    questions3 = [ # Hard questions
        ("Sprint wins", 1, numberSprintWins, "sprint_wins"),
    ]

    def __init__(self, difficulty:int, setseed:int=None) -> None:
        super().__init__()
        self.choose_question(difficulty, setseed=setseed)

class DriverDataQuestion(Question):
    questions1 = [ # Easy questions
        ("Driver nationality", "German", driverNationality, "nationality"),
        ("Driver nationality", "British", driverNationality, "nationality"),
        ("Driver nationality", "Italian", driverNationality, "nationality"),
        ("Driver nationality", "French", driverNationality, "nationality"),
        ("Driver nationality", "Brazilian", driverNationality, "nationality")
    ]
    questions2 = [ # Medium questions
        ("Driver nationality", "American", driverNationality, "nationality"),
        ("Driver nationality", "Australian", driverNationality, "nationality"),
        ("Driver nationality", "Spanish", driverNationality, "nationality"),
    ]
    questions3 = [ # Hard questions
        ("Driver nationality", "Japanese", driverNationality, "nationality"),
        ("Driver nationality", "Canadian", driverNationality, "nationality"),
        ("Driver nationality", "Finnish", driverNationality, "nationality"),
    ]

    def __init__(self, difficulty:int, setseed:int=None) -> None:
        super().__init__()
        self.choose_question(difficulty, setseed=setseed)

class DriverTeamQuestion(Question):
    questions1 = [ # Easy questions
        ("Driven for team", "Williams", driverTeam, "teams", "name"),
        ("Driven for team", "McLaren", driverTeam, "teams", "name"),
        ("Driven for team", "Ferrari", driverTeam, "teams", "name")
    ]
    questions2 = [ # Medium questions
        ("Driven for team", "Mercedes", driverTeam, "teams", "name"),
        ("Driven for team", "Red Bull", driverTeam, "teams", "name"),
        ("Driven for team", "Renault", driverTeam, "teams", "name")
    ]
    questions3 = [ # Hard questions
        ("Driven for team", "Sauber", driverTeam, "teams", "name"),
        ("Driven for team", "Toro Rosso", driverTeam, "teams", "name"),
    ]

    def __init__(self, difficulty:int, setseed:int=None) -> None:
        super().__init__()
        self.choose_question(difficulty, setseed=setseed)

def new_question(difficulty:int, questiontype:int) -> Question:
    """
    Create a new question
    Parameters:
        difficulty: int; difficulty of question, 1 = Easy, 2 = Medium, 3 = Hard
        questiontype: int; type of quetion to be asked.
            1 = 50% driver achievment question, 50% driver nationality question
            2 = 50% driver achievment question, 50% driver team question
    Outputs:
        question: Question; randomly selected question type.
    """
    assert isinstance(difficulty, int) and 1 <= difficulty <= 3, "Difficulty must be integer 1-3"
    assert isinstance(questiontype, int) and 1 <= questiontype <= 2, "Questiontype must be integer 1-2"
    achievment = random.randint(1,2)
    if achievment == 2:
        return DriverAchievmentQuestion(difficulty)
    elif questiontype == 1:
        return DriverDataQuestion(difficulty)
    elif questiontype == 2:
        return DriverTeamQuestion(difficulty)

