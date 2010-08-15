#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import os
from models import Surrogate
import helptool

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class PlainAlive(webapp.RequestHandler):
  def get(self):
    surrogates = Surrogate.all().order('country').order('hostname').filter('alive =',True)
    template_values = {
      'surrogates': surrogates
      }
    path = os.path.join(os.path.dirname(__file__), 'json/plain')
    self.response.headers['Content-Type'] = "application/json"
    self.response.out.write(template.render(path, template_values))

class PlainAll(webapp.RequestHandler):
  def get(self):
    surrogates = Surrogate.all().order('country').order('hostname')
    template_values = {
      'surrogates': surrogates
      }
    path = os.path.join(os.path.dirname(__file__), 'json/plain')
    self.response.headers['Content-Type'] = "application/json"
    self.response.out.write(template.render(path, template_values))

class CnameAlive(webapp.RequestHandler):
  def get(self):
    surrogates = Surrogate.all().order('country').order('hostname').filter('type =',"CNAME").filter('alive =',True)
    template_values = {
      'surrogates': surrogates
      }
    path = os.path.join(os.path.dirname(__file__), 'json/plain')
    self.response.headers['Content-Type'] = "application/json"
    self.response.out.write(template.render(path, template_values))

class CnameAll(webapp.RequestHandler):
  def get(self):
    surrogates = Surrogate.all().order('country').order('hostname').filter('type =',"CNAME")
    template_values = {
      'surrogates': surrogates
      }
    path = os.path.join(os.path.dirname(__file__), 'json/plain')
    self.response.headers['Content-Type'] = "application/json"
    self.response.out.write(template.render(path, template_values))


application = webapp.WSGIApplication(
  [("/json/alive", PlainAlive),
   ("/json/all", PlainAll),
   ("/json/cname/all", CnameAll),
   ("/json/cname/alive", CnameAlive)
   ],
  debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
