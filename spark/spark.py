# This program takes an input csv file of wind speeds in a 1602 x 2975 array for a 
# time point YYYY-MM-DD HH:MM:SS and  explodes data into schema
# y, x, v, t format, and loads to Postgres for querying

### Original Schema ###
# NULL  0    1   2  ..    2975
# 0     v00 v01 v02 ..  v02975
# 1     v10 v11 v12 ..  v12975
# 2     v20 v21 v22 ..  v22975
# ..    ..  ..  ..  ..  ..
# 1602 ..   ..  ..  ..  v16022975

###     New Schema  ###
# y    x    v         t
# 0    0    v00       0
# 1    0    v10       0
# 2    0    v20       0
# ..   ..   ..        ..
# 1602 2975 v16022975 0

import os
import csv
from app.utils import Database
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, input_file_name, substring
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType, DateType

# Set default Python version 
os.environ["PYSPARK_PYTHON"]="/home/ubuntu/miniconda3/bin/python3.6"
os.environ["PYSPARKDRIVER_PYTHON"]="/home/ubuntu/miniconda3/bin/python3.6"

# To get AWS bucket name
config = ConfigParser()
config.read(abspath('config.ini'))
bucket_csv = config.get('AWS', 'bucket_csv')

# Given dataframe of 1602 x 2975 shape, return dataframe of 1602 x 4 shape
# With columns y, x, v, t
def create_df(df, idx):
  df_temp = df\
  .select("y", "{}".format(idx))\
  .withColumn("x", lit("{}".format(idx)))\
  .withColumnRenamed("{}".format(idx), "v")\
  .withColumn("t", input_file_name())\
  .select("y", "x", "v", "t")
  df_result = df_temp.withColumn("x", df_temp["x"].cast(IntegerType()))
  return df_result

# Clean up timestamp column 
def create_substring(df):
  df = df.select("y", "x", "v", df.t.substr(30,10).alias("t"))
  return(df)

# Convert timestamp string column to date column 
def convert_substring(df):
  df = df.withColumn("t", df['t'].cast(DateType()))\
      .select("y", "x", "v", "t")
  return(df)

# main method that executes spark job
if __name__ == '__main__':
    # Read dataframe from CSV file directory. 
    df_csv = spark.read.format('csv').options(header='true', inferSchema='true').load(bucket_csv)

    # Change name of first column, get timestamp from file name
    df_y = df_csv.withColumnRenamed("_c0", "y") 
    df_t = df_y.withColumn("t", input_file_name())

    # Create Database object with required credentials to write to Database
    db = Database()

    # Loop through columns 0 -> 2975, create new dataframe for each and write to Database.
    # Downsampling is highly recommended as a "full resolution" job processing data 
    # across a 2 km x 2 km grid of the U.S. takes 16 hours per 100 time points on a 
    # 4 node m4.2xlarge cluster. Suggested step rate of 5-10 provides 
    # lower spatial resolution of 10 km - 20 km (data sampling every 6 - 12 miles)
    for idx in range(30, 2975, 10):
        df_orig = create_df(df_t, idx)
        df_substring = create_substring(df_orig)
        df_final = convert_substring(df_substring)
        db.save(df_final, table='topwind')

    spark.stop()