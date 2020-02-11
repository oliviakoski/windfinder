import h5py
import numpy as np
import pandas as pd
import s3fs


# Create s3 context
s3 = s3fs.S3FileSystem()

# Load file from S3 bucket
f = h5py.File(s3.open("s3://wind-toolkit-hdf5/2007-01.h5"), "r")
datetime = f["datetime"]

# Create a dataframe for each timepoint and write to csv and parquet
for i in range(len(datetime)):
    timeframe = datetime[i]
    df = pd.DataFrame(f['windspeed_100m'][i])

    # Write to csv
    filename_csv = "s3://wind-toolkit-csv/" + str(timeframe) + ".csv"
    df.to_csv(filename_csv)


f.close()
