import json
import os
import time
import glob
import ntpath


PATH_COMPLETE_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../webApp/json/")
PATH_INCOMPLETE_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../webApp/json/incomplete_data/")
DIRECTORY_RESULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../data/sql/")
USE_WIKIPEDIA = True

#Template
def template_header_file_sql():
    today_date = time.strftime("%Y-%m-%d %H:%M:%S ")
    header = "-- This file contains all sql commands in order to populate a sql database, tables and insertions"
    header += "\n-- Creation : "+ str(today_date)
    header += "\n-- Database : Arbres du Grand Lyon, la ville Lumiere"
    header += "\n\n"
    header += "\n-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------\n-- ----------------------------------------------------------------TABLES--------------------------------------------------------------------------------------------\n-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------"
    return header

def template_table_sql(table_name,table_fields,table_values,primary_key_field_name=None,primary_key_field_type=None):
    # table_name is the name of the table to create
    # table_values is a dictionary with in key the field_name and in value a list of values for this field name
    # table_fields is a dictionary with in key the field_name and in value a tuple that contains (field_type,can_field_be_null) which is (string,boolean)
    # primary_key_field_name is the name of the field that must be the primary key of the table, if it is not found in the json we create an artificial integer primary key
    # primary_key_field_type is a string that describes the type of the field that must be the primary key, we assume that we call with good parameters this function 
    table = "-- table "+ str(table_name)
    table += "\n"
    table += template_create_table_sql(table_name,table_fields,primary_key_field_name,primary_key_field_type)
    table += "\n\n"
    table += template_insert_values_table_sql(table_name,table_fields,table_values)
    table += "\n\n-- ------------------------------------------------------------------------------------------------------------------------\n-- ------------------------------------------------------------------------------------------------------------------------"

    return table

def template_create_table_sql(table_name,table_fields,primary_key_field_name=None,primary_key_field_type=None):
    # table_fields is a dictionary with in key the field_name and in value a tuple that contains (field_type,can_field_be_null) which is (string,boolean)
    # primary_key_field_name is the name of the field that must be the primary key of the table, if it is not found in the json we create an artificial integer primary key
    # primary_key_field_type is a string that describes the type of the field that must be the primary key, we assume that we call with good parameters this function 
    
    table = "\n-- Structure"
    table += "\n\n"
    table += "CREATE TABLE `"+ str(table_name) + "`("
    table += "\n"

    # management of the primary key
    if primary_key_field_name == None or primary_key_field_name not in table_fields:
        # we create an artificial primary key if there is not one or not found in table_fields
        #the first field is an artificial field for index in database
        nom_index = "pk_"+str(table_name)
        table += "  `"+nom_index+"` int(11) NOT NULL"
    else :
        nom_index = str(primary_key_field_name)
        table += "  `"+primary_key_field_name+"` "+ str(primary_key_field_type) +" NOT NULL"


    # we create the other attributes
    for key in table_fields.keys():
        if key != primary_key_field_name:
            table += ",\n"

            field_type,can_field_be_null = table_fields[key]

            table += "  `"+str(key)+"` "+str(field_type)

            if can_field_be_null == False:
                table += " NOT NULL"



    table += "\n);"


    table += "\n\n"
    table += "-- index for table"
    table += "\nALTER TABLE `"+str(table_name)+"`"
    table += "\n  ADD PRIMARY KEY (`"+nom_index+"`);"

    if primary_key_field_type == "int(11)" or primary_key_field_type == None or primary_key_field_name not in table_fields:
        # we do auto-increment only if the primary field key is an integer or if the primary key is an artificial one that we have just created
        table += "\n\n"
        table += "-- Auto increment for index"
        table += "\nALTER TABLE `"+str(table_name)+"`"
        table += "\n  MODIFY `"+nom_index+"` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;"

    return table


def template_insert_values_table_sql(table_name,table_fields,table_values):
    # table_fields is a dictionary with in key the field_name and in value a tuple that contains (field_type,can_field_be_null) which is (string,boolean)
    # table_values is a dictionary with in key the field_name and in value a list of values for this field name

    table = "\n-- Content for table "+str(table_name)
    table += "\n\n"
    table += "INSERT INTO `" + table_name + "` ("

    is_first_field = True #variable use in order to know if we add a `,` after the field name
    for key in table_values.keys():

        if is_first_field == False:
            table += " , "

        table += "`" + str(key) + "`"

        is_first_field = False

    table += ") VALUES \n"


    # now we go through values to create the tuples to insert
    table_values_list = list(table_values.values())
    i = 0
    is_first_values = True #variable use in order to know if we add a `,` after the values tuple
    if len(table_values_list) > 0:
        while i < len(table_values_list[0]):

            if is_first_values == False:
                 table += " , "
            table += "("


            is_first_value = True #variable use in order to know if we add a `,` after the value
            for values_list in table_values_list:
                if is_first_value == False:
                    table += " , "
                
                if values_list[i] != "":
                    table += "'"+ str(values_list[i]).replace("'","\\'") +"'"
                else:
                    table += "'Null'"
                is_first_value = False

            table += ")"
            is_first_values = False
            i += 1


    table += ";"

    return table


def open_json(file_path):
#open a file which contains a json and create an object that is returned
    try:
        with open(file_path) as data_file:   
            try :
            #we try to load the file as a json
                data = json.load(data_file)
                return data
            except:
                print("ERROR : file ",file_path," is not json valid. We try to load by removing first line")

        with open(file_path) as data_file:
            try :
            # we try to load the file as a json by removing the first line because in some json files, the first line is a number indicating the number of elements
                lines = ""
                is_first_line = True
                for line in data_file:
                    if is_first_line == False:
                        lines += line
                    is_first_line = False
                data = json.loads(lines)
                return data
            except:
                print("ERROR : file ",file_path," is not json valid. Return None")
                return None

    except:
        print("ERROR : file ",file_path," cannot be found")
        return None

def file_writer(directory_path,file_name,content):
    #content is a string that contains what to write in file
    if os.path.isdir(directory_path) == False:
        os.makedirs(directory_path)

    file_path = directory_path+file_name

    # save to file:
    with open(file_path, 'w+') as f:
        f.write(content)


def convert_json_to_SQL(file_json,primary_key_field_name=None,primary_key_field_type=None):
# create a script sql to generate table from json
# return a string containing the script
# primary_key_field_name is the name of the field that must be the primary key of the table, if it is not found in the json we create an artificial integer primary key
# primary_key_field_type is a string that describes the type of the field that must be the primary key, we assume that we call with good parameters this function 

    content = ""

    data = open_json(file_json)
    fields = {}
    values = {}

    # we flat all the dictionary contained in the json list object into one dictionary where key is still the same key 
    # but in values we have a list of values for this key for all the dictionaries
    if data != None:
        
        for dico in data:
            (fields,values) = analyze_dico(dico,fields,values)    


    file_name = str(os.path.splitext(ntpath.basename(file_json))[0])
    content += "\n\n" + template_table_sql(file_name,fields,values,primary_key_field_name,primary_key_field_type)

    return content


def analyze_dico(dico,fields,values):
# take in parameter a dictionary to analyse, and tow dictionaries that we will inject the result of the processing
# return a tuple (fields,values)
# we suppose that dico has only one level keys.
# fields is a dictionary where key is the keys of the dico, and value the type of the keys
# values is a list that contains the values of the dico
    for key in dico.keys():
        if key not in fields:
            if isinstance(dico[key],int):
                fields[key] = ("int(11)",True)
            elif isinstance(dico[key],float):
                fields[key] = ("double",True)
            else:
                fields[key] = ("varchar(255)",True)

            values[key] = []

        if key in dico.keys() and key in values:
            values[key].append(dico[key])

    return (fields,values)

def create_script_SQL(directory_json_path,result_filename="script_sql.sql"):
# create a script SQL to generate tables from json. 
# directory_json_path parameter is the path to the directory that contains the json we want to create tables from.
# result_filename parameter is the name of the result file which will contain the sql script.
# the script will be writen in directory data/sql/.

    content = template_header_file_sql()
    content += "\n\n\n"

    for file_json in glob.glob(os.path.join(directory_json_path, '*.json')):
        #all json files are array that contains objects
        content += convert_json_to_SQL(file_json)

    file_writer(DIRECTORY_RESULT_PATH,result_filename,content)

def convert_nom_binominal_json_to_sql():
# convert json file "nomBinominal.json" to sql.
# we use a method for this file because it needs a special attention and processing because containing the equivalent of three SQL tables
# we suppose we have perfect knowledge of what contains nom_binomial_json file, all its keys so we can do specific processing for each key
# return a string containing the SQL script
    content = ""
    file_nom_binominal_json = os.path.join(PATH_COMPLETE_DATA,"nomBinominal.json")

    # here we define all the first level keys we can found in json file
    species_page_key = "species_page"
    genus_page_key = "genus_page"
    french_infos_key = "info_francais"
    genus_key = "genre"
    specie_key = "espece"
    foliage_key = "feuillage"
    vernacular_name_key = "nom_vernaculaire"


    #here are the primary key fields
    species_page_pk = "url"
    genus_page_pk = "url"
    french_infos_pk = "Nom binominal"

    #here are the jointure foreign key
    species_page_fk = "species_page_fk"
    genus_page_fk = "genus_page_fk"

    # here we do the processing
    data = open_json(file_nom_binominal_json)
    species_page_fields = {}
    species_page_values = {}

    genus_page_fields = {}
    genus_page_values = {}

    french_infos_fields = {"Nom binominal":("varchar(255)",True),"Division":("varchar(255)",True),"Règne":("varchar(255)",True),"Classe":("varchar(255)",True),"Famille":("varchar(255)",True),"Sous-famille":("varchar(255)",True),"Clade":("varchar(255)",True),"Sous-règne":("varchar(255)",True),"Ordre":("varchar(255)",True),"Sous-classe":("varchar(255)",True),genus_key:("varchar(255)",True),specie_key:("varchar(255)",True),foliage_key:("varchar(255)",True),vernacular_name_key:("varchar(255)",True)}
    french_infos_values = {}

    if data != None:
        
        for dico in data:

            species_page_dico = dico[species_page_key]
            genus_page_dico = dico[genus_page_key]

            is_specie_page_already_in_table = False
            is_genus_page_already_in_table = False

            # we check that primary key are unique
            if len(species_page_values)!=0 and len(species_page_dico)!=0:
                if species_page_dico[species_page_pk] in species_page_values[species_page_pk]:
                    is_specie_page_already_in_table = True

            if len(genus_page_values) != 0 and len(genus_page_dico) != 0:
                if genus_page_dico[genus_page_pk] in genus_page_values[genus_page_pk]:
                    is_genus_page_already_in_table = True

            #we group all the other infos in one dictionary, we use for base the franch_infos_dico
            french_infos_dico = dico[french_infos_key]
            french_infos_dico[genus_key] = dico[genus_key]
            french_infos_dico[specie_key] = dico[specie_key]
            french_infos_dico[foliage_key] = dico[foliage_key]
            french_infos_dico[vernacular_name_key] = dico[vernacular_name_key]



            # now we go through dico values

            if len(species_page_dico) != 0:
                if is_specie_page_already_in_table == False:
                    (species_page_fields,species_page_values) = analyze_dico(species_page_dico,species_page_fields,species_page_values)
                french_infos_dico[species_page_fk] = species_page_dico[species_page_pk]
                

            if len(genus_page_dico) != 0:
                if is_genus_page_already_in_table == False: 
                    (genus_page_fields,genus_page_values) = analyze_dico(genus_page_dico,genus_page_fields,genus_page_values)
                french_infos_dico[genus_page_fk] = genus_page_dico[genus_page_pk]

            #(_,french_infos_values) = analyze_dico(french_infos_dico,french_infos_fields,french_infos_values)

            for key in french_infos_fields:
                if key not in french_infos_values:
                        french_infos_values[key] = []

                if key not in french_infos_dico.keys():
                    french_infos_values[key].append("")
                else:
                    french_infos_values[key].append(french_infos_dico[key])

            json.dump(french_infos_values, open("text.txt",'w+'))
            #json.dump(french_infos_dico, open("french_infos_dico.txt",'w+'))

    content += "\n\n" + template_table_sql("species_page",species_page_fields,species_page_values,species_page_pk,"varchar(255)")
    content += "\n\n" + template_table_sql("genus_page",genus_page_fields,genus_page_values,genus_page_pk,"varchar(255)")
    content += "\n\n" + template_table_sql("nom_binominal",french_infos_fields,french_infos_values)

    return content


def convert_green_pages_jsons_to_sql():
    
    result_filename="script_sql.sql"

    file_arbre_json = os.path.join(PATH_COMPLETE_DATA,"arbre.json")
    file_feuillage_json = os.path.join(PATH_COMPLETE_DATA,"feuillage.json")
    file_nom_binominal_json = os.path.join(PATH_COMPLETE_DATA,"nomBinominal.json")
    

    content = template_header_file_sql()
    content += "\n\n\n"

    content += convert_json_to_SQL(file_arbre_json,"id","varchar(255)")
    content += convert_json_to_SQL(file_feuillage_json)

    if USE_WIKIPEDIA:
        content += convert_nom_binominal_json_to_sql()
    else:
        content += convert_json_to_SQL(file_nom_binominal_json,"Nom binominal","varchar(255)")

    
    file_writer(DIRECTORY_RESULT_PATH,result_filename,content)



convert_green_pages_jsons_to_sql()
