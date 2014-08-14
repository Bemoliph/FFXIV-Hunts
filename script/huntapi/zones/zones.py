import cherrypy

import huntdocs

import getzones
import getspawns

class Zones(object):
	getZones = getzones.renderPage
	getSpawns = getspawns.renderPage
	
	@cherrypy.expose
	def index(self, **params):
		return huntdocs.generateApiDocs(huntdocs.getApiDocs(self))
