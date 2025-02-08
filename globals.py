import os
from csv import reader
from unicodedata import normalize

PROJECT_NAME = "FormulaDoku"

GLOBALSFILE = os.path.abspath(__file__) # Path to this file
HOMEDIR = os.path.dirname(GLOBALSFILE) # Path to home directory, that is the parent directory of this file

TEMP_DIRNAME = "temps" # Name of folder where to output extracted data from archive
TEMP_DIRPATH = os.path.join(HOMEDIR, TEMP_DIRNAME) # Extracted data archive directory path

ARCHIVE_FILE = os.path.join(HOMEDIR, "archive2.zip") # Path to archive file
DEFAULT_PICTURE = os.path.join(HOMEDIR, "default.jpg")

DEMONYM_CSV = os.path.join(HOMEDIR, "demonyms.csv")

def remove_accents(input_str:str):
    """
    Remove accents, diacritics etc. from string.
    Parameters:
        input_str: str; String to remove accents and diacritics from
    Outputs:
        only_ascii: str; String with removed accents and diacritics, e.g. "Räikkönen" -> "Raikkonen"
    """
    nfkd_form = normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return str(only_ascii, 'utf-8')

def isFloat(input_str:str) -> bool:
    """
    Check if input string is decimal number, i.e. can be turned into float
    Parameters:
        input_str: str; string to be tested
    Outputs:
        b: bool; True if input string can be converted to float, else False
    """
    try:
        float(input_str)
    except ValueError:
        return False
    else:
        return True

def sumWithNone(num_list:list) -> float:
    """
    Sum list with numbers and nones
    Parameters:
        num_list: list[int | float | None]; list of ints, floats and None to be summed
    Outputs:
        sum: int; sum of num_list, with None mapped to 0
    """
    return sum([0 if x == None else x for x in num_list])

class CountryConverter():

    def __init__(self, demonym_csv_path=DEMONYM_CSV):
        self.demonym_csv = demonym_csv_path
        self.demonyms = {}
        with open(self.demonym_csv, encoding="utf-8") as demonym_file:
            r = reader(demonym_file)
            for row in r:
                self.demonyms[remove_accents(row[0].lower().strip())] = remove_accents(row[1].lower().strip())


    def demonym_to_country(self, demonym:str) -> str:
        """
        Converts demonym to country of origin. E.g. "French" -> "France"
        Parameters:
            demonym: str; demonym to convert
        Output:
            country: str; country name
        """
        return self.demonyms[demonym.lower()]

    def country_to_demonym(self, country:str) -> str:
        """
        Converts country to demonym. E.g. "France" -> "French"
        Parameters:
            country: str; country name to convert
        Output:
            demonym: str; demonym of country
        """
        raise NotImplementedError()
