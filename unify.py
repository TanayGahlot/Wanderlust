#oggpnosn 
#hkhr 

#unifying all the data file into a single meaningful json 

import sys 
import json

placeInfoFilename = sys.argv[1]
geocodeFileName = sys.argv[2]
ratingsFilename = sys.argv[3]

fob = open(placeInfoFilename)
placeInfoRawText = fob.read()

placeInfoRawText = placeInfoRawText.split("\n")
locations = []
for i in range(0, len(placeInfoRawText), 3):
	locations.append({"name": placeInfoRawText[i].replace("\r", ""),
					  "categories": [x.replace("\r", "") for x in placeInfoRawText[i+2].split(",")]})



fob = open(geocodeFileName)
geocodeRaw = fob.read().split("\n")
geocodeInfo = {}
for i in range(len(geocodeRaw)):
	line = geocodeRaw[i].split(",")
	if len(line) == 3:
		geocodeInfo[line[0]] = { "latitude": line[1], 
	     			"longitude": line[2]}
	else:
		geocodeInfo[line[0]] = None


#add geocode info to locations 
for i in range(len(locations)): 
	try:
		if geocodeInfo[locations[i]["name"]] != None :
			locations[i]["latitude"] = geocodeInfo[locations[i]["name"]]["latitude"]
			locations[i]["longitude"] = geocodeInfo[locations[i]["name"]]["longitude"]
		else:
			locations[i]["latitude"] = None
			locations[i]["longitude"] = None
	except:
		#print locations[i]["name"]
		locations[i]["latitude"] = None
		locations[i]["longitude"] = None
		continue


fob = open(ratingsFilename)
ratingsRawText = fob.read().split("\n")
ratings = {}
for line in ratingsRawText:
	try:
		line = line.split(",")
		name = line[1].replace('"', '')
		ratings[name] = float(line[2].replace('"', '').split(" ")[0])
	except:
		continue


#combine rating info 
for i in range(len(locations)): 
	try:
		locations[i]["rating"] = ratings[locations[i]["name"]]
	except:
		locations[i]["rating"] = None
		continue

refinedLocations = []
for location in locations:
	if location["latitude"] != None and location["rating"] != None:
		refinedLocations.append(location)


print json.dumps(refinedLocations)


