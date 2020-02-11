# -*- coding: utf-8 -*-
from os.path import abspath
from configparser import ConfigParser
from pyspark.sql import SparkSession

# -- Load Configuration --
config = ConfigParser()
config.read(abspath('config.ini'))

# -- Init Spark --
spark = SparkSession.builder.appName('windfinder').config("spark.jars", "/home/ubuntu/sparkclass/jar/postgresql-42.2.9.jar").getOrCreate()
