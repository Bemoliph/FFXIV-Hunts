import cherrypy
from huntserv import HuntServ

root = HuntServ.HuntServ()
root.api = HuntServ.HuntApi()

if __name__ == "__main__":
	config = {
				'global': {
					'server.socket_host':'0.0.0.0',
					'server.socket_port':80,
				},
				
				'/static': {
					'tools.staticdir.dir':"E:\\Users\\Bemoliph\\Desktop\\ffxiv-hunts\\ffxiv-hunts\\static",
					'tools.staticdir.on': True,
				}
			}
	cherrypy.quickstart(root, config=config)