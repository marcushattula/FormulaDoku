from globals import *
#from readArchive import ArchiveReader

FASTEST_DRIVERS_50S = {
    1950: [[642], [579], [593], [642], [642], [579], [579]],
    1951: [[579], [766], [579], [579], [642], [579], [642], [579]],
    1952: [[641], [657], [647], [647], [647], [647], [647], [647, 498]],
    1953: [[647], [657], [633], [498], [579], [647, 498], [647], [647], [579]],
    1954: [[498], [658], [579], [478], [579, 498, 578, 475, 670, 647, 554], [648], [579], [498], [647]],
    1955: [[579], [579], [657], [579], [643], [475], [475]],
    1956: [[579], [579], [559], [475], [579], [475], [579], [475]],
    1957: [[475], [579], [509], [577], [475], [579], [475], [479]],
    1958: [[579], [578], [475], [529], [578], [578], [578], [475], [578], [403], [475]],
    1959: [[356], [512], [475], [475], [475], [479], [475], [403], [427]]
}

HALF_POINT_RACES = {
    1975: ["1975 Spanish Grand Prix", "1975 Austrian Grand Prix"],
    1984: ["1984 Monaco Grand Prix"],
    1991: ["1991 Australian Grand Prix"],
    2009: ["2009 Malaysian Grand Prix"],
    2021: ["2021 Belgian Grand Prix"]
}

SHARED_DRIVES = {
    # 1950
    838: [(741, 774), (801, 627)],
    839: [(802, 647), (641, 579)],
    # 1951
    826: [(658, 675)],
    828: [(786, 579), (647, 498), (579, 786)],
    831: [(697, 642)],
    # 1952
    817: [(609, 642)],
    820: [(723, 721), (640, 501)],
    823: [(622, 759)],
    # 1953
    808: [(427, 501)],
    809: [(611, 518), (615, 555), (509, 513), (529, 521, 520), (700, 702), (701, 509), (449, 612, 630), (654, 804), (677, 512, 797), (659, 521, 612)],
    810: [(697, 498)],
    811: [(660, 579)],
    814: [(647, 633), (633, 647)],
    815: [(579, 697), (697, 579)],
    816: [(644, 577)],
    # 1954
    800: [(526, 518), (555, 659), (656, 593, 611, 612, 653), (521, 654), (518, 613, 799, 529), (596, 702), (611, 653, 509), (449, 513), (520, 613), (512, 612, 519), (612, 702), (509, 559), (677, 805), (678, 730)],
    801: [(578, 498)],
    803: [(669, 541), (633, 647)],
    804: [(498, 578)],
    806: [(620, 498)],
    807: [(640, 638)],
    # 1955
    792: [(498, 642, 427), (642, 427, 620), (478, 648, 475), (501, 554), (577, 644, 501), (644, 554, 577), (645, 501, 496), (608, 633)],
    793: [(554, 607), (641, 632), (607, 554)],
    794: [(529, 555), (654, 519)],
    795: [(643, 554)],
    797: [(578, 608), (663, 501), (666, 661)],
    # 1956
    784: [(577, 579), (622, 583), (623, 806), (579, 577)],
    785: [(581, 579), (579, 608), (625, 429)],
    786: [(596, 532)],
    787: [(607, 475)],
    788: [(607, 475), (578, 501)],
    789: [(606, 581), (608, 606)],
    790: [(606, 581), (577, 608)],
    791: [(581, 579), (579, 608), (620, 554), (633, 347)],
    # 1957
    776: [(606, 498), (607, 581, 476)],
    777: [(476, 578), (483, 501)],
    779: [(617, 356)],
    780: [(479, 475), (427, 581), (475, 479)],
    783: [(483, 501), (609, 638)],
    # 1958
    770: [(590, 479)],
    774: [(418, 566)],
    # 1959 (No shared drives)
    # 1960
    746: [(427, 475)],
    # 1961
    745: [(482, 418)],
    # 1962 & 1963 no shared drives
    # 1964
    717: [(374, 373), (373, 374)]
}

def fix_demonym(cc: CountryConverter):
    """
    Fixes missing demonym-country pairs in CountryConverter
    """
    cc.demonyms["american-italian"] = "italy"
    cc.demonyms["argentine-italian"] = "argentina"
    cc.demonyms["east german"] = "germany"

def amend_missing_race_data(archive):#: ArchiveReader):
    """
    Ammend missing data from races
    """

    def add_missing_fastest_driver():
        """
        Set fastest driver for races with missing lap time data
        """

        def filter_helper1(driver_team_tuple, year, i) -> bool:
            return driver_team_tuple[0].driverId in FASTEST_DRIVERS_50S[year][i]
        
        def filter_helper2(driver_team_tuple) -> bool: # Hamilton finder
            return driver_team_tuple[0].fullname == "Lewis Hamilton"

        # 1950s
        for season in archive.seasons:
            # HARDCODED FIX: NO LAP DATA FOR 1950S RACES
            if season.year in FASTEST_DRIVERS_50S.keys():
                assert len(FASTEST_DRIVERS_50S[season.year]) == len(season.races), f"Incorrect number of races in {season.year}! Expected {len(season.races)}"
                for i in range(len(season.races)):
                    race = season.races[i]
                    fastest_drivers = [driver_team_tuple for driver_team_tuple in race.get_entrants() if filter_helper1(driver_team_tuple, season.year, i)]
                    race.fastest_drivers = fastest_drivers
                    race.finish._hardcoded_fastest_lap_data(fastest_drivers)
            # HARDCODED FIX: NOT AWARDED FOR 2021 Belgian GP
            elif season.year == 2021:
                for race in season.races:
                    if str(race) == "2021 Belgian Grand Prix":
                        race.fastest_drivers = []
                        race.finish._hardcoded_fastest_lap_data(True)
            # HARDCODED FIX: MISSING LAP TIME DATA FOR 2024 MONACO GP
            elif season.year == 2024:
                for race in season.races:
                    if str(race) == "2024 Monaco Grand Prix":
                        fastest_drivers = [driver_team_tuple for driver_team_tuple in race.get_entrants() if filter_helper2(driver_team_tuple)]
                        race.fastest_drivers = fastest_drivers
                        race.finish._hardcoded_fastest_lap_data(fastest_drivers)

    def half_points():
        """
        Award half points for predetermined races
        """
        for season in archive.seasons:
            if season.year in HALF_POINT_RACES.keys():
                for race in season.races:
                    if str(race) in HALF_POINT_RACES[season.year]:
                        race.half_points = [0.5*x for x in season.select_race_points_system()]

    def shared_drives():
        """
        Share points between drivers who shared a car
        """
        # TODO: Implement or scrap
        for season in archive.seasons:
            for race in season.races:
                if race.raceId in SHARED_DRIVES:
                    pass

    def fix_circuit_locations():
        for circuit in archive.circuits:
            if circuit.country == "usa":
                circuit.country = "united states"
            elif circuit.country == "uk":
                circuit.country = "united kingdom"

    add_missing_fastest_driver()
    fix_circuit_locations()
    half_points()
