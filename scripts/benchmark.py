from wikipediaQueryEngine import *
import wptools
import xlrd
from utils import normalize
import time
from datetime import timedelta
import json

def benchmark():

    start_time = time.time()
    
    excel_file = xlrd.open_workbook('../data/arbres.xls')

    data = excel_file.sheets()[0]

    id_list = data.col(1)
    names_french_list = data.col(2)
    genus_list = data.col(3)
    species_list = data.col(4)
    
    tupleList = list(zip(id_list, names_french_list, genus_list, species_list))

    wqe = WikipediaQueryEngine()

    count = 0
    success = 0
    total = len(tupleList)-1

    errors = []

    successes = {}

    for i in range(total-1):
        r = wqe.enrich_data(tupleList[i+1][1].value, tupleList[i+1][2].value, tupleList[i+1][3].value)
        if bool(r):
            
            success += 1
            successes[tupleList[i+1][0].value] = r
        else:
            errors.append((tupleList[i+1][0].value, tupleList[i+1][1].value, tupleList[i+1][2].value))
        count += 1
        print(str(count)+'th try : '+str(success)+' successes yet, out of '+str(total))
    print(str(success*100/total)+"% of success")
    errors_file = open('errors.log', 'w')
    for error in errors:
        errors_file.write(str(error[0])+', '+str(error[1])+', '+str(error[2])+'\n')
    errors_file.close()

    elapsed_time_secs = time.time() - start_time

    print("Execution took: %s secs (Wall clock time)" % timedelta(seconds=round(elapsed_time_secs)))
    
    with open('enriched_data.json', 'w') as fp:
        json.dump(successes, fp, sort_keys=True, indent=4)

benchmark()
