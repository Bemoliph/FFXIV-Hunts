import cherrypy
import time

import huntdb
import huntutils

class GetStatus(object):
	def getTargetIDs(self, params):
		if "targetIDs" not in params or not params["targetIDs"]:
			raise ValueError("Missing mandatory input 'targetIDs'.")
		else:
			return huntutils.parseCSV(int, "targetIDs", params.get("targetIDs"))
	
	def getStatus(self, targetIDs):
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
	def index(self, **params):
		try:
			targetIDs = self.getTargetIDs(params)
		except ValueError as e:
			return {"success": False, "message": e.message}
		
		statuses = self.getStatus(targetIDs)
		
		return {"success": True, "message": "OK", "data": statuses}