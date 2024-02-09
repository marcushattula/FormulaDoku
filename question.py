import random
from globals import *

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
    
    def choose_question(self, difficulty:int, setseed=None):
        """
        Choose a question depending on difficulty. One question cannot be selected multiple times.
        Parameters:
            difficulty: int; difficulty of question, 1 = Easy, 2 = Medium, 3 = Hard
            (Optional) setseed: int; use predetermined seed for question selection. Default = None = Random
        """
        if setseed and isinstance(setseed, int):
            random.seed(setseed)
        if difficulty == 1:
            self.question = random.choice(self.questions1)
            self.questions1.pop(self.questions1.index(self.question))
        elif difficulty == 2:
            self.question = random.choice(self.questions2)
            self.questions2.pop(self.questions2.index(self.question))
        elif difficulty == 3:
            self.question = random.choice(self.questions3)
            self.questions3.pop(self.questions3.index(self.question))
        
    def check_question(self, answer:MyDataClass) -> bool:
        """
        Check if question was answered correctly
        Parameters:
            answer: MyDataClass; The object given as an answer.
        Outputs:
            correct: bool; True if correct, False if incorrect
        """
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
                self.example_answer = candidate
                return True
        return False

class DriverAchievmentQuestion(Question):
    questions1 = [ # Easy questions
        ("Race wins", 5, numberWins),
        ("World championships", 1, numberChampionships),
        ("Race entries", 20, numberEntries),
        ("Pole positions", 5, numberPoles),
        ("Number of wins in a season", 3, numberSeasonWins),
        ]
    questions2 = [ # Medium questions
        ("Number of podiums in a season", 6, numberSeasonPodiums),
        ("Number of points during career", 300, numberPoints),
        ("Podiums", 10, numberPodiums),
    ]
    questions3 = [ # Hard questions
        ("Sprint wins", 1, numberSprintWins),
    ]

    def __init__(self, difficulty:int) -> None:
        super().__init__()
        self.choose_question(difficulty)

class DriverDataQuestion(Question):
    questions1 = [ # Easy questions
        ("Driver nationality", "German", driverNationality),
        ("Driver nationality", "British", driverNationality),
        ("Driver nationality", "Italian", driverNationality),
        ("Driver nationality", "French", driverNationality)
    ]
    questions2 = [ # Medium questions
        ("Driver nationality", "American", driverNationality),
        ("Driver nationality", "Australian", driverNationality),
        ("Driver nationality", "Spanish", driverNationality),
    ]
    questions3 = [ # Hard questions
        ("Driver nationality", "Japanese", driverNationality),
        ("Driver nationality", "Canadian", driverNationality),
    ]

    def __init__(self, difficulty:int) -> None:
        super().__init__()
        self.choose_question(difficulty)

class DriverTeamQuestion(Question):
    questions1 = [ # Easy questions
        ("Driven for team", "Williams", driverTeam),
        ("Driven for team", "McLaren", driverTeam),
        ("Driven for team", "Ferrari", driverTeam)
    ]
    questions2 = [ # Medium questions
        ("Driven for team", "Mercedes", driverTeam),
        ("Driven for team", "Red Bull", driverTeam),
        ("Driven for team", "Renault", driverTeam)
    ]
    questions3 = [ # Hard questions
        ("Driven for team", "Sauber", driverTeam),
        ("Driven for team", "Toro Rosso", driverTeam),
        ("Driven for team", "Alfa Romeo", driverTeam)
    ]

    def __init__(self, difficulty:int) -> None:
        super().__init__()
        self.choose_question(difficulty)

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

