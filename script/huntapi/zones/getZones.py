import cherrypy
import time

import huntdb
import huntdocs

def getZones():
	dbConn, dbCursor = huntdb.getConnectionWithCursor(dictCursor = True)
	
	query = """SELECT zoneID, zoneName FROM hunts.zones ORDER BY zoneID ASC;"""
	dbCursor.execute(query)
	zones = [dict(x) for x in dbCursor.fetchall()]
	
	huntdb.putConnectionWithCursor(dbConn, dbCursor)
	
	return zones

@cherrypy.expose
@cherrypy.tools.json_out()
@huntdocs.apiDoc("GET", "/api/zones/getZones/",
"""Returns a list of all hunt-enabled zones.

* Inputs:
    + None
* Outputs:
    + **Data** - List of dictionaries containing the following for each zone:
        - **zoneID** - ID of the zone, useful for other queries.
        - **zoneName** - Name of the zone.
""")
def renderPage(self, **params):
	zones = getZones()
	
	return {"success": True, "message": "OK", "data": zones}
