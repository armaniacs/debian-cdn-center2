# -*- coding: utf-8 -*-

import urllib2
import logging
import datetime
import os
import re

def is_dev():
   return os.environ.get('SERVER_SOFTWARE', '').startswith('Development')

def ipFormatCheck(ip_str):
   pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
   if re.match(pattern, ip_str):
      return True
   else:
      return False

def countryFormatCheck(c_str):
    pattern = r"\b\w\w\w\b"
    if re.match(pattern, c_str):
        return True
    else:
        return False

def targetnetFormatCheck(ip_str):
   pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/[0-9]?[0-9]\b"
   if re.match(pattern, ip_str):
      return True
   elif ip_str == "":
      return True
   else:
      return False

def delegateForCname(ipaddr):
   try:
      if is_dev():
         req = urllib2.Request(url="http://localhost:3000/cname_check/ip?ip=" + ipaddr)
      else:
         req = urllib2.Request(url="http://cnameqrv.araki.net/cname_check/ip?ip=" + ipaddr)
      req.add_header('User-Agent',"Debian-cdn-helptool/0.1")

      f = urllib2.urlopen(req)

      body = f.read()
      bodies = body.splitlines()
      lmt = datetime.datetime.strptime(bodies[0], "%a %b %d %H:%M:%S UTC %Y")
      logging.info(bodies[0])
   except urllib2.URLError, e:
      message = "%s is not working. %s" % (ipaddr,e)
      logging.info(message)
      return False
   except ValueError, e:
      message = "%s is not working. %s" % (ipaddr,e)
      logging.info(message)
      return False
   return True, lmt
