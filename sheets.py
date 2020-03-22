import os
import csv
import openpyxl

dir_name = "data"

sheets = os.listdir(dir_name)
### loading first element
workbook = openpyxl.load_workbook(os.path.join('data', sheets[0]))
