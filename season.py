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

SPRINT_POINTS_SYSTEMS = [
    [0], # 1950 - 2020
    [3, 2, 1], # 2021
    [8, 7, 6, 5, 4, 3, 2, 1]
]

BEST_OF_N_CHAMPION = [
    (4), # 1950-1953
    (5), # 1954-1957, 1959, 1961-1962, 1966
    (6), # 1958, 1960, 1963-1965
    ((5,6),(4,5)), # 1967, 1969
    ((5,6),(5,6)), # 1968, 1972
    ((6,7),(5,6)), # 1970-1971
    ((7,8),(6,7)), # 1973, 1975
    ((7,8),(7,8)), # 1974, 1976, 1978
    ((8,9),(7,8)), # 1977
    ((4,7),(4,8)), # 1979
    ((5,7),(5,7)), # 1980
    (10), # 1981
    (11), # 1982-1990
    (0), # 1991-
]

FASTEST_LAP_POINTS = 1
RECURSION_LIMIT = 50

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

    def get_results(self, driver:Driver) -> list[int]:
        """
        Return the finishing positions of a driver
        """
        return [race.get_position(driver) for race in self.races]

    def get_points(self, driver:Driver) -> list[int]:
        """
        Return the points scored from each race for a driver
        """
        points_per_race = []
        for race in self.races:
            race_driver_points = race.points_per_driver
            if driver in race_driver_points.keys():
                points = race_driver_points[driver]# if race_driver_points[driver] != None else 0
                points_per_race.append(points)
            else:
                points_per_race.append(None)
        return points_per_race

    def get_all_driver_points(self):
        """
        Get the finishing position of each driver for every race
        """
        full_standings = {}
        for entrant in self.driver_standings.keys():
            full_standings[entrant] = self.get_points(entrant)
        return full_standings

    def get_driver_stats(self, driver:Driver) -> dict:
        """
        Get the stats of a driver for a season, regardless of team
        Parameters:
            driver: Driver; entrant to get stats of
        Outputs:
            driverstats: dict; dictionary with the following key-value pairs:

        """
        entrants = [entrant for entrant in self.driver_standings.keys() if entrant[0].fullname == driver.fullname]
        # TODO: Finish implementing

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
        if 1950 <= year <= 2020:
            return SPRINT_POINTS_SYSTEMS[0]
        elif year == 2021:
            return SPRINT_POINTS_SYSTEMS[1]
        elif year >= 2022:
            return SPRINT_POINTS_SYSTEMS[2]

    def select_fastest_lap_points(self) -> tuple[int, int]:
        """
        Return how many points to score for fastest lap and eligibility
        Parameters:
            None
        Outputs:
            t: tuple[int, int]; tuple of points and position eligibility for fastest lap, 0 means any position
        """
        year = int(self.year)
        assert year >= 1950, "Invalid year"
        if year >= 2019:
            return (1, 10)
        elif 1950 <= year <= 1959:
            return (1, 0)
        else:
            return (0, 0)

    def select_champion_method(self):
        """
        Select which method to use to determine champion
        Parameters:
            None
        Outputs:
            best_of_n: Any; championship determining parameter
        """
        year = self.year
        assert year >= 1950, "Invalid year!"
        if 1950 <= year <= 1953:
            return BEST_OF_N_CHAMPION[0]
        elif year in [1954, 1955, 1956, 1957, 1959, 1961, 1962, 1966]:
            return BEST_OF_N_CHAMPION[1]
        elif year in [1958, 1960, 1963, 1964, 1965]:
            return BEST_OF_N_CHAMPION[2]
        elif year in [1967, 1969]:
            return BEST_OF_N_CHAMPION[3]
        elif year in [1968, 1972]:
            return BEST_OF_N_CHAMPION[4]
        elif year in [1970, 1971]:
            return BEST_OF_N_CHAMPION[5]
        elif year in [1973, 1975]:
            return BEST_OF_N_CHAMPION[6]
        elif year in [1974, 1976, 1978]:
            return BEST_OF_N_CHAMPION[7]
        elif year == 1977:
            return BEST_OF_N_CHAMPION[8]
        elif year == 1979:
            return BEST_OF_N_CHAMPION[9]
        elif year == 1980:
            return BEST_OF_N_CHAMPION[10]
        elif year == 1981:
            return BEST_OF_N_CHAMPION[11]
        elif 1982 <= year <= 1990:
            return BEST_OF_N_CHAMPION[12]
        elif 1991 <= year:
            return BEST_OF_N_CHAMPION[13]
        else:
            raise AssertionError("WTF??")       

    def update_standings(self) -> list[Driver]:
        """
        Resolve a tie between two drivers with the same number of points
        Parameters:
            driverarr: list[Driver]; list of drivers in tie to be resolved
        Outputs:
            tiebroken: list[Driver]; list of drivers after tie break resolved, from higher position to lower
        """

        def tiebreaker(driverarr:list[Driver], finish_pos=1) -> list[Driver]:
            """
            Resolve a tie between drivers with the same number of points
            """
            try:
                ordered = []
                if isinstance(driverarr, list) and len(driverarr) == 1:
                    return driverarr[0]
                elif finish_pos > RECURSION_LIMIT:
                    raise RecursionError("Unresolved tie")
                pos_finishes = {}
                for driver in driverarr:
                    n_finishes = self.get_results(driver).count(finish_pos)
                    if n_finishes in pos_finishes:
                        pos_finishes[n_finishes].append(driver)
                    else:
                        pos_finishes[n_finishes] = [driver]
                for n_finish in sorted(pos_finishes.keys(), reverse=True):
                    if len(pos_finishes[n_finish]) == 1:
                        ordered.append(pos_finishes[n_finish][0])
                    else:
                        ordered.extend(tiebreaker(pos_finishes[n_finish], finish_pos=finish_pos+1))
                return ordered
            except RecursionError as e:
                bestresult = min(v for v in self.get_results(driverarr[0]) if v is not None)
                if all([min(v for v in self.get_results(x) if v is not None) == bestresult for x in driverarr]):
                    return sorted(driverarr, key= lambda x: self.get_results(x).index(bestresult))
                else:
                    breakpoint()
                    raise AssertionError("WTF")
            except Exception as e:
                raise e


        tiebroken = []
        points_dist = {}
        for driver in self.driver_standings.keys():
            driver_points = sum(filter(None, self.get_points(driver)))
            if driver_points in points_dist:
                points_dist[driver_points].append(driver)
            else:
                points_dist[driver_points] = [driver]
        for point_score in sorted(points_dist.keys(), reverse=True):
            if len(points_dist[point_score]) == 1:
                tiebroken.append(points_dist[point_score][0])
            else:
                assert len(points_dist[point_score]) > 1, "Must be one or more drivers per unique score"
                tiebroken.extend(tiebreaker(points_dist[point_score]))
        return tiebroken

    def full_standings(self):
        """
        
        """
        return [(entrant, sum(filter(None, self.get_points(entrant)))) for entrant in self.update_standings()]

    def determine_champion(self, best_of_n) -> None:
        """
        Determine the champion of this season
        Parameters:
            best_of_n: int; how to calculate points in "best of n" championship, 0 = every race counted
        Outputs:
            None
            driver determined to be champion is set to self.champion
        """
        if best_of_n == 0: # Most points total
            self.champion = self.update_standings()[0]
        elif isinstance(best_of_n, int): # Best n finishes
            champion = (None, None) # Champion in (entrant, points)
            points_dist = self.get_all_driver_points()
            for entrant in points_dist.keys():
                entrant_points_ordered = sorted(filter(None, points_dist[entrant]), reverse=True)
                entrant_best_of_n = sum(entrant_points_ordered[0:best_of_n])
                if champion[1] == None or entrant_best_of_n > champion[1]:
                    champion = (entrant, entrant_best_of_n)
            self.champion = champion
        else: # Best n of first m races and best i of last k races, ((n,m),(i,k))
            assert len(best_of_n) == 2 and all([len(x) == 2 for x in best_of_n]), "Incorrect formatting of championship best of n!"
            champion = (None, None) # Champion in (entrant, points)
            points_dist = self.get_all_driver_points()
            for entrant in points_dist.keys():
                results = points_dist[entrant]
                set1 = sorted(filter(None, results[0:best_of_n[0][1]]), reverse=True)
                set2 = sorted(filter(None, results[best_of_n[0][1]:]), reverse=True)
                if champion[1] == None or set1+set2 > champion[1]:
                    champion = (entrant, set1+set2)
            self.champion = champion

    def award_points(self, pointssystem=None):
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
        
        fastest_lap_points = self.select_fastest_lap_points()

        points_arr_driver_sprint = self.select_sprint_points_system()

        # Update standings accoring to results of each race
        for race in sorted(self.races, key=lambda r: r.round):
            if race.half_points == None:
                points_arr = points_arr_driver
            else:
                points_arr = race.half_points
            driver_points = race.calculate_driver_points(points_arr, points_arr_driver_sprint, fastest_lap_points)
            constructor_points = race.calculate_constructor_points(points_arr_constructor, fastest_lap_points)
            for entrant in driver_points.keys():
                if entrant in self.driver_standings.keys() and isinstance(self.driver_standings[entrant], list):
                    self.driver_standings[entrant].append(driver_points[entrant])
                else:
                    self.driver_standings[entrant] = [driver_points[entrant]]
            for constructor in constructor_points:
                if constructor in self.constuctor_standings:
                    self.constuctor_standings[constructor].append(constructor_points[constructor])
                else:
                    self.constuctor_standings[constructor] = [constructor_points[constructor]]

        # Award championships
        self.determine_champion(self.select_champion_method())
