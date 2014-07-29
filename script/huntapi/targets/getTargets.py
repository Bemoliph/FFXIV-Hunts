import cherrypy
import time

import huntdb
import huntutils

class GetTargets(object):
	def getTargets(self):
		dbConn, dbCursor = huntdb.getConnectionWithCursor(dictCursor = True)
		
		query = """
			SELECT t.targetID, t.targetName, r.rankName, z.zoneName, extract(epoch from t.minSpawnTime) as minSpawnTime
			FROM hunts.targets AS t
			JOIN hunts.ranks AS r ON r.rankID = t.rankID
			JOIN hunts.zones AS z ON z.zoneID = t.zoneID;"""
		dbCursor.execute(query)
		targets = [dict(x) for x in dbCursor.fetchall()]
		
		huntdb.putConnectionWithCursor(dbConn, dbCursor)
		
		return targets
	
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def index(self, **params):
		targets = self.getTargets()
		
		return {"success": True, "message": "OK", "data": targets}