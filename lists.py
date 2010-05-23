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


class AddrLists(webapp.RequestHandler):
  def get(self):
    surrogates = Surrogate.all().order('country').order('hostname').filter('alive =',True)
    
    addr_db = {}
    for surrogate in surrogates:
        funi = surrogate
    
    self.response.headers['Content-Type'] = "application"
    self.response.out.write(dir(addr_db))


application = webapp.WSGIApplication(
  [('/lists/addr', AddrLists)],
  debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
