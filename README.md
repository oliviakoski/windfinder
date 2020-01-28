# windfinder
Wind Finder uses Amazon Web Services cluster computing resources to quickly identify
areas of steady, constant winds using data available from the 
National Renewable Energy Laboratory's WIND Toolkit dataset. These target areas
may then be further studied by renewable energy entrpreneurs to determine
suitability for building wind turbines. 

# ingestion
-> get h5 file from S3
-> downsample using NumPy
-> convert to Parquet

# spark
-> read parquet or csv from S3
-> transform data
-> load into postgreSQL

# frontend
-> query data
-> display data

# atom of data
INPUT: t, x, y, v
OUTPUT: delta_t, x, y, v_avg
