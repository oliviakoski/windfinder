# This program executes SQL queries on the topwind table 
# to compute top average wind speeds over y, x and t to find the 
# top windiest spots across the U.S. 
# Lat, long columns are added to the results table so
# that y, x index values can be converted to lat, long values

import psycopg2
from os.path import abspath
from configparser import ConfigParser

def create_avg_speeds():
    # Create table with average wind speed results
    cur.execute('''CREATE TABLE IF NOT EXISTS avgresults
             AS SELECT y, x, t, avg(v) FROM topwind
             GROUP BY y, x, t;''')

def create_top_results():
    # Get the top 20 average speed values for each time period 
    cur.execute('''CREATE TABLE IF NOT EXISTS topresults AS 
                SELECT y, x, t, avg FROM (SELECT ROW_NUMBER() OVER (PARTITION BY t ORDER BY avg DESC) AS RESULTS, t.* FROM avgresults t) NUMBER 
                WHERE NUMBER.RESULTS <= 20;''')

def creat_lat_long():
    # Create latitude and longitude fields to convert x, y index values
    cur.execute('''ALTER TABLE topresults ADD COLUMN lat_y FLOAT8, ADD COLUMN long_x FLOAT8;''')

if __name__ == '__main__':
    # db details
    config = ConfigParser()
    config.read(abspath('config.ini'))
    instance = config.get('PostgreSQL', 'instance')
    db = config.get('PostgreSQL', 'databaes')
    username = config.get('PostgreSQL', 'username')
    password = config.get('PostgreSQL', 'password')

    conn = psycopg2.connect(host=instance,database=db, user=username, password=password)

    cur = conn.cursor()
    
    # Create tables and add lat, long columns
    create_avg_speeds()
    create_top_results()
    create_lat_long()

    cur.close()
    conn.commit()