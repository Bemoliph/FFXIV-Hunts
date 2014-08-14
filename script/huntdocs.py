import inspect
import markdown

def apiDoc(requestType, name, docstring):
	"Decorator for setting endpoint documentation."
	def apiDoc_(endpointFunc):
		endpointFunc.endpointDoc = (requestType, name, docstring)
		return endpointFunc
	return apiDoc_

def getEndpoints(obj):
	return (func[1] for func in inspect.getmembers(obj, predicate=inspect.ismethod))

def isExposed(func):
	return hasattr(func, "exposed") and func.exposed

def hasApiDoc(func):
	return hasattr(func, "endpointDoc")

def getApiDocs(obj):
	return (endpoint.endpointDoc for endpoint in getEndpoints(obj) if isExposed(endpoint) and hasApiDoc(endpoint))

def generateApiDocs(apiDocs):
	# TODO:  Stop cheating
	html = "<html>\n<body>\n%s</body>\n</html>"
	docsHtml = ""
	
	for requestType, name, docstring in apiDocs:
		docsHtml += "<h3>%s %s</h3>\n%s\n" % (requestType, name, markdown.markdown(docstring))
	
	return html % docsHtml
