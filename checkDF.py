import xlrd

def check_genre_implies_type(genre_implies_type, datas, row, errors):
    #we get the associated type to this genre (if it is not present we add it)
    tree_type = genre_implies_type.setdefault(datas.cell(row,3).value, datas.cell(row,5).value)

    #we check if the tree_type is the same
    if tree_type != datas.cell(row,5).value:
        errors.append('{} DF broken: different type for genre {}, we have: {} and {}'.format(row+1, datas.cell(row,3).value,tree_type, datas.cell(row,5).value))

def check_espece_implies_genre(espece_implies_genre, datas, row, errors):
    genre = espece_implies_genre.setdefault(datas.cell(row,4).value, datas.cell(row,3).value)

    if genre != datas.cell(row,3).value:
        errors.append('{} DF broken: different genre for same espece {}: {} and {}'.format(row+1, datas.cell(row,4).value, genre, datas.cell(row,3).value))

def check_type_implies_espece(type_implies_espece, datas, row, errors):
    espece = type_implies_espece.setdefault(datas.cell(row,2).value, datas.cell(row,4).value)

    if  datas.cell(row,4).value != espece:
        errors.append('{} DF broken: different espece for same type {}: {} and {}'.format(row+1, datas.cell(row,2).value, espece, datas.cell(row,4).value))


def chechDF():
    # genre => type arbre
    # espece => genre
    # espece <=> type en francais

    excel_file = xlrd.open_workbook('./datas/arbres.xls')

    datas = excel_file.sheets()[0]

    errors = []

    genre_implies_type = {}
    espece_implies_genre = {}
    type_implies_espece = {}

    for row in range(datas.nrows):
        #genre_implies_type
        #check_genre_implies_type(genre_implies_type, datas, row, errors)

        #espece_implies_genre
        #check_espece_implies_genre(espece_implies_genre, datas, row, errors)

        #espece <=> type en francais : it is a double DF
        check_type_implies_espece(type_implies_espece, datas, row, errors)

    return errors

errors = chechDF()

for line in errors:
    print(line)
