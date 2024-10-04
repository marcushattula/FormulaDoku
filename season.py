from mydataclass import MyDataClass
from driver import Driver
from constructor import Constructor
from race import Race

SEASON_DATA_FIELDS = ["year","url"]

POINTS_SYSTEMS = [
     [8, 6, 4, 3, 2], # 1950 - 1959
     [8, 6, 4, 3, 2, 1], # 1960 (& 1961 constructors)
     [9, 6, 4, 3, 2, 1], # 1961 - 1990 (& 1960 drivers)
     [10, 6, 4, 3, 2, 1], # 1991 - 2002
     [10, 8, 6, 5, 4, 3, 2, 1], # 2003 - 2009
     [25, 18, 15, 12, 10, 8, 6, 4, 2, 1], # 2010 -
]

class Season(MyDataClass):

    def __init__(self):
        """
        Initializes season class
        """
        self.data_fields = SEASON_DATA_FIELDS
        self.races: list[Race] = []
        self.season_data = {} # driver: season_data
        self.driver_standings = {}
        self.constuctor_standings = {}
        self.champion = None
    
    def __str__(self):
        """
        String function override. Returns "{year} Formula One World Championship"
        """
        return f"{str(self.year)} Formula One World Championship"

    def read_data(self, data:list[str]):
        """
        Adds data from CSV to this season data
        """
        self.read_csv_data(data)
        if isinstance(self.year, str) and self.year.isnumeric():
            self.year = int(self.year)
        assert isinstance(self.year, int), "Year must be integer!"

    def add_race(self, race:Race) -> None:
        """
        Add a race to this season
        Parameters:
            race: Race; Race to be added to this season
        Outputs:
            Adds race to self.races
        """
        assert isinstance(race, Race), "Race must be of type Race!"
        assert race not in self.races, "Race already added!"
        assert hasattr(race, "round") and isinstance(race.round, int) and race.round, "Race missing round"
        while race.round > len(self.races):
            self.races.append(None)
        self.races[race.round-1] = race

    def select_race_points_system(self, drivers_champ:bool=True) -> list[int]: 
        """
        Return which points system to use for each year
        Parameters:
            None
        Outputs:
            points_system: list[int]; Points awarded per position, i.e. P1 ->
        """
        year = int(self.year)
        assert year >= 1950, "Invalid year"
        if year >= 2010:
            return POINTS_SYSTEMS[5]
        elif year >= 2003:
            return POINTS_SYSTEMS[4]
        elif year >= 1991:
            return POINTS_SYSTEMS[3]
        elif year >= 1962:
            return POINTS_SYSTEMS[2]
        elif year >= 1960:
            if year == 1961 and drivers_champ:
                return POINTS_SYSTEMS[2]
            return POINTS_SYSTEMS[1]
        elif year >= 1950:
            return POINTS_SYSTEMS[0]
        else:
            raise AssertionError("WTF???")

    def select_sprint_points_system(self) -> list[int]:
        """
        Return which sprint points system to use for each year
        Parameters:
            None
        Outputs:
            points_system: list[int]; Points awarded per position, i.e. P1 ->
        """
        year = int(self.year)
        assert year >= 2021, "Invalid year"
        if year == 2021:
            return [3, 2, 1]
        elif year >= 2022:
            return [8, 7, 6, 5, 4, 3, 2, 1]

    def award_points(self, pointssystem=None, fastest_lap_points:int=None):
        """
        Award the points for each race in this season to the drivers
        Parameters:
            pointssystem: int | list[int] | None; Which points system to use. Default = None = Automatic
            fastest_lap_points: int | None; How many points to award for fastest lap. Default = None = Automatic
        Outputs:
            Gives each entrant driver and constructor the points they scored each race this season
        """

        assert len(self.races) > 0, "Season not initialized!"
        assert all([isinstance(race, Race) for race in self.races]), "Wrong formatting in races list!"
        
        # Get points system
        if pointssystem == None:
            points_arr_driver = self.select_race_points_system()
            points_arr_constructor = self.select_race_points_system(drivers_champ=False)
        elif isinstance(pointssystem, list) and len(pointssystem) > 0 and all([isinstance(x, int) for x in pointssystem]):
            points_arr_driver = pointssystem
            points_arr_constructor = pointssystem
        elif isinstance(pointssystem, int):
            assert 0 <= pointssystem < len(POINTS_SYSTEMS), "Out of range"
            points_arr_driver = POINTS_SYSTEMS[pointssystem]
            points_arr_constructor = POINTS_SYSTEMS[pointssystem]
        else:
            raise AssertionError("WTF???")
        
        # Update standings accoring to results of each race
        for race in sorted(self.races, key=lambda r: r.round):
            driver_points = race.calculate_driver_points(points_arr_driver, fastest_lap_points)
            constructor_points = race.calculate_constructor_points(points_arr_constructor, fastest_lap_points)
            for entrant in driver_points.keys():
                if entrant in self.driver_standings.keys():
                    self.driver_standings[entrant] += driver_points[entrant]
                else:
                    self.driver_standings[entrant] = driver_points[entrant]
            for constructor in constructor_points:
                if constructor in self.constuctor_standings:
                    self.constuctor_standings[constructor] += constructor_points[constructor]
                else:
                    self.constuctor_standings[constructor] = constructor_points[constructor]

        # Award championships
        self.champion = max(self.driver_standings, key=lambda driver: self.driver_standings[driver])