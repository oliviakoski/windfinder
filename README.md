# Wind Finder #
## Unleash the Power of Wind ##

Wind Finder uses Amazon Web Services cluster computing
resources to identify areas of steady, constant
winds with data available from the National Renewable
Energy Laboratory's WIND Toolkit dataset. This project was completed during the Insight Data
Engineering Fellowship in early 2020.

Users can view top average wind speeds across the U.S. Data from wind speeds at typical turbine height of 100 meters is averaged from multiple daily measurements across the U.S at spatial resolution or 2 km x 2 km. The top sites of highest average wind speed are visualized on a map using Tableau.

Visit [intuidata.live](http://intuidata.live) for a demo of the program

## Pipeline ## 
The source data is available from the Amazon Open Data Registry in a S3 bucket in HDF5 (.h5 format). A 2D time slice of the data across a U.S. grid is extracted to .CSV format before processing in Spark. The .CSV formatted y-x array of wind speeds at time t is transformed to a dataframe of x, y, v, t values that are loaded to PostgreSQL, queried to identify top average speeds and 
visualized with Tableau. 

## Data Source ## 
The NREL Wind Integration National Dataset is available via Amazon Web Service's Registry of Open Data here: https://registry.opendata.aws/nrel-pds-wtk/
For a quick introduction to the data via API check out examples developed by NREL's Caleb Phillips, John Readey, and Jordan Perr-Sauer via [hsds-examples](https://github.com/NREL/hsds-examples).

## Set Up and Execution ## 
This program uses a 4 node AWS EC2 Spark cluster launched using [Pegasus](https://github.com/InsightDataScience/pegasus). Separate EC2 instances should be launched for the web server front end and PostgreSQL database. Clone this repository from the master node and run programs from the command line. Create a config file with S3 and PostgreSQL details using the template config.ini file provided.

./ingestion-run.sh

./spark-run.sh

./postgres-run.sh
