import webapp2

form="""
<form method="post">
    What is your birthday?
    <br>
    <label>
    Day
        <input type="text" name="day">
    </label>
    
    <label>
    Month
        <input type="text" name="month">
    </label>
    
    <label>
    Year
        <input type="text" name="year">
    </label>
    
    <input type="submit">
</form>
"""

# -----------
# User Instructions
# 
# Modify the valid_month() function to verify 
# whether the data a user enters is a valid 
# month. If the passed in parameter 'month' 
# is not a valid month, return None. 
# If 'month' is a valid month, then return 
# the name of the month with the first letter 
# capitalized.
#

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']
          
# def valid_month(month):
# 
# valid_month("january") => "January"    
# valid_month("January") => "January"
# valid_month("foo") => None
# valid_month("") => None

month_abbvs = dict((m[:3].lower(), m) for m in months)

def valid_month(month):
    if month:
        short_month = month[:3].lower()
        return month_abbvs.get(short_month)

print valid_month('')


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(form)

    def post(self):
        self.response.out.write("Thanks! That's valid!")

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)


# class TestHandler(webapp2.RequestHandler):
#   def post(self):
# 
#       # GET 
#         # - parameters are included in URL
#         # - used for fetching documents
#         # - maximum URL length
#         # - OK to cache
#         # - shouldn't change the server
#       # POST 
#         # - parameters are included in request headers
#         # - used for updating data
#         # - no max length
#         # - not OK to cache
#         # - ok to change the server
#         
#       # q = self.request.get("q")
#       # self.response.out.write(q)
#       
#       self.response.headers['Content-Type'] = 'text/plain'
#       self.response.out.write(self.request)