class MyDataClass():

    def __init__(self):
        self.data_fields = []
    
    def get_field(self, field:str):
        assert hasattr(self, field), f"Object {self.__class__.__name__} has no field {field}!"
        return getattr(self, field)
