#!/usr/bin/env python

import os
import webapp2
import re
import jinja2
import random
import string
import hashlib
import hmac
import logging
import time

from models import *

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env= jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

SECRET = 'imsosecret'

# --------------------------------------
# SESSION FUNCTIONS
# --------------------------------------
def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASS_RE.match(password)

def valid_email(email):
    if email == "":
        return True
    else:
        return EMAIL_RE.match(email)
            
def escape_html(s):
    for (i, o) in (("&", "&amp;"),
                   ("<", "&lt;"),
                   (">", "&gt;"),
                   ('"', "&quot;")):
        s = s.replace(i, o)
    return s

def elapsed_time(cache_time):
    time_since = int(time.time() - cache_time)
    return '{0} second{1}'.format(time_since, 's' if time_since != 1 else '')

# Cookie Hash Functions
def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val

# Password Hash Functions
def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest() # =todo: use bcrypt - http://www.udacity.com/wiki/CS253%20Unit%204
    return '%s|%s' % (h, salt)

def valid_pw(name, pw, h):
    salt = h.split('|')[1]
    return make_pw_hash(name, pw, salt) == h
    

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
        
class RegistrationHandler(Handler):
    def render_registration(self, username="", email="", error_username="", error_password="",
                   error_verify="", error_email="", request_path=""):
        self.render("registration.html", username=username, email=email, error_username=error_username,
                    error_password=error_password, error_verify=error_verify, error_email=error_email, 
                    request_path=request_path)

    def get(self):
        # If we have a cookie for this user, send them 
        # to the welcome page instead
        user_id = -1
        user_id_str = self.request.cookies.get('user_id')
        if user_id_str:
            cookie_val = check_secure_val(user_id_str)
            if cookie_val:
                user_id = int(cookie_val)
        
        l = re.compile("/").split(self.request.path)
        request_path = l[1]

        if user_id == -1:
            self.render_registration("", "", "", "", "", "", request_path)
        else:
            if request_path == '':
                self.redirect('/welcome')
            elif request_path == 'wiki':
                self.redirect('/wiki')
            else:
                self.redirect('/')
            

    def post(self):
        username = escape_html(self.request.get('username'))
        password = self.request.get('password')
        password_verify = self.request.get('verify')
        email = escape_html(self.request.get('email'))

        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""

        is_valid = True
        
        l = re.compile("/").split(self.request.path)
        request_path = l[1]

        # If user is already registered, we 
        user = db.Query(User).filter("username =", username).fetch(limit=1)
        if user:
            error_username = "That user already exists."
            is_valid = False
        else:
            if not valid_username(username):
                error_username = "That's not a valid username."
                is_valid = False
            if not valid_password(password):
                error_password = "That wasn't a valid password."
                is_valid = False
            if password != password_verify:
                error_verify = "Your passwords didn't match."
                is_valid = False
            if  not valid_email(email):
                error_email = "That's not a valid email."
                is_valid = False

        if is_valid:
            # Create and save the user model
            pw_hash =  make_pw_hash(username, password)
            u = User(username=username, password=pw_hash, email=email)
            u.put()

            # Create the cookie
            user_id = str(u.key().id())
            user_id = make_secure_val(user_id)
            self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/' % user_id)
            
            if request_path == '':
                self.redirect('/welcome')
            elif request_path == 'wiki':
                self.redirect('/wiki')
            else:
                self.redirect('/')
        else:
            self.render_registration(username, email, error_username, error_password, error_verify, error_email, request_path)


class LoginHandler(Handler):   
    def render_login(self, username="", error="", request_path=""):
        self.render("login.html", username=username, error=error, request_path=request_path)

    def get(self):
        # If we have a cookie for this user, send them 
        # to the welcome page instead
        user_id = -1
        user_id_str = self.request.cookies.get('user_id')
        if user_id_str:
            cookie_val = check_secure_val(user_id_str)
            if cookie_val:
                user_id = int(cookie_val)
            
        l = re.compile("/").split(self.request.path)
        request_path = l[1]

        if user_id == -1:
            self.render_login("", "", request_path)
        else:
            if request_path == '':
                self.redirect('/welcome')
            elif request_path == 'wiki':
                self.redirect('/wiki')
            else:
                self.redirect('/')

    def post(self):
        username = escape_html(self.request.get('username'))
        password = self.request.get('password')
        error = ""
        
        l = re.compile("/").split(self.request.path)
        request_path = l[1]

        u = db.Query(User).filter("username =", username).fetch(limit=1)
        if u:
            if valid_pw(username, password, u[0].password):
                # Create the cookie
                user_id = str(u[0].key().id())
                user_id = make_secure_val(user_id)
                self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/' % user_id)
                if request_path == '':
                    self.redirect('/welcome')
                elif request_path == 'wiki':
                    self.redirect('/wiki')
                else:
                    self.redirect('/')
            else:
                error = "Invalid login"
                self.render_login(username, error, request_path)
        else:
            error = "Invalid login"
            self.render_login(username, error, request_path) 


class LogoutHandler(Handler):   
    def get(self):
        # If we have a cookie for this user, blank out user_id
        user_id_str = self.request.cookies.get('user_id')
        if user_id_str:
            self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
        
        l = re.compile("/").split(self.request.path)
        if l[1] == '':
            self.redirect('/register')
        elif l[1] == 'wiki':
            self.redirect('/wiki/register')
        else:
            self.redirect('/')

# class UserHandler(Handler):
#     def render_user(self):
#         user_id = -1
#         user_id_str = self.request.cookies.get('user_id')
#         if user_id_str:
#             cookie_val = check_secure_val(user_id_str)
#             if cookie_val:
#                 user_id = int(cookie_val)
# 
#         posts, cache_time = top_posts()
# 
#         cache_timer = elapsed_time(cache_time)
# 
#         if user_id != -1:
#             user = User.get_by_id(int(user_id))
#             self.render("user.html", posts=posts, cache_timer=cache_timer, user=user)
#         else:
#             self.render("user.html", posts=posts, cache_timer=cache_timer)
# 
#     def get(self):
#         self.render_user()

# http://stackoverflow.com/questions/11653347/adding-usernames-to-the-path-of-the-url
class ProfileHandler(Handler):
    def render_user(self):
        user_id = -1
        user_id_str = self.request.cookies.get('user_id')
        if user_id_str:
            cookie_val = check_secure_val(user_id_str)
            if cookie_val:
                user_id = int(cookie_val)

        if user_id != -1:
            user = User.get_by_id(int(user_id))
            self.render("profile.html", user=user)
        else:
            self.render("profile.html")

    def get(self, user):
        self.render_user()
