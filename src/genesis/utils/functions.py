import re
import unicodedata

from .ibge import cities


def remove_accents(word):

    nfkd = unicodedata.normalize("NFKD", word)
    latin = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    return re.sub("[^a-zA-Z0-9 \\\]", "", latin)  # noqa W602


def get_city_data(city, state):
    data = list(filter(lambda d: d['Nome'] == city and d["Uf"] == state, cities))
    if len(data) != 1:
        return {}
    return data[0]
