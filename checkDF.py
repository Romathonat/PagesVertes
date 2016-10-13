import xlrd

def check_genre_espece_implies_type_feuillage(genre_espece_implies_type_feuillage, data, row, errors):
    #we get the associated type to this genre (if it is not present we add it)
    tree_type = genre_espece_implies_type_feuillage.setdefault((data[row][3],data[row][4]), data[row][5])

    #we check if the tree_type is the same
    if tree_type != data[row][5]:
        errors.append('{} DF broken: different type for genre-espec {} {}, we have: {} and {}'.format(row+1, data[row][3], data[row][4],tree_type, data[row][5]))

def check_espece_implies_genre(espece_genre_implies_genre, data, row, errors):
    genre = espece_genre_implies_genre.setdefault(data[row][4], data[row][3])

    if genre != data[row][3]:
        errors.append('{} DF broken: different genre for same espece {}: {} and {} type francais:{}'.format(row+1, data[row][4], genre, data[row][3], data[row][2]))

def check_type_implies_espece(type_implies_espece, data, row, errors):
    espece = type_implies_espece.setdefault(data[row][2], data[row][4])

    if  data[row][4] != espece:
        errors.append('{} DF broken: different espece for same type {}: {} and {}'.format(row+1, data[row][2], espece, data[row][4]))


def checkDF(data):
    # genre => type arbre
    # espece => genre
    # espece <=> type en francais


    errors = []

    genre_espece_implies_type_feuillage = {}
    espece_genre_implies_genre = {}
    type_implies_espece = {}

    for row in range(len(data)):
        #we don't consider incomplete lines
        if data[row][4] != 'sp.':
            #genre_implies_type
            check_genre_espece_implies_type_feuillage(genre_espece_implies_type_feuillage, data, row, errors)

            #espece_implies_genre
            #check_espece_implies_genre(espece_genre_implies_genre, data, row, errors)

            #espece <=> type en francais : it is a double DF
            check_type_implies_espece(type_implies_espece, data, row, errors)

    return errors
