import cherrypy
import time

import huntdb
import huntdocs
import huntutils

def getTargets():
	dbConn, dbCursor = huntdb.getConnectionWithCursor(dictCursor = True)
	
	query = """
		SELECT t.targetID, t.targetName, r.rankName, z.zoneName, extract(epoch from t.minSpawnTime) as minSpawnTime
		FROM hunts.targets AS t
		JOIN hunts.ranks AS r ON r.rankID = t.rankID
		JOIN hunts.zones AS z ON z.zoneID = t.zoneID
		ORDER BY t.targetID ASC;"""
	dbCursor.execute(query)
	targets = [dict(x) for x in dbCursor.fetchall()]
	
	huntdb.putConnectionWithCursor(dbConn, dbCursor)
	
	return targets

@cherrypy.expose
@cherrypy.tools.json_out()
@huntdocs.apiDoc("GET", "/api/target/getTargets/",
"""Returns a list of all targets.

* Input:
    + None
* Output:
    + **data** - List of dictionaries containing the following for each target:
        - **targetID** - ID of the target, useful for other queries.
        - **targetName** - Name of the target.
        - **rankName** - Rank of target, either B, A, or S.
        - **zoneName** - Name of the zone the target spawns in.
        - **minSpawnTime** - The minimum amount of time it takes for the target to respawn, in seconds.
""")
def renderPage(self, **params):
	targets = getTargets()
	
	return {"success": True, "message": "OK", "data": targets}
