#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import os
import socket
import datetime
import urllib2
from models import Surrogate

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class ResetPrefSurrogate(webapp.RequestHandler):
    def get(self):
        message = 'reset checkpref more than 100'
        lm = ''
        dm = ''

        surrogates = db.GqlQuery("SELECT * FROM Surrogate WHERE checkpref > 100")
            
        for surrogate in surrogates:
            surrogate.checkpref = 50
            surrogate.put()
            
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'surrogates': surrogates,
            'url': url,
            'url_linktext': url_linktext,
            'message': message,
            'lm':lm,
            'dm':dm,
            }
        
        path = os.path.join(os.path.dirname(__file__), 'managesurrogate.html')
        self.response.out.write(template.render(path, template_values))


application = webapp.WSGIApplication(
  [('/resetcheckpref', ResetPrefSurrogate)],
  debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
