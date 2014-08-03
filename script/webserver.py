import cherrypy
import psycopg2

from huntsite import huntsite
from huntapi import huntapi

root = huntsite.HuntSite()
root.api = huntapi.HuntAPI()

if __name__ == "__main__":
	cherrypy.quickstart(root, config="cherrypy.cfg")