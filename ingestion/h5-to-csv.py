# This program extracts a timeslice of the 'windspeed_100m' attribute from the National
# Renewable Energy Laboratory Wind Toolkit Dataset for all y, x values on a 2 km x 2 km grid 
# across the U.S. and exports the result to a 1602 x 2975 array in .csv format
#  ###### Output Format ####### 
#       0   1   2   ... 2975
# 0     v00 v01 v02     v02975
# 1     v10 v11 v12
# ..
# 1601  v16010 ....     v16012975

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

# Get timestamp from time index. This is used to name the csv file.
def get_timestamp(filename_hdf, time_index):
    f = h5py.File(s3f.open(bucket_hdf + "/" + filename_hdf), "r")
    timestamps = f['datetime']
    time_str = str(timestamps[time_index])
    time_inner = time_str.replace("b'", "")
    time_clean = time_inner.replace("'", "")
    timestamp = datetime.strptime(time_clean, "%Y%m%d%H%M%S")
    f.close()
    return(timestamp)

# Creates dataframes of windspeeds for each timeslice 
# in a specified range according to start, stop, and step values.
# Each hdf file is one month of data with name format 'YYYY-MM.h5'
# All files start at 0 and end at between 719 to 791 depending on the
# length of the month. The max number of time slices per month is 
# 792 or 792 hours of wind data  
def create_csv(filename_hdf, start, stop, step):
    for index in range(start,stop,step):
        timestamp = get_timestamp(filename_hdf, index)
        f = h5py.File(s3f.open(bucket_hdf + "/" + filename_hdf), "r")
        df = pd.DataFrame(f['windspeed_100m'][index])
        filename_csv = bucket_csv + "/" + str(timestamp) + ".csv"
        df.to_csv(filename_csv)
        f.close()

if __name__ == '__main__':

    hdf_file_names = (get_s3_keys(bucket_hdf))

    # Example for creating files for two 24 hour every 6 hours 
    # (8 data samples per day) for every .h5 file in the folder 
    for item in hdf_file_names:
        create_csv(item, 24, 48, 6)
        create_csv(item, 360, 384, 6)