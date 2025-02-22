import random
from mydataclass import MyDataClass, find_single_object_by_field_value
from driver import Driver
from globals import remove_accents, sumWithNone
from readArchive import ArchiveReader

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

def hasTeammate(teammate:Driver, answer:MyDataClass) -> bool:
    return teammate in answer.teammates

def hasTeammateSimple(teammatename:str, answer:MyDataClass) -> bool:
    return any(remove_accents(teammate.fullname) == remove_accents(teammatename) 
               for teammate in answer.teammates)

def wildcard(_, answer:MyDataClass) -> bool:
    return True

def wonRaceInYear(year:int, answer:MyDataClass) -> bool:
    return (year in answer.get_all_seasons_data().keys() and answer.get_all_seasons_data()[year]["n_wins"] >= 1)

def wonRaceIn(country:str, answer:MyDataClass) -> bool:
    country = country.lower()
    wins_per_country = answer.get_wins_per_country()
    return country in wins_per_country and len(wins_per_country[country]) > 0

def wonHomeRace(_, answer:MyDataClass) -> bool:
    return wonRaceIn(answer.country, answer)


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
        self._mutual_answers = {}
    
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
    
    def quiz_format_str(self) -> str:
        """
        
        """
        if self.modifier:
            temp_str = self.base + ": " + str(self.modifier)
            if len(temp_str) > 25:
                temp_str = self.base + ":\n" + str(self.modifier)
        else:
            temp_str = self.base
        return temp_str

    def set_question(self, question_tuple:tuple) -> None:
        assert len(question_tuple) > 4, f"At least 4 fields expected in question tuple, currently {len(question_tuple)}!"
        self.question_id = question_tuple[0]
        self.base = question_tuple[1]
        self.modifier = question_tuple[2]
        self.func = question_tuple[3]
        self.bonus_fields = [question_tuple[i] for i in range(4, len(question_tuple))]

    def choose_question(self, difficulty:int, setseed=None, questionID:int=None):
        """
        Set a question. May be predetermined, random or pseudorandom
        Parameters:
            difficulty: int; difficulty of the question to generate
            (Optional) setseed: Any; seed to use when randomizing questions. Default = None = Random
            (Optional) questionID: int; ID of predetermined question. Default = None
        """
        if isinstance(questionID, int):
            new_question_tuple = self.get_question(questionID)
        else:
            new_question_tuple = self.random_question(difficulty, setseed=setseed)
        self.set_question(new_question_tuple)
    
    def random_question(self, difficulty:int, setseed=None) -> tuple:
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
    
    def get_question(self, question_id:int) -> tuple:
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
        if otherQuestion in self._mutual_answers:
            return len(self.get_mutual_answers(otherQuestion,candidates)) > 0
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
        if self in self._mutual_answers.keys():
            return self._mutual_answers[self]
        self._mutual_answers[self] = []
        for candidate in candidates:
            if self.check_question(candidate):
                self._mutual_answers[self].append(candidate)
        return self._mutual_answers[self]
    
    def get_mutual_answers(self, other_question, candidates:list[MyDataClass]) -> list[MyDataClass]:
        """
        Get all correct answers to two mutual questions form list of candidate answers.
        Parameters:
            other_question: Question; the other question to be filtered for
            candidates: list[MyDataClass]; list of candidate answers
        Outputs:
            Returns list of valid answers
        """
        if other_question in self._mutual_answers.keys():
            return self._mutual_answers[other_question]
        mutual_list = []
        for candidate in candidates:
            if self.check_question(candidate) and other_question.check_question(candidate):
                mutual_list.append(candidate)
        self._mutual_answers[other_question] = mutual_list
        other_question._mutual_answers[self] = mutual_list
        return self._mutual_answers[other_question]

class DriverQuestion(Question):
    questions1 = [] # Easy questions
    questions2 = [] # Medium questions
    questions3 = [] # Hard questions

    def __init__(self):
        super().__init__()

class DriverAchievmentQuestion(DriverQuestion):
    questions1 = [ # Easy questions
        (1000, "Race wins", 5, numberWins, "get_career_data", "n_wins"),
        (1001, "World championships", 1, numberChampionships, "get_career_data", "n_championships"),
        (1002, "No world championships", "", noChampionships, "get_career_data", "n_championships"),
        (1003, "Race entries", 20, numberEntries, "get_career_data", "n_entries"),
        (1004, "Pole positions", 5, numberPoles, "get_career_data", "n_poles"),
        ]
    questions2 = [ # Medium questions
        (1100, "Number of season podiums", 6, numberSeasonPodiums, "get_all_seasons_data", "n_wins"),
        (1101, "Number of career points", 300, numberPoints, "get_career_data", "n_points"),
        (1102, "Number of wins in a season", 3, numberSeasonWins, "get_all_seasons_data", "n_wins"),
        (1103, "Podiums", 10, numberPodiums, "get_all_seasons_data", "n_podiums"),
        (1104, "No wins", "", noWins, "get_career_data", "n_wins")
    ]
    questions3 = [ # Hard questions
        (1201, "Sprint wins", 1, numberSprintWins, "get_career_data", "n_sprint_wins"),
        (1201, "Scored zero during any season", "", noSeasonPoints, "get_all_seasons_data", "n_points"),
        (1202, "No pole positions", "", noPoles, "get_career_data", "n_poles")
    ]

    def __init__(self, difficulty:int, setseed:int=None, questionID:int=None) -> None:
        super().__init__()
        self.choose_question(difficulty, setseed=setseed, questionID=questionID)

class DriverDataQuestion(DriverQuestion):
    questions1 = [ # Easy questions
        (2000, "Driver nationality", "German", driverNationality, "nationality"),
        (2001, "Driver nationality", "British", driverNationality, "nationality"),
        (2002, "Driver nationality", "Italian", driverNationality, "nationality"),
        (2003, "Driver nationality", "French", driverNationality, "nationality"),
        (2004, "Driver nationality", "Brazilian", driverNationality, "nationality")
    ]
    questions2 = [ # Medium questions
        (2100, "Driver nationality", "American", driverNationality, "nationality"),
        (2101, "Driver nationality", "Australian", driverNationality, "nationality"),
        (2102, "Driver nationality", "Spanish", driverNationality, "nationality"),
    ]
    questions3 = [ # Hard questions
        (2200, "Driver nationality", "Japanese", driverNationality, "nationality"),
        (2201, "Driver nationality", "Canadian", driverNationality, "nationality"),
        (2202, "Driver nationality", "Finnish", driverNationality, "nationality"),
    ]

    def __init__(self, difficulty:int, setseed:int=None, questionID:int=None) -> None:
        super().__init__()
        self.choose_question(difficulty, setseed=setseed, questionID=questionID)

class DriverTeamQuestion(DriverQuestion):
    questions1 = [ # Easy questions
        (3000, "Driven for team", "Williams", driverTeam, "teams", "name"),
        (3001, "Driven for team", "McLaren", driverTeam, "teams", "name"),
        (3002, "Driven for team", "Ferrari", driverTeam, "teams", "name"),
        (3003, "Driven for team", "Team Lotus", driverTeam, "teams", "name")
    ]
    questions2 = [ # Medium questions
        (3100, "Driven for team", "Mercedes", driverTeam, "teams", "name"),
        (3101, "Driven for team", "Red Bull", driverTeam, "teams", "name"),
        (3102, "Driven for team", "Renault", driverTeam, "teams", "name")
    ]
    questions3 = [ # Hard questions
        (3200, "Driven for team", "Sauber", driverTeam, "teams", "name"),
        (3201, "Driven for team", "Toro Rosso", driverTeam, "teams", "name"),
        (3202, "Driven for team", "Jordan", driverTeam, "teams", "name")
    ]

    def __init__(self, difficulty:int, setseed:int=None, questionID:int=None) -> None:
        super().__init__()
        self.choose_question(difficulty, setseed=setseed, questionID=questionID)

class DriverSpecialQuestion(DriverQuestion):
    questions1 = [
        (4000, "WILDCARD", "FREE SPACE", wildcard, "")
    ]
    questions2 = [
        (4100, "Has had teammate", "Michael Schumacher", hasTeammateSimple, "teammates"),
        (4101, "Has had teammate", "Kimi Räikkönen", hasTeammateSimple, "teammates"),
        (4102, "Has had teammate", "Fernando Alonso", hasTeammateSimple, "teammates")
    ]
    questions3 = [
        (4200, "Won a race in", 2012, wonRaceInYear, "get_all_seasons_data", "n_wins"),
        (4201, "Won a race on home soil", "", wonHomeRace, "get_all_seasons_data", "wins"),
        (4202, "Won a race in", "Monaco", wonRaceIn, "get_all_seasons_data", "wins")
    ]

    def __init__(self, difficulty, setseed:int=None, questionID:int=None) -> None:
        super().__init__()
        self.choose_question(difficulty, setseed=setseed, questionID=questionID)

class QuestionGenerator():
    """
    Object for procedurally generating questions
    """
    question_formulae = [] # Formulae for questions (id, base, modifier type, check function, get data function, subfield1, subfield2...)

    def __init__(self, archive, validation_list_name:str):
        self.archive = archive
        self.validation_list_name = validation_list_name
    
    def get_validation_list(self):
        assert hasattr(self.archive, self.validation_list_name), f"Archive missing attribute '{self.validation_list_name}'"
        return getattr(self.archive, self.validation_list_name)

    def get_formula_from_id(self, id:int):
        assert isinstance(id, int) and id >= 0, "Question id must be positive integer!"
        for formula in self.question_formulae:
            if formula[0] == id:
                return formula
        raise ValueError(f"No question formula with id {id} found!")
    
    def get_modifier(self, modifier_id:int) -> MyDataClass:
        raise NotImplementedError("Not defined for parent class! Use subclasses!")

    def generate_question(self, id:int, modifier) -> Question:
        question_formula = self.get_formula_from_id(id)
        assert type(modifier) == question_formula[2], f"Mismatching formula modifier type! Exptected {question_formula[2]}, got {type(modifier)}!"
        new_q = Question()
        new_question_formula = list(question_formula)
        new_question_formula[2] = modifier
        new_q.set_question(tuple(new_question_formula))
        return new_q

class DriverQuestionGenerator(QuestionGenerator):

    question_formulae = [
        (1, "Number of race wins", int, numberWins, "get_career_data", "n_wins"),
        (2, "Number of championships", int, numberChampionships, "get_career_data", "n_championships"),
        (3, "Has been teammates with", Driver, hasTeammate, "teammates")
    ]

    def __init__(self, archive:ArchiveReader):
        super().__init__(archive, "drivers")

    def get_modifier(self, modifier_id:int):
        return find_single_object_by_field_value(self.get_validation_list(), "driverId", modifier_id)

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

def all_questions(quiz_category:int):# -> [Question]:
    """
    Returns a list with all questions for quiz category
    Parameters:
        None
    Returns:
        questions: [Question]; list containing all created questions
    """
    if quiz_category == 0:
        questionClass = DriverQuestion
    else:
        raise NotImplementedError("Other question classes not implemented!")
    questions = []
    for questiontype in questionClass.__subclasses__():
        for question_difficulty in ["1", "2", "3"]:
            question_tuple_list = getattr(questiontype, "questions" + question_difficulty)
            for question_tuple in question_tuple_list:
                question_id = question_tuple[0]
                question = questiontype(question_difficulty, questionID=question_id)
                questions.append(question)
    return questions
