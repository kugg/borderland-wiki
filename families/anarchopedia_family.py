# -*- coding: utf-8  -*-
"""Family module for Anarchopedia wiki."""

__version__ = '$Id$'

import family


# The Anarchopedia family
class Family(family.Family):

    """Family class for Anarchopedia wiki."""

    def __init__(self):
        """Constructor."""
        family.Family.__init__(self)
        self.name = 'anarchopedia'

        self.languages_by_size = [
            'ar', 'en', 'de', 'nl', 'el', 'it', 'fa', 'fi', 'fr', 'he',
            'es', 'hy', 'id', 'meta', 'ja', 'ko', 'lv', 'lt', 'no', 'hr',
            'pl', 'pt', 'ro', 'ru', 'sr', 'sq', 'da', 'sv', 'tr', 'zh',
            'eo',
        ]
        self.langs = dict([(lang, '%s.anarchopedia.org' % lang)
                           for lang in self.languages_by_size])

        # Override defaults
        self.namespaces[1]['fr'] = u'Discuter'
        self.namespaces[3]['fr'] = u'Discussion Utilisateur'
        self.namespaces[6]['tr'] = u'Resim'
        self.namespaces[6]['da'] = u'Billede'
        self.namespaces[6]['sq'] = u'Figura'
        self.namespaces[7]['da'] = u'Billeddiskussion'
        self.namespaces[7]['fr'] = u'Discussion Fichier'
        self.namespaces[7]['sq'] = u'Figura diskutim'
        self.namespaces[7]['tr'] = u'Resim tartışma'
        self.namespaces[11]['fr'] = u'Discussion Modèle'
        self.namespaces[13]['fr'] = u'Discussion Aide'
        self.namespaces[14]['sq'] = u'Kategori'
        self.namespaces[15]['fr'] = u'Discussion Catégorie'
        self.namespaces[15]['sq'] = u'Kategori Diskutim'

        # Most namespaces are inherited from family.Family.
        # Translation used on all wikis for the different namespaces.
        # (Please sort languages alphabetically)
        # You only need to enter translations that differ from _default.
        self.namespaces[4] = {
            '_default': u'Anarchopedia',
            'ar': u'أنارشوبيديا',
            'el': u'Αναρχοπαίδεια',
            'eo': u'Anarĥopedio',
            'es': u'Anarcopedia',
            'fa': u'آنارکوپديا',
            'he': u'אנרכופדיה',
            'hy': u'Անարխոպեդիա',
            'it': u'Anarcopedia',
            'ja': u'アナーキォペディア',
            'ko': u'아나코백과',
            'lv': u'Anarkopēdija',
            'pt': u'Anarcopédia',
            'ro': u'Anarhopedia',
            'ru': u'Анархопедия',
            'sq': u'Anarshipedia',
            'sr': u'Anarhopedija / Анархопедија',
            'tr': u'Anarşipedi',
            'zh': u'安那其百科',
        }
        self.namespaces[5] = {
            '_default': u'Anarchopedia talk',
            'ar': u'نقاش أنارشوبيديا',
            'bs': u'Разговор о Anarchopedia',
            'da': u'Anarchopedia-diskussion',
            'de': u'Anarchopedia Diskussion',
            'el': u'Αναρχοπαίδεια συζήτηση',
            'es': u'Anarcopedia Discusión',
            'fa': u'بحث آنارکوپديا',
            'fi': u'Keskustelu Anarchopediasta',
            'fr': u'Discussion Anarchopedia',
            'he': u'שיחת אנרכופדיה',
            'hy': u'Անարխոպեդիայի քննարկում',
            'id': u'Pembicaraan Anarchopedia',
            'it': u'Discussioni Anarcopedia',
            'ja': u'アナーキォペディア‐ノート',
            'ko': u'아나코백과토론',
            'lv': u'Anarkopēdija diskusija',
            'nl': u'Overleg Anarchopedia',
            'no': u'Anarchopedia-diskusjon',
            'or': u'Anarchopedia-diskusjon',
            'pl': u'Dyskusja Anarchopedia',
            'pt': u'Anarcopédia Discussão',
            'ro': u'Discuţie Anarhopedia',
            'ru': u'Обсуждение Анархопедии',
            'sh': u'Разговор о Anarhopedija / Анархопедија',
            'sq': u'Anarshipedia diskutim',
            'sr': u'Разговор о Anarhopedija / Анархопедија',
            'sv': u'Anarchopediadiskussion',
            'tr': u'Anarşipedi tartışma',
            'zh': u'安那其百科 talk',
        }

        self.namespaces[100] = {'en':u'Focus'}

        self.namespaces[101] = {'en':u'Focus talk'}

        self.nocapitalize = self.langs.keys()

        self.obsolete = {
            # ISO 639-2 -> ISO 639-1 mappings
            'ara': 'ar',
            'chi': 'zh',
            'dan': 'da',
            'deu': 'de',
            'dut': 'nl',
            'ell': 'el',
            'eng': 'en',
            'epo': 'eo',
            'fas': 'fa',
            'fin': 'fi',
            'fra': 'fr',
            'ger': 'de',
            'gre': 'el',
            'heb': 'he',
            'hye': 'hy',
            'ind': 'id',
            'ita': 'it',
            'jpn': 'ja',
            'kor': 'ko',
            'lav': 'lv',
            'lit': 'lt',
            'nno': 'no',
            'nob': 'no',
            'nor': 'no',
            'pol': 'pl',
            'por': 'pt',
            'rum': 'ro',
            'rus': 'ru',
            'spa': 'es',
            'srp': 'sr',
            'sqi': 'sq',
            'swe': 'sv',
            'tur': 'tr',
            'zho': 'zh',

            # ISO 639-1 -> ISO 639-1 mappings
            'bs': 'hr',

            # Non-compliant mappings
            'bos': 'hr',
            'nsh': 'hr',
        }

    def version(self, code):
        """Return the version for this family."""
        return "1.14alpha"

    def scriptpath(self, code):
        """Return the script path for this family."""
        return ''

    def nicepath(self, code):
        return '/'
