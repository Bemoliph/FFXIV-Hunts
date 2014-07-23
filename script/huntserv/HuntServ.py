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
	
	def getTargetData(self, params):
		targetData = {}
		
		try:
			targetData["targetID"] = int(params.get("targetID", None))
		except ValueError:
			targetData["targetID"] = None
		
		try:
			targetData["xCoord"] = int(params.get("xCoord", None))
		except ValueError:
			targetData["targetID"] = None
		
		try:
			targetData["yCoord"] = int(params.get("yCoord", None))
		except ValueError:
			targetData["targetID"] = None
		
		targetData["datetime"] = datetime.datetime.now()
		targetData["password"] = params.get("password", None)
		
		return targetData
	
	def isValidTargetData(self, targetData):
		if type(targetData) is not dict:
			return False
		
		# TODO: remove
		if targetData["password"] != "1ObVxHAN":
			return False
		
		# Make sure we have all the data we need
		requiredKeysAndTypes = [("targetID", int), ("xCoord", int), ("yCoord", int), ("datetime", datetime.datetime)]
		for key, valueType in requiredKeysAndTypes:
			if key not in targetData or type(targetData[key]) is not valueType:
				return False
		
		# Verify map coordinates are within valid constraints
		minCoord = 0
		maxCoord = 41
		xCoord = targetData["xCoord"]
		yCoord = targetData["yCoord"]
		
		if (xCoord < 0 or xCoord > 41) or (yCoord < 0 or yCoord > 41):
			return False
		
		# Make sure target exists
		dbConn = pool.getconn()
		dbCursor = dbConn.cursor()
		
		dbCursor.execute("""SELECT count(1) FROM hunts.sightings WHERE hunts.sightings.targetID = %s""", (targetData["targetID"],))
		targetExists = dbCursor.fetchone()
		
		dbCursor.close()
		pool.putconn(dbConn)
		
		if not targetExists:
			return False
		
		return True
	
	def isDuplicateSighting(self, targetData):
		# Duplicate as defined by already reported in the last five minutes
		dbConn = pool.getconn()
		dbCursor = dbConn.cursor()
		
		dbCursor.execute("""SELECT age(datetime) as lastDatetime FROM hunts.sightings WHERE targetID = %s ORDER BY datetime DESC LIMIT 1""", (targetData["targetID"],))
		lastDatetime = dbCursor.fetchone()
		
		dbCursor.close()
		pool.putconn(dbConn)
		
		if lastDatetime is None:
			# Target has never been reported before, not a duplicate report
			return False
		elif lastDatetime[0] < datetime.timedelta(minutes = 5):
			return True
		else:
			return False
	
	def addSighting(self, targetData):
		dbConn = pool.getconn()
		dbCursor = dbConn.cursor()
		
		#submitterIP = cherrypy.request.headers['HTTP_X_FORWARDED_FOR']
		submitterIP = cherrypy.request.remote.ip
		rowData = (targetData["datetime"], targetData["targetID"], targetData["xCoord"], targetData["yCoord"], submitterIP)
		dbCursor.execute("""INSERT INTO hunts.sightings VALUES (%s)""" % ", ".join(("%s",)*len(rowData)), rowData)
		
		dbConn.commit()
		dbCursor.close()
		pool.putconn(dbConn)
	
	def crunchSightingStats(self, targetData):
		# TODO: regenerate stats for reported monster
		pass
	
	@cherrypy.expose
	#@cherrypy.tools.json_in()
	#@cherrypy.tools.json_out()
	def updateTarget(self, **params):
		#targetData = cherrypy.request.json
		targetData = self.getTargetData(params)
		
		if not self.isValidTargetData(targetData):
			raise cherrypy.HTTPRedirect("/")
			#return {"success":False, w"message":"Invalid input."}
		
		if self.isDuplicateSighting(targetData):
			raise cherrypy.HTTPRedirect("/")
			#return {"success":False, "message":"Duplicate sighting."}
		
		self.addSighting(targetData)
		self.crunchSightingStats(targetData)
		
		#return {"success":True, "message":"Sighting added."}
		raise cherrypy.HTTPRedirect("/")
	
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def getTargets(self, **params):
		dbConn = pool.getconn()
		dbCursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
		
		# Get most recent monster sightings
		dbCursor.execute("""SELECT DISTINCT ON (t.targetID) t.targetID, t.targetName, r.rankName, z.zoneName, extract(epoch from s.datetime)*1000 AS lastSeen FROM hunts.targets AS t JOIN hunts.ranks AS r ON t.rankID = r.rankID JOIN hunts.zones AS z ON t.zoneID = z.zoneID JOIN hunts.sightings AS s on t.targetID = s.targetID ORDER BY t.targetID, s.datetime DESC;""")
		targets = [dict(x) for x in dbCursor.fetchall()]
		
		dbCursor.close()
		pool.putconn(dbConn)
		
		return targets

class HuntServ(object):
	@cherrypy.expose
	def index(self, **params):
		dbConn = pool.getconn()
		dbCursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
		
		# Get most recent monster sightings
		dbCursor.execute("""SELECT t.targetID, t.targetName FROM hunts.targets AS t ORDER BY t.targetName ASC;""")
		targetList = [dict(x) for x in dbCursor.fetchall()]
		
		dbCursor.close()
		pool.putconn(dbConn)
		
		template = env.get_template("hunts.tmpl")
		return template.render(title="FFXIV Hunt Tracker - Excalibur", targetList=targetList)
