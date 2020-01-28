# -*- coding: utf-8 -*-
from app.utils import CSVFile
from app.utils import Database


if __name__ == '__main__':
    csvname = 'longspeak_wtk.csv'
    csv_task = CSVFile(csvname)
    csv = csv_task.load()
    db = Database()
    db.save(csv, table='t1')
