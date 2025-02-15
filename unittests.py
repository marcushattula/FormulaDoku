import unittest
import random

from readArchive import ArchiveReader
from globals import ARCHIVE_FILE, remove_accents, isFloat, CountryConverter
from mydataclass import MyDataClass, find_objects_by_field_value, find_single_object_by_field_value
from circuit import Circuit
from constructor import Constructor
from driver import Driver
from race import Race, Result, RACE_RESULT_DATA_FIELDS
from season import Season
from question import Question, DriverAchievmentQuestion, DriverDataQuestion, DriverTeamQuestion, new_question, all_questions
from quizgame import QuizGame, DriverQuiz, QuizConstructor

TESTARCHIVE = ArchiveReader(archive_path=ARCHIVE_FILE, skip=True)

def error_msg(attr:str, expected, got):
    """
    Create error message according to expected attribute, expected value and received value
    Parameters:
        attr: str; Name of attribute that was parsed incorrectly
        expected: any; Expected value of field
        got: any; Received value of field
    Outputs
        error_msg: str; Error message with given information formatted according to each type
        "Incorrect {attr}! Expected '{expected}', got '{got}'!"
        If expected or got are type int, float or None, remove respective appostrophes.
    """
    error_msg = f"Incorrect {attr}! Expected "
    if isinstance(expected, int) or isinstance(expected, float) or expected == None:
        error_msg += f"{expected}"
    else:
        error_msg += f"'{expected}'"
    error_msg += ", got "
    if isinstance(got, int) or isinstance(got, float) or got == None:
        error_msg += f"{got}!"
    else:
        error_msg += f"'{got}'!"
    return error_msg

def compare_attributes(testcase:unittest.TestCase, dataclass_obj:MyDataClass, csv_data:list[str]):
    """
    Function is used to compare the input of a dataclass and its assigned values
    Compares each assigned attribute from csv data to assigned attributes.
    Paramters:
        testcase: unittest.TestCase; TestCase object parent running this comparison
        datclass_obj: MyDataClass; dataclass object to verify
        csv_data: list[str]; Data gotten from csv file
    Outputs:
        Raises AssertionError if any comparison fails
    """
    for i in range(len(dataclass_obj.data_fields)):
            dataclass_attribute = dataclass_obj.data_fields[i]
            testcase.assertTrue(hasattr(dataclass_obj, dataclass_attribute), f"Race object missing attribute '{dataclass_attribute}'!")
            attribute_value = getattr(dataclass_obj, dataclass_attribute)
            expected_value = csv_data[i]
            if expected_value.isnumeric():
                expected_value = int(expected_value)
            elif expected_value == "\\N":
                expected_value = None
            elif isFloat(expected_value): 
                expected_value = float(expected_value)
            testcase.assertTrue(attribute_value == expected_value, error_msg(dataclass_attribute, expected_value, attribute_value))

class TestGlobals(unittest.TestCase):
    """
    Testclass includes tests for functions and methods defined in globals.py and some auxiliary functions
    """

    def test_isFloat(self):
        """
        Tests isFloat() method.
        """
        string1 = "abcd" # Should fail
        self.assertFalse(isFloat(string1))
        string2 = "1024" # Should succeed
        self.assertTrue(isFloat(string2))
        string3 = "0.1A" # Should fail
        self.assertFalse(isFloat(string3))
        string4 = "54.321" # Should succeed
        self.assertTrue(isFloat(string4))

    def test_RemoveAccents(self):
        """
        Test that remove_accents() function works as expected.
        """
        removed_accents_map = {
            "Lewis Hamilton": "Lewis Hamilton",
            "Kimi Räikkönen": "Kimi Raikkonen",
            "ABCDÅÄÖ": "ABCDAAO",
            "Sergio Pérez": "Sergio Perez",
            "Nico Hülkenberg": "Nico Hulkenberg"
        }
        for accent_name in removed_accents_map.keys():
            expected_name = removed_accents_map[accent_name]
            self.assertTrue(remove_accents(accent_name) == expected_name,
                            f"'{accent_name}' should become '{expected_name}' when using remove_accents()!")
    
    def test_FindObjects_Correct(self):
        """
        Test that find_objects_by_field_value() works as expected when used correctly.
        """
        search_results = find_objects_by_field_value(TESTARCHIVE.drivers, "forename", "Alex")
        self.assertTrue(len(search_results) == 5, f"Incorrect number of search results! Expected 5 matches, got {len(search_results)}!")
        for result in search_results:
            self.assertTrue(hasattr(result, "forename"), f"Missing attribute!")
            self.assertTrue(result.forename == "Alex", f"Incorrect forename! Expected 'Alex', got '{result.forename}'")
    
    def test_FindObjects_Incorrect(self):
        """
        Test that find_objects_by_field_value() works as expected with incorrect input (raises error)
        """
        try:
            find_objects_by_field_value(TESTARCHIVE.drivers, "kills", 100)
        except Exception as e:
            self.assertTrue(isinstance(e, AssertionError), f"Incorrect use of find_objects_by_field_value() should raise AssertionError, not {type(e)}!")
            self.assertTrue(str(e) == "Object Driver has no field 'kills'!", "Incorrect error message!")

    def test_FindSingleObject_Correct(self):
        """
        Test that find_single_object_by_field_value() works as expected with correct inputs
        """
        search_result = find_single_object_by_field_value(TESTARCHIVE.circuits, "country", "sweden")
        self.assertTrue(search_result.country == "sweden", f"Incorrect location! Expected sweden, got {search_result.country}!")
    
    def test_FindSingleObject_Incorrect1(self):
        """
        Test that find_single_object_by_field_value() works as expected with incorrect input (raises error)
        """
        try:
            find_single_object_by_field_value(TESTARCHIVE.constructors, "money", 0)
        except Exception as e:
            self.assertTrue(isinstance(e, AssertionError), f"Incorrect use of find_objects_by_field_value() should raise AssertionError, not {type(e)}!")
            self.assertTrue(str(e) == "Object Constructor has no field 'money'!", "Incorrect error message!")

    def test_FindSingleObject_Incorrect2(self):
        """
        Test that find_objects_by_field_value() works as expected with more than 1 result (raises error)
        """
        try:
            find_single_object_by_field_value(TESTARCHIVE.circuits, "country", "united kingdom")
        except Exception as e:
            self.assertTrue(isinstance(e, AssertionError), f"Incorrect use of find_objects_by_field_value() should raise AssertionError, not {type(e)}!")
            self.assertTrue(str(e) == f"Incorrect number of objects found with field 'country' value 'united kingdom'! (Found 4)")

    def test_CountryConverter(self):
        cc = CountryConverter()
        testdemonyms = {"british": "united kingdom", "British": "united kingdom", "French": "france", "American": "united states"}
        for demonym in testdemonyms.keys():
            exp_country = testdemonyms[demonym]
            got_country = cc.demonym_to_country(demonym)
            self.assertTrue(got_country == exp_country, error_msg("country", exp_country, got_country))


class TestArchiveReader(unittest.TestCase):
    """
    Testclass includes tests for testing ArchiveReader class
    """

    def test_Reader(self):
        self.assertTrue(len(TESTARCHIVE.circuits) == 77)
        self.assertTrue(len(TESTARCHIVE.constructors) == 212)
        self.assertTrue(len(TESTARCHIVE.drivers) == 861)
        self.assertTrue(len(TESTARCHIVE.races) == 1125)
        self.assertTrue(len(TESTARCHIVE.seasons) == 75)


class TestMyDataClasses(unittest.TestCase):
    """
    Testclass includes tests for MyDataClass derivatives
    """
    def test_CircuitClass(self):
        myCircuit = Circuit()
        csv_data_line = ["4", "kymi_ring", "KymiRing", "Iitti", "finland", "60.877222", "26.481944", "76", "https://github.com/marcushattula/FormulaDoku"]
        myCircuit.read_data(csv_data_line)
        compare_attributes(self, myCircuit, csv_data_line)

    def test_ConstructorClass(self):
        """
        Test initializing constructor data class
        """
        myConstructor = Constructor()
        csv_data_line = ["10", "best_team", "Macke Team", "Finnish", "https://github.com/marcushattula/FormulaDoku"]
        myConstructor.read_data(csv_data_line)
        self.assertTrue(myConstructor.constructorId == 10, f"Incorrect constructorId! Expected 10, got {myConstructor.constructorId}!")
        self.assertTrue(myConstructor.constructorRef == "best_team", f"Incorrect constructorRef! Expected 'best_team', got {myConstructor.constructorRef}!")
        self.assertTrue(myConstructor.name == "Macke Team", f"Incorrect name! Expected 'Macke Team', got {myConstructor.name}!")
        self.assertTrue(myConstructor.nationality == "Finnish", f"Incorrect nationality! Expected 'Finnish', got {myConstructor.nationality}!")
        self.assertTrue(myConstructor.url == csv_data_line[4], f"Incorrect url! Expected {csv_data_line[4]}, got {myConstructor.url}!")
    
    def test_DriverClass(self):
        myDriver = Driver()
        csv_data_line = ["123", "macke", "23", "MAC", "The", "Macke", "2000-02-29", "Finnish", "https://github.com/marcushattula/FormulaDoku"]
        myDriver.read_data(csv_data_line)
        compare_attributes(self, myDriver, csv_data_line)

    def test_RaceClass(self):
        myRace = Race()
        csv_data_line = (
            '1108,2023,10,9,"British Grand Prix","2023-07-09","14:00:00","'
            'https://en.wikipedia.org/wiki/2023_British_Grand_Prix",'
            '"2023-07-07","11:30:00","2023-07-07","15:00:00","2023-07-08",'
            '"10:30:00","2023-07-08","14:00:00",\\N,\\N').split(',')
        myRace.read_data(csv_data_line)
        compare_attributes(self, myRace, csv_data_line)

    def test_SeasonClass(self):
        mySeason = Season()
        csv_data_line = ['2024', "https://github.com/marcushattula/FormulaDoku"]
        mySeason.read_data(csv_data_line)
        compare_attributes(self, mySeason, csv_data_line)

    def test_ResultClass(self):
        res = Result()
        driver1 = TESTARCHIVE.drivers[0] # Lewis Hamilton
        constructor1 = TESTARCHIVE.constructors[0] # McLaren
        status = dict(zip(RACE_RESULT_DATA_FIELDS,[57,20,1,1,22,3,13,"13",13,0,56,"\\N","\\N",25,19,"1:35.520","203.969",11]))
        res.add_entrant((driver1, constructor1),status)
        exp = "Lewis Hamilton-McLaren"
        self.assertTrue(str(res) == exp, error_msg("str method", exp, str(res)))
        self.assertTrue(len(res.entrants) == 1, error_msg("len method", 1, len(res.entrants)))
        self.assertTrue(len(res.data) == 1 and res.data[0] == status, "Incorrect status for Result object!")

    def test_mapStrFunction(self):
        wehrlein = TESTARCHIVE.drivers[835]
        self.assertTrue(wehrlein.map_to_string("get_career_data", field2="n_points") == "6.0")
        self.assertTrue(wehrlein.map_to_string("get_all_seasons_data", field2="n_entries") == "2016: 21, 2017: 18")


class TestQuestions(unittest.TestCase):
    """
    Testclass includes tests for Question class
    """

    def test_QuestionClass(self):
        question1 = new_question(1, questiontype=1, questionID=1001) # World championships: 1
        self.assertTrue(str(question1) == 'World championships: 1')
    
    def test_GetAnswers(self):
        question1 = new_question(1, 2, questionID=2000) # Driver nationality: German
        answers = question1.get_all_answers(TESTARCHIVE.drivers)
        self.assertTrue(len(answers) == 50, f"Incorrect number of answers! Expected 50, got {len(answers)}!")
        for driver in answers:
            self.assertTrue(driver.nationality == "German", f"Incorrect nationality! Expected German, got {driver.nationality}!")

    def test_GetMutualAnswers(self):
        question1 = new_question(1, 2, questionID=2202) # Drier nationality: Finnish
        question2 = new_question(1, 1, questionID=1000) # Race wins: 5
        mutual_answers = question1.get_mutual_answers(question2, TESTARCHIVE.drivers) # Valtteri, Kimi, Mika, Keke
        self.assertTrue(len(mutual_answers) == 4, error_msg("number of mutual answers", 4, len(mutual_answers)))

    def test_GetAllQuestions(self):
        questions = all_questions(0)
        question1 = new_question(1, questiontype=1, questionID=1001) # World championships: 1
        self.assertTrue(len(questions) > 30, "Found fewer questions than expected!")
        self.assertTrue(question1 in questions, "Expected question missing from all questions!")
        

class TestQuizClass(unittest.TestCase):
    """
    Testclass includes tests for Quiz class
    """

    def test_QuizInit(self):
        testquiz = QuizGame(TESTARCHIVE)
        self.assertTrue(testquiz.n_columns == 3, error_msg("n_columns", 3, testquiz.n_columns))
        self.assertTrue(testquiz.n_rows == 3, error_msg("n_rows", 3, testquiz.n_rows))
        self.assertTrue(testquiz.guesses == 9, error_msg("guesses", 9, testquiz.guesses))
        self.assertTrue(testquiz.difficulty == 3, error_msg("difficulty", 3, testquiz.difficulty))
    
    def test_DriverQuizFalseValidation(self):
        driverQuiz = DriverQuiz(TESTARCHIVE)
        driverQuiz.set_n_columns(2)
        driverQuiz.set_n_rows(1)
        question1 = new_question(1, 2, questionID=2000) # Driver nationality: German
        question2 = new_question(2, 3, questionID=3101) # Driven for team: Red Bull
        question3 = new_question(3, 3, questionID=3201) # Driven for team: Toro Rosso
        driverQuiz.set_row_question(0, question1)
        driverQuiz.set_col_question(0, question2)
        driverQuiz.set_col_question(1, question3)
        # This quiz is unsolveable, since only Vettel is a valid answer for both cells
        self.assertFalse(driverQuiz.full_validation())
    
    def test_DriverQuizTrueValidation(self):
        driverQuiz = DriverQuiz(TESTARCHIVE)
        driverQuiz.set_n_columns(2)
        driverQuiz.set_n_rows(2)
        question1 = DriverDataQuestion(1, setseed=123) # Driver nationality: German
        question2 = DriverDataQuestion(3, setseed=654) # Drier nationality: Finnish
        question3 = DriverAchievmentQuestion(1, setseed=1) # World championships: 1
        question4 = DriverTeamQuestion(1, setseed=5) # Driven for team: Ferrari
        driverQuiz.set_row_question(0, question1)
        driverQuiz.set_row_question(1, question2)
        driverQuiz.set_col_question(0, question3)
        driverQuiz.set_col_question(1, question4)
        self.assertTrue(driverQuiz.full_validation())
        valid_answers = {
            (0, 0): TESTARCHIVE.drivers[2],
            (0, 1): TESTARCHIVE.drivers[7],
            (1, 0): TESTARCHIVE.drivers[19],
            (1, 1): TESTARCHIVE.drivers[62]
        }
        self.assertTrue(driverQuiz.possible_answers == valid_answers)

    def test_DriverQuizLongValidation(self):
        driverQuiz = DriverQuiz(TESTARCHIVE)
        driverQuiz.set_n_columns(3)
        driverQuiz.set_n_rows(3)
        question1 = DriverDataQuestion(1, setseed=1234) # Driver nationality: French
        question2 = DriverDataQuestion(3, setseed=654) # Drier nationality: Finnish
        question3 = DriverDataQuestion(2, setseed=9) # Driver nationality: Australian
        question4 = DriverAchievmentQuestion(1, setseed=1) # World championships: 1
        driverQuiz.set_row_question(0, question1)
        driverQuiz.set_row_question(1, question2)
        driverQuiz.set_row_question(2, question3)
        driverQuiz.set_col_question(0, question4)
        driverQuiz.set_col_question(1, question4)
        driverQuiz.set_col_question(2, question4)
        # This quiz is unsolveable, since there are only two Australian champions
        self.assertFalse(driverQuiz.full_validation())


class TestQuizConstructorClass(unittest.TestCase):

    def test_ConstructorInit(self):
        qc = QuizConstructor(TESTARCHIVE)
        self.assertIsNone(qc.all_questions, "Constructor all_questions attribute should not be initialized yet!")
        self.assertIsNone(qc.quiz, "Constructor quiz attribute should not be initialized yet!")
        qc.create_quiz()
        self.assertTrue(all([isinstance(q, Question) for q in qc.all_questions]) and len(qc.all_questions) > 30
                        , "Found fewer questions than expected!")
        self.assertTrue(isinstance(qc.quiz, DriverQuiz), "Constructor quiz attribute should be of type DriverQuiz!")
        qg = qc.start_quiz()
        self.assertTrue(isinstance(qg, DriverQuiz), "Should have initiated driver quiz!")
    
    def test_SeededQuiz(self):
        qc = QuizConstructor(TESTARCHIVE, seed=7)
        qc.create_quiz()
        qg = qc.start_quiz()
        exp_col_q = ["Driver nationality: Canadian", "No wins", "Driver nationality: German"]
        exp_row_q = ["No pole positions", "Podiums: 10", "Pole positions: 5"]
        self.assertTrue(len(qg.col_questions) == 3, error_msg("col_questions", 3, len(qg.col_questions)))
        self.assertTrue(len(qg.row_questions) == 3, error_msg("row_questions", 3, len(qg.row_questions)))
        for i in range(3):
            got_col_q = qg.col_questions[i]
            self.assertTrue(str(got_col_q) == exp_col_q[i], f"Mismatching column question at index {i}!")
            got_row_q = qg.row_questions[i]
            self.assertTrue(str(got_row_q) == exp_row_q[i], f"Mismatching row question at index {i}!")


if __name__ == '__main__':
    unittest.main()