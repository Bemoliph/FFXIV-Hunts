import cherrypy
import time

import huntdb
import huntutils

class GetHistory(object):
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
	
	def getHistories(self, inputData):
		dbConn, dbCursor = huntdb.getConnectionWithCursor(dictCursor = True)
		
		if "after" in inputData:
			query = """
				SELECT extract(epoch from datetime) as datetime, isDead, xCoord, yCoord
				FROM hunts.sightings
				WHERE targetID = %s AND %s < datetime
				ORDER BY datetime DESC
				LIMIT %s;"""
			timePartition = inputData["after"]
		else:
			query = """
				SELECT extract(epoch from datetime) as datetime, isDead, xCoord, yCoord
				FROM hunts.sightings
				WHERE targetID = %s AND datetime < %s
				ORDER BY datetime DESC
				LIMIT %s;"""
			timePartition = inputData["before"]
		
		targetHistories = {}
		for tID in inputData["targetIDs"]:
			queryInput = (tID, timePartition, inputData["maxRecords"])
			dbCursor.execute(query, queryInput)
			targetHistories[tID] = [dict(x) for x in dbCursor.fetchall()]
		
		huntdb.putConnectionWithCursor(dbConn, dbCursor)
		
		return targetHistories
	
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def index(self, **params):
		try:
			inputData = self.getInputs(params)
		except ValueError as e:
			return {"success": False, "message": e.message}
		
		targetHistories = self.getHistories(inputData)
		
		return {"success": True, "message": "OK", "data": targetHistories}