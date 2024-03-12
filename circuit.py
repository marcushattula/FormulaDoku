from mydataclass import MyDataClass

CIRCUIT_DATA_FIELDS = ["circuitId","circuitRef","name","location","country","lat","lng","alt","url"]

class Circuit(MyDataClass):
    """
    Dataclass for storing data of a circuit.
    """

    def __init__(self):
        """
        Initializes empty class where all fields are set to None or empty lists.
        """
        for data_field in CIRCUIT_DATA_FIELDS:
            setattr(self, data_field, None)
    
    def __str__(self):
        return self.name
    
    def read_data(self, data:list[str]):
        assert len(data) == len(CIRCUIT_DATA_FIELDS), f"Unsupported number of fields! Must be {len(CIRCUIT_DATA_FIELDS)}, found {len(data)}!"
        for i in range(len(data)):
            setattr(self,CIRCUIT_DATA_FIELDS[i], data[i])

