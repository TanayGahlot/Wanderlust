#oggpnosn 
#hkhr 

#mapper 


def parseMapingFile(filename):
	fob = open(filename)
	text = fob.read()
	categories = text.split("\n\n")
	maping = {}
	for category in categories:
		lines = category.split("\n")
		maping[lines[0][1:]] = lines[1:]
	return maping 

map = parseFile("./data/classes.txt")
print map