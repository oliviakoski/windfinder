# This program uses the Python geopy package to retrieve latitude and longitude coordinates
# from an address using Nominatim, the search engine for OpenStreetMap
# See https://geopy.readthedocs.io/en/stable/#geopy.geocoders.options for more

from geopy.geocoders import Nominatim
import ssl
import geopy.geocoders

# Fix SSL certification error
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
geopy.geocoders.options.default_ssl_context = ctx

user_query = input("Which location would you like lat/lon coordinates for?:  ")

def get_lat_lon(user_query):
    geolocator = Nominatim(user_agent='my-application')
    location = geolocator.geocode(user_query)
    return(location.latitude, location.longitude)

print(get_lat_lon(user_query))
