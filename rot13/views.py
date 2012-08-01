#!/usr/bin/env python

# Rot13

import os
import webapp2
import jinja2

# templating setup
template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True) # escape the html entities automatically

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
        
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class Rot13Handler(BaseHandler):
	def get(self):
		self.render('rot13.html')

	def post(self):
		rot13 = ''
		text = self.request.get('text')
		if text:
			# python has a built-in rot13 codec - http://docs.python.org/library/codecs.html
			rot13 = text.encode('rot13')

		self.render('rot13.html', text = rot13)
