import xlrd

def check_genre_espece_implies_type_feuillage(genre_espece_implies_type_feuillage, data, row, errors):
    #we get the associated type to this genre_espece (if it is not present we add it)
    tree_type = genre_espece_implies_type_feuillage.setdefault((data[row][3],data[row][4]), data[row][5])

    #we check if the tree_type is the same
    if tree_type != data[row][5]:
        errors.append('{} DF broken: different type for genre-espece {}, we have:\
         {} and {}'.format(row+1, (data[row][3],data[row][4]),tree_type, data[row][5]))

def check_type_implies_genre_espece(type_implies_genre_espece, data, row, errors):
    genre_espece = type_implies_genre_espece.setdefault(data[row][2],\
     (data[row][3],data[row][4]))

    if (data[row][3],data[row][4]) != genre_espece:
        errors.append('{} DF broken: different espece for same type {}: {} and {}'\
        .format(row+1, data[row][2], genre_espece,(data[row][3],data[row][4])))

def check_id_implies_genre_espece(id_implies_genre_espece, data, row, errors):
    genre_espece = id_implies_genre_espece.setdefault(data[row][1],\
     (data[row][3],data[row][4]))

    if (data[row][3],data[row][4]) != genre_espece:
        errors.append('{} DF broken: different espece for same id {}: {} and {}'\
        .format(row+1, data[row][1], genre_espece,(data[row][3],data[row][4])))

def checkDF(data):
    # genre => type feuillage
    # type en francis => genre-espece

    errors = []

    # model of this dict :
    # ("genre", "espece"): "type feuillage"
    genre_espece_implies_type_feuillage = {}
    type_implies_genre_espece = {}
    id_implies_genre_espece = {}

    for row in range(len(data)):
        #we don't consider incomplete lines
        if data[row][4] != 'sp.':
            check_genre_espece_implies_type_feuillage(genre_espece_implies_type_feuillage, data, row, errors)
            check_type_implies_genre_espece(type_implies_genre_espece, data, row, errors)
            check_id_implies_genre_espece(id_implies_genre_espece, data, row, errors)

    return errors
