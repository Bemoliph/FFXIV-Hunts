import cherrypy

class Thing(object):
	@cherrypy.expose
	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()
	def index(self, **params):
		rawInputs = cherrypy.request.json