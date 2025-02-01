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
        self.data_fields = DRIVER_DATA_FIELDS
        for data_field in self.data_fields:
            setattr(self, data_field, None)
        for data_field in DRIVER_CAREER_DATA:
            setattr(self, data_field, 0)
        self.teams = []
        self.teammates = []
        self.season_data = {}
        self.race_entries = {}
        self.season_entries = {}
    
    def __str__(self):
        """
        Returns full name of driver
        """
        return self.fullname
    
    def read_data(self, data:list[str]):
        """
        Adds data from CSV to this drivers data
        """
        self.read_csv_data(data)
        self.fullname = self.forename + " " + self.surname

    def add_to_season_data(self, year:int, field:str, value:float):
        """
        Adds data from a season to drivers statistics.
        """
        assert isinstance(value, float) or isinstance(value, int), f"Value must be int or float, currently {type(value)}!"
        if not year in self.season_data:
            self.season_data[year] = {"wins":0,"podiums":0,"points":0,"poles":0,"entries":0,"sprint_wins":0,"teammates":[]}
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

    def add_race_to_data(self, race):#: Race):
        """
        Add all relevant data from a race to this driver's data
        Parameters:
            race: Race; Race class to read data from
        Outputs:
            Adds data to self
        """
        #assert isinstance(race, Race), "Input race must be of race type!"
        year = race.year
        if year in self.race_entries.keys():
            self.race_entries[year].append(race)
        else:
            self.race_entries[year] = [race]

    def add_season_to_data(self, season):
        """
        Add a season to this driver's data
        Parameters:
            season: Season; season object
        Outputs:
            Adds data to self
        """
        year = season.year
        self.season_entries[year] = season

    
    def get_season_data(self, year:int):
        """
        Get the results of this driver for a given year
        Parameters:
            year: int; the year to get the results of
        Outputs:
            results: dict; dictionary with the following fields:
                champion: bool
                entries: list[Race]
                teammates: list[Driver]
                wins: list[int]
                podiums: list[int]
                poles: list[int]
                points: list[int]
        """
        season = self.season_entries[year]
        results = {
            "champion": season.champion[0] == self,
        }
        # TODO: Finish implementing
    
    def get_carreer_data(self):
        """
        Get the combined results of this driver
        Parameters:
            None
        Outputs:
            career_data: dict; dictionary with the following fields:
        """