#!/usr/bin/env python

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
            
# JSON functions
def create_post_dict(post):
    post_dict = {}
    post_dict['content'] = post.content
    post_dict['created'] = post.created.strftime("%c")
    post_dict['subject'] = post.subject
    return post_dict

# Memcache functions
def top_posts(update = False):
    key_post = "top"
    
    posts = memcache.get(key_post)
    
    if posts is None or update:
        logging.error("DB QUERY")
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 10")
        posts = list(posts)
        posts = (posts, time.time())
        memcache.set(key_post, posts)
    
    return posts

def single_post(post_id):
    # leaving out update param because we never edit the post
    key_post = "post_" + post_id

    post = memcache.get(key_post)

    if post is None:
        logging.error("DB QUERY")
        post = Post.get_by_id(int(post_id))
        post = (post, time.time())
        memcache.set(key_post, post)

    return post


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


class MainHandler(Handler):
    def get(self):
        self.render("home.html")
    

class WelcomeHandler(Handler):
    def get(self):
        user_id = -1
        user_id_str = self.request.cookies.get('user_id')
        if user_id_str:
            cookie_val = check_secure_val(user_id_str)
            if cookie_val:
                user_id = int(cookie_val)
                        
        if user_id != -1:
            user = User.get_by_id(int(user_id))
            if user:
                self.render("welcome.html", user=user)
            else:
                self.redirect("/blog/signup")
        else:
            self.redirect("/blog/signup")
        

class BlogHandler(Handler):
    def render_blog(self):
        user_id = -1
        user_id_str = self.request.cookies.get('user_id')
        if user_id_str:
            cookie_val = check_secure_val(user_id_str)
            if cookie_val:
                user_id = int(cookie_val)
        
        posts, cache_time = top_posts()
        
        cache_timer = elapsed_time(cache_time)
        
        if user_id != -1:
            user = User.get_by_id(int(user_id))
            self.render("blog.html", posts=posts, cache_timer=cache_timer, user=user)
        else:
            self.render("blog.html", posts=posts, cache_timer=cache_timer)
        
    def get(self):
        self.render_blog()
    

class JSONBlogHandler(Handler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
        posts_list = []
        for post in posts:
            posts_list.append(create_post_dict(post))
        self.response.headers['Content-Type'] = 'application/json'
        self.write(json.dumps(posts_list))
    

class NewPostHandler(Handler):
    def render_newpost(self, subject="", content="", error=""):
        self.render("newpost.html", subject=subject, content=content, error=error)
    
    def get(self):
        self.render_newpost()
    
    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        
        if subject and content:
            p = Post(subject=subject, content=content)
            p.put()
            #rerun the query and update the cache
            top_posts(True)
            
            self.redirect("/blog/%s" % p.key().id())
        else:
            error = "subject and content needed!"
            self.render_newpost(subject, content, error)
        
    
class PostHandler(Handler):    
    def get(self, post_id):
        post, cache_time = single_post(post_id)
        cache_timer = elapsed_time(cache_time)
        if post:
            self.render("post.html", post=post, cache_timer=cache_timer)
        else:
            self.render_post(error="Blog post %s not found!" % post_id)
        

class JSONPostHandler(Handler):
    def get(self, post_id):
        post = Post.get_by_id(int(post_id))
        post_dict = create_post_dict(post)
        self.response.headers['Content-Type'] = 'application/json'
        self.write(json.dumps(post_dict))

class FlushHandler(Handler):
    def get(self):
        memcache.flush_all()
        self.redirect('/blog')
