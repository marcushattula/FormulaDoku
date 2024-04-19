import os
from unicodedata import normalize

PROJECT_NAME = "FormulaDoku"

GLOBALSFILE = os.path.abspath(__file__) # Path to this file
HOMEDIR = os.path.dirname(GLOBALSFILE) # Path to home directory, that is the parent directory of this file

TEMP_DIRNAME = "temps" # Name of folder where to output extracted data from archive
TEMP_DIRPATH = os.path.join(HOMEDIR, TEMP_DIRNAME) # Extracted data archive directory path

ARCHIVE_FILE = os.path.join(HOMEDIR, "archive.zip") # Path to archive file
DEFAULT_PICTURE = os.path.join(HOMEDIR, "default.jpg")

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
