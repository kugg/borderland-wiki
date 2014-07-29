# -*- coding: utf-8  -*-

import family

# The official Mozilla Wiki.

class Family(family.Family):
    def __init__(self):
        family.Family.__init__(self)

        self.name = 'mozilla'

        self.langs = {
                'en': 'wiki.mozilla.org',
        }
        self.namespaces[4] = {
            '_default': [u'MozillaWiki', self.namespaces[4]['_default']],
        }
        self.namespaces[5] = {
            '_default': [u'MozillaWiki talk', self.namespaces[5]['_default']],
        }

    def version(self, code):
        return '1.19.11'

    def scriptpath(self, code):
        return ''

    def nicepath(self, code):
        return '/'
