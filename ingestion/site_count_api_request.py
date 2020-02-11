from urllib import request, parse

# Base URL being accessed 
url = 'https://developer.nrel.gov/api/wind-toolkit/wind/site_count'

# Example direct API call from browser (with public API key)
# https://developer.nrel.gov/api/wind-toolkit/wind/site_count.json?api_key=gkvd8S4FhRFnPitCqciuDqtIc6G0UCue7eBo13pT&wkt=POLYGON((-114.9609375 39.50404070558415,-112.67578124999999 39.50404070558415,-112.67578124999999 38.13455657705411,-114.9609375 38.13455657705411,-114.9609375 39.50404070558415))

# WKT Polygon for Pennsylvania
# POLYGON((-80.5174 42.3261,-80.0821 42.3961,-79.7621 42.5167,-79.7607 42.0003,-75.3580 41.9983,-75.2673 41.9431,-75.1794 41.8696,-75.0586 41.7713,-75.0366 41.6729,-75.0641 41.6021,-74.9927 41.5086,-74.7935 41.4283,-74.7070 41.3933,-74.8608 41.2282,-75.1355 40.9830,-75.0490 40.8554,-75.1904 40.6806,-75.2124 40.5639,-75.1025 40.5743,-75.0600 40.5013,-75.0655 40.4208,-74.9776 40.4072,-74.9432 40.3392,-74.8389 40.2628,-74.7221 40.1495,-75.0929 39.9592,-75.2577 39.8370,-75.4321 39.8128,-75.6477 39.8317,-75.7892 39.7199,-80.5243 39.7220,-80.5202 42.3240,-80.5174 42.3261))

# https://developer.nrel.gov/api/wind-toolkit/wind/site_count.json?api_key=gkvd8S4FhRFnPitCqciuDqtIc6G0UCue7eBo13pT&wkt=POLYGON((-114.9609375 39.50404070558415,-112.67578124999999 39.50404070558415,-112.67578124999999 38.13455657705411,-114.9609375 38.13455657705411,-114.9609375 39.50404070558415))


# Dictionary of query parameters (if any)
parms = {
   'api_key' : 'gkvd8S4FhRFnPitCqciuDqtIc6G0UCue7eBo13pT',
   'wkt' : 'POLYGON((-114.9609375 39.50404070558415,-112.67578124999999 39.50404070558415,-112.67578124999999 38.13455657705411,-114.9609375 38.13455657705411,-114.9609375 39.50404070558415))'
}

# Encode the query string
querystring = parse.urlencode(parms)

# Make a GET request and read the response
u = request.urlopen(url+'?' + querystring)
resp = u.read()

import json
from pprint import pprint

json_resp = json.loads(resp.decode('utf-8'))
pprint(json_resp)