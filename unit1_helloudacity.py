import webapp2

# Hello Udacity
# classes are a way of grouping together functions and data that are related to the same thing
class MainPage(webapp2.RequestHandler):
  # our class has a funtion called get with a parameter called self
  def get(self):
      self.response.headers['Content-Type'] = 'text/plain'
      self.response.out.write('Hello, Udacity!')

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)