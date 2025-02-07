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

NON_SCORING_POS_POINTS = 0

class Result():
    """
    Class for storing data related to a result of race
    """

    def __init__(self):
        self.entrants = []
        self.data = []

    def __str__(self):
        return ', '.join([(str(x[0]) + '-' + str(x[1])) for x in self.entrants])
    
    def __repr__(self):
        return "Result: " + str(self)

    def add_entrant(self, entrant, data):
        """
        Adds entrant to this result
        """
        assert entrant not in self.entrants, f"Entrant {str(entrant)} already added!"
        self.entrants.append(entrant)
        self.data.append(data)


class ResultOrder(dict):
    """
    Class for storing entire classifications
    """
    def __init__(self, event, title):
        self.event = event
        self.title = title
        self._hardcoded_fastest_drivers = []
    
    def __str__(self):
        return "\n".join([(str(x) + ": " + str(self[x])) for x in self.sorted_order()])

    def __repr__(self):
        return f"{self.event} - {self.title}\n" + str(self)

    def _hardcoded_fastest_lap_data(self, *args):
        raise NotImplementedError("Method not implemented for base class!")

    def sorted_order(self):
        positions = [x for x in self.keys() if isinstance(x, int)]
        status = [x for x in self.keys() if isinstance(x, str)]
        return sorted(positions) + sorted(status)

    def add_result(self, *args):
        raise NotImplementedError("Method not implemented for base class!")
    
    def get_fastest_lap(self, *args):
        raise NotImplementedError("Method not implemented for base class!")

    def get_entrant(self, entrant):
        """
        
        """
        for i in self.keys():
            if entrant in self[i].entrants:
                return i
        raise ValueError("Entrant not found!")

    def get_position(self, position):
        """
        
        """
        return self[position]

    def get_order(self):
        """
        
        """
        order = []
        for pos in self.sorted_order():
            for ent in self.get_position(pos).entrants:
                order.append(ent)
        return order

    def pos_points(self, points_system):
        """
        Returns dictionary of entrant:points
        """
        points_per_entrant = {}
        for i in range(len(self.keys())):
            if i >= len(points_system):
                pos_points = 0
            else:
                pos_points = points_system[i]
            result = self[i+1]
            for entrant in result.entrants:
                if (entrant not in points_per_entrant.keys() or
                    points_per_entrant[entrant] < pos_points/len(result.entrants)):
                    points_per_entrant[entrant] = pos_points/len(result.entrants)
        return points_per_entrant

    def determine_points(self, points_system, fastest_lap_tuple):
        """
        
        """
        def eligible_for_fastest_lap(entrant, fastest_lap_tuple) -> bool:
            """
            Determine if finishing position is elegible for the fastest lap point(s)
            """
            return (fastest_lap_tuple[1] == 0 or 
                    0 <= self.get_entrant(entrant) <= fastest_lap_tuple[1])

        driver_points = self.pos_points(points_system)
        fastest_drivers = self.get_fastest_lap()
        for fastest_driver in fastest_drivers[0]:
            if eligible_for_fastest_lap(fastest_driver, fastest_lap_tuple):
                driver_points[fastest_driver] += fastest_lap_tuple[0]/len(fastest_drivers[0])
        return driver_points


class RaceOrder(ResultOrder):

    def __init__(self, event, subtext="Race Classification"):
        super().__init__(event, subtext)
    
    def _hardcoded_fastest_lap_data(self, fastest_drivers):
        """
        
        """
        self._hardcoded_fastest_drivers = fastest_drivers
    
    def add_result(self, entrant, result_dict):
        """
        
        """
        pos = int(result_dict["positionOrder"])
        if pos not in self.keys():
            self[pos] = Result()
        self[pos].add_entrant(entrant, result_dict)
    
    def get_fastest_lap(self):
        """
        Gets driver who set fastest lap
        """
        if not self._hardcoded_fastest_drivers:
            fastest_time = None
            fastest_entrants = []
            for result in self.keys():
                for i in range(len(self[result].entrants)):
                    entrant = self[result].entrants[i]
                    entrant_time = self[result].data[i]["fastestLapTime"]
                    if fastest_time == None or entrant_time < fastest_time:
                        fastest_time = entrant_time
                        fastest_entrants = [entrant]
                    elif fastest_time == entrant_time:
                        fastest_entrants.append(entrant)
            return (fastest_entrants, fastest_time)
        else:
            if self._hardcoded_fastest_drivers == True:
                self._hardcoded_fastest_drivers = []
            return (self._hardcoded_fastest_drivers, None)


class GridOrder(ResultOrder):
    
    def __init__(self, event, subtext="Starting Grid"):
        super().__init__(event,subtext)
    
    def add_result(self, entrant, result_dict):
        """
        
        """
        pos = int(result_dict["grid"])
        if pos == 0: 
            pos = "PL"
        if pos not in self.keys():
            self[pos] = Result()
            self[pos].add_entrant(entrant, result_dict)
        elif pos == "PL":
            self["PL"].add_entrant(entrant, result_dict)


class SprintOrder(RaceOrder):

    def __init__(self, event):
        super().__init__(event, subtext="Sprint Classification")


class SprintGridOrder(GridOrder):

    def __init__(self, event):
        super().__init__(event, subtext="Sprint Starting Grid")


class QualifyingOrder(ResultOrder):

    def __init__(self, event):
        super().__init__(event, "Qualifying Classification")

    # TODO: Finish Implementing
    
        
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
        self.sprint_entrants = {}
        self.grid = []
        self.finish = []
        self.finish_new:ResultOrder = None
        self.sprint_event = False # Flag for if race had sprint event, assumed false unless add_sprint_entrant() method is called
        self.sprint_finish = []
        self.sprint_new = None
        self.sprint_grid_new = None
        self.fastest_drivers = None
        self.points_per_driver = {}
        self.half_points = None # None if not half points awarded for this race, else is list of new points
        self._saved_points = {}
        
    def __str__(self):
        """
        String function override. Returns "{year} {name}", e.g. "2009 British Grand Prix"
        """
        return f"{str(self.year)} {str(self.name)}"
    
    def read_data(self, data:list[str]):
        self.read_csv_data(data)
        self.finish_new = RaceOrder(str(self))
        self.grid_new = GridOrder(str(self))
    
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
        driver_team_tuple = (driver, constructor)
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
        self.entrants[driver_team_tuple] = results_dict

        # New implementation
        try:
            self.finish_new.add_result(driver_team_tuple, results_dict)
            self.grid_new.add_result(driver_team_tuple, results_dict)
        except Exception as e:
            print(e)
            breakpoint()
   
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
        driver_team_tuple = (driver, constructor)
        if driver_team_tuple in self.sprint_entrants:
            return {}
        results_dict = {}
        assert isinstance(driver, Driver), "Driver must be instance of class Driver!"
        assert isinstance(constructor, Constructor), "Constructor must be instance of class Constructor!"
        assert len(results) == len(SPRINT_RESULT_DATA_FIELDS), f"Incorrect number of data fields! (Got {len(results)}, expected {len(SPRINT_RESULT_DATA_FIELDS)})"
        # results[0]
        assert int(results[1]) == self.raceId, "Incorrect race result!"
        assert int(results[2]) == driver.driverId, "Incorrect driver id!"
        assert int(results[3]) == constructor.constructorId, "Incorrect constructor id!"
        results_dict["constructor"] = constructor
        for i in range(4, len(SPRINT_RESULT_DATA_FIELDS)):
            results_dict[SPRINT_RESULT_DATA_FIELDS[i]] = results[i]
        self.sprint_entrants[driver_team_tuple] = results_dict
        if not self.sprint_event:
            self.sprint_event = True
            self.sprint_new = SprintOrder(str(self))
            self.sprint_grid_new = SprintGridOrder(str(self))
        
        # New implementation
        try:
            self.sprint_new.add_result(driver_team_tuple, results_dict)
            self.sprint_grid_new.add_result(driver_team_tuple, results_dict)
        except Exception as e:
            print(e)
            breakpoint()
            raise e

    def get_grid(self) -> list[Driver]:
        """
        Get the starting grid of this race, in ascending order
        Paramters:
            None
        Outputs:
            grid: list[Driver]; Grid as ordered list of driver objects
        """
        return self.grid_new.get_order()
        if len(self.grid) != 0:
            return self.grid
        else:
            assert len(self.entrants) > 0, f"Uninitialized entrants! Use method add_entrant()!"
            self.grid = [None] * len(self.entrants)
            for entrant in self.entrants.keys():
                grid_pos = int(self.entrants[entrant]["grid"])
                self.grid[grid_pos-1] = entrant
            return self.get_grid()

    def get_finish(self) -> list[Driver]:
        """
        Get the finishing order of this race, in ascending order
        Paramters:
            None
        Outputs:
            finish: list[Driver]; Finish as ordered list of driver objects
        """
        return self.finish_new.get_order()
        if len(self.finish) != 0:
            return self.finish
        else:
            assert len(self.entrants) > 0 or self.year == 2024, f"Uninitialized entrants! Use method add_entrant()!"
            self.finish = [[] for _ in range(len(self.entrants))]
            for entrant in self.entrants.keys():
                finish_pos = int(self.entrants[entrant]["positionOrder"])
                self.finish[finish_pos-1].append(entrant)
            return self.finish

    def get_position(self, driver) -> int:
        """
        Get the finishing position of a driver
        Parameters:
            driver: Driver; driver object to get position of
        Returns:
            pos: int; finishing position of driver
        """
        for i in self.finish_new.sorted_order():
            finisher = self.finish_new[i]
            if any([driver == ent[0] for ent in finisher.entrants]):
                return i
        return None
        for i in range(len(self.get_finish())):
            finisher = self.get_finish()[i]
            if driver in finisher:
                return i + 1
        return None

    def get_sprint_finish(self) -> list[Driver]:
        """
        Get the finishing order of sprint, in ascending order
        Paramters:
            None
        Outputs:
            finish: list[Driver]; Sprint finish as ordered list of driver objects
        """
        if len(self.sprint_finish) != 0:
            return self.sprint_finish
        else:
            assert len(self.sprint_entrants) > 0 or self.year == 2024, f"Uninitialized entrants! Use method add_entrant()!"
            self.sprint_finish = [[] for _ in range(len(self.sprint_entrants))]
            for entrant in self.sprint_entrants.keys():
                finish_pos = int(self.sprint_entrants[entrant]["positionOrder"])
                self.sprint_finish[finish_pos-1].append(entrant)
            return self.sprint_finish

    def get_sprint_position(self, driver) -> int:
        """
        Get the finishing position of a driver in sprint race
        Parameters:
            driver: Driver; driver object to get position of
        Returns:
            pos: int; finishing position of driver in sprint
        """
        assert self.sprint_event, "Event must be sprint race!"
        for i in range(len(self.get_sprint_finish())):
            finisher = self.get_sprint_finish()[i]
            if driver in finisher:
                return i + 1

    def get_fastest_lap(self) -> list[Driver]:
        """
        Get the driver who set the fastest lap during the race
        Paramters:
            None
        Outputs:
            fastest_driver: list[Driver]; Driver(s) who set the fastest lap
        """
        if self.fastest_drivers == None:
            assert len(self.entrants) > 0, f"Uninitialized entrants! Use method add_entrant()!"
            fastest_time = None
            fastest_drivers = []
            for entrant in self.entrants.keys():
                driver_time = self.entrants[entrant]["fastestLapTime"]
                if fastest_time == None or driver_time < fastest_time:
                    fastest_time = driver_time
                    fastest_drivers = [entrant]
                elif driver_time == fastest_time:
                    fastest_drivers.append(entrant)
            self.fastest_drivers = fastest_drivers
        else:
            assert all([isinstance(fastest_driver[0], Driver) for fastest_driver in self.fastest_drivers]), f"Fastest driver must be class Driver!"
            assert all([isinstance(fastest_driver[1], Constructor) for fastest_driver in self.fastest_drivers]), f"Fastest team must be class Constructor!"
        return self.fastest_drivers

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
        assert isinstance(points_system, list) and all([isinstance(x, int) or isinstance(x, float) for x in points_system]), "Points system must be list of ints or floats!"
        if finish_pos > len(points_system):
            return NON_SCORING_POS_POINTS
        else:
            return points_system[finish_pos-1]

    def eligible_for_fastest_lap(self, pos, fastest_lap_tuple) -> bool:
        """
        Determine if finishing position is elegible for the fastest lap point(s)
        """
        return fastest_lap_tuple[1] == 0 or 0 <= pos <= fastest_lap_tuple[1]

    def calculate_driver_points(self, pointssystem, sprint_pointssystem, fastest_lap_tuple, force:bool=False) -> dict:
        """
        Calculate and distribute points to drivers according to given pointssystem
        Parameters:
            pointssystem: list[int]; How to award points for each finishing position.
            sprint_pointssystem: list[int]; How to award points for each finish position in sprint
            fastest_lap: int; How many to give point for fastest lap.
        Outputs:
            Gives each entrant driver and team their points
        """
        driver_points = self.finish_new.determine_points(pointssystem, fastest_lap_tuple)
        if self.sprint_event:
            sprint_points = self.sprint_new.determine_points(sprint_pointssystem, (0,0))
            for entrant in sprint_points.keys():
                driver_points[entrant] += sprint_points[entrant]
        driver_points = dict(zip([x[0] for x in driver_points.keys()], driver_points.values()))
        self._saved_points = driver_points
        return driver_points
        if not force and hasattr(self, "points_per_driver") and self.points_per_driver:
            return self.points_per_driver
        driver_points = {}
        for entrant in self.entrants.keys():
            pos = self.get_position(entrant)
            points_driver = self.score_for_pos(pos, pointssystem)/len(self.get_finish()[pos-1])
            if entrant in self.get_fastest_lap() and self.eligible_for_fastest_lap(pos, fastest_lap_tuple) and fastest_lap_tuple[0]:
                assert len(self.get_fastest_lap()) < 8 and fastest_lap_tuple[0], f"Missing lap time data for {str(self)}!"
                points_driver += fastest_lap_tuple[0]/len(self.get_fastest_lap())
            if self.sprint_event:
                sprint_pos = self.get_sprint_position(entrant)
                points_driver += self.score_for_pos(sprint_pos, sprint_pointssystem)
            driver_points[entrant] = points_driver
        self.points_per_driver = driver_points
        return driver_points
    
    def calculate_constructor_points(self, pointssystem, fastest_lap:int) -> dict:
        """
        Calculate and distribute points to constructors according to given points system
        """
        return {}
