import re

from unidecode import unidecode

replacements = {
    'ә': 'а',
    'қ': 'к',
    'ғ': 'г',
    'ң': 'н',
    'һ': 'х',
    'є': 'e',
    'ұ': 'у'
}


def to_latin_from_cyrillic(text_cyrillic):
    text_cyrillic = text_cyrillic.lower()
    for pattern, replacement in replacements.items():
        text_cyrillic = re.sub(pattern, replacement, text_cyrillic)

    text_latin = re.sub(r'\'', '', unidecode(text_cyrillic))
    return text_latin
