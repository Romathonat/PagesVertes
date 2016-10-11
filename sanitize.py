import xlrd
from utils import normalize
from checkDF import checkDF

excel_file = xlrd.open_workbook('./datas/arbres.xls')

datas = excel_file.sheets()[0]

new_datas = []

#this dict contains the right espce for each type en francais
correction_espece_type = {
    'frene a fleurs': 'ornus'
}



for row in range(datas.nrows):
    new_line = [normalize(datas.cell(row,i).value) for i in range(datas.ncols)]

    #there are a lot of mistakes with saccharinum. It has a unique type "Erable argenté", so we correct these lines
    if normalize(datas.cell(row,4).value) == 'saccharinum' and normalize(datas.cell(row,2).value) != 'erable argente':
        #we have a mistake here, so we need to check the espece for each type we have
        if new_line[2] == 'frene a fleurs':
            new_line[4] = correction_espece_type['frene a fleurs']

    new_datas.append(new_line)

#print(new_datas)
errors = checkDF(new_datas)

for line in errors:
    print(line)
