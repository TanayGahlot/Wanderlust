#oggpnosn 
#hkhr 

#algorithm for calculating path 

import math 
import sys 
import json

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
		timeToSpend = 3600 #to spend an hour at the least 
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



def computeScore(location, interest):
	#to compute the interst based score
	setOflocationCategories = set(location.categories)
	setOfInterest = set(interest)
	intersection = setOfInterest.intersection(setOflocationCategories)
	score = len(intersection)*1.0*location.rating/len(setOfInterest)
	return score 



# def recalculate_coordinate(val,  _as=None):
#   """
#     Accepts a coordinate as a tuple (degree, minutes, seconds)
#     You can give only one of them (e.g. only minutes as a floating point number) 
#     and it will be duly recalculated into degrees, minutes and seconds.
#     Return value can be specified as 'deg', 'min' or 'sec'; default return value is 
#     a proper coordinate tuple.
#   """
#   deg,  min,  sec = val
#   # pass outstanding values from right to left
#   min = (min or 0) + int(sec) / 60
#   sec = sec % 60
#   deg = (deg or 0) + int(min) / 60
#   min = min % 60
#   # pass decimal part from left to right
#   dfrac,  dint = math.modf(deg)
#   min = min + dfrac * 60
#   deg = dint
#   mfrac,  mint = math.modf(min)
#   sec = sec + mfrac * 60
#   min = mint
#   if _as:
#     sec = sec + min * 60 + deg * 3600
#     if _as == 'sec': return sec
#     if _as == 'min': return sec / 60
#     if _as == 'deg': return sec / 3600
#   return deg,  min,  sec
      

# def points2distance(start,  end):
#   """
#     Calculate distance (in kilometers) between two points given as (long, latt) pairs
#     based on Haversine formula (http://en.wikipedia.org/wiki/Haversine_formula).
#     Implementation inspired by JavaScript implementation from 
#     http://www.movable-type.co.uk/scripts/latlong.html
#     Accepts coordinates as tuples (deg, min, sec), but coordinates can be given 
#     in any form - e.g. can specify only minutes:
#     (0, 3133.9333, 0) 
#     is interpreted as 
#     (52.0, 13.0, 55.998000000008687)
#     which, not accidentally, is the lattitude of Warsaw, Poland.
#   """
#   start_long = math.radians(recalculate_coordinate(start[0],  'deg'))
#   start_latt = math.radians(recalculate_coordinate(start[1],  'deg'))
#   end_long = math.radians(recalculate_coordinate(end[0],  'deg'))
#   end_latt = math.radians(recalculate_coordinate(end[1],  'deg'))
#   d_latt = end_latt - start_latt
#   d_long = end_long - start_long
#   a = math.sin(d_latt/2)**2 + math.cos(start_latt) * math.cos(end_latt) * math.sin(d_long/2)**2
#   c = 2 * math.atan2(math.sqrt(a),  math.sqrt(1-a))
#   return 6371 * c


 
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
fileName = sys.argv[1]
T = float(sys.argv[2])
speed = float(sys.argv[3])
latitude = float(sys.argv[4])
longitude = float(sys.argv[5])

locations = parseLocationsFile(fileName)
interest = ['Historic Walking Areas', 'Bodies of Water'] #for demo------
for location in locations:
	location.score = computeScore(location, interest)

startLocation = Location("start", "", latitude, longitude, '', [], '')
path = route(locations, T, startLocation, speed)

