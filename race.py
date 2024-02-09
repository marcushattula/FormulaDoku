from mydataclass import MyDataClass

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
    
    def read_data(self, data:list[str]):
        assert len(data) == len(RACE_DATA_FIELDS), f"Unsupported number of fields! Must be {len(RACE_DATA_FIELDS)}, found {len(data)}!"
        for i in range(len(data)):
            setattr(self,RACE_DATA_FIELDS[i], data[i])