import cherrypy

from getZones import GetZones
from getSpawns import GetSpawns

class Zones(object):
	@cherrypy.expose
	def index(self, **params):
		# TODO: API docs
		return ""
	
	getZones = GetZones()
	getSpawns = GetSpawns()