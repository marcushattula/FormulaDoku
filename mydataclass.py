from webbrowser import open

class MyDataClass():
    """
    Parent class for inheritance by dataclasses.
    """

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
        # TODO: Move to globals.py to improve imports!
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

    def map_to_string(self, field1:str, field2:str=None) -> str:
        """
        Get any field of this object and map according to other fields
        Example:
            if self.field1 is str or int:
                return str(self.field1)
            elif self.field1 is list of objects [a, b, c]:
                return "{a.field2}, {b.field2}, {c.field2}"
            elif self.field1 is dict of dicts: {a: {field2: 1, field3: 2}, b: {field2: 3, field3: 4}}
                return "{a}: {a[field2]}, {b}: {b[field2]}"
        Parameters:
            field1: str; attribute name to retrieve
            (Optional) field2: str; subfield to map or filter by
        Outputs:
            s: str; string of mapped fields
        """
        assert hasattr(self, field1), f"Object {self.__class__.__name__} has no field {field1}!"
        field_value = self.get_field(field1)
        if isinstance(field_value, list):
            assert field2 != None, "Missing parameter field2!"
            str_arr = self.get_multiple_fields_map(field1, field2)
            return ", ".join([str(obj) for obj in str_arr])
        elif isinstance(field_value, dict):
            assert field2 != None, "Missing parameter field2!"
            str_arr = self.get_dict_fields_map(field1, field2)
            return ", ".join([str(obj) for obj in str_arr])
        else:
            return str(field_value)

    def get_multiple_fields_map(self, field1:str, field2:str) -> list:
        """
        Map list of objects to certain field
        Example:
            self.some_list = [a, b, c]
            =>
            self.get_multiple_fields_map('some_list', 'name')
            = [a.name, b.name, c.name]
        Parameters:
            field1: str; field of this object containing list of objects
            field2: str; field to map each object to
        Outputs:
            mapped_list: list[any]; list of objects in self.field1 mapped to field2
        """
        field_list = self.get_field(field1)
        assert isinstance(field_list, list), f"Object {self.__class__.__name__} attribute {field1} is not of type list!"
        assert hasattr(field_list[0], field2), f"Object {field_list[0].__class__.__name__} has no field {field2}!"
        return [obj.get_field(field2) for obj in field_list]

    def get_dict_fields_map(self, field1, field2) -> list:
        """
        Map dictionary to dictionary key
        Example:
            self.some_dict =   {'a': {'x': 0, 'y': 1, 'z': 2},
                                'b': {'x': 3, 'y': 4, 'z': 5},
                                'c': {'x': 6, 'y': 7, 'z': 8}}
            =>
            self.get_dict_fields_map('some_dict', 'y')
            = ['a: 1', 'b: 4', 'c: 7']
        Parameters:
            field1: str; attribute name of dictionary
            field2: str; sub dictionary key to search for
        Outputs:
            mapped_list: list; list of subdictionary keys mapped
        """
        field_dict = self.get_field(field1)
        assert isinstance(field_dict, dict), f"Object {self.__class__.__name__} attribute {field1} is not of type dict!"
        mapped_list = []
        for key in field_dict.keys():
            subdict = field_dict[key]
            assert isinstance(subdict, dict), "Sub-dictionary must be of instance dictionary!"
            assert field2 in subdict.keys(), f"'{field2}' is not a key of sub-dictionary!"
            mapped_list.append(str(key) + ": " + str(subdict[field2]))
        return mapped_list   

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
