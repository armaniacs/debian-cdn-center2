#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import os
from models import Surrogate
import helptool
import logging

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class MainPage(webapp.RequestHandler):
  def get(self):
    surrogates = Surrogate.all().order('checkpref').order('country')
    alive_surrogates = Surrogate.all().filter('alive =', 'True')

    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
      f_login = True
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'
      f_login = False
    alive_surrogates = db.GqlQuery("SELECT * FROM Surrogate WHERE alive = True")
      
    template_values = {
      'surrogates': surrogates,
      'num_all': surrogates.count(),
      'num_alive': alive_surrogates.count(),
      'url': url,
      'url_linktext': url_linktext,
      'f_login': f_login,
      }

    path = os.path.join(os.path.dirname(__file__), 'managesurrogate.html')
    self.response.out.write(template.render(path, template_values))


class RemoveSurrogate(webapp.RequestHandler):
  def post(self):
    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'

    deleteids = self.request.get("deleteid", allow_multiple=True)
    for deleteid in deleteids:
      db.delete(db.Key(deleteid))

    self.redirect("/managesurrogate")

class PickSurrogate(webapp.RequestHandler):
  def get(self):
    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'

    entity = db.get(self.request.get("id"))

    template_values = {
      'surrogate': entity,
      }

    path = os.path.join(os.path.dirname(__file__), 'updatesurrogate.html')
    self.response.out.write(template.render(path, template_values))

class UpdateSurrogate(webapp.RequestHandler):
  def post(self):
    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'

    surrogate = db.get(self.request.get("id"))
    s_ip = self.request.get("ip")
    s_preference = self.request.get("preference")
    s_country = self.request.get("country")
    s_continent = self.request.get("continent")
    s_hostname = self.request.get("hostname")
    s_targetnet = self.request.get("targetnet")
    s_type = self.request.get("type")
    s_targetasnum = self.request.get("targetasnum")

    if helptool.ipFormatCheck(s_ip):
      if helptool.countryFormatCheck(s_country):
        surrogate.ip = s_ip 
        surrogate.preference = int(s_preference)
        surrogate.continent = s_continent
        surrogate.country = s_country
        surrogate.hostname = s_hostname
        surrogate.type = s_type
        if helptool.targetnetFormatCheck(s_targetnet):
          surrogate.targetnet = s_targetnet
        if s_targetasnum:
          surrogate.targetasnum = int(s_targetasnum)
        surrogate.put()

    self.redirect("/managesurrogate")
    
class AddSurrogate(webapp.RequestHandler):
  def post(self):
    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'

    s_ip = self.request.get("ip")
    s_preference = self.request.get("preference")
    s_country = self.request.get("country")
    s_continent = self.request.get("continent")
    s_hostname = self.request.get("hostname")
    s_targetnet = self.request.get("targetnet")
    s_targetasnum = self.request.get("targetasnum")

    if helptool.ipFormatCheck(s_ip):
      if helptool.countryFormatCheck(s_country):
        surrogate = Surrogate(ip = s_ip)
        surrogate.preference = int(s_preference)
        surrogate.continent = s_continent
        surrogate.country = s_country
        surrogate.hostname = s_hostname
        if helptool.targetnetFormatCheck(s_targetnet):
          surrogate.targetnet = s_targetnet
        if s_targetasnum:
          surrogate.targetasnum = int(s_targetasnum)
        surrogate.put()

    self.redirect("/managesurrogate")

application = webapp.WSGIApplication(
  [("/managesurrogate", MainPage),
   ('/', MainPage),
   ('/removesurrogate', RemoveSurrogate),
   ('/updatesurrogate', UpdateSurrogate),
   ('/picksurrogate', PickSurrogate),
   ('/addsurrogate', AddSurrogate)],
  debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
