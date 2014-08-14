import cherrypy

import huntdocs

import gettargets
import getstatus
import gethistory
import getspawns
import getdeltas

import updatestatus

class Targets(object):
	getTargets = gettargets.renderPage
	getStatus = getstatus.renderPage
	getHistory = gethistory.renderPage
	getSpawns = getspawns.renderPage
	getDeltas = getdeltas.renderPage
	
	updateStatus = updatestatus.renderPage
	
	@cherrypy.expose
	def index(self, **params):
		return huntdocs.generateApiDocs(huntdocs.getApiDocs(self))
