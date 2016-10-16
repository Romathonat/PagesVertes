from wikipediaQueryEngine import *
import wptools
import xlrd
from utils import normalize

def benchmark2():
    
    excel_file = xlrd.open_workbook('./data/arbres.xls')

    data = excel_file.sheets()[0]

    names_french_list = data.col(2)
    genus_list = data.col(3)
    species_list = data.col(4)
    
    tupleList = list(zip(names_french_list, genus_list, species_list))

    wqe = WikipediaQueryEngine()

    count = 0
    success = 0
    total = len(tupleList)-1

    errors = []

    for i in range(total-1):
        r = wqe.correct_and_enrich_species(tupleList[i+1][0].value, tupleList[i+1][1].value, tupleList[i+1][2].value)
        if bool(r):
            success += 1
        else:
            errors.append((tupleList[i+1][0].value, tupleList[i+1][1].value, tupleList[i+1][2].value))
        count += 1
        print(str(count)+'th try : '+str(success)+' successes yet, out of '+str(total))
    
    errors_file = open('errors.log', 'w')
    for error in errors:
        errors_file.write(str(error[0])+', '+str(error[1])+', '+str(error[2])+'\n')
    errors_file.close()

def benchmark():

    f = open('noms', 'r')
    data = f.read()
    namesList = data.splitlines()
    namesList = [namesList[i] for i in range(len(namesList)) if i == namesList.index(namesList[i])]

    i = 0
    wqe_counter = 0
    wp_counter = 0    

    wqe = WikipediaQueryEngine()

    #import pdb; pdb.set_trace()

    wqe_errors_file = open('wqe_errors.txt', 'w')
    wp_errors_file = open('wp_errors.txt', 'w')

    for name in namesList:
        
        # wqe
        words = name.split()
        name = ""
        for word in words:
            if(word.lower() == 'indéterminé' or word.lower() == 'inconnu'):
                pass
            else:
                name += word+' '
        name = name.strip()

        wqe_results = wqe.query_for(name)
        if(wqe_results["found"] == True):
            wqe_counter+=1
        else:
            wqe_errors_file.write(name+'\n')

        # wp
        wp_found = True
        try:
            wp_result = wptools.page(name, lang='fr').get()
            wikidata = wp_result.wikidata
            if "taxon rank" in wikidata:
                if wikidata["taxon rank"] != 'espèce':
                    wp_found = False
                    wp_errors_file.write(name+'\n')
            else:
                wp_found = False
                wp_errors_file.write(name+'\n')
        except:
            wp_found = False
            wp_errors_file.write(name+'\n')
        finally:
            if wp_found == True:
               wp_counter+=1
            i+=1
            print('\n'+str(i)+' out of '+str(len(namesList)))
            print('WQE : found '+str(wqe_counter)+' matches out of '+str(len(namesList)) )
            print('WP : found '+str(wp_counter)+' matches out of '+str(len(namesList)) )
    wqe_errors_file.close()
    wp_errors_file.close()

benchmark2()
	

