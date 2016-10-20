import xlrd
from utils import normalize
from checkDF import checkDF
from wikipediaQueryEngine import WikipediaQueryEngine
import os

def sanitize(useWikipedia):
    """useWikipedia is a boolean telling if we want to add a step to enrich and
    correct data with wikipedia"""

    excel_file = xlrd.open_workbook(os.path.join(os.path.dirname(__file__),'../data/arbres.xls'))
    data = excel_file.sheets()[0]
    new_data = []
    incomplete_data = []

    if(useWikipedia):
        w = WikipediaQueryEngine()
    #this dict contains the right espece for each type en francais
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
        'araucaria du bresil': 'angustifolia',
        'pommier d\'ornement "professor sprenger"': 'Professor Sprenger',
        'pommier microcarpe de siberie': 'baccata',
        'epicea indetermine': 'sp.',
        'orme de samarie': 'trifoliata',
        'robinier a fleurs rouges': 'pseudoacacia',
        'cornouiller des pagodes': 'controversa',
        'micocoulier': 'australis',
        'fevier d\'amerique a feuilles dorees': 'triacanthos',
        'fevier d\'amerique sans epines': 'triacanthos',
        'pommier indetermine': 'sp.',
        'pommier toringo': 'sieboldii',
        'aulne glutineux a feuilles laciniees': 'glutinosa',
        'caryer blanc':'ovata'
    }

    #this dict contains the right genre-espece for each type en francais
    correction_genre_espece = {
        'sequoia toujours vert': ('sequoia', 'sempervirens'),
        'douglas': ('picea', 'douglasii')
    }

    correction_type_arbre = {
        ('taxus', 'baccata'): 'conifere',
        ('taxodium', 'distichum'): 'conifere',
        ('ginkgo', 'biloba'): 'feuillu',
        ('pyrus', 'glutinosa'): 'feuillu',
        ('quercus', 'trojana'): 'feuillu'
    }

    for row in range(data.nrows):
        new_line = [normalize(data.cell(row,i).value) for i in range(data.ncols)]
        #we expand the size of the line to add  info_french, url and description
        new_line.extend(["" for i in range(4)])
        
        if new_line[4] != 'sp.':
            #we correct datas with wikipedia, if requested
            if useWikipedia and row > 0:
                print('{} {} {}'.format(data.cell(row,2).value, new_line[3], new_line[4]))
                r = w.correct_and_enrich_species(data.cell(row,2).value, new_line[3], new_line[4])
                print(r)



                if r and r['suggested_name_french'] != '' and r['genus'] != '' and r['species'] != '':
                    #if we have a blank for the type_francais
                    if new_line[2] == '':
                        new_line[2] = r['suggested_name_french']

                    new_line[3] = normalize(r['genus'])
                    new_line[4] = normalize(r['species'])

                    #this line is a nested informations
                    new_line[9] = r['info_french']
                    new_line[10] = normalize(r['url'])
                    new_line[11] = normalize(r['description'])
                    new_line[12] = normalize(r['suggested_name_french'])



            #we have a mistake here, so we need to check the espece for each type we have
            for type_francais, espece in correction_espece_type.items():
                if new_line[2] == type_francais:
                    new_line[4] = espece

            for type_francais, espece_genre in correction_genre_espece.items():
                if new_line[2] == type_francais:
                    new_line[3] = espece_genre[0]
                    new_line[4] = espece_genre[1]

            for espece_genre, type_arbre in correction_type_arbre.items():
                if (new_line[3], new_line[4]) == espece_genre:
                    new_line[5] = type_arbre

            #we don't pay attention to the first line
            if row > 0:
                if new_line[2] != '' and new_line[3] != '' and new_line[4] != '':
                    new_data.append(new_line)
                else:
                    incomplete_data.append(new_line)
        else:
            incomplete_data.append(new_line)

    #print(new_data)
    errors = checkDF(new_data)

    for line in errors:
        print(line)

    return (new_data, incomplete_data)
