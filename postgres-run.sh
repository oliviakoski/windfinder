#!/bin/bash
#
python make_coordinates_file.py
python postgres_create_tables.py
python postgres_update_lat_long.py
