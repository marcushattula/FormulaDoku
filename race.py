from mydataclass import MyDataClass
from driver import Driver
from constructor import Constructor
from circuit import Circuit

RACE_DATA_FIELDS = ["raceId","year","round","circuitId",
                    "name","date","time","url",
                    "fp1_date","fp1_time","fp2_date","fp2_time",
                    "fp3_date","fp3_time","quali_date","quali_time",
                    "sprint_date","sprint_time"]

RACE_RESULT_DATA_FIELDS = ["resultId","raceId","driverId","constructorId",
                      "number","grid","position","positionText",
                      "positionOrder","points","laps","time",
                      "milliseconds","fastestLap","rank","fastestLapTime",
                      "fastestLapSpeed","statusId"]

SPRINT_RESULT_DATA_FIELDS = ["resultId","raceId","driverId","constructorId",
                      "number","grid","position","positionText",
                      "positionOrder","points","laps","time","milliseconds",
                      "fastestLap","fastestLapTime","statusId"]

FASTEST_LAP_POINT = 1
NON_SCORING_POS_POINTS = 0


class Race(MyDataClass):
    """
    Dataclass for storing race information.
    """

    def __init__(self):
        """
        Initializes empty class where all fields are set to None or empty lists.
        """
        self.data_fields = RACE_DATA_FIELDS
        for data_field in self.data_fields:
            setattr(self, data_field, None)
        self.entrants = {}
        self.sprint_entrants = None
        self.grid = []
        self.finish = []
        self.sprint_event = False # Flag for if race had sprint event, assumed false unless add_sprint_entrant() method is called
        self.sprint_finish = []
        self.fastest_driver = None
        
    def __str__(self):
        """
        String function override. Returns "{year} {name}", e.g. "2009 British Grand Prix"
        """
        return f"{str(self.year)} {str(self.name)}"
    
    def read_data(self, data:list[str]):
        self.read_csv_data(data)
    
    def add_circuit(self, circuit:Circuit):
        """
        Adds given circuit to self.circuit
        Parameters:
            circuit: Circuit; Circuit object to be added to this object
        Outputs:
            Sets self.circuit to circuit if circuit is of correct instance
        """
        assert isinstance(circuit, Circuit), "Circuit parameter must be of type Circuit!"
        self.circuit = circuit
    
    def add_race_entrant(self, driver:Driver, constructor:Constructor, results:list):
        """
        Add driver and team to list of entrants
        Parameters:
            driver: Driver; Entrant driver
            constructor: Constructor; Entrant constructor
            result: list[str]; Entrant result from race, from result csv
        Outputs:
            Adds team as key and driver as value to self.entrants
        """
        results_dict = {}
        assert isinstance(driver, Driver), "Driver must be instance of class Driver!"
        assert len(results) == len(RACE_RESULT_DATA_FIELDS), f"Incorrect number of data fields! (Got {len(results)}, expected {len(RACE_RESULT_DATA_FIELDS)})"
        # results[0]
        assert int(results[1]) == self.raceId, "Incorrect race result!"
        assert int(results[2]) == driver.driverId, "Incorrect driver id!"
        assert int(results[3]) == constructor.constructorId, "Incorrect constructor id!"
        results_dict["constructor"] = constructor
        for i in range(4, len(RACE_RESULT_DATA_FIELDS)):
            results_dict[RACE_RESULT_DATA_FIELDS[i]] = results[i]
        self.entrants[driver] = results_dict
    
    def add_sprint_entrant(self, driver:Driver, constructor:Constructor, results:list):
        """
        Add driver and team to list of sprint entrants
        Parameters:
            driver: Driver; Entrant driver
            constructor: Constructor; Entrant constructor
            result: list[str]; Entrant result from race, from result csv
        Outputs:
            Adds team as key and driver as value to self.entrants
        """
        if not self.sprint_entrants:
            self.sprint_entrants = {}
        results_dict = {}
        assert isinstance(driver, Driver), "Driver must be instance of class Driver!"
        assert len(results) == len(SPRINT_RESULT_DATA_FIELDS), f"Incorrect number of data fields! (Got {len(results)}, expected {len(SPRINT_RESULT_DATA_FIELDS)})"
        # results[0]
        assert int(results[1]) == self.raceId, "Incorrect race result!"
        assert int(results[2]) == driver.driverId, "Incorrect driver id!"
        assert int(results[3]) == constructor.constructorId, "Incorrect constructor id!"
        results_dict["constructor"] = constructor
        for i in range(4, len(SPRINT_RESULT_DATA_FIELDS)):
            results_dict[SPRINT_RESULT_DATA_FIELDS[i]] = results[i]
        self.sprint_entrants[driver] = results_dict
        if not self.sprint_event:
            self.sprint_event = True

    def get_grid(self) -> list[Driver]:
        """
        Get the starting grid of this race, in ascending order
        Paramters:
            None
        Outputs:
            grid: list[Driver]; Grid as ordered list of driver objects
        """
        if len(self.grid) != 0:
            return self.grid
        else:
            assert len(self.entrants) > 0, f"Uninitialized entrants! Use method add_entrant()!"
            self.grid = [None] * len(self.entrants)
            for entrant in self.entrants.keys():
                grid_pos = int(self.entrants[entrant]["grid"])
                self.grid.insert(grid_pos-1, entrant)
            return self.get_grid()

    def get_finish(self) -> list[Driver]:
        """
        Get the finishing order of this race, in ascending order
        Paramters:
            None
        Outputs:
            finish: list[Driver]; Finish as ordered list of driver objects
        """
        if len(self.finish) != 0:
            return self.finish
        else:
            assert len(self.entrants) > 0, f"Uninitialized entrants! Use method add_entrant()!"
            self.finish = [None] * len(self.entrants)
            for entrant in self.entrants.keys():
                finish_pos = int(self.entrants[entrant]["position"])
                self.finish.insert(finish_pos-1, entrant)
            return self.get_finish()

    def get_sprint_finish(self) -> list[Driver]:
        """
        Get the finishing order of sprint, in ascending order
        Paramters:
            None
        Outputs:
            finish: list[Driver]; Sprint finish as ordered list of driver objects
        """
        assert self.sprint_event, f"Unable to get sprint finish of non-sprint race!"
        if len(self.sprint_finish) != 0:
            return self.sprint_finish
        else:
            assert len(self.entrants) > 0, f"Uninitialized entrants! Use method add_entrant()!"
            self.sprint_finish = [None] * len(self.entrants)
            for entrant in self.sprint_entrants.keys():
                finish_pos = int(self.sprint_entrants[entrant]["position"])
                self.sprint_finish.insert(finish_pos-1, entrant)
            return self.get_sprint_finish()

    def get_fastest_lap(self) -> Driver:
        """
        Get the driver who set the fastest lap during the race
        Paramters:
            None
        Outputs:
            fastest_driver: Driver; Driver who set the fastest lap
        """
        if self.fastest_driver == None:
            assert len(self.entrants) > 0, f"Uninitialized entrants! Use method add_entrant()!"
            fastest_time = None
            fastest_driver = None
            for entrant in self.entrants.keys():
                driver_time = self.entrants[entrant]["fastestLapTime"]
                if fastest_time == None or driver_time < fastest_time:
                    fastest_time = driver_time
                    fastest_driver = entrant
            self.fastest_driver = fastest_driver
        else:
            assert isinstance(self.fastest_driver, Driver), f"Fastest driver must be class Driver!"
        return self.fastest_driver

    def score_for_pos(self, finish_pos:int, points_system:list[int]) -> int:
        """
        Retrieve number of points scored for position in event based on poins system
        Parameters:
            finish_pos: int; Finishing position
            points_system: list[int]; Points system to use
        Outputs:
            points: int; How many points are scored for said finish
        """
        assert isinstance(finish_pos, int), "Finishing position must be integer!"
        assert isinstance(points_system, list) and all([isinstance(x, int) for x in points_system]), "Points system must be list of ints!"
        if finish_pos > len(points_system):
            return NON_SCORING_POS_POINTS
        else:
            return points_system[finish_pos-1]

    def calculate_points(self, pointssystem, fastest_lap:int):
        """
        Calculate and distribute points to drivers according to given pointssystem
        Parameters:
            pointssystem: list[int]; How to award points for each finishing position.
            fastest_lap: int; How many to give point for fastest lap.
        Outputs:
            Gives each entrant driver and team their points
        """
        
        assert len(self.entrants) > 0, f"Uninitialized entrants! Use method add_entrant()!"
        for entrant in self.entrants.keys():
            pos = int(self.entrants[entrant]["position"])
            points_driver = self.score_for_pos(pos, pointssystem)
            # TODO: Finish implementing
    