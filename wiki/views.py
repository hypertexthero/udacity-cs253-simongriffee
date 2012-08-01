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
import random
import string
import hashlib
import hmac
import json
import logging
import time

from google.appengine.api import memcache
from models import *

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env= jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

SECRET = 'imsosecret'

# --------------------------------------
# FUNCTIONS
# --------------------------------------
def escape_html(s):
    for (i, o) in (("&", "&amp;"),
                   ("<", "&lt;"),
                   (">", "&gt;"),
                   ('"', "&quot;")):
        s = s.replace(i, o)
    return s

def get_user(self):
    user_id = -1
    user_id_str = self.request.cookies.get('user_id')
    if user_id_str:
        cookie_val = check_secure_val(user_id_str)
        if cookie_val:
            user_id = int(cookie_val)
            if user_id != -1:
                user = User.get_by_id(int(user_id))
                if user:
                    return user
    return None

# Cookie Hash Functions
def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val

# --------------------------------------
# HANDLERS
# --------------------------------------
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class WikiHandler(Handler):
    def get(self):
        user = get_user(self)
        wikis = db.GqlQuery("SELECT * FROM WikiPage where version=1 ORDER BY title DESC")
        wikis = list(wikis)
        
        if user:
            self.render("wiki.html", wikis=wikis, user=user)
        else:
            self.render("wiki.html", wikis=wikis)
    

class EditPageHandler(Handler):
    def render_editwiki(self, user="", title="", content="", error=""):
        self.render("editwiki.html", user=user, title=title, content=content, error=error)
    
    def get(self, title):
        user = get_user(self)
        v = self.request.get('v')
        
        if user:
            if v:
                v = int(v)
                wiki_valid = db.GqlQuery("SELECT * FROM WikiPage WHERE title = :1 AND version = :2 ORDER BY created DESC", title, v).get()
                if not wiki_valid:
                    self.redirect("/wiki/_edit%s" % title)
            else:
                wiki_valid = db.GqlQuery("SELECT * FROM WikiPage WHERE title = :1 ORDER BY created DESC LIMIT 1", title).get()
                if not wiki_valid:
                    self.render_editwiki(user, title)
            
            if wiki_valid:
                id = wiki_valid.key().id()
                wiki_page = WikiPage.get_by_id(int(id))
                self.render_editwiki(user, wiki_page.title, wiki_page.content)
        else:
            self.redirect("/wiki/signup")
        
    def post(self, title):
        content = self.request.get("content")
        user = get_user(self)
                        
        if user:
            if title and content:
                wiki_valid = db.GqlQuery("SELECT * FROM WikiPage where title = :1 ORDER BY created DESC LIMIT 1", title).get()
                if wiki_valid:
                    id = wiki_valid.key().id()
                    prev_wiki_page = WikiPage.get_by_id(int(id))
                    cur_version = prev_wiki_page.version + 1
                    wiki_page = WikiPage(title=title, content=content, version=cur_version)
                    wiki_page.put()
                else:
                    wiki_page = WikiPage(title=title, content=content, version=1)
                    wiki_page.put()

                self.redirect("/wiki%s" % wiki_page.title)
            else:
                error = "content needed!"
                self.render_editwiki(user, title, content, error)
        else:
            self.redirect("/wiki/signup")

    
class HistoryPageHandler(Handler):
    def get(self, title):
        user = get_user(self)
        if user:
            wikis = db.GqlQuery("SELECT * FROM WikiPage WHERE title = :1 ORDER BY created DESC", title)
            if wikis:
                wikis = list(wikis)
                self.render("wikihistory.html", wikis=wikis, user=user)
            else:
                self.redirect("/wiki/_edit%s" % title)
        else:
            self.redirect("/wiki/signup")
        


class WikiPageHandler(Handler):
    def get(self, title):
        wiki_valid = None
        v = self.request.get('v')
        
        if v:
            v = int(v)
            wiki_valid = db.GqlQuery("SELECT * FROM WikiPage WHERE title = :1 AND version = :2 ORDER BY created DESC", title, v).get()
            if not wiki_valid:
                self.redirect("/wiki%s" % title)
        else:
            wiki_valid = db.GqlQuery("SELECT * FROM WikiPage WHERE title = :1 ORDER BY created DESC LIMIT 1", title).get()
            if not wiki_valid:
                self.redirect("/wiki/_edit%s" % title)
                
        if wiki_valid:
            id = wiki_valid.key().id()
            wiki_page = WikiPage.get_by_id(int(id))
            user = get_user(self)
            if user:
                self.render("wikipage.html", wiki_page=wiki_page, user=user)
            else:
                self.render("wikipage.html", wiki_page=wiki_page)
            
    