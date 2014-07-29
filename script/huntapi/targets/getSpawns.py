import cherrypy
import time

import huntdb
import huntutils

class GetSpawns(object):
	def getInputs(self, params):
		inputData = {}
		
		if "targetIDs" not in params or not params["targetIDs"]:
			raise ValueError("Missing mandatory input 'targetIDs'.")
		
		inputData["targetIDs"] = huntutils.parseCSV(int, "targetIDs", params.get("targetIDs"))
		inputData["maxRecords"] = huntutils.getConstrainedValue(1, huntutils.parseValue(int, "maxRecords", params.get("maxRecords", 10)), 1000)
		inputData["before"] = huntutils.getDatetime("before", huntutils.parseValue(float, "before", params.get("before", time.time())))
		if "after" in params:
			inputData["after"] = huntutils.getDatetime("after", huntutils.parseValue(float, "after", params.get("after")))
		
		return inputData
	
	def getSpawns(self, inputData):
		dbConn, dbCursor = huntdb.getConnectionWithCursor(dictCursor = True)
		
		query = """
			SELECT DISTINCT ON (xCoord, yCoord) xCoord, yCoord
			FROM hunts.sightings
			WHERE targetID = %s AND xCoord IS NOT NULL AND yCoord IS NOT NULL
			ORDER BY xCoord, yCoord ASC;"""
		
		targetSpawns = {}
		for tID in inputData["targetIDs"]:
			queryInput = (tID, )
			dbCursor.execute(query, queryInput)
			targetSpawns[tID] = [dict(x) for x in dbCursor.fetchall()]
		
		huntdb.putConnectionWithCursor(dbConn, dbCursor)
		
		return targetSpawns
	
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def index(self, **params):
		try:
			inputData = self.getInputs(params)
		except ValueError as e:
			return {"success": False, "message": e.message}
		
		targetSpawns = self.getSpawns(inputData)
		
		return {"success": True, "message": "OK", "data": targetSpawns}