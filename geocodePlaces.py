#oggpnosn 
#hkhr 

#extracting geolocation 

from urllib import urlencode
from urllib2 import urlopen
import json
import sys 

key = "AIzaSyBk21CHntg-QcGbm4l4wq5L0hhV5AKNbGA"


def getGeocode(searchTerm, key):
    searchTerm = searchTerm.lower().replace("nr", "").replace("at", "")     
    url = "https://maps.googleapis.com/maps/api/geocode/json?%s&key=%s"
    query = {"address": searchTerm}
    response = urlopen(url%(urlencode(query), key))
    if response.code == 200: #is succesull
        result = json.loads(response.read())
        if result["results"]:
            return (result["results"][0]["geometry"]['location']['lat'], result["results"][0]["geometry"]['location']['lng'])
    else:
        raise Exception, "Wanderlust: Network issues"


def loadPlaceNames(filename):
	fob = open(filename)
	text = fob.read()
	lines = text.split("\n")
	places = []
	for line in lines[1:]:
		if line:
			if "(" not in line: #to account for extraction flaws 
				line = line.split(",")
				places.append(line[1].replace('"', ""))
	return places

filename = sys.argv[1]
places = loadPlaceNames(filename)

for place in places:
	searchTerm = place + "Goa"
	print place, "," , getGeocode(searchTerm, key) 

