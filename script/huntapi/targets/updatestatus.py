import cherrypy
import datetime
import time

import huntdb
import huntdocs

def getInputs(rawInput):
	if type(rawInput) is not dict:
		raise ValueError("Expected dictionary, got %s" % type(rawInput))
	
	# TODO: Implement proper authentication, sessions and/or API keys
	password = rawInput.get("password")
	if password != "placeholder":
		raise ValueError("Invalid password.")
	
	if "time" not in rawInput:
		rawInput["time"] = time.time()
	
	# Make sure we have all the data we need
	# TODO: Find a more graceful way of including None and/or multiple types
	requiredKeysAndTypes = [("targetID", [int,]), ("xCoord", [int, type(None)]), ("yCoord", [int, type(None)]), ("isDead", [bool,]), ("time", [int, float])]
	for key, valueTypes in requiredKeysAndTypes:
		if key not in rawInput:
			raise ValueError("Missing mandatory input '%s'." % key)
		elif type(rawInput[key]) not in valueTypes:
			raise ValueError("'%s' must be %s, got %s" % (valueTypes, type(rawInput[key])))
	
	targetStatus = {}
	targetStatus["targetID"] = rawInput.get("targetID")
	targetStatus["xCoord"] = rawInput.get("xCoord")
	targetStatus["yCoord"] = rawInput.get("yCoord")
	targetStatus["isDead"] = rawInput.get("isDead")
	targetStatus["time"] = datetime.datetime.utcfromtimestamp(rawInput.get("time"))
	
	# Verify map coordinates are within valid constraints
	minCoord = 0
	maxCoord = 41
	xCoord = targetStatus.get("xCoord")
	yCoord = targetStatus.get("yCoord")
	
	if xCoord is not None and (xCoord < minCoord or xCoord > maxCoord):
		raise ValueError("'xCoord' is out of range [%s, %s], got %s." % (minCoord, maxCoord, xCoord))
	
	if yCoord is not None and (yCoord < minCoord or yCoord > maxCoord):
		raise ValueError("'yCoord' is out of range [%s, %s], got %s." % (minCoord, maxCoord, yCoord))
	
	# Make sure target exists
	dbConn, dbCursor = huntdb.getConnectionWithCursor()
	
	dbCursor.execute("""SELECT count(1) FROM hunts.sightings WHERE hunts.sightings.targetID = %s;""", (targetStatus.get("targetID"),))
	targetExists = dbCursor.fetchone()
	
	huntdb.putConnectionWithCursor(dbConn, dbCursor)
	
	if not targetExists:
		raise ValueError("Invalid targetID.")
	
	return targetStatus

def isDuplicateSighting(targetData):
	dbConn, dbCursor = huntdb.getConnectionWithCursor()
	
	# Get time since last report
	query = """
		SELECT abs(extract(epoch from datetime) - extract(epoch from %s)) AS timedelta
		FROM hunts.sightings
		WHERE targetID = %s AND isDead = %s
		ORDER BY timedelta ASC
		LIMIT 1;"""
	queryInputs = (targetData["time"], targetData["targetID"], targetData["isDead"])
	dbCursor.execute(query, queryInputs)
	result = dbCursor.fetchone()
	
	huntdb.putConnectionWithCursor(dbConn, dbCursor)
	
	if result is None:
		# Target has never been reported before, not a duplicate report
		return False
	
	# Consider it a duplicate if reported in the last 10 minutes
	nearestDelta = datetime.timedelta(seconds = result[0])
	minimumDelta = datetime.timedelta(minutes = 10)
	
	if nearestDelta < minimumDelta:
		return True
	else:
		return False

def addSighting(targetData):
	dbConn, dbCursor = huntdb.getConnectionWithCursor()
	
	submitterIP = None
	
	rowData = (targetData["time"], targetData["isDead"], targetData["targetID"], targetData["xCoord"], targetData["yCoord"], submitterIP)
	dbCursor.execute("""INSERT INTO hunts.sightings VALUES (%s);""" % ", ".join(("%s",)*len(rowData)), rowData)
	dbConn.commit()
	
	huntdb.putConnectionWithCursor(dbConn, dbCursor)

@cherrypy.expose
@cherrypy.tools.json_in()
@cherrypy.tools.json_out()
@huntdocs.apiDoc("POST", "/api/target/updateStatus/",
"""Updates the current status of the indicated target.

* Input:
    + **targetID** - ID of the target to update.
    + **time** - (optional) Time of status change, in seconds.  If not set, time of query will be used.
    + **isDead** - True if time of death, False if time of sighting.
    + **xCoord** - x coordinate of target on in-game map.
    + **yCoord** - y coordinate of target on in-game map.
""")
def renderPage(self, **params):
	try:
		rawInputs = cherrypy.request.json
	except AttributeError:
		return {"success": False, "message": "updateStatus only supports JSON via POST."}
	
	try:
		targetStatus = getInputs(rawInputs)
	except ValueError as e:
		return {"success": False, "message": e.message}
	
	if isDuplicateSighting(targetStatus):
		return {"success": False, "message": "Duplicate sighting."}
	
	addSighting(targetStatus)
	
	return {"success":True, "message":"Sighting added."}
