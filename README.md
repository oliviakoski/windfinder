# Wind Finder #
## Unleash the Power of Wind ##

Wind Finder uses Amazon Web Services cluster computing
resources to quickly identify areas of steady, constant
winds using data available from the National Renewable
Energy Laboratory's WIND Toolkit dataset. These target
areas may then be further studied by renewable energy
entrpreneurs to determine suitability for building wind
turbines. 

This project was completed during the Insight Data
Engineering Fellowship in early 2020, uses publicly
available wind data from the National Renewable Energy
Laboratory to help wind power entrepreneurs discover
areas of high wind availability. 

Users can view top average wind speeds across the U.S. Data from wind speeds at typical turbine height of 100 meters is averaged from multiple daily measurements over a 2 km x 2 km grid. The top 20 sites of highest average wind speed are visualized on a map using Tableau. The user may look at top average speeds over time to determine areas worthy of further study. 

Visit intuidata.live for a demo of the program

# Pipeline # 
The source data is available from the Amazon Open Data Registry in a S3 bucket in HDF5 (.h5 format). A 2D time slice of the data across a U.S. grid is extracted to .CSV format before processing in Spark. The .CSV formatted x-y array of wind speeds at time t is transformed to a dataframe of x, y, v, t values that are loaded to PostgreSQL, queried to identify top average speeds and 
visualized with Tableau. 


# Ingestion #
* get h5 file from S3
* Select wind speeds at 100 meters (typical turbine height) 
* Convert to .CSV  

# Spark # 
* Read .csv from S3
* Transform data
* Load into postgreSQL

# PostgreSQL # 
* Query top speeds 
* Translate y, x index values to latitude, longitude values
* Save to results table 

# Tableau #
* Connect visualization tool to PostgreSQL
* Display top average wind speeds over time 

# Schema #
INPUT: y (latitude), x (longitude), v (speed at 100 m), t (time)
OUTPUT: top v_avg, x, y, delta_t
