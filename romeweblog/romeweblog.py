import webapp2

form="""
<form action="/testform">
    <input name="q">
    <input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):# classes are a way of grouping together functions and data that are related to the same thing
    def get(self): # our class has a funtion called get with a parameter called self
        # self.response.headers['Content-Type'] = 'text/plain'
        # self.response.headers['Content-Type'] = 'text/html'
        # self.response.out.write('Hello, Udacity!')
        self.response.out.write(form)

class TestHandler(webapp2.RequestHandler):# classes are a way of grouping together functions and data that are related to the same thing
    def get(self): # our class has a funtion called get with a parameter called self
        # q = self.request.get("q")
        # self.response.out.write(q)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(self.request)
        

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/testform', TestHandler)],
                              debug=True)