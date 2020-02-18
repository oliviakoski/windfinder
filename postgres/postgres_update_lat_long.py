# This program queries rows from the top windiest spots table 
# in the windfinder database in order to translate y, x index
# values from NREL Wind Toolkit dataset into latitude and longitude locations.
# Requires that you've generated a  coordinates file csv 
# called "yx_to_latlong.csv" with make_coordinates_file.py

import psycopg2
from os.path import abspath
from configparser import ConfigParser

# Function to translate y, x indices to lat, long values
def get_lat_long(y, x):
    # Selects 'nth' column and yth row of the dataframe. Result is string formatted lat, long
    # values that need to be cleaned up
    x_str = str(x)
    c_string = coordinates[x_str][y]
    c_split = c_string.split(",")
    # Convert lat string to float
    lat_str = c_split[0].replace("(", "")
    lat = float(lat_str)
    # Convert lon string to float
    lon_str = c_split[1].replace(")", "")
    lon = float(lon_str)
    return(lat, lon)

# Returns a dictionary of y, x values for top speed results
def get_y_x():
    """ query y, x values from the topwind table """
    cur.execute("SELECT y, x FROM topresults10s")
    rows = cur.fetchall()
    results = []
    y = 0
    x = 0
    for row in rows:
        dict_vals = {'y':row[0], 'x':row[1]}
        results.append(dict_vals) 
    return(results)

def update_latitude(lat_y, y, x):
    """ update longitude value based on y, x index combo """
    sql = """ UPDATE topresults10s SET lat_y = %s WHERE y = %s AND x = %s"""
    cur.execute(sql, (lat_y, y, x))

def update_longitude(long_x, y, x):
    """ update longitude value based on y, x index combo """
    sql = """ UPDATE topresults10s SET long_x = %s WHERE y = %s AND x = %s"""
    cur.execute(sql, (long_x, y, x))
   
if __name__ == '__main__':

    coordinates = pd.read_csv("coordinates.csv")

    # db details
    config = ConfigParser()
    config.read(abspath('config.ini'))
    instance = config.get('PostgreSQL', 'instance')
    db = config.get('PostgreSQL', 'database')
    username = config.get('PostgreSQL', 'username')
    password = config.get('PostgreSQL', 'password')

    conn = psycopg2.connect(host=instance,database=db, user=username, password=password)

    cur = conn.cursor()

    # Get dictionary of top y, x pairs (locations)
    top_locations = get_y_x()

    # Iterate through the dictionary and translate y, x index to latitude and longitude 
    for key in top_locations:
        y_index = (key['y'])
        x_index = (key['x'])
        lat_long = get_lat_long(y_index, x_index)
        update_latitude(lat_long[0], y_index, x_index)
        conn.commit()
        update_longitude(lat_long[1], y_index, x_index)
        conn.commit()

    cur.close()
