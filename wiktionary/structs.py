#!/usr/bin/python
# -*- coding: utf-8  -*-

'''
Basic structures for wiktionary.py
'''

isolangs = ['af', 'an', 'ar', 'ast', 'ay', 'az', 'bam', 'be', 'bg', 'bi', 'bn',
            'br', 'bs', 'ca', 'che', 'chp', 'co', 'cpf', 'cs', 'cy', 'da', 'de',
            'dgd', 'el', 'eml', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fo',
            'fr', 'fur', 'fy', 'ga', 'gil', 'gl', 'grc', 'gu', 'hat', 'haw',
            'he', 'hi', 'hr', 'hu', 'hy', 'ia', 'id', 'io', 'is', 'it', 'ja',
            'ja-ro', 'jv', 'ka', 'ko', 'kok', 'ku', 'la', 'lad', 'lb', 'li',
            'ln', 'lt', 'lv', 'ma', 'mas', 'mg', 'mh', 'mi', 'mn', 'mnc', 'mr',
            'ms', 'mt', 'my', 'myn', 'na', 'nah', 'nap', 'nds', 'no', 'ny',
            'oc', 'oen', 'pa', 'pap', 'pau', 'pl', 'pt', 'pzh', 'qu', 'ra',
            'rap', 'rmr', 'ro', 'roh', 'ru', 'sa', 'sc', 'scn', 'sco', 'si',
            'sk', 'sl', 'sm', 'smi', 'sn', 'so', 'sov', 'sq', 'sr', 'src',
            'sro', 'su', 'sv', 'sw', 'tay', 'th', 'ti', 'tl', 'tn', 'tox',
            'tpn', 'tr', 'ts', 'tt', 'tum', 'tvl', 'uk', 'ur', 'vi', 'vo', 'wa',
            'wo', 'xh', 'zh', 'zu',
            ]

wiktionaryformats = {
    'nl': {
        'langheader': u'{{-%%ISOLangcode%%-}}',
        'translang': u':*{{%%ISOLangcode%%}}',
        'beforeexampleterm': u"'''",
        'afterexampleterm': u"'''",
        'gender': u"{{%%gender%%}}",
        'posheader': {
            'noun': u'{{-noun-}}',
            'adjective': u'{{-adj-}}',
            'verb': u'{{-verb-}}',
        },
        'translationsheader': u"{{-trans-}}",
        'transbefore': u'{{top}}',
        'transinbetween': u'{{mid}}',
        'transafter': u'{{after}}',
        'transnoAtoM': u'<!-- Vertalingen van A tot M komen hier-->',
        'transnoNtoZ': u'<!-- Vertalingen van N tot Z komen hier-->',
        'synonymsheader': u"{{-syn-}}",
        'relatedheader': u'{{-rel-}}',
    },
    'en': {
        'langheader': u'==%%langname%%==',
        'translang': u'*%%langname%%',
        'beforeexampleterm': u"'''",
        'afterexampleterm': u"'''",
        'gender': u"''%%gender%%''",
        'posheader': {
            'noun': u'===Noun===',
            'adjective': u'===Adjective===',
            'verb': u'===Verb===',
        },
        'translationsheader': u"====Translations====",
        'transbefore': u'{{top}}',
        'transinbetween': u'{{mid}}',
        'transafter': u'{{after}}',
        'transnoAtoM': u'<!-- Translations from A tot M go here-->',
        'transnoNtoZ': u'<!-- Translations from N tot Z go here-->',
        'synonymsheader': u"====Synonyms====",
        'relatedheader': u'===Related words===',
    }
}

pos = {
    u'noun': u'noun',
    u'adjective': u'adjective',
    u'verb': u'verb',
}

otherheaders = {
    u'see also': u'seealso',
    u'see': u'seealso',
    u'translations': u'trans',
    u'trans': u'trans',
    u'synonyms': u'syn',
    u'syn': u'syn',
    u'antonyms': u'ant',
    u'ant': u'ant',
    u'pronunciation': u'pron',
    u'pron': u'pron',
    u'related terms': u'rel',
    u'rel': u'rel',
    u'acronym': u'acr',
    u'acr': u'acr',
    u'etymology': u'etym',
    u'etym': u'etym',
}

langnames = {
    'nl': {
        'translingual': u'Taalonafhankelijk',
        'nl': u'Nederlands',
        'en': u'Engels',
        'de': u'Duits',
        'fr': u'Frans',
        'it': u'Italiaans',
        'eo': u'Esperanto',
        'es': u'Spaans',
    },
    'de': {
        'translingual': u'???',
        'nl': u'Niederländisch',
        'en': u'Englisch',
        'de': u'Deutsch',
        'fr': u'Französisch',
        'it': u'Italienisch',
        'eo': u'Esperanto',
        'es': u'Spanisch',
    },
    'en': {
        'translingual': u'Translingual',
        'nl': u'Dutch',
        'en': u'English',
        'de': u'German',
        'fr': u'French',
        'it': u'Italian',
        'eo': u'Esperanto',
        'es': u'Spanish',
    },
    'eo': {
        'translingual': u'???',
        'nl': u'Nederlanda',
        'en': u'Angla',
        'de': u'Germana',
        'fr': u'Franca',
        'it': u'Italiana',
        'eo': u'Esperanto',
        'es': u'Hispana',
    },
    'ia': {
        'translingual': u'translingual',
        'nl': u'nederlandese',
        'en': u'anglese',
        'de': u'germano',
        'fr': u'francese',
        'it': u'italiano',
        'eo': u'esperanto',
        'es': u'espaniol',
    },
    'it': {
        'translingual': u'???',
        'nl': u'olandese',
        'en': u'inglese',
        'de': u'tedesco',
        'fr': u'francese',
        'it': u'italiano',
        'eo': u'esperanto',
        'es': u'spagnuolo',
    },
    'fr': {
        'translingual': u'???',
        'nl': u'néerlandais',
        'en': u'anglais',
        'de': u'allemand',
        'fr': u'français',
        'it': u'italien',
        'eo': u'espéranto',
        'es': u'espagnol',
    },
    'es': {
        'translingual': u'???',
        'nl': u'olandés',
        'en': u'inglés',
        'de': u'alemán',
        'fr': u'francés',
        'it': u'italiano',
        'eo': u'esperanto',
        'es': u'español',
    },
}


def invertlangnames():
    '''
    On the English Wiktionary it is customary to use full language names. For
    parsing we need a dictionary to efficiently convert these back to iso
    abbreviations.
    The dictionary that gets created also contains common misspellings

    '''
    invertedlangnames = {}
    for ISOKey in langnames.keys():
        for ISOKey2 in langnames[ISOKey].keys():
            lowercaselangname = langnames[ISOKey][ISOKey2].lower()
            # Put in the names of the languages so we can easily do a reverse
            # lookup lang name -> iso abbreviation
            invertedlangnames.setdefault(lowercaselangname, ISOKey2)
            # Now all the correct forms are in, but we also want to be able to
            # find them when there are typos in them
            for index in range(1, len(lowercaselangname)):
                # So first we create all the possibilities with one letter gone
                invertedlangnames.setdefault(
                    lowercaselangname[:index] + lowercaselangname[index + 1:],
                    ISOKey2)
                # Then we switch two consecutive letters
                invertedlangnames.setdefault(
                    lowercaselangname[:index - 1] +
                    lowercaselangname[index] +
                    lowercaselangname[index - 1] +
                    lowercaselangname[index + 1:],
                    ISOKey2)
                # There are of course other typos possible, but this caters for
                # a lot of possibilities already
                # TODO One other treatment that would make sense is to filter
                # out the accents.
    return invertedlangnames


def createPOSlookupDict():
    '''
    The dictionary for looking up parts of speech gets completed
    with common misspellings

    '''
    for key in pos.keys():
        lowercasekey = key.lower()
        value = pos[key]
        for index in range(1, len(lowercasekey)):
            # So first we create all the possibilities with one letter gone
            pos.setdefault(lowercasekey[:index] + lowercasekey[index + 1:],
                           value)
            # Then we switch two consecutive letters
            pos.setdefault(lowercasekey[:index - 1] + lowercasekey[index] +
                           lowercasekey[index - 1] + lowercasekey[index + 1:],
                           value)
            # There are of course other typos possible, but this caters for a
            # lot of possibilities already
    return pos


def createOtherHeaderslookupDict():
    '''
    The dictionary for looking up names of other headers gets completed
    with common misspellings

    '''
    for key in otherheaders.keys():
        lowercasekey = key.lower()
        value = otherheaders[key]
        for index in range(1, len(lowercasekey)):
            # So first we create all the possibilities with one letter gone
            otherheaders.setdefault(lowercasekey[:index] +
                                    lowercasekey[index + 1:], value)
            # Then we switch two consecutive letters
            otherheaders.setdefault(lowercasekey[:index - 1] +
                                    lowercasekey[index] +
                                    lowercasekey[index - 1] +
                                    lowercasekey[index + 1:], value)
            # There are of course other typos possible, but this caters for a
            # lot of possibilities already
    return otherheaders


# Execute the functions that will take care of setting up and completing
# lookup dictionaries for stuff that can appear in headers.
invertedlangnames = invertlangnames()
createPOSlookupDict()
createOtherHeaderslookupDict()
