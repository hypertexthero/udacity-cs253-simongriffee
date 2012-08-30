#!/usr/bin/env python

import os
import webapp2
import re
import jinja2

from session.views import *
from blog.views import *
from rot13.views import *
from wiki.views import *

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'

app = webapp2.WSGIApplication([('/',                        MainHandler),
                               ('/unit2/rot13',             Rot13Handler),
                               ('/blog/signup',             SignupHandler),
                               ('/blog/login',              LoginHandler),
                               ('/blog/logout',             LogoutHandler),
                               ('/blog/welcome',            WelcomeHandler),
                               ('/blog',                    BlogHandler),
                               ('/blog/.json',              JSONBlogHandler),
                               ('/blog.json',               JSONBlogHandler),
                               ('/blog/newpost',            NewPostHandler),
                               ('/blog/(\d+)',              PostHandler),
                               ('/blog/(\d+)/.json',        JSONPostHandler),
                               ('/blog/(\d+).json',         JSONPostHandler),
                               ('/blog/flush',              FlushHandler),
                               ('/wiki',                    WikiHandler),
                               ('/wiki/signup',             SignupHandler),
                               ('/wiki/login',              LoginHandler),
                               ('/wiki/logout',             LogoutHandler),
                               ('/wiki/_edit' + PAGE_RE,    EditPageHandler),
                               ('/wiki/_history' + PAGE_RE, HistoryPageHandler),
                               ('/wiki' + PAGE_RE,          WikiPageHandler)],
                              debug=True)
