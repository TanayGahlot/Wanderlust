#oggpnosn 
#hkhr

import urllib2 as u2
import urllib as ul
from lxml import html
from lxml import etree
import os
import hashlib
import string
import random
import json
import ast
import logging
from random import randrange
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import mail
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from copy import deepcopy
import math 

class Location():
    def __init__(self, name,  description, latitude, longitude, rating, categories, timeToSpend):
        self.name = name 
        self.description = description
        self.latitude = latitude
        self.longitude = longitude 
        self.rating = rating 
        self.categories = categories
        self.score = 0
        self.timeToSpend = timeToSpend
        self.greedyScore = 0
    def __str__(self):
        data = {}
        data["name"] = self.name  
        data["description"] = self.description 
        data["latitude"] = self.latitude 
        data["longitude"] = self.longitude 
        data["rating"] = self.rating
        data["categories"] = self.categories 
        data["timeToSpend"] = self.timeToSpend
        return json.dumps(data)

def parseLocationsFile(fileName):
    fob = open(fileName)
    data = json.load(fob)
    locations = []
    for item in data:
        name= item["name"]
        description = ""
        latitude= float(item["latitude"])
        longitude= float(item["longitude"])
        rating = float(item["rating"])
        categories= item["categories"]
        timeToSpend = randrange(15*60, 120*60) #to spend an hour at the least 
        location = Location(name,  description, latitude, longitude, rating, categories, timeToSpend)
        locations.append(location)
    return locations


class Path():
    def __init__(self, startLocation):
        self.locations = [startLocation]
        self.epoch = [0]
    def add(self, location, travelTime):
        self.epoch.append(travelTime + location.timeToSpend)
        self.locations.append(location)
    def objectify(self):
        dataObject = []
        i=0
        time = 0
        for location in self.locations:
            time += self.epoch[i]
            data = {}
            data["name"] = location.name  
            data["description"] = location.description 
            data["latitude"] = location.latitude 
            data["longitude"] = location.longitude 
            data["rating"] = location.rating
            data["categories"] = location.categories 
            data["timeToSpend"] = location.timeToSpend
            data ["time"] = time 
            i+=1
            dataObject.append(data)
        return dataObject

def parseMapingFile(filename):
    fob = open(filename)
    text = fob.read()
    categories = text.split("\n\n")
    maping = {}
    for category in categories:
        lines = category.split("\n")
        maping[lines[0][1:]] = lines[1:]
    return maping 


def computeScore(location, interest):
    #to compute the interst based score
    setOflocationCategories = set(location.categories)
    setOfInterest = set(interest)
    intersection = setOfInterest.intersection(setOflocationCategories)
    score = len(intersection)*1.0*location.rating/len(setOfInterest)
    return score 



 
def computeDistance(source, destination):
    lat1 = source.latitude
    long1 = source.longitude
    lat2 = destination.latitude
    long2 = destination.longitude
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
    
    # Compute spherical distance from spherical coordinates.

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
                 math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    return arc*6371 #(in km)

def computeTime(source, destination, speed):
    distance = computeDistance(source, destination)
    return distance*3600.0/speed #returns time in seconds 

def route(Locations, T, startLocation, speed):
    """
        T: time in secondds 
        speed: speed in km/hr 
    """
    current  = startLocation 
    path = Path(startLocation)

    while T > 0:
        maxScoreLocation = None
        maxScore = -1
        travelTime = 0
        for location in Locations:
            travelTime = computeTime(current, location, speed)
            if travelTime == 0:
                travelTime = 5
            location.greedyScore = location.score*1.0/travelTime
            if location.greedyScore > maxScore:
                maxScore = location.greedyScore
                maxScoreLocation = location
        
        T -= computeTime(current, maxScoreLocation, speed) #edge time 
        T += computeTime(current, startLocation, speed) #removing time to go back from current location to start time 
        T -= computeTime(maxScoreLocation, startLocation, speed) #adding time to go back from  new location to start location 
        T -= maxScoreLocation.timeToSpend
        
        Locations.remove(maxScoreLocation)
        if T>0:
            path.add(maxScoreLocation, travelTime)
        current = maxScoreLocation

    return path 

#parsing all input arguments 
fileName = "./data/goa.json"
locations = parseLocationsFile(fileName)
mapping = parseMapingFile("./data/classes.txt")




class MainHandler(webapp2.RequestHandler):
    def post(self):
        logging.debug("Dekho: " + self.request.get("T") )
        T = float(self.request.get("T")) #in seconds 
        primaryInterest = self.request.get("interest").split("\t")
        latitude = float(self.request.get("latitude"))
        longitude = float(self.request.get("longitude"))
        speed = 20
        localLocations = deepcopy(locations)
        
        interest = []
        for prime in primaryInterest:
            interest.extend(mapping[prime])

        for location in localLocations:
            location.score = computeScore(location, interest)
        startLocation = Location("start", "", latitude, longitude, '', [], '')
        path = route(localLocations, T, startLocation, speed)

        self.response.write(json.dumps(path.objectify()))


app = webapp2.WSGIApplication([
    ('/', MainHandler), 
], debug=True)