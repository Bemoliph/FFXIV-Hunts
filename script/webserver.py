import cherrypy
import psycopg2

from huntsite import huntsite
from huntapi import huntapi

root = huntsite.HuntSite()
root.api = huntapi.HuntAPI()

def connect():
	credentials = cherrypy.config.get("database")
	print credentials
	
	pool = psycopg2.pool.ThreadedConnectionPool(1, 10, **credentials)
	
	return pool

if __name__ == "__main__":
	cherrypy.quickstart(root, config="cherrypy.cfg")
	pool = connect()