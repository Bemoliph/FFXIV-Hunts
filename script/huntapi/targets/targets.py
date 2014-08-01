import cherrypy

from getHistory import GetHistory
from getTargets import GetTargets
from getStatus import GetStatus
from getSpawns import GetSpawns

from updateStatus import UpdateStatus

class Targets(object):
	@cherrypy.expose
	def index(self, **params):
		# TODO: API docs
		return ""
	
	getHistory = GetHistory()
	getTargets = GetTargets()
	getStatus = GetStatus()
	getSpawns = GetSpawns()
	
	updateStatus = UpdateStatus()
