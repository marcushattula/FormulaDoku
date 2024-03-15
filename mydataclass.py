class MyDataClass():
    """
    Parent class for inheritance by dataclasses.
    """

    def __init__(self):
        """
        Initializes empty class where all fields are set to None or empty lists.
        """
        self.data_fields = []
    
    def __eq__(self, other_obj):
        return str(self) == str(other_obj)
    
    def __hash__(self):
        return hash(str(self))
    
    def map_to_string(self, field1:str, field2:str=None) -> str:
        """
        Get any field of this object and map according to other fields
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
        assert hasattr(self, field), f"Object {self.__class__.__name__} has no field {field}!"
        return getattr(self, field)
