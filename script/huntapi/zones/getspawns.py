import cherrypy

import huntdb
import huntdocs
import huntutils

def getInputs(params):
	if "zoneIDs" not in params or not params["zoneIDs"]:
		raise ValueError("Missing mandatory input 'zoneIDs'.")
	
	return huntutils.parseCSV(int, "zoneIDs", params.get("zoneIDs"))

def getSpawns(zoneIDs):
	dbConn, dbCursor = huntdb.getConnectionWithCursor(dictCursor = True)
	
	query = """
		SELECT DISTINCT ON (xCoord, yCoord) xCoord, yCoord
		FROM hunts.sightings
		WHERE targetID IN (SELECT targetID FROM hunts.targets WHERE zoneID = %s) AND xCoord IS NOT NULL AND yCoord IS NOT NULL
		ORDER BY xCoord, yCoord ASC;"""
	
	zoneSpawns = {}
	for zID in zoneIDs:
		queryInput = (zID, )
		dbCursor.execute(query, queryInput)
		zoneSpawns[zID] = [dict(x) for x in dbCursor.fetchall()]
	
	huntdb.putConnectionWithCursor(dbConn, dbCursor)
	
	return zoneSpawns

@cherrypy.expose
@cherrypy.tools.json_out()
@huntdocs.apiDoc("GET", "/api/zones/getZones/",
"""Returns map coordinates of all spawn points of all targets in the indicated zones.

* Inputs:
    + **zoneIDs** - Comma separated list of zone IDs.
* Outputs:
    + **Data** - List of dictionaries containing the following for each zone:
        - **xCoord** - x coordinate of ANY target in the zone on in-game map.
        - **yCoord** - y coordinate of ANY target in the zone on in-game map.
""")
def renderPage(self, **params):
	try:
		zoneIDs = getInputs(params)
	except ValueError as e:
		return {"success": False, "message": e.message}
	
	zoneSpawns = getSpawns(zoneIDs)
	
	return {"success": True, "message": "OK", "data": zoneSpawns}
