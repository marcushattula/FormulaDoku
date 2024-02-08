from mydataclass import MyDataClass

CONSTRUCTOR_DATA_FIELDS = ["constructorId","constructorRef","name","nationality","url"]

class Constructor(MyDataClass):

    def __init__(self):
        for data_field in CONSTRUCTOR_DATA_FIELDS:
            setattr(self, data_field, None)
        self.drivers = []
    
    def read_data(self, data:list[str]):
        assert len(data) == len(CONSTRUCTOR_DATA_FIELDS), f"Unsupported number of fields! Must be {len(CONSTRUCTOR_DATA_FIELDS)}, found {len(data)}!"
        for i in range(len(data)):
            setattr(self,CONSTRUCTOR_DATA_FIELDS[i], data[i])