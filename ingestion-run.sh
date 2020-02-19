#!/bin/bash
#
python ingestion/get_datetime_index_values.py
python ingestion/h5_to_csv.py
