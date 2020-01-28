# This program takes an input csv file "longspeak_wtk.csv" and outputs a filtered dataset

# Access the SparkSession module from pyspark
from pyspark.sql import SparkSession
import csv


# Open a Spark session
spark = SparkSession.builder.appName("find_the_wind").getOrCreate()
       
df = spark.read.csv("s3a://wind-toolkit-hdf5/longspeak_wtk.csv")
df = spark.read.format('csv').options(header='true', inferSchema='true').load("s3a://wind-toolkit-hdf5/longspeak_wtk.csv")
df = spark.read.format('csv').options(header='true', inferSchema='true').load('test_data/longspeak_wtk.csv')


df.show(5)
#df.printSchema()
df[df.windspeed_100m > 15].show(4)

#df.write.options("header", "true").csv('test_data/output')
#df.write.csv(os.path.join(tempfile.mkdtemp(), 'data'))
                
spark.stop()
