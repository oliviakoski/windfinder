#!/bin/bash
#
#/usr/local/spark/bin/spark-submit s3-spark-postgres-wind-2.py
/usr/local/spark/bin/spark-submit spark://10.0.0.11:7077 process_csv.py 

