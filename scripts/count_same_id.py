import xlrd
import os

excel_file = xlrd.open_workbook(os.path.join(os.path.dirname(__file__), '../data/arbres.xls'))
data = excel_file.sheets()[0]

count_error = 0
id_arbres = set()

for row in range(data.nrows):
    id_arbre = data.cell(row,1).value[2:]
    if(id_arbre in id_arbres):
        count_error += 1
    else:
        id_arbres.add(id_arbre)

print(count_error)
