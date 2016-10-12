import xlrd
from utils import normalize
from checkDF import checkDF

excel_file = xlrd.open_workbook('./datas/arbres.xls')

datas = excel_file.sheets()[0]

new_datas = []

#this dict contains the right espce for each type en francais
correction_espece_type = {
    'frene a fleurs': 'ornus',
    'evodia de daniel': 'daniellii',
    'sequoia toujours vert': 'sempervirens',
    'fevier d\'amerique': 'triacanthos',
    'erable du fleuve amour': 'ginnala',
    'cerisier a grappes': 'padus',
    'erable de cappadoce': 'cappadocicum',
    'oranger des osages': 'pomifera',
    'charme commun': 'betulus',
    'charme-houblon': 'carpinifolia',
    'acajou de chine': 'sinensis',
    'arbre de fer': 'persica',
    'phellodendron liege de l\'amour': 'amurense',
    'sophora du japon': 'japonica',
    'hetre commun': 'sylvatica',
    'micocoulier de virginie': 'occidentalis',
    'erable trifide': 'buergerianum',
    'virgilier': 'lutea',
    'orme du caucase': 'carpinifolia',
    'savonnier': 'paniculata',
    'arbre a soie': 'julibrissin',
    'amelanchier gracieux': 'amabilis',
    'robinier faux-acacia': 'pseudoacacia',
    'orme champetre': 'campestris',
    'chicot du canada': 'dioicus',
    'frene commun': 'excelsior',
    'cercidiphyllum du japon': 'japonicum',
    'erable rouge': 'rubrum',
    'cerisier a fleurs': 'serrulata',
    'bouleau blanc d\'europe': 'alba',
    'erable du japon': 'palmatum',
    'pin sylvestre': 'sylvestris',
    'cerisier a fleurs': 'serrulata',
    'tilleul argente': 'tomentosa',
    'araucaria du bresil': 'angustifolia'
}



for row in range(datas.nrows):
    new_line = [normalize(datas.cell(row,i).value) for i in range(datas.ncols)]

    #we have a mistake here, so we need to check the espece for each type we have
    for type_francais, espece in correction_espece_type.items():
        if new_line[2] == type_francais:
            new_line[4] = espece

    new_datas.append(new_line)

#print(new_datas)
errors = checkDF(new_datas)

for line in errors:
    print(line)
