from mydataclass import MyDataClass

CONSTRUCTOR_DATA_FIELDS = ["constructorId","constructorRef","name","nationality","url"]

class Constructor(MyDataClass):
    """
    Dataclass for storing results of a constructor.
    """

    def __init__(self):
        """
        Initializes empty class where all fields are set to None or empty lists.
        """
        self.data_fields = CONSTRUCTOR_DATA_FIELDS
        for data_field in self.data_fields:
            setattr(self, data_field, None)
        self.drivers = []
    
    def __str__(self):
        return self.name
    
    def read_data(self, data:list[str]):
        """
        Map data from driver csv to this driver.
        Parameters:
            data: list[str]; Array created from line in csv. Fields are (in order):
                constructorId: number that is unique for this team
                constructorRef: name that is unique for this team
                name: official name of team
                nationality: country where team is registered
                url: wikipedia link
        Outputs:
            Adds data fields as attributes to this object.
        """
        self.read_csv_data(data)
    