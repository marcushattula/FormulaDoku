from webbrowser import open
from globals import *

class MyDataClass():
    """
    Parent class for inheritance by dataclasses.
    """
    cc = CountryConverter()

    def __init__(self):
        """
        Initializes empty class where all fields are set to None or empty lists.
        """
        self.data_fields = []

    def __str__(self):
        assert hasattr(self, "name"), "Missing name attribute!"
        return self.name

    def __repr__(self):
        return f"{self.__class__.__name__}: {str(self)}"

    def __eq__(self, other_obj):
        return str(self) == str(other_obj)
    
    def __hash__(self):
        return hash(str(self))

    def read_csv_data(self, data:list[str]):
        """
        Read data directly from csv file. If numeric, make into integer
        Parameters:
            data: list[str]; Data from csv, matching row
        Outputs:
            Sets data from csv according to self.data_fields, defined in subclasses
        """
        assert len(data) == len(self.data_fields), f"Unsupported number of fields! Must be {len(self.data_fields)}, found {len(data)}!"
        for i in range(len(data)):
            temp = data[i]
            if temp.isnumeric():
                temp = int(temp)
            elif isFloat(temp):
                temp = float(temp)
            elif temp == "\\N":
                temp = None
            setattr(self,self.data_fields[i], temp)

    def map_to_string(self, field1:str, field2=None) -> str:
        """
        Get any field of this object and map according to other fields, field1 may be callable
        Example:
            if self.field1 is list of objects [a, b, c]:
                return "{a.field2}, {b.field2}, {c.field2}"
            elif self.field1 is dict of dicts: {a: {field2: 1, field3: 2}, b: {field2: 3, field3: 4}}
                return "{a}: {a[field2]}, {b}: {b[field2]}"
            elif self.field1 is dict:
                return str(self.field1[field2])
            else:
                return str(self.field1)
        Parameters:
            field1: str; attribute name to retrieve
            (Optional) field2: str | int; subfield to map or filter by
        Outputs:
            s: str; string of mapped fields
        """
        if field1 == "":
            return ""
        mappable = self.get_field(field1)
        if callable(mappable):
            mappable = mappable()
        if isinstance(mappable, list):
            if isinstance(field2, int):
                return str(mappable[field2])
            elif isinstance(field2, str) and all([hasattr(x, field2) for x in mappable]):
                return ", ".join([x.get_field(field2) for x in mappable])
            else:
                return ""
        elif isinstance(mappable, dict) and all([(isinstance(mappable[x], dict) and field2 in mappable[x]) for x in mappable.keys()]):
            return ", ".join([f"{str(x)}: {str(mappable[x][field2])}" for x in mappable.keys()])
        elif isinstance(mappable, dict) and field2 in mappable.keys():
            return str(mappable[field2])
        else:
            return str(mappable)

    def get_field(self, field:str):
        """
        Fetch a value of a certain field. Assertion protected.
        Parameters:
            field: str; name of field to search.
        Outputs:
            attr: Any; value stored in field, equivalent to self."field"
        """
        assert hasattr(self, field), f"Object {self.__class__.__name__} has no field '{field}'!"
        return getattr(self, field)

    def wiki(self) -> None:
        assert hasattr(self, "url") and self.url, "Obect missing url!"
        open(self.url, new=0, autoraise=True)


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

def find_single_object_by_field_value(obj_list: list[MyDataClass], field_name:str, field_value, strict:bool=True) -> MyDataClass:
    """
    Find one object with a certain value in a given field
    Parameters:
        obj_list: list[MyDataClass]; list of objects to be searched through
        field_name: str; name of field to be searched in
        field_value: Any; value or string to be found in given field
        (Optional) strict: bool; Be strict with capitalization or diacritics. Default = True
    Outputs:
        matching_obj: MyDataClass; object that meets the given criteria.
    """
    candidates = find_objects_by_field_value(obj_list, field_name, field_value, strict=strict)
    assert len(candidates) == 1, f"Incorrect number of objects found with field '{field_name}' value '{field_value}'! (Found {len(candidates)})"
    return candidates[0]
