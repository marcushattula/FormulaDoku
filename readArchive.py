from globals import *
from mydataclass import find_single_object_by_field_value, MyDataClass
from driver import Driver
from circuit import Circuit
from constructor import Constructor
from season import Season
from race import Race
from hardcodes import amend_missing_race_data, fix_demonym
import shutil
import csv

class ArchiveReader():
    """
    Class for reading and storing data from archive.
    """

    def __init__(self, archive_path:str=None, skip=True):
        """
        Run main commands
        """
        if not skip:
            try:
                self.db_path = TEMP_DIRPATH
                self.reset_db()
            except AssertionError as e:
                print(e)
            except Exception as e:
                raise e
            self.db_path = self.init_db(archive_path=archive_path)
        else:
            self.db_path = TEMP_DIRPATH
        fix_demonym(MyDataClass.cc)
        self.drivers = self.open_drivers()
        self.constructors = self.open_constructors()
        self.circuits = self.open_circuits()
        self.races = self.open_races()
        self.seasons = self.open_seasons()
        self.read_driver_results()
        self.process_races()
        amend_missing_race_data(self)
        self.process_seasons()

    def init_db(self, archive_path:str=None, target_path:str=None) -> str:
        """
        Initialize db from archive file.
        Parameters:
            (Optional) archive_path: str; path to archive containing data, must be .zip file. Defualt = ARCHIVE_FILE global variable
            (Optional) target_path: str; path where archive will be extracted to. Default = TEMP_DIRPATH global variable
        Outputs:
            Extracts data from archive to output folder
            Returns path to unpacked archive if successful
        """
        if not archive_path:
            archive_path = ARCHIVE_FILE
        if not target_path:
            target_path = TEMP_DIRPATH
        assert os.path.isfile(archive_path), "Archive file not found!"
        dirname, ext = os.path.splitext(archive_path)
        assert ext == ".zip", "Archive must be .zip file!"
        assert not os.path.isdir(target_path), "Database directory already exists."
        shutil.unpack_archive(archive_path, target_path, ext[1:])
        return target_path

    def reset_db(self) -> None:
        """
        Delete all opened db data.
        Parameters:
            None
        Outputs:
            Removes specified folder and all of its contents
        """
        assert os.path.isdir(self.db_path), f"Could not find directory {self.db_path}!"
        shutil.rmtree(self.db_path)

    def open_drivers(self) -> list[Driver]:
        """
        Extract all drivers from driver csv.
        Parameters:
            None
        Outputs:
            drivers: list[Driver]; List of Driver objects, initialized per line in csv.
        """
        driver_csv = os.path.join(self.db_path, "drivers.csv")
        with open(driver_csv, encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            drivers = []
            for row in csv_reader:
                if line_count == 0:
                    pass
                else:
                    new_driver = Driver()
                    new_driver.read_data(row)
                    drivers.append(new_driver)
                line_count += 1
        return drivers

    def open_seasons(self) -> list[Season]:
        """
        Extract all seasons from constructor csv.
        Parameters:
            None
        Outputs:
            seasons: list[Season]; List of Season objects, initialized per line in csv.
        """
        season_csv = os.path.join(self.db_path, "seasons.csv")
        with open(season_csv, encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            seasons = []
            for row in csv_reader:
                if line_count == 0:
                    pass
                else:
                    new_season = Season()
                    new_season.read_data(row)
                    seasons.append(new_season)
                line_count += 1
        return seasons

    def open_constructors(self) -> list[Constructor]:
        """
        Extract all constructors from constructor csv.
        Parameters:
            None
        Outputs:
            constructors: list[Constructor]; List of Constructor objects, initialized per line in csv.
        """
        constructor_csv = os.path.join(self.db_path, "constructors.csv")
        with open(constructor_csv, encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            constructors = []
            for row in csv_reader:
                if line_count == 0:
                    pass
                else:
                    new_constructor = Constructor()
                    new_constructor.read_data(row)
                    constructors.append(new_constructor)
                line_count += 1
        return constructors

    def open_circuits(self) -> list[Circuit]:
        """
        Extract all circuits from circuit csv.
        Parameters:
            None
        Outputs:
            circuits: list[Circuit]; List of circuit objects, initialized per line in csv.
        """
        circuits_csv = os.path.join(self.db_path, "circuits.csv")
        with open(circuits_csv, encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            circuits = []
            for row in csv_reader:
                if line_count == 0:
                    pass
                else:
                    new_circuit = Circuit()
                    new_circuit.read_data(row)
                    circuits.append(new_circuit)
                line_count += 1
        return circuits

    def open_races(self) -> list[Race]:
        """
        Extract all races from circuit csv.
        Parameters:
            None
        Outputs:
            races: list[Race]; List of race objects, initialized per line in csv.
        """
        races_csv = os.path.join(self.db_path, "races.csv")
        with open(races_csv, encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            races = []
            for row in csv_reader:
                if line_count == 0:
                    pass
                else:
                    new_race = Race()
                    new_race.read_data(row)
                    races.append(new_race)
                line_count += 1
        return races

    def read_driver_results(self) -> None:
        """
        Extract all race results from results csv and add them to each driver.
        Parameters:
            (Optional) db_path: str; path to directory where db was extracted. Default = TEMP_DIRPATH global variable.
        Outputs:
            races: list[Race]; List of race objects, initialized per line in csv.
        """

        # Read race results
        race_results_csv = os.path.join(self.db_path, "results.csv")
        with open(race_results_csv, encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    pass
                else:
                    race = find_single_object_by_field_value(self.races, "raceId", int(row[1]))
                    year = race.year
                    driver = find_single_object_by_field_value(self.drivers, "driverId", int(row[2]))
                    constructor = find_single_object_by_field_value(self.constructors, "constructorId", int(row[3]))
                    race.add_race_entrant(driver, constructor, row)
                    if constructor not in driver.teams:
                        driver.teams.append(constructor)
                    if driver not in constructor.drivers:
                        constructor.drivers.append(driver)
                    # driver.entries += 1
                    # driver.add_to_season_data(year, "entries", 1)
                    # if row[5] == '1':
                    #     driver.poles += 1
                    #     driver.add_to_season_data(year, "poles", 1)
                    # if row[6] == '1':
                    #     driver.wins += 1
                    #     driver.add_to_season_data(year, "wins", 1)
                    # if row[6] in ['1','2','3']:
                    #     driver.podiums += 1
                    #     driver.add_to_season_data(year, "podiums", 1)
                    # driver.career_points += float(row[9])
                    # driver.add_to_season_data(year, "points", float(row[9]))
                line_count += 1

        # Read sprint results
        sprint_results_csv = os.path.join(self.db_path, "sprint_results.csv")
        with open(sprint_results_csv, encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    pass
                else:
                    race = find_single_object_by_field_value(self.races, "raceId", int(row[1]))
                    year = race.year
                    driver = find_single_object_by_field_value(self.drivers, "driverId", int(row[2]))
                    constructor = find_single_object_by_field_value(self.constructors, "constructorId", int(row[3]))
                    race.add_sprint_entrant(driver, constructor, row)
                    # if row[6] == '1':
                    #     driver.sprint_wins += 1
                    #     driver.add_to_season_data(year, "sprint_wins", 1)
                    # driver.career_points += float(row[9])
                    # driver.add_to_season_data(year, "points", float(row[9]))
                line_count += 1
        
        # # Determine champion of each year
        # champions_dict = {}
        # for driver in self.drivers:
        #     for season in driver.season_data:
        #         if season not in champions_dict or driver.season_data[season]["points"] > champions_dict[season].season_data[season]["points"]:
        #             champions_dict[season] = driver
        # # SPECIAL CASE!!! Surtees won 1964, although he did not score the most points. This is a hardcoded fix.
        # #champions_dict[1964] = find_single_object_by_field_value(self.drivers, "driverId", 341)
        # # SPECIAL CASE!!! Senna won 1988, although he did not score the most points. This is a hardcoded fix.
        # #champions_dict[1988] = find_single_object_by_field_value(self.drivers, "driverId", 102)
        # for year in champions_dict:
        #     champions_dict[year].championships += 1

    def process_races(self) -> None:
        """
        Reads self.races and adds appropriate data to different objects
        """
        for race in self.races:
            year = race.year
            circuit = find_single_object_by_field_value(self.circuits, "circuitId", race.circuitId)
            race.add_circuit(circuit)
            season:Season = find_single_object_by_field_value(self.seasons, "year", year)
            season.add_race(race)
    
    def process_seasons(self) -> None:
        """
        Reads self.seasons and adds appropriate data to different fields
        """
        for season in self.seasons:
            season.award_points()

    def get_category(self, listname:str, categoryname:str) -> list:
        """
        Return a list mapped to a certain category of said list (e.g. the forename of every driver).
        Parameters: 
            listname: str; The name of the list to be mapped (drivers, races, constructors etc.)
            categoryname: str; The name of the attribute to map to (surname, fullname etc.)
        Outputs:
            returnlist: list; A list where each element is mapped to given attribute
        """
        listname = listname.lower()
        categoryname = categoryname.lower()
        assert listname in ["drivers", "constructors", "circuits", "races"], f"Unknown list: {listname}!"
        searchlist = getattr(self, listname)
        returnlist = []
        if listname == "drivers":
            assert hasattr(searchlist[0], categoryname), f"Unknown field {categoryname}!"
            for obj in searchlist:
                returnlist.append(getattr(obj, categoryname))
        return returnlist


if __name__ == "__main__":
    
    myArchive = ArchiveReader(archive_path=ARCHIVE_FILE)
    breakpoint()
