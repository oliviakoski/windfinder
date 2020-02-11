# -*- coding: utf-8 -*-
from app.utils import CSVFile
from app.utils import Database


csvname = "wtk_site_metadata.csv"
csv_task = CSVFile(csvname)
csv = csv_task.load()
db = Database()
db.save(csv, table='testwind')

