#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

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