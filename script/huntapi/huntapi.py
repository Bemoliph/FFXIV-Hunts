import cherrypy

from targets import targets
from zones import zones

class HuntAPI(object):
	@cherrypy.expose
	def index(self, **params):
		# TODO: API docs
		return ""
	
	targets = targets.Targets()
	zones = zones.Zones()
