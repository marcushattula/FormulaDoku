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
    
    def get_field(self, field:str):
        """
        Fetch a value of a certain field. Assertion protected.
        Parameters:
            field: str; name of field to search.
        Outputs:
            attr: ?; value stored in field, equivalent to self."field"
        """
        assert hasattr(self, field), f"Object {self.__class__.__name__} has no field {field}!"
        return getattr(self, field)
