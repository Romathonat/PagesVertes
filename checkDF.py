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

def check_espece_equiv_type(espece_equivalent_type, datas, row, errors):
    tree_type = espece_equivalent_type.setdefault(datas.cell(row,4).value, datas.cell(row,5).value)
    espece = espece_equivalent_type.setdefault(datas.cell(row,5).value, datas.cell(row,4).value)

    if espece != datas.cell(row,4).value or tree_type != datas.cell(row,5).value:
        errors.append('{} equivalence problem between espece and type (look to previous lines)'.format(row+1))


def chechDF():
    # genre => type arbre
    # espece => genre
    # espece <=> type en francais

    excel_file = xlrd.open_workbook('./datas/arbres.xls')

    datas = excel_file.sheets()[0]

    errors = []

    genre_implies_type = {}
    espece_implies_genre = {}
    espece_equivalent_type = {}

    for row in range(datas.nrows):
        #genre_implies_type
        check_genre_implies_type(genre_implies_type, datas, row, errors)

        #espece_implies_genre
        check_espece_implies_genre(espece_implies_genre, datas, row, errors)

        #espece <=> type en francais : it is a double DF
        check_espece_equiv_type(espece_equivalent_type, datas, row, errors)

    return errors

print(chechDF())
