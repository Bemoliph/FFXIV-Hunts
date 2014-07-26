import ConfigParser
import psycopg2.pool

def createConnectionPool():
	config = ConfigParser.ConfigParser()
	config.read("database.cfg")
	
	user = config.get("postgresql", "user")
	password = config.get("postgresql", "password")
	host = config.get("postgresql", "host")
	database = config.get("postgresql", "database")
	
	minPoolSize = config.getint("postgresql", "minPoolSize")
	maxPoolSize = config.getint("postgresql", "maxPoolSize")
	
	pool = psycopg2.pool.ThreadedConnectionPool(minconn=minPoolSize, maxconn=maxPoolSize, user=user, password=password, host=host, database=database)
	
	return pool

pool = createConnectionPool()