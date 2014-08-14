import cherrypy
import time

import huntdb
import huntdocs
import huntutils

def getTargetIDs(params):
	if "targetIDs" not in params or not params["targetIDs"]:
		raise ValueError("Missing mandatory input 'targetIDs'.")
	else:
		return huntutils.parseCSV(int, "targetIDs", params.get("targetIDs"))

def getStatus(targetIDs):
	dbConn, dbCursor = huntdb.getConnectionWithCursor(dictCursor = True)
	
	query = """
		SELECT DISTINCT ON (targetID) extract(epoch from datetime) AS lastSeen, isDead
		FROM hunts.sightings
		WHERE targetID = %s
		ORDER BY targetID, datetime DESC;"""
	
	statuses = {}
	for tID in targetIDs:
		dbCursor.execute(query, (tID, ))
		state = dbCursor.fetchone()
		if state is not None:
			statuses[tID] = dict(state)
		else:
			statuses[tID] = None
	
	huntdb.putConnectionWithCursor(dbConn, dbCursor)
	
	return statuses

@cherrypy.expose
@cherrypy.tools.json_out()
@huntdocs.apiDoc("GET", "/api/target/getStatus/",
"""Returns the current status of the specified targets.

* Input:
    + **targetIDs** - Comma separated list of target IDs.
* Output:
    + **data** - Dictionary of targetID:dictionary pairs containing the following:
        - **isDead** - True if last reported dead, False if last reported alive.
        - **lastSeen** - UNIX timestamp of last status update for target.
""")
def renderPage(self, **params):
	try:
		targetIDs = getTargetIDs(params)
	except ValueError as e:
		return {"success": False, "message": e.message}
	
	statuses = getStatus(targetIDs)
	
	return {"success": True, "message": "OK", "data": statuses}
