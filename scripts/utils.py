from unidecode import unidecode
import re

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

class hashableDict(dict):
    def __key(self):
        return tuple((k,self[k]) for k in sorted(self))
    def __hash__(self):
        return hash(self.__key())
    def __eq__(self, other):
        return self.__key() == other.__key()

class hashableDictArbre(hashableDict):
    # we define the hash as the id so that we don't have two dict with the same id
    def __hash__(self):
        return hash(dict(self.items())['id'])
    def __eq__(self, other):
        return dict(self.items())['id'] == dict(other.items())['id']


def set_to_json(set_to_convert):
    return re.sub(r'[\']','"',repr(set_to_convert))
