# This program creates a csv file of the 'coordinates' dataset from NREL's wind toolkit API. This 
# dataset maps the y, x index values used in the dataset to latitud and longitude.
# Both a y and x index are required to get a corresponding lat, long mapping.

import h5pyd
import pandas as pd

# Get dataset through NREL API call.
def make_coordinates_file():
    f = h5pyd.File("/nrel/wtk-us.h5", 'r')
    coordinates = f['coordinates']
    f.close()
    df = pd.DataFrame(coordinates)
    df.to_csv("coordinates.csv")

make_coordinates_file()