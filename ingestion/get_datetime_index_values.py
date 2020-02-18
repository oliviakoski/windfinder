# This program gets datetime values for each time index from NREL Wind toolkit .h5 files and stores the result
# to csv. This is for informational purposes to understand which date and time values
# you are sampling for each month.  

import os, sys
from os.path import abspath
from configparser import ConfigParser
from datetime import datetime
import s3fs, boto3
import numpy as np
import pandas as pd
import h5py

# To get AWS bucket names 
config = ConfigParser()
config.read(abspath('config.ini'))
bucket_hdf = config.get('AWS', 'bucket_hdf')
bucket_csv = config.get('AWS', 'bucket_csv')

# s3fs and boto3 are both used in this program to communicate with S3. boto3 is used to list
# filenames in bucket, s3fs is needed for communicating with .h5 files 
s3b = boto3.client('s3')
s3f = s3fs.S3FileSystem()

# Returns file names within s3 bucket 
def get_s3_keys(bucket):
    """Get a list of keys in an S3 bucket."""
    keys = []
    resp = s3b.list_objects_v2(Bucket=bucket)
    for obj in resp['Contents']:
        keys.append(obj['Key'])
    return keys

# Function to get datetime values from .h5 file in specific bucket and save to .csv 
def get_datetime_values(filename):
    #s3f = s3fs.S3FileSystem()
    f = h5py.File(s3f.open(bucket_hdf + "/" + filename), "r")
    df = pd.DataFrame(f['datetime'])
    df.to_csv(filename)

if __name__ == '__main__':
    hdf_file_names = (get_s3_keys(bucket_hdf))

    for item in hdf_file_names:
        get_datetime_values(item)











