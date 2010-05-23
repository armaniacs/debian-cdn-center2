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

class MainPage(webapp.RequestHandler):
  def get(self):
    surrogates = Surrogate.all().order('checkpref').order('country')

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

    deleteips = self.request.get("deleteip", allow_multiple=True)
    for deleteip in deleteips:
      q = db.GqlQuery("SELECT * FROM Surrogate WHERE ip = :1", deleteip)
      results = q.fetch(10)
      db.delete(results)


#     nouseips = self.request.get("nouseip", allow_multiple=True)
#     for nouseip in nouseips:
#       surrogate = Surrogate(ip = nouseip)
#       surrogate.nouse = True

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

    if helptool.ipFormatCheck(s_ip):
      if helptool.countryFormatCheck(s_country):
        surrogate = Surrogate(ip = s_ip)
        surrogate.preference = int(s_preference)
        surrogate.continent = s_continent
        surrogate.country = s_country
        surrogate.hostname = s_hostname
        surrogate.put()

    self.redirect("/managesurrogate")

application = webapp.WSGIApplication(
  [("/managesurrogate", MainPage),
   ('/removesurrogate', RemoveSurrogate),
   ('/addsurrogate', AddSurrogate)],
  debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
