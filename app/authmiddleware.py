class AuthMiddleware(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        print("middleware accessed")
    
        headers = environ['werkzeug.request'].headers
        
        for header in headers.keys():
            print("%s=%s" % (header, headers[header]))

        return self.app(environ, start_response)