import cherrypy
import datetime
import jinja2
import os.path
import psycopg2.extras
import time

import HuntDB

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
		
		if targetData["isNow"]:
			targetData["time"] = datetime.datetime.now()
		else:
			seconds = targetData.get("time", None)
			if seconds is not None:
				targetData["time"] = datetime.datetime.utcfromtimestamp(seconds)
		
		# Make sure we have all the data we need
		# TODO: Find a more graceful way of including None and/or multiple types
		requiredKeysAndTypes = [("targetID", [int,]), ("xCoord", [int, type(None)]), ("yCoord", [int, type(None)]), ("isDead", [bool,]), ("isNow", [bool,]), ("time", [datetime.datetime,])]
		for key, valueTypes in requiredKeysAndTypes:
			if key not in targetData or type(targetData[key]) not in valueTypes:
				return False
		
		# Verify map coordinates are within valid constraints
		
		minCoord = 0
		maxCoord = 41
		xCoord = targetData["xCoord"]
		yCoord = targetData["yCoord"]
		
		if xCoord is not None and (xCoord < minCoord or xCoord > maxCoord):
			return False
		
		if yCoord is not None and (yCoord < minCoord or yCoord > maxCoord):
			return False
		
		if targetData["isDead"] is None:
			return False
		
		# Make sure target exists
		dbConn, dbCursor = HuntDB.getConnectionWithCursor()
		
		dbCursor.execute("""SELECT count(1) FROM hunts.sightings WHERE hunts.sightings.targetID = %s;""", (targetData["targetID"],))
		targetExists = dbCursor.fetchone()
		
		HuntDB.putConnectionWithCursor(dbConn, dbCursor)
		
		if not targetExists:
			return False
		
		return True
	
	def isDuplicateSighting(self, targetData):
		dbConn, dbCursor = HuntDB.getConnectionWithCursor()
		
		# Get time since last report
		rowInputs = (targetData["time"], targetData["time"], targetData["targetID"], targetData["isDead"])
		dbCursor.execute("""SELECT abs(extract(epoch from datetime) - extract(epoch from %s)) AS timedelta, extract(epoch from %s) as inputTime FROM hunts.sightings WHERE targetID = %s AND isDead = %s ORDER BY timedelta ASC LIMIT 5;""", rowInputs)
		result = dbCursor.fetchone()
		
		HuntDB.putConnectionWithCursor(dbConn, dbCursor)
		
		if result is None:
			# Target has never been reported before, not a duplicate report
			return False
		
		# Consider it a duplicate if reported in the last 10 minutes
		nearestDelta = datetime.timedelta(seconds = result[0])
		minimumDelta = datetime.timedelta(minutes = 10)
		
		if nearestDelta < minimumDelta:
			return True
		else:
			return False
	
	def addSighting(self, targetData):
		dbConn, dbCursor = HuntDB.getConnectionWithCursor()
		
		submitterIP = cherrypy.request.remote.ip
		
		rowData = (targetData["time"], targetData["isDead"], targetData["targetID"], targetData["xCoord"], targetData["yCoord"], submitterIP)
		dbCursor.execute("""INSERT INTO hunts.sightings VALUES (%s);""" % ", ".join(("%s",)*len(rowData)), rowData)
		dbConn.commit()
		
		HuntDB.putConnectionWithCursor(dbConn, dbCursor)
	
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
		dbConn, dbCursor = HuntDB.getConnectionWithCursor(dictCursor = True)
		
		# Get most recent monster sightings
		dbCursor.execute("""SELECT DISTINCT ON (t.targetID) t.targetID, t.targetName, r.rankName, z.zoneName, extract(epoch from t.minSpawnTime) as minSpawnTime, extract(epoch from s.datetime) AS lastSeen, s.isDead FROM hunts.targets AS t JOIN hunts.ranks AS r ON t.rankID = r.rankID JOIN hunts.zones AS z ON t.zoneID = z.zoneID JOIN hunts.sightings AS s on t.targetID = s.targetID ORDER BY t.targetID, s.datetime DESC;""")
		targets = [dict(x) for x in dbCursor.fetchall()]
		
		HuntDB.putConnectionWithCursor(dbConn, dbCursor)
		
		return targets

class HuntServ(object):
	@cherrypy.expose
	def index(self, **params):
		dbConn, dbCursor = HuntDB.getConnectionWithCursor(dictCursor = True)
		
		# Get list of targets
		dbCursor.execute("""SELECT t.targetID, t.targetName FROM hunts.targets AS t ORDER BY t.targetName ASC;""")
		targetList = [dict(x) for x in dbCursor.fetchall()]
		
		HuntDB.putConnectionWithCursor(dbConn, dbCursor)
		
		template = env.get_template("hunts.tmpl")
		return template.render(title="FFXIV Hunt Tracker - Excalibur", targetList=targetList)
