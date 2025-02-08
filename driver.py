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
        self.country = self.cc.demonym_to_country(self.nationality.strip())

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
        if teammate != self and teammate not in self.teammates:
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
        return self.get_all_seasons_data()[year]
    
    def get_all_seasons_data(self):
        if hasattr(self, "_all_seasons_data") and self._all_seasons_data:
            return self._all_seasons_data
        all_season_data = {}
        for season_year in self.season_entries.keys():
            season = self.season_entries[season_year]
            all_season_data[season_year] = season.get_driver_stats(self)
        self._all_seasons_data = all_season_data
        return self.get_all_seasons_data()

    def get_career_data(self):
        """
        Get the combined results of this driver
        Parameters:
            None
        Outputs:
            career_data: dict; dictionary with the following fields:
        """
        if hasattr(self, "_career_data") and self._career_data:
            return self._career_data
        career_results = {
            "n_championships": 0,
            "n_entries": 0,
            "n_wins": 0,
            "n_podiums": 0,
            "n_poles": 0,
            "n_points": 0,
            "n_sprint_entries": 0,
            "n_sprint_wins": 0,
            "n_sprint_podiums": 0,
            "n_sprint_poles": 0
        }
        for season_year in self.season_entries.keys():
            season_data = self.get_season_data(season_year)
            career_results["n_championships"] += season_data["champion"]
            career_results["n_entries"] += season_data["n_entries"]
            career_results["n_wins"] += season_data["n_wins"]
            career_results["n_podiums"] += season_data["n_podiums"]
            career_results["n_poles"] += season_data["n_poles"]
            career_results["n_points"] += season_data["n_points"]
            career_results["n_sprint_entries"] += season_data["n_sprint_entries"]
            career_results["n_sprint_wins"] += season_data["n_sprint_wins"]
            career_results["n_sprint_podiums"] += season_data["n_sprint_podiums"]
            career_results["n_sprint_poles"] += season_data["n_sprint_poles"]
        self._career_data = career_results
        return self.get_career_data()
    