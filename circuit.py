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
        self.data_fields = CIRCUIT_DATA_FIELDS
        for data_field in self.data_fields:
            setattr(self, data_field, None)
    
    def read_data(self, data:list[str]):
        self.read_csv_data(data)
        self.country = self.country.lower()

