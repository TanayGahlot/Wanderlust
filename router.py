#oggpnosn 
#hkhr 

#algorithm for calculating path 

import math 
import sys 

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

class Path():
	def __init__(self):
		self.locations = []
	def add(self, location):
		self.locations.append(location)
	def __str__(self):
		for location in self.locations:
			print location.name, "-> ", 


def computeScore(location, interest):
	#to compute the interst based score
	setOflocationCategories = set(location.categories)
	setOfInterest = set(interest)
	intersection = setOfInterest.intersection(setOflocationCategories)
	score = len(intersection)*1.0*location.rating/len(setOfInterest)
	return score 



def recalculate_coordinate(val,  _as=None):
  """
    Accepts a coordinate as a tuple (degree, minutes, seconds)
    You can give only one of them (e.g. only minutes as a floating point number) 
    and it will be duly recalculated into degrees, minutes and seconds.
    Return value can be specified as 'deg', 'min' or 'sec'; default return value is 
    a proper coordinate tuple.
  """
  deg,  min,  sec = val
  # pass outstanding values from right to left
  min = (min or 0) + int(sec) / 60
  sec = sec % 60
  deg = (deg or 0) + int(min) / 60
  min = min % 60
  # pass decimal part from left to right
  dfrac,  dint = math.modf(deg)
  min = min + dfrac * 60
  deg = dint
  mfrac,  mint = math.modf(min)
  sec = sec + mfrac * 60
  min = mint
  if _as:
    sec = sec + min * 60 + deg * 3600
    if _as == 'sec': return sec
    if _as == 'min': return sec / 60
    if _as == 'deg': return sec / 3600
  return deg,  min,  sec
      

def points2distance(start,  end):
  """
    Calculate distance (in kilometers) between two points given as (long, latt) pairs
    based on Haversine formula (http://en.wikipedia.org/wiki/Haversine_formula).
    Implementation inspired by JavaScript implementation from 
    http://www.movable-type.co.uk/scripts/latlong.html
    Accepts coordinates as tuples (deg, min, sec), but coordinates can be given 
    in any form - e.g. can specify only minutes:
    (0, 3133.9333, 0) 
    is interpreted as 
    (52.0, 13.0, 55.998000000008687)
    which, not accidentally, is the lattitude of Warsaw, Poland.
  """
  start_long = math.radians(recalculate_coordinate(start[0],  'deg'))
  start_latt = math.radians(recalculate_coordinate(start[1],  'deg'))
  end_long = math.radians(recalculate_coordinate(end[0],  'deg'))
  end_latt = math.radians(recalculate_coordinate(end[1],  'deg'))
  d_latt = end_latt - start_latt
  d_long = end_long - start_long
  a = math.sin(d_latt/2)**2 + math.cos(start_latt) * math.cos(end_latt) * math.sin(d_long/2)**2
  c = 2 * math.atan2(math.sqrt(a),  math.sqrt(1-a))
  return 6371 * c

def computeTime(source, destination, speed):
	distance = points2distance(((0, source.latitude, 0), (0, source.longitude, 0)), ((0, destination.latitude, 0), (0, destination.longitude, 0)))
	return distance*3600/speed #returns time in seconds 

def route(Locations, T, startLocation, speed):
	"""
		T: time in secondds 
		speed: speed in km/hr 
	"""
	current  = startLocation 
	path = Path()
	path.add(startLocation)

	while T > 0:
		maxScoreLocation = None
		maxScore = -1
		
		for location in Locations:
			location.greedyScore = location.score*1.0/computeTime(current, location, speed)
			if location.greedyScore > maxScore:
				maxScore = location.greedyScore
				maxScoreLocation = location
		
		T -= computeTime(current, maxScoreLocation, speed) #edge time 
		T += computeTime(current, startLocation, speed) #removing time to go back from current location to start time 
		T -= computeTime(maxScoreLocation, startLocation, speed) #adding time to go back from  new location to start location 
		T -= maxScoreLocation.timeToSpend
		
		path.add(maxScoreLocation)
		current = maxScoreLocation

	return path 

#parsing all input arguments 
fileName = sys.argv[1]
T = float(sys.argv[2])
speed = float(sys.argv[3])
latitude = float(sys.argv[4])
longitude = float(sys.argv[5])

locations = parseLocationsFile(fileName)
path = route(locations, T, latitude, longitude)

print path 




