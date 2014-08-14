import cherrypy
import time

import huntdb
import huntdocs
import huntutils

def getInputs(params):
	inputData = {}
	
	if "targetIDs" not in params or not params["targetIDs"]:
		raise ValueError("Missing mandatory input 'targetIDs'.")
	
	inputData["targetIDs"] = huntutils.parseCSV(int, "targetIDs", params.get("targetIDs"))
	inputData["maxRecords"] = huntutils.getConstrainedValue(1, huntutils.parseValue(int, "maxRecords", params.get("maxRecords", 10)), 1000)
	
	return inputData

def getDeltas(inputData):
	dbConn, dbCursor = huntdb.getConnectionWithCursor(dictCursor = True)
	
	query = """
		SELECT extract(epoch from datetime - lag(datetime) OVER (ORDER BY datetime)) AS spawnDelta
		FROM hunts.sightings
		WHERE targetID = %s
		ORDER BY spawnDelta ASC
		LIMIT %s;"""
	
	spawnDeltas = {}
	for tID in inputData["targetIDs"]:
		queryInput = (tID, inputData["maxRecords"])
		dbCursor.execute(query, queryInput)
		spawnDeltas[tID] = [x['spawndelta'] for x in dbCursor.fetchall()]
	
	huntdb.putConnectionWithCursor(dbConn, dbCursor)
	
	return spawnDeltas

@cherrypy.expose
@cherrypy.tools.json_out()
@huntdocs.apiDoc("GET", "/api/target/getDeltas/",
"""Returns a list of shortest times between consecutive sightings of the specified targets.

* Input:
    + **targetIDs** - Comma separated list of target IDs.
	+ **maxRecords** - (optional) Maximum number of records to return per target ID.  Default 10, max 1000.
* Output:
    + **data** - Dictionary of targetID:list pairs containing up to maxRecord of the following:
	    - **spawnDelta** - Number of seconds between two consecutive sightings.
""")
def renderPage(self, **params):
	try:
		inputData = getInputs(params)
	except ValueError as e:
		return {"success": False, "message": e.message}
	
	targetHistories = getDeltas(inputData)
	
	return {"success": True, "message": "OK", "data": targetHistories}
