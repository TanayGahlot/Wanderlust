#oggpnosn 
#hkhr 

#algorithm for calculating path 

class Location():
	def __init__(self, latitude, longitude, rating, category):
		self.latitude = latitude
		self.longitude = longitude 
		self.rating = rating 
		self.category = category 
		self.score = 0
		self.timeToSpend = 1
	def 