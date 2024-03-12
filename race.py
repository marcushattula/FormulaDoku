from mydataclass import MyDataClass
from driver import Driver
from constructor import Constructor
from circuit import Circuit

RACE_DATA_FIELDS = ["raceId","year","round","circuitId",
                    "name","date","time","url",
                    "fp1_date","fp1_time","fp2_date","fp2_time",
                    "fp3_date","fp3_time","quali_date","quali_time",
                    "sprint_date","sprint_time"]

class Race(MyDataClass):
    """
    Dataclass for storing race information.
    """

    def __init__(self):
        """
        Initializes empty class where all fields are set to None or empty lists.
        """
        for data_field in RACE_DATA_FIELDS:
            setattr(self, data_field, None)
        self.entrants = {}
        
    def __str__(self):
        """
        String function override. Returns "{year} {name}", e.g. "2009 British Grand Prix"
        """
        return f"{str(self.year)} {str(self.name)}"
    
    def read_data(self, data:list[str]):
        assert len(data) == len(RACE_DATA_FIELDS), f"Unsupported number of fields! Must be {len(RACE_DATA_FIELDS)}, found {len(data)}!"
        for i in range(len(data)):
            setattr(self,RACE_DATA_FIELDS[i], data[i])
    
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
    
    def add_entrant(self, team:Constructor, driver:Driver):
        """
        Add driver and team to list of entrants
        Parameters:
            team: Constructor; Constructor of entrant
            driver: Driver; Entrant driver
        Outputs:
            Adds team as key and driver as value to self.entrants
        """
        assert isinstance(team, Constructor), "Team must be instance of class Constructor!"
        assert isinstance(driver, Driver), "Driver must be instance of class Driver!"
        if team not in self.entrants:
            self.entrants[team] = []
        self.entrants[team].append(driver)
