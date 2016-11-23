import json
import os
import time
import glob
import ntpath

#Template
def template_header_file_sql():
    today_date = time.strftime("%Y-%m-%d %H:%M:%S ")
    header = "-- This file contains all sql commands in order to populate a sql database, tables and insertions"
    header += "\n-- Creation : "+ str(today_date)
    header += "\n-- Database : Arbres du Grand Lyon, la ville Lumiere"
    header += "\n\n"
    header += "\n-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------\n-- ----------------------------------------------------------------TABLES--------------------------------------------------------------------------------------------\n-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------"
    return header

def template_table_sql(table_name,table_fields,table_values):
    # table_fields is a dictionary with in key the field_name and in value a tuple that contains (field_type,can_field_be_null) which is (string,boolean)
    table = "-- table "+ str(table_name)
    table += "\n"
    table += template_create_table_sql(table_name,table_fields)
    table += "\n\n"
    table += template_insert_values_table_sql(table_name,table_fields,table_values)
    table += "\n\n-- ------------------------------------------------------------------------------------------------------------------------\n-- ------------------------------------------------------------------------------------------------------------------------"

    return table

def template_create_table_sql(table_name,table_fields):
    # table_fields is a dictionary with in key the field_name and in value a tuple that contains (field_type,can_field_be_null) which is (string,boolean)
    
    table = "\n-- Structure"
    table += "\n\n"
    table += "CREATE TABLE `"+ str(table_name) + "`("
    table += "\n"
    #the first field is an artificial field for index in database
    nom_index = "pk_"+str(table_name)
    table += "  `"+nom_index+"` int(11) NOT NULL"

    for key in table_fields.keys():
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


    table += "\n\n"
    table += "-- Auto increment for index"
    table += "\nALTER TABLE `"+str(table_name)+"`"
    table += "\n  MODIFY `"+"pk_"+str(table_name)+"` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;"

    return table


def template_insert_values_table_sql(table_name,table_fields,table_values):
    # table_fields is a dictionary with in key the field_name and in value a tuple that contains (field_type,can_field_be_null) which is (string,boolean)
    # table values is a list of lists

    table = "\n-- Content for table "+str(table_name)
    table += "\n\n"
    table += "INSERT INTO `" + table_name + "` ("

    is_first_field = True #variable use in order to know if we add a `,` after the field name
    for key in table_fields.keys():

        if is_first_field == False:
            table += " , "

        table += "`" + str(key) + "`"

        is_first_field = False

    table += ") VALUES \n"

    is_first_values = True #variable use in order to know if we add a `,` after the values tuple
    for values in table_values:
        if is_first_values == False:
            table += " , "
        table += "("

        is_first_value = True #variable use in order to know if we add a `,` after the value
        for value in values:
            if is_first_value == False:
                table += " , "
            
            table += "\""+str(value).replace("\"","'")+"\""
            
            if value == "":
                table += ""
            is_first_value = False

        table += ")"
        is_first_values = False

    table += ";"

    return table




def open_json(file_path):
#open a file which contains a json and create an object that is returned
    try:
        with open(file_path) as data_file:    
            try :
                data = json.load(data_file)
                return data
            except:
                print("ERROR : file ",file_path," is not json valid")
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


def test():

    path = "../webApp/json/feuillage.json"
    #path = "../data/json/feuillage_short_standard.json"
    data = open_json(path)
    #print(data)

    directory_json_path = "../webApp/json/"

    content = template_header_file_sql()
    content += "\n\n\n"

    #for file_json in os.listdir(directory_json_path):
    for file_json in glob.glob(os.path.join(directory_json_path, '*.json')):
        #all json files are array that contains objects
        data = open_json(file_json)

        values = []

        for dico in data:
            fields = {}
            values_item = []

            for key in dico.keys():
                if isinstance(dico[key],int):
                    fields[key] = ("int(11)",True)
                elif isinstance(dico[key],float):
                    fields[key] = ("double",True)
                else:
                    fields[key] = ("varchar(255)",True)

                values_item.append(dico[key])

            values.append(values_item)

        file_name = str(os.path.splitext(ntpath.basename(file_json))[0])
        content += "\n\n" + template_table_sql(file_name,fields,values)



    file_sql_name = "script_sql.sql"
    directory_result_path = "../data/sql/"
    file_writer(directory_result_path,file_sql_name,content)


test()