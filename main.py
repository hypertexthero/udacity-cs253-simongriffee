#!/usr/bin/env python

# URL router

import os
import webapp2
import re
import jinja2

from session.views import *
from blog.views import *
from rot13.views import *
from wiki.views import *

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'


# https://developers.google.com/appengine/docs/python/gettingstartedpython27/usingusers
# from google.appengine.api import users
# 
# class MainPage(webapp2.RequestHandler):
#   def get(self):
#       user = users.get_current_user()
# 
#       if user:
#           self.response.headers['Content-Type'] = 'text/plain'
#           self.response.out.write('Hello, ' + user.nickname())
#       else:
#           self.redirect(users.create_login_url(self.request.uri))
# 
# app = webapp2.WSGIApplication([('/', MainPage)],
#                             debug=True)


app = webapp2.WSGIApplication([('/',                        BlogHandler),
                               # ('/unit2/rot13',           Rot13Handler),
                               # ('/helloworld',           MainPage),
                               ('/register',                RegistrationHandler),
                               ('/login',                   LoginHandler),
                               ('/logout',                  LogoutHandler),
                               ('/welcome',                 WelcomeHandler),
                               ('/user/^(?P<username>\w+)',          UserHandler), # =todo
                               # ('/',                  BlogHandler),
                               ('/user/^(?P<username>\w+)/.json',              JSONBlogHandler),
                               ('/user/^(?P<username>\w+).json',               JSONBlogHandler),
                               ('/user/^(?P<username>\w+)/post/newpost',            NewPostHandler),
                               ('/user/^(?P<username>\w+)/post/(\d+)',              PostHandler),
                               ('/user/^(?P<username>\w+)/post/(\d+)/.json',        JSONPostHandler),
                               ('/user/^(?P<username>\w+)/post/(\d+).json',         JSONPostHandler),
                               ('/flush',                   FlushHandler),
                               ('/wiki',                    WikiHandler),
                               ('/wiki/register',           RegistrationHandler),
                               ('/wiki/login',              LoginHandler),
                               ('/wiki/logout',             LogoutHandler),
                               ('/wiki/_edit' + PAGE_RE,    EditPageHandler),
                               ('/wiki/_history' + PAGE_RE, HistoryPageHandler),
                               ('/wiki' + PAGE_RE,          WikiPageHandler)],
                              debug=True)

