# -*- coding: utf-8 -*-
# dccapp.models

from google.appengine.ext import db

# Create your models here.

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
    nouse = db.BooleanProperty()
    failreason = db.StringProperty()
    targetnet = db.StringProperty()
