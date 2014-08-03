import cherrypy
import psycopg2

from huntapi import huntapi

api = huntapi.HuntAPI()

if __name__ == "__main__":
	cherrypy.quickstart(api, "/api", config="cherrypy.cfg")