#oggpnosn 
#hkhr 

#testing backend 

from urllib import urlencode
from urllib2 import urlopen
from urllib2 import Request
import json
import sys 


data = {'T': 18000,
 'interest': 'Beaches\tAncient Ruins',
 'latitude': 15.3180882,
 'longitude': 73.899606599999998}

url = "http://localhost:8000/"
# url = "http://wunderlust-c7579.appspot.com/"

request = Request(url, data=urlencode(data))
response = urlopen(request)
print response.read()