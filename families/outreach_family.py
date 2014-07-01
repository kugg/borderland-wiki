# -*- coding: utf-8  -*-

__version__ = '$Id$'

import family


# Outreach wiki custom family
class Family(family.WikimediaFamily):
    def __init__(self):
        super(Family, self).__init__()
        self.name = u'outreach'
        self.langs = {
            'outreach': 'outreach.wikimedia.org',
        }

        self.namespaces[4] = {
            '_default': [u'Wikimedia', self.namespaces[4]['_default']],
        }
        self.namespaces[5] = {
            '_default': [u'Wikimedia talk', self.namespaces[5]['_default']],
        }
        self.namespaces[1198] = {
            '_default': u'Translations',
        }
        self.namespaces[1199] = {
            '_default': u'Translations talk',
        }

        self.interwiki_forward = 'wikipedia'
