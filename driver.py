from mydataclass import MyDataClass

DRIVER_DATA_FIELDS = ["driverId","driverRef","number","code","forename","surname","dob","nationality","url"]
DRIVER_CAREER_DATA = ["championships","wins","podiums","career_points","poles","entries","sprint_wins"]

class Driver(MyDataClass):
    """
    Dataclass for storing results of a driver.
    """

    def __init__(self):
        """
        Initializes empty class where all fields are set to None or empty lists.
        """
        for data_field in DRIVER_DATA_FIELDS:
            setattr(self, data_field, None)
        for data_field in DRIVER_CAREER_DATA:
            setattr(self, data_field, 0)
        self.teams = []
        self.teammates = []
        self.season_data = {}
    
    def __str__(self):
        """
        Returns full name of driver
        """
        return self.fullname
    
    def read_data(self, data:list[str]):
        """
        Adds data from CSV to this drivers data
        """
        assert len(data) == len(DRIVER_DATA_FIELDS), f"Unsupported number of fields! Must be {len(DRIVER_DATA_FIELDS)}, found {len(data)}!"
        for i in range(len(data)):
            setattr(self,DRIVER_DATA_FIELDS[i], data[i])
        self.fullname = self.forename + " " + self.surname

    def add_to_season_data(self, year:str, field:str, value:float):
        """
        Adds data from a season to drivers statistics.
        """
        assert year.isnumeric(), f"Year must be numeric, currently {year}!"
        assert isinstance(value, float) or isinstance(value, int), f"Value must be int or float, currently {type(value)}!"
        if not year in self.season_data:
            self.season_data[year] = {"wins":0,"podiums":0,"points":0,"poles":0,"entries":0,"sprint_wins":0}
        assert field in self.season_data[year], f"Unknown field {field}!"
        self.season_data[year][field] += value

    def add_teammate(self, teammate):
        """
        Adds other driver to self.teammates
        Parameters:
            teammate: Driver; This drivers teammate. Must be of class Driver.
        Outputs:
            Adds teammate to self.teammates if not already present.
        """
        assert isinstance(teammate, Driver), "Teammate must be of class Driver!"
        if teammate not in self.teammates:
            self.teammates.append(teammate)
