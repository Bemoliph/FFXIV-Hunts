import datetime
import psycopg2

if __name__ == "__main__":
	# TODO: move this stuff into a config somewhere
	user = "hunts"
	password = "***REMOVED***"
	host = "127.0.0.1"
	database = "ffxiv"
	
	dbConn = psycopg2.connect(user=user, password=password, host=host, database=database)
	dbCursor = dbConn.cursor()
	
	# Set up Hunts
	dbCursor.execute("""CREATE SCHEMA hunts;""")
	
	dbCursor.execute("""CREATE TABLE hunts.zones (zoneID integer PRIMARY KEY, zoneName text);""")
	dbCursor.execute("""INSERT INTO hunts.zones VALUES (%s, %s);""", (0, "Western La Noscea",))
	dbCursor.execute("""INSERT INTO hunts.zones VALUES (%s, %s);""", (1, "Middle La Noscea",))
	dbCursor.execute("""INSERT INTO hunts.zones VALUES (%s, %s);""", (2, "Eastern La Noscea",))
	dbCursor.execute("""INSERT INTO hunts.zones VALUES (%s, %s);""", (3, "Lower La Noscea",))
	dbCursor.execute("""INSERT INTO hunts.zones VALUES (%s, %s);""", (4, "Upper La Noscea",))
	dbCursor.execute("""INSERT INTO hunts.zones VALUES (%s, %s);""", (5, "Outer La Noscea",))
	dbCursor.execute("""INSERT INTO hunts.zones VALUES (%s, %s);""", (6, "Eastern Shroud",))
	dbCursor.execute("""INSERT INTO hunts.zones VALUES (%s, %s);""", (7, "South Shroud",))
	dbCursor.execute("""INSERT INTO hunts.zones VALUES (%s, %s);""", (8, "Central Shroud",))
	dbCursor.execute("""INSERT INTO hunts.zones VALUES (%s, %s);""", (9, "North Shroud",))
	dbCursor.execute("""INSERT INTO hunts.zones VALUES (%s, %s);""", (10, "Western Thanalan",))
	dbCursor.execute("""INSERT INTO hunts.zones VALUES (%s, %s);""", (11, "Eastern Thanalan",))
	dbCursor.execute("""INSERT INTO hunts.zones VALUES (%s, %s);""", (12, "Southern Thanalan",))
	dbCursor.execute("""INSERT INTO hunts.zones VALUES (%s, %s);""", (13, "Northern Thanalan",))
	dbCursor.execute("""INSERT INTO hunts.zones VALUES (%s, %s);""", (14, "Central Thanalan",))
	dbCursor.execute("""INSERT INTO hunts.zones VALUES (%s, %s);""", (15, "Coerthas Central Highlands",))
	dbCursor.execute("""INSERT INTO hunts.zones VALUES (%s, %s);""", (16, "Mor Dhona",))
	
	dbCursor.execute("""CREATE TABLE hunts.ranks (rankID integer PRIMARY KEY, rankName text);""")
	dbCursor.execute("""INSERT INTO hunts.ranks VALUES (%s, %s);""", (0, "B",))
	dbCursor.execute("""INSERT INTO hunts.ranks VALUES (%s, %s);""", (1, "A",))
	dbCursor.execute("""INSERT INTO hunts.ranks VALUES (%s, %s);""", (2, "S",))
	
	dbCursor.execute("""CREATE TABLE hunts.loot (lootID integer PRIMARY KEY, rankID integer REFERENCES hunts.ranks(rankID), lootName text, lootQty integer);""")
	dbCursor.execute("""INSERT INTO hunts.loot VALUES (%s, %s, %s, %s);""", (0, 0, "Allied Seals", 5))
	dbCursor.execute("""INSERT INTO hunts.loot VALUES (%s, %s, %s, %s);""", (1, 1, "Allied Seals", 20))
	dbCursor.execute("""INSERT INTO hunts.loot VALUES (%s, %s, %s, %s);""", (2, 1, "Blood-spattered Mark Log", 1))
	dbCursor.execute("""INSERT INTO hunts.loot VALUES (%s, %s, %s, %s);""", (3, 2, "Allied Seals", 50))
	dbCursor.execute("""INSERT INTO hunts.loot VALUES (%s, %s, %s, %s);""", (4, 2, "Blood-spattered Mark Log", 3))
	
	dbCursor.execute("""CREATE TABLE hunts.targets (targetID integer PRIMARY KEY, zoneID integer REFERENCES hunts.zones(zoneID), rankID integer REFERENCES hunts.ranks(rankID), targetName text, minSpawnTime interval);""")
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (0, 0, 2, "Bonnacon", None))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (1, 0, 1, "Nahn", datetime.timedelta(seconds=12600)))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (2, 0, 0, "Dark Helmet", None))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (3, 1, 2, "Croque-Mitaine", None))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (4, 1, 1, "Vogaal Ja", datetime.timedelta(seconds=12600)))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (5, 1, 0, "Skogs Fru", None))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (6, 2, 2, "Garlok", None))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (7, 2, 1, "Hellsclaw", datetime.timedelta(seconds=12600)))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (8, 2, 0, "Bloody Mary", None))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (9, 3, 2, "Croakadile", None))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (10, 3, 1, "Unktehi", datetime.timedelta(seconds=13500)))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (11, 3, 0, "Barbastelle", None))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (12, 4, 2, "Nandi", None))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (13, 4, 1, "Marberry", datetime.timedelta(seconds=10800)))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (14, 4, 0, "Myradrosh", None))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (15, 5, 2, "Mahisha", None))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (16, 5, 1, "Cornu", datetime.timedelta(seconds=12600)))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (17, 5, 0, "Vuokho", None))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (18, 6, 2, "Wulgaru", None))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (19, 6, 1, "Melt", datetime.timedelta(seconds=10800)))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (20, 6, 0, "Stinging Sophie", None))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (21, 7, 2, "Mindflayer", None))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (22, 7, 1, "Ghede Ti Malice", datetime.timedelta(seconds=13500)))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (23, 7, 0, "Monarch Ogrefly", None))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (24, 8, 2, "Laideronnette", None))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (25, 8, 1, "Forneus", datetime.timedelta(seconds=12600)))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (26, 8, 0, "White Joker", None))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (27, 9, 2, "Thousand-Cast Theda", None))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (28, 9, 1, "Girtab", datetime.timedelta(seconds=13500)))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (29, 9, 0, "Phecda", None))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (30, 10, 2, "Zona Seeker", None))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (31, 10, 1, "Alectyron", datetime.timedelta(seconds=12600)))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (32, 10, 0, "Sewer Syrup", None))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (33, 11, 2, "Lampalagua", None))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (34, 11, 1, "Maahes", datetime.timedelta(seconds=10800)))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (35, 11, 0, "Gatling", None))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (36, 12, 2, "Nunyunuwi", None))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (37, 12, 1, "Zanig'oh", datetime.timedelta(seconds=13500)))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (38, 12, 0, "Albin The Ashen", None))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (39, 13, 2, "Minhocao", None))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (40, 13, 1, "Dalvag's Final Flame", datetime.timedelta(seconds=14400)))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (41, 13, 0, "Flame Sergeant Dalvag", None))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (42, 14, 2, "Brontes", None))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (43, 14, 1, "Sabotender Bailarina", datetime.timedelta(seconds=14400)))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (44, 14, 0, "Ovjang", None))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (45, 15, 2, "Safat", None))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (46, 15, 1, "Marraco", datetime.timedelta(seconds=10800)))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (47, 15, 0, "Naul", None))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (48, 16, 2, "Agrippa The Mighty", None))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (49, 16, 1, "Kurrea", datetime.timedelta(seconds=12600)))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s, %s);""", (50, 16, 0, "Leech King", None))
	
	
	dbCursor.execute("""CREATE TABLE hunts.sightings (datetime timestamptz, isDead boolean, targetID integer REFERENCES hunts.targets(targetID), xCoord integer, yCoord integer, submitterIP inet);""")
	dbCursor.execute("""CREATE INDEX ON hunts.sightings (datetime DESC);""")
	
	dbConn.commit()
	dbCursor.close()
	dbConn.close()
	