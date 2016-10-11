import xlrd

excel_file = xlrd.open_workbook('./datas/arbres.xls')

datas = excel_file.sheets()[0]

errors = []

for row in range(datas.nrows):
    passs
