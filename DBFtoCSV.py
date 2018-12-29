#DBF to CSV converter
"""Converts the .dbf files that are output by the Stack Profile tool into .csv
files that can be analyzed in Python"""



#!/usr/bin/python

import csv
from dbfpy import dbf
import os
import sys

os.chdir("C:\Users\graham.farley\Downloads\Data\Mountain_Profiles")
files = os.listdir(os.getcwd())
for filename in files:
    if filename.endswith('.dbf'):
        print "Converting %s to csv" % filename
        csv_fn = filename[:-4]+ ".csv"
        with open(csv_fn,'wb') as csvfile:
            in_db = dbf.Dbf(filename)
            out_csv = csv.writer(csvfile)
            names = []
            for field in in_db.header.fields:
                names.append(field.name)
            out_csv.writerow(names)
            for rec in in_db:
                out_csv.writerow(rec.fieldData)
            in_db.close()
            print "Done..."
    else:
      print "Filename does not end with .dbf"
