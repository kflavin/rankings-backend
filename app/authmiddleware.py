class AuthMiddleware(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        print("middleware accessed")
        # from pprint import pprint
        # print(environ['werkzeug.request'].headers)
        # print(environ['werkzeug.request'].cookies)
        headers = environ['werkzeug.request'].headers
        # print(headers)
    
        # print("your headers")
        # print(environ.keys())

        if 'werkzeug.request' in environ:
            headers = environ['werkzeug.request'].headers

        # for header in headers.keys():
            # print("%s=%s" % (header, headers[header]))
        # print("Your headers")
        print(headers)

        return self.app(environ, start_response)