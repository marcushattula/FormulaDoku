import random
from mydataclass import MyDataClass
from globals import remove_accents, sumWithNone

def numberWins(n:int, answer:MyDataClass) -> bool:
    """
    Determine if given answer meets criteria
    Parameters:
        n: int; limit

    """
    return answer.get_career_data()["n_wins"] >= n

def numberChampionships(n:int, answer:MyDataClass) -> bool:
    """
    Determine if given answer meets criteria
    Parameters:
        n: int; limit

    """
    return answer.get_career_data()["n_championships"] >= n

def numberEntries(n:int, answer:MyDataClass) -> bool:
    """
    Determine if given answer meets criteria
    Parameters:
        n: int; limit

    """
    return answer.get_career_data()["n_entries"] >= n

def numberPoles(n:int, answer:MyDataClass) -> bool:
    return answer.get_career_data()["n_poles"] >= n

def numberPodiums(n:int, answer:MyDataClass) -> bool:
    return answer.get_career_data()["n_podiums"] >= n

def numberPoints(n:int, answer:MyDataClass) -> bool:
    return answer.get_career_data()["n_points"] >= n

def numberSprintWins(n:int, answer:MyDataClass) -> bool:
    return answer.get_career_data()["n_sprint_wins"] >= n

def driverNationality(nationality:str, answer:MyDataClass) -> bool:
    """"""
    return nationality == answer.nationality

def driverTeam(team:str, answer:MyDataClass) -> bool:
    """"""
    return any(constructor.name == team for constructor in answer.teams)

def numberSeasonPoints(n:int, answer:MyDataClass) -> bool:
    return any([len(answer.get_season_data(i)["points"]) >= n for i in answer.season_entries.keys()])
    # for year in answer.season_data:
    #     season = answer.season_data[year]
    #     if season["points"] >= n:
    #         return True
    # return False

def numberSeasonPoles(n:int, answer:MyDataClass) -> bool:
    return any([len(answer.get_season_data(i)["poles"]) >= n for i in answer.season_entries.keys()])
    # for year in answer.season_data:
    #     season = answer.season_data[year]
    #     if season["poles"] >= n:
    #         return True
    # return False

def numberSeasonPodiums(n:int, answer:MyDataClass) -> bool:
    return any([len(answer.get_season_data(i)["podiums"]) >= n for i in answer.season_entries.keys()])
    # for year in answer.season_data:
    #     season = answer.season_data[year]
    #     if season["podiums"] >= n:
    #         return True
    # return False

def numberSeasonWins(n:int, answer:MyDataClass) -> bool:
    return any([len(answer.get_season_data(i)["wins"]) >= n for i in answer.season_entries.keys()])
    # for year in answer.season_data:
    #     season = answer.season_data[year]
    #     if season["wins"] >= n:
    #         return True
    # return False

def noChampionships(n:int, answer:MyDataClass) -> bool:
    return answer.get_career_data()["n_championships"] == 0

def noWins(n:int, answer:MyDataClass) -> bool:
    return answer.get_career_data()["n_wins"] == 0

def noPoles(n:int, answer:MyDataClass) -> bool:
    return answer.get_career_data()["n_poles"] == 0

def noSeasonPoints(n:int, answer:MyDataClass) -> bool:
    return any([sumWithNone(answer.get_season_data(year)["points"]) == 0 for year in answer.season_data.keys()]) 

def hasTeammate(teammatename:str, answer:MyDataClass) -> bool:
    return any(remove_accents(teammate.fullname) == remove_accents(teammatename) 
               for teammate in answer.teammates)

def wildcard(_, answer:MyDataClass) -> bool:
    return True

def wonRaceInYear(year:int, answer:MyDataClass) -> bool:
    return (year in answer.get_all_seasons_data().keys() and answer.get_all_seasons_data()[year]["n_wins"] >= 1)

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
        Parent init initializes later variables as None
        """
        self.question_id:int = None
        self.base:str = None
        self.modifier = None
        self.func = None
        self.map_field1 = None
        self.map_field2 = None
    
    def __str__(self) -> str:
        """
        Overwrite string method to return string consisting of question base and limit/target
        """
        if self.modifier:
            return self.base + ": " + str(self.modifier)
        else:
            return self.base

    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, other_question):
        return str(self) == str(other_question)
    
    def choose_question(self, difficulty:int, setseed=None, questionID:int=None):
        """
        Set a question. May be predetermined, random or pseudorandom
        Parameters:
            difficulty: int; difficulty of the question to generate
            (Optional) setseed: Any; seed to use when randomizing questions. Default = None = Random
            (Optional) questionID: int; ID of predetermined question. Default = None
        """
        if isinstance(questionID, int):
            self.question = self.get_question(questionID)
        else:
            self.question = self.random_question(difficulty, setseed=setseed)
        self.question_id = self.question[0]
        self.base = self.question[1]
        self.modifier = self.question[2]
        self.func = self.question[3]

    def random_question(self, difficulty:int, setseed=None):
        """
        Choose a question depending on difficulty. One question cannot be selected multiple times.
        Parameters:
            difficulty: int; difficulty of question, 1 = Easy, 2 = Medium, 3 = Hard
            (Optional) setseed: int; use predetermined seed for question selection. Default = None = Random
        """
        if setseed and isinstance(setseed, int) or setseed == None:
            random.seed(setseed)
        if difficulty == 1:
            return random.choice(self.questions1)
        elif difficulty == 2:
            return random.choice(self.questions2)
        elif difficulty == 3:
            return random.choice(self.questions3)
    
    def get_question(self, question_id:int):
        """
        Set predetermined question based on question id
        Parameters:
            question_id: int; ID of the question
        Outputs:
            question: tuple; tuple containing question details
        """
        assert isinstance(question_id, int), "Question ID must be integer!"
        for question in self.questions1:
            if question[0] == question_id:
                return question
        for question in self.questions2:
            if question[0] == question_id:
                return question
        for question in self.questions3:
            if question[0] == question_id:
                return question
        raise AssertionError(f"No question with ID {question_id} was found!")

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
            return self.func(self.modifier, answer)

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
            self._mutual_answers[other_question] = other_question._mutual_answers[self]
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
        (0, "Race wins", 5, numberWins, "get_career_data", "n_wins"),
        (1, "World championships", 1, numberChampionships, "get_career_data", "n_championships"),
        (2, "No world championships", "", noChampionships, "get_career_data", "n_championships"),
        (3, "Race entries", 20, numberEntries, "get_career_data", "n_entries"),
        (4, "Pole positions", 5, numberPoles, "get_career_data", "n_poles"),
        ]
    questions2 = [ # Medium questions
        (100, "Number of podiums in a season", 6, numberSeasonPodiums, "get_all_seasons_data", "n_wins"),
        (101, "Number of points during career", 300, numberPoints, "get_career_data", "n_points"),
        (102, "Number of wins in a season", 3, numberSeasonWins, "get_all_seasons_data", "n_wins"),
        (103, "Podiums", 10, numberPodiums, "get_all_seasons_data", "n_podiums"),
        (104, "No wins", "", noWins, "get_career_data", "n_wins")
    ]
    questions3 = [ # Hard questions
        (201, "Sprint wins", 1, numberSprintWins, "get_career_data", "n_sprint_wins"),
        (201, "Scored zero during any season", "", noSeasonPoints, "get_all_seasons_data", "n_points"),
        (202, "No pole positions", "", noPoles, "get_career_data", "n_poles")
    ]

    def __init__(self, difficulty:int, setseed:int=None, questionID:int=None) -> None:
        super().__init__()
        self.choose_question(difficulty, setseed=setseed, questionID=questionID)

class DriverDataQuestion(Question):
    questions1 = [ # Easy questions
        (0, "Driver nationality", "German", driverNationality, "nationality"),
        (1, "Driver nationality", "British", driverNationality, "nationality"),
        (2, "Driver nationality", "Italian", driverNationality, "nationality"),
        (3, "Driver nationality", "French", driverNationality, "nationality"),
        (4, "Driver nationality", "Brazilian", driverNationality, "nationality")
    ]
    questions2 = [ # Medium questions
        (100, "Driver nationality", "American", driverNationality, "nationality"),
        (101, "Driver nationality", "Australian", driverNationality, "nationality"),
        (102, "Driver nationality", "Spanish", driverNationality, "nationality"),
    ]
    questions3 = [ # Hard questions
        (200, "Driver nationality", "Japanese", driverNationality, "nationality"),
        (201, "Driver nationality", "Canadian", driverNationality, "nationality"),
        (202, "Driver nationality", "Finnish", driverNationality, "nationality"),
    ]

    def __init__(self, difficulty:int, setseed:int=None, questionID:int=None) -> None:
        super().__init__()
        self.choose_question(difficulty, setseed=setseed, questionID=questionID)

class DriverTeamQuestion(Question):
    questions1 = [ # Easy questions
        (0, "Driven for team", "Williams", driverTeam, "teams", "name"),
        (1, "Driven for team", "McLaren", driverTeam, "teams", "name"),
        (2, "Driven for team", "Ferrari", driverTeam, "teams", "name"),
        (3, "Driven for team", "Team Lotus", driverTeam, "teams", "name")
    ]
    questions2 = [ # Medium questions
        (100, "Driven for team", "Mercedes", driverTeam, "teams", "name"),
        (101, "Driven for team", "Red Bull", driverTeam, "teams", "name"),
        (102, "Driven for team", "Renault", driverTeam, "teams", "name")
    ]
    questions3 = [ # Hard questions
        (200, "Driven for team", "Sauber", driverTeam, "teams", "name"),
        (201, "Driven for team", "Toro Rosso", driverTeam, "teams", "name"),
        (202, "Driven for team", "Jordan", driverTeam, "teams", "name")
    ]

    def __init__(self, difficulty:int, setseed:int=None, questionID:int=None) -> None:
        super().__init__()
        self.choose_question(difficulty, setseed=setseed, questionID=questionID)

class DriverSpecialQuestion(Question):
    questions1 = [
        (0, "WILDCARD", "FREE SPACE", wildcard, "")
    ]
    questions2 = [
        (100, "Has had teammate", "Michael Schumacher", hasTeammate, "teammates"),
        (101, "Has had teammate", "Kimi Räikkönen", hasTeammate, "teammates"),
        (102, "Has had teammate", "Fernando Alonso", hasTeammate, "teammates")
    ]
    questions3 = [
        (200, "Won a race in",  2012, wonRaceInYear, "get_all_seasons_data", "n_wins")
    ]

    def __init__(self, difficulty, setseed:int=None, questionID:int=None) -> None:
        super().__init__()
        self.choose_question(difficulty, setseed=setseed, questionID=questionID)

def new_question(difficulty:int, questiontype:int=None, setseed=None, questionID:int=None) -> Question:
    """
    Create a new question
    Parameters:
        difficulty: int; difficulty of question, 1 = Easy, 2 = Medium, 3 = Hard
        questiontype: int; type of quetion to be asked.
            1 = DriverAchievmentQuestion
            2 = DriverDataQuestion
            3 = DriverTeamQuestion
            4 = DriverSpecialQuestion
    Outputs:
        question: Question; randomly selected question type.
    """
    if questiontype == None:
        questiontype = random.randint(1,4)
    assert isinstance(difficulty, int) and 1 <= difficulty <= 3, "Difficulty must be integer 1-3"
    assert isinstance(questiontype, int) and 1 <= questiontype <= 4, "Questiontype must be integer 1-4"
    if questiontype == 1:
        return DriverAchievmentQuestion(difficulty, setseed=setseed, questionID=questionID)
    elif questiontype == 2:
        return DriverDataQuestion(difficulty, setseed=setseed, questionID=questionID)
    elif questiontype == 3:
        return DriverTeamQuestion(difficulty, setseed=setseed, questionID=questionID)
    elif questiontype == 4:
        return DriverSpecialQuestion(difficulty, setseed=setseed, questionID=questionID)

