import re
import unicodedata


def remove_accents(word):

    nfkd = unicodedata.normalize("NFKD", word)
    latin = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    return re.sub("[^a-zA-Z0-9 \\\]", "", latin)  # noqa W602
