import cherrypy
import datetime
import jinja2
import os.path
import psycopg2, psycopg2.pool, psycopg2.extras

def connect():
	# TODO: move this stuff into a config somewhere
	user = "hunts"
	password = "***REMOVED***"
	host = "127.0.0.1"
	database = "ffxiv"
	
	pool = psycopg2.pool.ThreadedConnectionPool(1, 10, user=user, password=password, host=host, database=database)
	
	return pool

pool = connect()

# Set up template environment
env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

class HuntApi(object):
	@cherrypy.expose
	def index(self, **params):
		# TODO: API docs
		return ""
	
	def isValidTargetData(self, targetData):
		if type(targetData) is not dict:
			return False
		
		# TODO: Implement proper authentication, sessions and/or API keys
		password = targetData.get("password")
		if password != "***REMOVED***":
			return False
		
		seconds = targetData.get("time", None)
		if seconds is not None:
			targetData["time"] = datetime.datetime.fromtimestamp(seconds)
		
		# Make sure we have all the data we need
		requiredKeysAndTypes = [("targetID", int), ("xCoord", int), ("yCoord", int), ("isDead", bool), ("isNow", bool), ("time", datetime.datetime)]
		for key, valueType in requiredKeysAndTypes:
			if key not in targetData or type(targetData[key]) is not valueType:
				return False
		
		# Verify map coordinates are within valid constraints
		minCoord = 0
		maxCoord = 41
		xCoord = targetData["xCoord"]
		yCoord = targetData["yCoord"]
		
		if (xCoord < minCoord or xCoord > maxCoord) or (yCoord < minCoord or yCoord > maxCoord):
			return False
		
		if targetData["isDead"] is None:
			return False
		
		# Make sure target exists
		dbConn = pool.getconn()
		dbCursor = dbConn.cursor()
		
		dbCursor.execute("""SELECT count(1) FROM hunts.sightings WHERE hunts.sightings.targetID = %s;""", (targetData["targetID"],))
		targetExists = dbCursor.fetchone()
		
		dbCursor.close()
		pool.putconn(dbConn)
		
		if not targetExists:
			return False
		
		return True
	
	def isDuplicateSighting(self, targetData):
		dbConn = pool.getconn()
		dbCursor = dbConn.cursor()
		
		if targetData["isDead"]:
			# Get time since last killed report
			dbCursor.execute("""SELECT age(datetime, %s) FROM hunts.sightings WHERE targetID = %s AND isDead ORDER BY age(datetime, %s) DESC LIMIT 1;""", (targetData["time"], targetData["targetID"], targetData["time"]))
		else:
			# Get time since last sighted report
			dbCursor.execute("""SELECT age(datetime, %s) FROM hunts.sightings WHERE targetID = %s AND NOT isDead ORDER BY age(datetime, %s) DESC LIMIT 1;""", (targetData["time"], targetData["targetID"], targetData["time"]))
		
		nearestTimedelta = dbCursor.fetchone()
		
		dbCursor.close()
		pool.putconn(dbConn)
		
		if nearestTimedelta is None:
			# Target has never been reported before, not a duplicate report
			return False
		#elif nearestTimedelta[0] < datetime.timedelta(minutes = 10):
		elif abs(nearestTimedelta[0].total_seconds()) < abs(datetime.timedelta(minutes = -10).total_seconds()):
			# Consider it a duplicate if reported in the last 10 minutes
			return True
		else:
			return False
	
	def addSighting(self, targetData):
		dbConn = pool.getconn()
		dbCursor = dbConn.cursor()
		
		#submitterIP = cherrypy.request.headers['HTTP_X_FORWARDED_FOR']
		submitterIP = cherrypy.request.remote.ip
		
		rowData = (targetData["time"], targetData["isDead"], targetData["targetID"], targetData["xCoord"], targetData["yCoord"], submitterIP)
		dbCursor.execute("""INSERT INTO hunts.sightings VALUES (%s);""" % ", ".join(("%s",)*len(rowData)), rowData)
		
		dbConn.commit()
		dbCursor.close()
		pool.putconn(dbConn)
	
	def crunchSightingStatistics(self, targetData):
		# TODO: regenerate stats for reported monster
		pass
	
	@cherrypy.expose
	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()
	def updateTarget(self, **params):
		targetData = cherrypy.request.json
		
		if not self.isValidTargetData(targetData):
			return {"success":False, "message":"Invalid input."}
		
		if self.isDuplicateSighting(targetData):
			return {"success":False, "message":"Duplicate sighting."}
		
		self.addSighting(targetData)
		self.crunchSightingStatistics(targetData)
		
		return {"success":True, "message":"Sighting added."}
	
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def getTargets(self, **params):
		dbConn = pool.getconn()
		dbCursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
		
		# Get most recent monster sightings
		dbCursor.execute("""SELECT DISTINCT ON (t.targetID) t.targetID, t.targetName, r.rankName, z.zoneName, extract(epoch from t.minSpawnTime) as minSpawnTime, extract(epoch from s.datetime) AS lastSeen, s.isDead FROM hunts.targets AS t JOIN hunts.ranks AS r ON t.rankID = r.rankID JOIN hunts.zones AS z ON t.zoneID = z.zoneID JOIN hunts.sightings AS s on t.targetID = s.targetID ORDER BY t.targetID, s.datetime DESC;""")
		targets = [dict(x) for x in dbCursor.fetchall()]
		
		dbCursor.close()
		pool.putconn(dbConn)
		
		return targets

class HuntServ(object):
	@cherrypy.expose
	def index(self, **params):
		dbConn = pool.getconn()
		dbCursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
		
		# Get list of targets
		dbCursor.execute("""SELECT t.targetID, t.targetName FROM hunts.targets AS t ORDER BY t.targetName ASC;""")
		targetList = [dict(x) for x in dbCursor.fetchall()]
		
		dbCursor.close()
		pool.putconn(dbConn)
		
		template = env.get_template("hunts.tmpl")
		return template.render(title="FFXIV Hunt Tracker - Excalibur", targetList=targetList)
