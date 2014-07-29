import cherrypy
import time

import huntdb
import huntutils

class GetStatus(object):
	def getTargetIDs(self, params):
		if "targetIDs" not in params or not params["targetIDs"]:
			return None
		else:
			return huntutils.parseCSV(int, "targetIDs", params.get("targetIDs"))
	
	def getStatus(self, inputData):
		dbConn, dbCursor = huntdb.getConnectionWithCursor(dictCursor = True)
		
		query = """
			SELECT DISTINCT ON (t.targetID) t.targetID, t.targetName, r.rankName, z.zoneName, extract(epoch from t.minSpawnTime) as minSpawnTime, extract(epoch from s.datetime) AS lastSeen, s.isDead
			FROM hunts.targets AS t
			JOIN hunts.ranks AS r ON t.rankID = r.rankID
			JOIN hunts.zones AS z ON t.zoneID = z.zoneID
			JOIN hunts.sightings AS s on t.targetID = s.targetID
			ORDER BY t.targetID, s.datetime DESC;"""
		dbCursor.execute(query)
		targetStatus = [dict(x) for x in dbCursor.fetchall()]
		
		huntdb.putConnectionWithCursor(dbConn, dbCursor)
		
		return targetStatus
	
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def index(self, **params):
		try:
			targetIDs = self.getTargetIDs(params)
		except ValueError as e:
			return {"success": False, "message": e.message}
		
		targetStatus = self.getStatus(targetIDs)
		
		return {"success": True, "message": "OK", "data": targetStatus}