#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import os
import socket
import datetime
import urllib2
import logging
import helptool
from models import Surrogate

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

def is_dev():
   return os.environ.get('SERVER_SOFTWARE', '').startswith('Development')

class CheckSurrogate(webapp.RequestHandler):
    def get(self):
        socket.timeout(1)
        
        check_server_count = 0
        check_period = 600
        mirrordelay = 86400
        t1 = datetime.datetime.now()
        lm = ''
        dm = ''
        ttmp = datetime.datetime.now()
        keika = ttmp - t1
        message = ''
        
        surrogates = Surrogate.all().order('checkpref').order('time')
        
        for surrogate in surrogates:
            if check_server_count >= 100 and not is_dev():
                break
            if surrogate.checkpref > 150 and not is_dev():
                continue

            ttmp = datetime.datetime.now()
            keika = ttmp - t1
            if keika > datetime.timedelta(0,20) and not is_dev():
                break

            if surrogate.checkpref:
                surrogate.checkpref += int(surrogate.checkpref)
            else:
                surrogate.checkpref = 0
                
            if surrogate.tracefile:
                True
            else:
                tracefile = 'ftp-master.debian.org'

            if surrogate.type == "CNAME":
                check_server_count += 1
                dm = 'go check'
                tf, lmt = helptool.delegateForCname(surrogate.ip)
                if tf:
                    message = surrogate.ip + " is alive (CNAME host)."
                else:
                    message = surrogate.ip + " is dead (CNAME host)."
                logging.info(message)
                surrogate.lastModifiedTime = lmt
                if surrogate.time - lmt > datetime.timedelta(0,mirrordelay):
                    surrogate.alive = False
                    surrogate.checkpref += 1
                    surrogate.failreason = "DELAY"
                else:
                    surrogate.alive = True
                    surrogate.checkpref = 0
                    surrogate.failreason = ""
                surrogate.put()
                
            elif surrogate.alive == None or t1 > surrogate.time + datetime.timedelta(0,check_period) or is_dev(): #remote_addr == "127.0.0.1":
                check_server_count += 1
                dm = 'go check'
                k = surrogate.ip
                req = urllib2.Request(url="http://" + k + '/debian/project/trace/' + tracefile)
                req.add_header('User-Agent',"Debian-cdn-mirror-ping/1.5")
                try:
                    f = urllib2.urlopen(req)
                    lm = f.info()['Last-Modified']
                    message = ''
                    lmt = datetime.datetime.strptime(lm, "%a, %d %b %Y %H:%M:%S GMT")
                    surrogate.lastModifiedTime = lmt
                    if surrogate.time - lmt > datetime.timedelta(0,mirrordelay):
                        surrogate.alive = False
                        surrogate.checkpref += 1
                        surrogate.failreason = "DELAY"
                    else:
                        surrogate.alive = True
                        surrogate.checkpref = 0
                        surrogate.failreason = ""
                      
                except urllib2.HTTPError, e:
                    message += "%s is not working. (HTTP error)" % (k)
                    surrogate.alive = False
                    surrogate.checkpref += 1
                    surrogate.failreason = "E:HTTP"
                    logging.info(message)
                except urllib2.URLError, e:
                    message += "%s is not working. (URL error)" % (k)
                    surrogate.alive = False
                    surrogate.checkpref += 1
                    surrogate.failreason = "E:URL"
                    logging.info(message)
                except:
                    message += "%s is not working. " % (k)
                    surrogate.alive = False
                    surrogate.checkpref += 1
                    surrogate.failreason = "E:NO WORK"
                    logging.info(message)                    
                surrogate.put()

            else:
                dm = 'no check: ' + "%s is checked less than %d sec ago (surrogate.time %s, %s)" % (surrogate.ip,check_period,surrogate.time,t1)
               
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        t2 = datetime.datetime.now()
        keika = t2 - t1
        template_values = {
            'surrogates': surrogates,
            'url': url,
            'url_linktext': url_linktext,
            'message': message,
            'lm':lm,
            'dm':dm,
            'keika':keika,
            }
        
        path = os.path.join(os.path.dirname(__file__), 'managesurrogate.html')
        self.response.out.write(template.render(path, template_values))


application = webapp.WSGIApplication(
  [('/checksurrogate', CheckSurrogate)],
  debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
