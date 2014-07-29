import cherrypy
import time

import huntdb
import huntutils

class GetSpawns(object):
	def getInputs(self, params):
		if "zoneIDs" not in params or not params["zoneIDs"]:
			raise ValueError("Missing mandatory input 'zoneIDs'.")
		
		return huntutils.parseCSV(int, "zoneIDs", params.get("zoneIDs"))
	
	def getSpawns(self, zoneIDs):
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
	def index(self, **params):
		try:
			zoneIDs = self.getInputs(params)
		except ValueError as e:
			return {"success": False, "message": e.message}
		
		zoneSpawns = self.getSpawns(zoneIDs)
		
		return {"success": True, "message": "OK", "data": zoneSpawns}