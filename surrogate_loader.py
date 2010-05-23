#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-

from google.appengine.ext import db
from google.appengine.tools import bulkloader

#from models import Surrogate

class Surrogate(db.Model):
    ip = db.StringProperty(required=True)
    hostname = db.StringProperty()
    type = db.StringProperty()
    preference = db.IntegerProperty()
    time = db.DateTimeProperty(auto_now=True)
    alive = db.BooleanProperty()
    country = db.StringProperty()
    continent = db.StringProperty()
    checkpref = db.IntegerProperty()
    tracefile = db.StringProperty()
    lastModifiedTime = db.DateTimeProperty()


class SurrogateLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'Surrogate',
                                   [('ip', str),
                                    ('hostname', str),
                                    ('preference', int),
                                    ('country', str),
                                    ('continent', str)
                                    ]
                                   )
        
loaders = [SurrogateLoader]
