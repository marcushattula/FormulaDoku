import os
from mydataclass import MyDataClass
from driver import Driver, DRIVER_CAREER_DATA, DRIVER_DATA_FIELDS
from constructor import Constructor
from circuit import Circuit
from race import Race
from question import new_question, Question
from unicodedata import normalize

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

PROJECT_NAME = "FormulaDoku"

GLOBALSFILE = os.path.abspath(__file__) # Path to this file
HOMEDIR = os.path.dirname(GLOBALSFILE) # Path to home directory, that is the parent directory of this file

TEMP_DIRNAME = "temps" # Name of folder where to output extracted data from archive
TEMP_DIRPATH = os.path.join(HOMEDIR, TEMP_DIRNAME) # Extracted data archive directory path

ARCHIVE_FILE = os.path.join(HOMEDIR, "archive.zip") # Path to archive file

def find_objects_by_field_value(obj_list: list[MyDataClass], field_name:str, field_value, strict:bool=True) -> list[MyDataClass]:
    """
    Find all objects with a certain value in a given field
    Parameters:
        obj_list: list[MyDataClass]; list of objects to be searched through
        field_name: str; name of field to be searched in
        field_value: int or str; value or string to be found in given field
        (Optional) strict: bool; Be strict with capitalization or diacritics. Default = True
    Outputs:
        matching_obj_list: list[MyDataClass]; list of all objects that meet the given criteria.
    """
    matching_obj_list = []
    for obj in obj_list:
        obj_value = obj.get_field(field_name)
        if  obj_value == field_value or (not strict and isinstance(obj_value, str) and remove_accents(obj_value).lower() == remove_accents(field_value).lower()):
            matching_obj_list.append(obj)
    return matching_obj_list

def find_single_object_by_field_value(obj_list: list[MyDataClass], field_name:str, field_value:str, strict:bool=True) -> MyDataClass:
    """
    Find one object with a certain value in a given field
    Parameters:
        obj_list: list[MyDataClass]; list of objects to be searched through
        field_name: str; name of field to be searched in
        field_value: str; value or string to be found in given field
        (Optional) strict: bool; Be strict with capitalization or diacritics. Default = True
    Outputs:
        matching_obj: MyDataClass; object that meets the given criteria.
    """
    candidates = find_objects_by_field_value(obj_list, field_name, field_value, strict=strict)
    assert len(candidates) == 1, f"Incorrect number of objects found with field {field_name} value {field_value}! (Found {len(candidates)})"
    return candidates[0]
