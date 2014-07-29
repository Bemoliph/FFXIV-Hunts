import cherrypy
import datetime
import jinja2
import os.path
import psycopg2.extras

import huntdb

# Set up template environment
env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

class HuntSite(object):
	@cherrypy.expose
	def index(self, **params):
		dbConn, dbCursor = huntdb.getConnectionWithCursor(dictCursor = True)
		
		# Get list of targets
		dbCursor.execute("""SELECT t.targetID, t.targetName FROM hunts.targets AS t ORDER BY t.targetName ASC;""")
		targetList = [dict(x) for x in dbCursor.fetchall()]
		
		huntdb.putConnectionWithCursor(dbConn, dbCursor)
		
		template = env.get_template("hunts.tmpl")
		return template.render(title="FFXIV Hunt Tracker - Excalibur", targetList=targetList)
