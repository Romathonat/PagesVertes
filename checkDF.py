import xlrd

def check_genre_implies_type(genre_implies_type, datas, row, errors):
    #we get the associated type to this genre (if it is not present we add it)
    tree_type = genre_implies_type.setdefault(datas[row][3], datas[row][5])

    #we check if the tree_type is the same
    if tree_type != datas[row][5]:
        errors.append('{} DF broken: different type for genre {}, we have: {} and {}'.format(row+1, datas[row][3],tree_type, datas[row][5]))

def check_espece_implies_genre(espece_implies_genre, datas, row, errors):
    genre = espece_implies_genre.setdefault(datas[row][4], datas[row][3])

    if genre != datas[row][3]:
        errors.append('{} DF broken: different genre for same espece {}: {} and {}'.format(row+1, datas[row][4], genre, datas[row][3]))

def check_type_implies_espece(type_implies_espece, datas, row, errors):
    espece = type_implies_espece.setdefault(datas[row][2], datas[row][4])

    if  datas[row][4] != espece:
        errors.append('{} DF broken: different espece for same type {}: {} and {}'.format(row+1, datas[row][2], espece, datas[row][4]))


def checkDF(datas):
    # genre => type arbre
    # espece => genre
    # espece <=> type en francais


    errors = []

    genre_implies_type = {}
    espece_implies_genre = {}
    type_implies_espece = {}

    for row in range(len(datas)):
        #we don't consider incomplete lines
        if datas[row][4] != 'sp.':
            #genre_implies_type
            #check_genre_implies_type(genre_implies_type, datas, row, errors)

            #espece_implies_genre
            #check_espece_implies_genre(espece_implies_genre, datas, row, errors)

            #espece <=> type en francais : it is a double DF
            check_type_implies_espece(type_implies_espece, datas, row, errors)

    return errors
