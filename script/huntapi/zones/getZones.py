import cherrypy
import time

import huntdb
import huntutils

class GetZones(object):
	def getZones(self):
		dbConn, dbCursor = huntdb.getConnectionWithCursor(dictCursor = True)
		
		query = """SELECT zoneID, zoneName FROM hunts.zones ORDER BY zoneID ASC;"""
		dbCursor.execute(query)
		zones = [dict(x) for x in dbCursor.fetchall()]
		
		huntdb.putConnectionWithCursor(dbConn, dbCursor)
		
		return zones
	
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def index(self, **params):
		zones = self.getZones()
		
		return {"success": True, "message": "OK", "data": zones}