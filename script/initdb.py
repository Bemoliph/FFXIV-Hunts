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
	
	dbCursor.execute("""CREATE TABLE hunts.targets (targetID integer PRIMARY KEY, zoneID integer REFERENCES hunts.zones(zoneID), rankID integer REFERENCES hunts.ranks(rankID), targetName text);""")
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (0, 0, 2, "Bonnacon"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (1, 0, 1, "Nahn"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (2, 0, 0, "Dark Helmet"))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (3, 1, 2, "Croque-Mitaine"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (4, 1, 1, "Vogaal Ja"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (5, 1, 0, "Skogs Fru"))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (6, 2, 2, "Garlok"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (7, 2, 1, "Hellsclaw"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (8, 2, 0, "Bloody Mary"))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (9, 3, 2, "Croakadile"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (10, 3, 1, "Unktehi"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (11, 3, 0, "Barbastelle"))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (12, 4, 2, "Nandi"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (13, 4, 1, "Marberry"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (14, 4, 0, "Myradrosh"))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (15, 5, 2, "Mahisha"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (16, 5, 1, "Cornu"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (17, 5, 0, "Vuokho"))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (18, 6, 2, "Wulgaru"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (19, 6, 1, "Melt"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (20, 6, 0, "Stinging Sophie"))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (21, 7, 2, "Mindflayer"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (22, 7, 1, "Ghede Ti Malice"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (23, 7, 0, "Monarch Ogrefly"))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (24, 8, 2, "Laideronnette"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (25, 8, 1, "Forneus"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (26, 8, 0, "White Joker"))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (27, 9, 2, "Thousand-Cast Theda"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (28, 9, 1, "Girtab"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (29, 9, 0, "Phecda"))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (30, 10, 2, "Zona Seeker"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (31, 10, 1, "Alectyron"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (32, 10, 0, "Sewer Syrup"))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (33, 11, 2, "Lampalagua"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (34, 11, 1, "Maahes"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (35, 11, 0, "Gatling"))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (36, 12, 2, "Nunyunuwi"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (37, 12, 1, "Zanig'oh"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (38, 12, 0, "Albin The Ashen"))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (39, 13, 2, "Minhocao"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (40, 13, 1, "Dalvag's Final Flame"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (41, 13, 0, "Flame Sergeant Dalvag"))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (42, 14, 2, "Brontes"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (43, 14, 1, "Sabotender Bailarina"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (44, 14, 0, "Ovjang"))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (45, 15, 2, "Safat"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (46, 15, 1, "Marraco"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (47, 15, 0, "Naul"))

	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (48, 16, 2, "Agrippa The Mighty"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (49, 16, 1, "Kurrea"))
	dbCursor.execute("""INSERT INTO hunts.targets VALUES (%s, %s, %s, %s);""", (50, 16, 0, "Leech King"))
	
	
	dbCursor.execute("""CREATE TABLE hunts.sightings (datetime timestamptz, targetID integer REFERENCES hunts.targets(targetID), xCoord integer, yCoord integer, submitterIP inet);""")
	dbCursor.execute("""CREATE INDEX ON hunts.sightings (datetime DESC);""")
	
	dbConn.commit()
	dbCursor.close()
	dbConn.close()
	