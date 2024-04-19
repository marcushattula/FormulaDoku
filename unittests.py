import unittest
import random

from readArchive import ArchiveReader
from globals import ARCHIVE_FILE, remove_accents, isFloat
from mydataclass import MyDataClass, find_objects_by_field_value, find_single_object_by_field_value
from circuit import Circuit
from constructor import Constructor
from driver import Driver
from race import Race
from season import Season
from question import DriverAchievmentQuestion, DriverDataQuestion, DriverTeamQuestion

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
    Testclass includes tests for functions and methods defined in globals.py
    """

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
        search_result = find_single_object_by_field_value(TESTARCHIVE.circuits, "country", "Sweden")
        self.assertTrue(search_result.country == "Sweden", f"Incorrect location! Expected Sweden, got {search_result.country}!")
    
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
            find_single_object_by_field_value(TESTARCHIVE.circuits, "country", "UK")
        except Exception as e:
            self.assertTrue(isinstance(e, AssertionError), f"Incorrect use of find_objects_by_field_value() should raise AssertionError, not {type(e)}!")
            self.assertTrue(str(e) == f"Incorrect number of objects found with field 'country' value 'UK'! (Found 4)")


class TestArchiveReader(unittest.TestCase):
    """
    Testclass includes tests for testing ArchiveReader class
    """

    def test_Reader(self):
        self.assertTrue(len(TESTARCHIVE.circuits) == 77)
        self.assertTrue(len(TESTARCHIVE.constructors) == 211)
        self.assertTrue(len(TESTARCHIVE.drivers) == 857)
        self.assertTrue(len(TESTARCHIVE.races) == 1101)
        self.assertTrue(len(TESTARCHIVE.seasons) == 74)


class TestMyDataClasses(unittest.TestCase):
    """
    Testclass includes tests for MyDataClass derivatives
    """
    def test_CircuitClass(self):
        myCircuit = Circuit()
        csv_data_line = ["4", "kymi_ring", "KymiRing", "Iitti", "Finland", "60.877222", "26.481944", "76", "https://github.com/marcushattula/FormulaDoku"]
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


class TestQuestions(unittest.TestCase):
    """
    Testclass includes tests for Question class
    """

    def test_QuestionClass(self):
        question1 = DriverAchievmentQuestion(1, setseed=1) # World championships: 1
        self.assertTrue(str(question1) == 'World championships: 1')
    
    def test_GetAnswers(self):
        question1 = DriverDataQuestion(1, setseed=123) # Driver nationality: German
        answers = question1.get_all_answers(TESTARCHIVE.drivers)
        self.assertTrue(len(answers) == 50, f"Incorrect number of answers! Expected 50, got {len(answers)}!")
        for driver in answers:
            self.assertTrue(driver.nationality == "German", f"Incorrect nationality! Expected German, got {driver.nationality}!")


class TestQuizClass(unittest.TestCase):
    """
    Testclass includes tests for Quiz class
    """

    def test_QuizClass(self):
        # TODO: Implement
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()