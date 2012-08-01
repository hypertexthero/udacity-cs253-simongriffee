import webapp2

form="""
<form method="post">
    What is your birthday?
    <br>
    <label>
        Day
        <input type="text" name="day" value="%(day)s">
    </label>
    <label>
        Month (name)
        <input type="text" name="month" value="%(month)s">
    </label>
    <label>
        Year
        <input type="text" name="year" value="%(year)s"> 
    </label>
    <div style="color:red;">%(error)s</div>
    <br>
    <br>
    <input type="submit">
</form>
"""

# DAY VALIDATION
# ==============
# Modify the valid_day() function to verify 
# whether the string a user enters is a valid 
# day. The valid_day() function takes as 
# input a String, and returns either a valid 
# Int or None. If the passed in String is 
# not a valid day, return None. 
# If it is a valid day, then return 
# the day as an Int, not a String. Don't 
# worry about months of different length. 
# Assume a day is valid if it is a number 
# between 1 and 31.
# Be careful, the input can be any string 
# at all, you don't have any guarantees 
# that the user will input a sensible 
# day.
#

def valid_day(day):
    if day and day.isdigit():
        day = int(day)
        if day > 0 and day <= 31:
            return day

# DAY VALIDATION TESTS
# --------
# valid_day('0') => None    
# valid_day('1') => 1
# valid_day('15') => 15
# valid_day('500') => None


# MONTH VALIDATION
# ==============
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
          
# MONTH VALIDATION TESTS
# --------
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

# print valid_month('')


# YEAR VALIDATION
# ==============
# Modify the valid_year() function to verify 
# whether the string a user enters is a valid 
# year. If the passed in parameter 'year' 
# is not a valid year, return None. 
# If 'year' is a valid year, then return 
# the year as a number. Assume a year 
# is valid if it is a number between 1900 and 
# 2020.
#

# FIRST TRY (for some reason < currentyear doesn't work)

# import datetime

# now = datetime.datetime.now()
# currentyear = now.strftime("%Y")

# def valid_year(year):
#     if year and year.isdigit():
#         year = int(year)
#         if year > 1900 and year < currentyear:
#             return year


def valid_year(year):
    if year and year.isdigit():
        year = int(year)
        if year > 1900 and year < 2020:
            return year


# YEAR VALIDATION TESTS
# --------
# valid_year('0') => None    
# valid_year('-11') => None
# valid_year('1950') => 1950
# valid_year('2000') => 2000


# ESCAPE HTML FROM FORM
# Implement the function escape_html(s), which replaces:
# > with &gt;
# < with &lt;
# " with &quot;
# & with &amp;
# and returns the escaped string
# Note that your browser will probably automatically 
# render your escaped text as the corresponding symbols, 
# but the grading script will still correctly evaluate it.
# 

import cgi
def escape_html(s):
    return cgi.escape(s, quote = True) # use existing escape function from python's cgi module - don't re-invent wheel!
    # for (i, o) in (("&", "&amp;"), # ampersand needs to be first!!
    #                (">", "&gt;"),
    #                ("<", "&lt;"),
    #                ('"', "&quote;")):
    #     s = s.replace(i, o)
    # return s

# print escape_html("test")

# MAIN APPLICATION
# --------

class MainPage(webapp2.RequestHandler):
    def write_form(self, error="", day="", month="", year=""):
        self.response.out.write(form % {"error": error,
                                         "day": escape_html(day), 
                                         "month": escape_html(month), 
                                         "year": escape_html(year)})

    def get(self):
        self.write_form()

    def post(self):
        user_day = self.request.get('day')
        user_month = self.request.get('month')
        user_year = self.request.get('year')

        day = valid_day(user_day)
        month = valid_month(user_month)
        year = valid_year(user_year)

        if not (day and month and year):
            self.write_form("That doesn't look valied to me, friend.",
                            user_day, user_month, user_year)
        else:
            self.redirect("/unit2/birthday/thanks")

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("<b>Thanks! That's totally valid!</b>")        

app = webapp2.WSGIApplication([('/unit2/birthday/', MainPage), ('/unit2/birthday/thanks', ThanksHandler)], debug=True)









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