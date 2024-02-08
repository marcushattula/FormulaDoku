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
    questions1 = []
    questions2 = []
    questions3 = []

    def __init__(self):
        pass
    
    def choose_question(self, difficulty:int):
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
            None
        Outputs:
            correct: bool; True if correct, False if incorrect
        """
        return self.question[2](self.question[1], answer)

    def validate_question(self, otherQuestion, candidates:list[MyDataClass]) -> bool:
        """"""
        for candidate in candidates:
            ans1 = self.check_question(candidate)
            ans2 = otherQuestion.check_question(candidate)
            if ans1 and ans2:
                self.example_answer = candidate
                return True
        return False

class DriverAchievmentQuestion(Question):
    questions1 = [
        ("Race wins", 5, numberWins),
        ("World championships", 1, numberChampionships),
        ("Race entries", 20, numberEntries),
        ("Pole positions", 5, numberPoles),
        ("Number of wins in a season", 3, numberSeasonWins),
        ]
    questions2 = [
        ("Number of podiums in a season", 6, numberSeasonPodiums),
        ("Number of points during career", 300, numberPoints),
        ("Podiums", 10, numberPodiums),
    ]
    questions3 = [
        ("Sprint wins", 1, numberSprintWins),
    ]

    def __init__(self, difficulty:int) -> None:
        super().__init__()
        self.choose_question(difficulty)

class DriverDataQuestion(Question):
    questions1 = [
        ("Driver nationality", "German", driverNationality),
        ("Driver nationality", "British", driverNationality),
        ("Driver nationality", "Italian", driverNationality),
        ("Driver nationality", "French", driverNationality)
    ]
    questions2 = [
        ("Driver nationality", "American", driverNationality),
        ("Driver nationality", "Australian", driverNationality),
        ("Driver nationality", "Spanish", driverNationality),
    ]
    questions3 = [
        ("Driver nationality", "Japanese", driverNationality),
        ("Driver nationality", "Canadian", driverNationality),
    ]

    def __init__(self, difficulty:int) -> None:
        super().__init__()
        self.choose_question(difficulty)

class DriverTeamQuestion(Question):
    questions1 = [
        ("Driven for team", "Williams", driverTeam),
        ("Driven for team", "McLaren", driverTeam),
        ("Driven for team", "Ferrari", driverTeam)
    ]
    questions2 = [
        ("Driven for team", "Mercedes", driverTeam),
        ("Driven for team", "Red Bull", driverTeam),
        ("Driven for team", "Renault", driverTeam)
    ]
    questions3 = [
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

