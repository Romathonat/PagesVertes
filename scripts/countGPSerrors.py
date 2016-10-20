import xlrd
import os

excel_file = xlrd.open_workbook(os.path.join(os.path.dirname(__file__), '../data/arbres.xls'))

data = excel_file.sheets()[0]

gps = {}

with open(os.path.join(os.path.dirname(__file__),'../data/arbresGPS.txt'), 'r+') as f:
    for line in f:
        line = line.replace(' ', '')
        id_arbre, latitude, longitude = line.split(',')
        longitude = longitude.rstrip()
        gps[str(id_arbre)] = (latitude, longitude)

count_error = 0

for row in range(data.nrows):
    tree_latitude, tree_longitude = 0,0
    try:
        id_arbre = data.cell(row,1).value[2:]
        tree_latitude, tree_longitude = gps[id_arbre]
    except:
        count_error += 1

print(count_error)
