from unidecode import unidecode

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def normalize(string_to_normalize):
    """This function return a lowercase, without accent version of string_to_normalize"""

    if not is_number(string_to_normalize):
        return unidecode(string_to_normalize).lower()
    else:
        return int(string_to_normalize)
