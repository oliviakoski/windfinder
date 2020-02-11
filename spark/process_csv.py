# This program takes an input csv file "b'20070122140000'.csv" and loads unfurled data 
# into a Postgres table with schema y, x, v(i), t(i)

import os

os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"
os.environ["PYSPARKDRIVER_PYTHON"]="/usr/bin/python3"

# -*- coding: utf-8 -*-
from app.utils import CSVFile
from app.utils import Database

#from pyspark.sql import functions as f
from pyspark.sql.functions import col, lit
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType

# Access the SparkSession module from pyspark
from pyspark.sql import SparkSession
import csv

# Open a Spark session
spark = SparkSession.builder.appName("find_the_wind").getOrCreate()

# Fetch .csv file from S3 bucket (see utils.py)
# csvname = "b'20070201010000'.csv"
# csv_task = CSVFile(csvname)
# csv = csv_task.load()

# Read dataframe in from CSV file. It's important to Infer Schema so strings are converted to numbers
# Each row is labeled by its index 
df_csv = spark.read.format('csv').options(header='true', inferSchema='true').load("s3a://wind-toolkit-csv/b'20070122140000'.csv")

# Change name of first column and save to dataframe df_y
#df_y = df.withColumnRenamed("_c0","lat_y")
df = df_csv.withColumnRenamed("_c0", "y") 

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

# Create our target dataframe structure
_schema = StructType([StructField("y", IntegerType()), StructField("x", IntegerType(), True), StructField("v", FloatType()),StructField("t", IntegerType(), True)])
nullFrame =  spark.createDataFrame([], _schema)

# Load column from dataframe into new schema structure
def create_part(df, idx, time):
  df_temp = df\
  .select("y", "{}".format(idx))\
  .withColumn("x", lit("{}".format(idx)))\
  .withColumn("t", lit("{}".format(time)))\
  .withColumnRenamed("{}".format(idx), "v")\
  .select("y", "x", "v", "t")
  df_result = df_temp.withColumn("x", df_temp["x"].cast(IntegerType()))\
  .withColumn("t", df_temp["t"].cast(IntegerType()))
  return df_result
#.cast(IntegerType())

# Initialize result
result = nullFrame

# Loop through columns 0 -> 2975 to get result
for idx in range(2975):
  result = result.union(create_part(df, idx, time=0))

# Create Database object with required credentials (see utils.py)
db = Database()

# Save column to database
db.save(result, table='topwind')

spark.stop()
