import ast
import datetime

def parseCSV(valueType, inputName, csvString):
	try:
		# Convert string to basic data types
		values = ast.literal_eval(csvString)
	except ValueError:
		# Couldn't parse malformed input
		raise ValueError("'%s' malformed, could not parse CSV: %s." % (inputName, csvString))
	
	if type(values) is valueType:
		# Found single value of desired type, wrap and send it back
		return (values, )
	
	if type(values) is not tuple:
		# Got something, just not what we wanted
		raise ValueError("'%s' must be comma separated %s." % (inputName, valueType))
		
	for tID in values:
		if type(tID) is not valueType:
			# One of the values wasn't the desired type
			raise ValueError("All values in '%s' must be %s, got %s" % (inputName, valueType, tID))
	
	return values

def getConstrainedValue(lower, value, upper):
	return min([max([value, lower]), upper])

def getDatetime(inputName, seconds):
	if seconds is None:
		return None
	
	try:
		return datetime.datetime.utcfromtimestamp(seconds)
	except TypeError:
		raise ValueError("'%s' must be an integer or a float." % inputName)

def parseValue(desiredType, inputName, value):
	if type(value) is desiredType or type(value) is None:
		return value
	
	try:
		parsedValue = ast.literal_eval(value)
	except ValueError as e:
		raise ValueError("'%s' malformed, could not parse: %s" % (inputName, value))
	
	if type(parsedValue) is not desiredType:
			raise ValueError("'%s' must be %s, got %s" % (inputName, desiredType, type(parsedValue)))
	
	return parsedValue